from sympy import re
from data import HistoricalData
from strategy import Strategy
from portfolio import Portfolio
from data_streamer import DataStreamer

from binance.spot import Spot as Client

from csv import writer
import pandas as pd


from datetime import datetime
import quantstats as qs
import yfinance as yf

class Backtest():

    def __init__(self, 
                client: Client, 
                start_timestamp, 
                end_timestamp, 
                symbols, 
                interval: str, 
                lookback, 
                principle_amount: float):
        self.client = client
        self.start_timestamp = start_timestamp
        #beginning of end candle
        self.end_timestamp = end_timestamp
        #symbol - e.g. BTC, ETH
        self.symbols = symbols
        #pairs - e.g. BTCUSDT, ETHUSDT
        self.pairs = [symbol.upper() + 'USDT' for symbol in symbols]
        self.principle_amount = principle_amount
        self.interval = interval
        self.lookback = lookback
        self.no_api_calls = 0
        self.current_interval=1
        self.interval_timestamps=[]

        #object which stores historical data, initilised with no data
        self.market_data = HistoricalData(self.client, self.pairs, self.start_timestamp, self.interval, self.lookback)
        #get lookback data
        self.market_data.get_historical_data()
        
        #initilise strategy which takes historical data and calculates metrics 
        self.strategy = Strategy(self.start_timestamp, self.end_timestamp, self.pairs, self.interval, self.lookback, self.market_data.market_data_cache, self.principle_amount)
        self.strategy.indicators_historical_data(10,1) #atr_period, multiplier

        #initilise portfolio class 
        self.portfolio = Portfolio(self.symbols, self.pairs, self.principle_amount)

        #initilise stream of data for period between start and end timestamps
        self.data_streamer = DataStreamer(self.client, self.start_timestamp, self.end_timestamp, self.pairs, self.interval)


        self.backtester_loop()



        self.strategy_stats()

        

        

    def backtester_loop(self):
        while self.data_streamer.backtest_complete == False:
            #print(self.portfolio.positions)
            #current candle is a dictionary with pairs as the keys and corresponding candles as the values
            current_candle = self.data_streamer.get_candle()
            dt = datetime.fromtimestamp(int(current_candle[self.pairs[0]][0])/1000)
            year = str(dt.year)
            month = str(dt.month)
            day = str(dt.day)
            date = year + '-' + month + '-' + day
            print(date)
            self.interval_timestamps.append(date)
            
            for symbol in self.symbols:
                self.portfolio.update_position_value(symbol, float(current_candle[symbol+'USDT'][1]))
            self.portfolio.calculate_pnl()
            #print(self.portfolio.pnl)
            self.strategy.market_data_cache.add_row(current_candle)
            self.strategy.indicators(10,1)
            self.strategy.make_decision(self.portfolio)

            self.current_interval+=1

        current_candle = self.data_streamer.get_candle()
        dt = datetime.fromtimestamp(int(current_candle[symbol+'USDT'][0])/1000)
        year = str(dt.year)
        month = str(dt.month)
        day = str(dt.day)
        date = year + '-' + month + '-' + day
        self.interval_timestamps.append(date)
        for symbol in self.symbols:
            self.portfolio.update_position_value(symbol, float(current_candle[symbol+'USDT'][1]))
        self.portfolio.calculate_pnl()

    

    def strategy_stats(self):
        returns = pd.DataFrame({'PnL': self.portfolio.pnl}, index = self.interval_timestamps)
        returns.index = pd.to_datetime(returns.index, format='%Y-%m-%d')
        returns = returns.squeeze()
        #print(returns)
        btc = [float(candle[1]) for candle in self.client.klines(symbol='BTCUSDT', interval='1d', startTime=self.start_timestamp, limit=366)]
        btc_pnl = [0]
        for i in range(1,len(btc)):
            btc_pnl.append((btc[i]-btc[i-1])/btc[i-1]) 
        btc_pnl = pd.DataFrame({'PnL': btc_pnl}, index = self.interval_timestamps)
        btc_pnl.index = pd.to_datetime(btc_pnl.index, format='%Y-%m-%d')
        btc_pnl = btc_pnl.squeeze()
        print(returns)
        print(btc_pnl)
        '''
        btc_usdt = yf.Ticker("USDT-BTC")
        benchmark = btc_usdt.history(period="smthing")
        benchmark['Open'] = 1/benchmark['Open']
        benchmark['High'] = 1/benchmark['High']
        benchmark['Low'] = 1/benchmark['Low']
        benchmark['Close'] = 1/benchmark['Close']
        '''
    
        qs.reports.html(returns, btc_pnl, output='Report.html', title='Returns Stats')
