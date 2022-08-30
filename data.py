from csv import writer
import pandas as pd

import datetime
import time

from binance.spot import Spot as Client

class HistoricalData():

    def __init__(self, client: Client, pairs, start_timestamp, interval: str, lookback: int):
        self.indicators = ['Open time','Open','High','Low','Close','Volume','Close time','Quote asset volume','Number of trades','Taker buy base asset volume','Taker buy quote asset volume', 'Can be ignored']
        self.client = client
        self.pairs = pairs
        self.start_timestamp = start_timestamp
        self.interval = interval
        self.lookback = lookback #in number of intervals
        self.no_api_calls = 0
        self.market_data_cache = {}
        
        self.create_dataframe()
        #self.get_historical_data()
        #data file has been created, historical data has been stored in file and in memory
        #strategy class can now copy data in memory and calculate indicators

    def create_dataframe(self):
        
        fieldnames = self.indicators

        #write data to file for storage
        with open('price_data.csv', 'a', newline='') as file_object:
            writer_object = writer(file_object)
            writer_object.writerow(['Pair']+fieldnames)

    def get_historical_data(self):

        fieldnames = self.indicators

        with open('price_data.csv', 'a', newline='') as file_object:
            writer_object = writer(file_object)

            for pair in self.pairs:
                #endTime will include the candle starting at that time
                #we request lookback+1 including and before our backtest start time and then remove the candle for the start time
                candles = self.client.klines(symbol=pair, interval=self.interval, endTime=self.start_timestamp, limit = self.lookback+1)[:-1]
                self.no_api_calls+=1
                #store historical data for each symbol in memory
                self.market_data_cache[pair] = pd.DataFrame(candles)
                self.market_data_cache[pair].columns = fieldnames
                self.market_data_cache[pair]['Open'] = self.market_data_cache[pair]['Open'].astype(float)
                self.market_data_cache[pair]['High'] = self.market_data_cache[pair]['High'].astype(float)
                self.market_data_cache[pair]['Low'] = self.market_data_cache[pair]['Low'].astype(float)
                self.market_data_cache[pair]['Close'] = self.market_data_cache[pair]['Close'].astype(float)
                self.market_data_cache[pair]['Volume'] = self.market_data_cache[pair]['Volume'].astype(float)

                for candle in candles:  
                    writer_object.writerow([pair]+candle)



#Testing
'''
client = Client()
pairs = ['BTCUSDT']

historical_data = HistoricalData(client, pairs, 1609459200000, '1d', 7)
historical_data.get_historical_data()
'''