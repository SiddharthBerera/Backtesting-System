from portfolio import Portfolio

import pandas as pd
import numpy as np
import math

class MarketDataCache():

    def __init__(self, historical_data, capacity):
        self.data = historical_data
        #how many rows of data to store in cache for each symbol
        self.capacity = capacity
        self.pairs = list(self.data.keys())
        #self.cols = [col for col in self.market_data_cache[self.symbols[0]]]
        #self.indicators = self.cols+additional_indicators
    
    def add_row(self, current_candle):
        for pair in self.pairs:
            #the nones at the end are filler at the end of the candle data from the api so that when adding to pd dataframe row is same size
            #self.data[pair].loc[self.data[pair].shape[0]] = current_candle[pair]+[np.nan]*(self.data[pair].shape[1]-len(current_candle[pair]))
            self.data[pair].loc[self.data[pair].shape[0]] = current_candle[pair]+[np.nan, np.nan, None, np.nan, np.nan, np.nan, np.nan]

        #if cache size has been exceeded delete oldest candle (row 0)
        if self.data[self.pairs[0]].shape[0]>self.capacity:
            for pair in self.pairs:
                self.data[pair].drop(index=self.data[pair].index[0], axis=0, inplace=True)
            
                

class Strategy():

    def __init__(self, start_timestamp, end_timestamp, pairs, interval, lookback, historical_data: dict, principle_amount):
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.pairs = pairs
        self.symbols = [pair[:-4] for pair in pairs]
        self.interval = interval
        self.lookback = lookback
        self.cache_capacity = max(10000, self.lookback)
        self.market_data_cache = MarketDataCache(historical_data, self.cache_capacity)  
        self.in_position = False
        self.principle_amount = principle_amount #in usdt
        #self.portfolio = Portfolio(self.symbols, self.pairs, self.principle_amount)

    def indicators_historical_data(self, atr_period, multiplier):
        for pair in self.pairs:
            table = self.market_data_cache.data[pair]
            price_diffs = [table['High'] - table['Low'], 
               table['High'] - table['Close'].shift(), 
               table['Close'].shift() - table['Low']]

            true_range = pd.concat(price_diffs, axis=1)
            true_range = true_range.abs().max(axis=1)
            atr = true_range.ewm(alpha=1/atr_period,min_periods=atr_period).mean()            

            hl2 = (table['High'] + table['Low'])/2

            final_upperband = upperband = hl2 + (multiplier*atr)
            final_lowerband = lowerband = hl2 - (multiplier*atr)

            supertrend = [True] * len(table)
            for i in range(1, len(table.index)):   
                curr, prev = i, i-1
                # if current close price crosses above upperband
                if table['Close'][curr] > final_upperband[prev]:
                    supertrend[curr] = True
                # if current close price crosses below lowerband
                elif table['Close'][curr] < final_lowerband[prev]:
                    supertrend[curr] = False
                # else, the trend continues
                else:
                    supertrend[curr] = supertrend[prev]
                # adjustment to the final bands
                if supertrend[curr] == True and final_lowerband[curr] < final_lowerband[prev]:
                    final_lowerband[curr] = final_lowerband[prev]
                if supertrend[curr] == False and final_upperband[curr] > final_upperband[prev]:
                    final_upperband[curr] = final_upperband[prev]
                
            self.market_data_cache.data[pair].insert(self.market_data_cache.data[pair].shape[1], "TR", true_range, True)
            self.market_data_cache.data[pair].insert(self.market_data_cache.data[pair].shape[1], "ATR", atr, True)
            self.market_data_cache.data[pair].insert(self.market_data_cache.data[pair].shape[1], "Supertrend", supertrend, True)
            self.market_data_cache.data[pair].insert(self.market_data_cache.data[pair].shape[1], "Lower Band", lowerband, True)
            self.market_data_cache.data[pair].insert(self.market_data_cache.data[pair].shape[1], "Final Lower Band", final_lowerband, True)
            self.market_data_cache.data[pair].insert(self.market_data_cache.data[pair].shape[1], "Upper Band", upperband, True)
            self.market_data_cache.data[pair].insert(self.market_data_cache.data[pair].shape[1], "Final Upper Band", final_upperband, True)
            

    def indicators(self, atr_period, multiplier):
        for pair in self.pairs:
            table = self.market_data_cache.data[pair]

            price_diff = [(table['High'].iloc[-1])-(table['Low'].iloc[-1]),
            (table['High'].iloc[-1])-(table['Close'].shift().iloc[-1]),
            (table['Close'].shift().iloc[-1])-(table['Low'].iloc[-1])]
            true_range = max(price_diff)
            self.market_data_cache.data[pair].loc[table.shape[0]-1,'TR'] = true_range
            #self.market_data_cache.data[pair]['TR'].iloc[-1] = true_range

            atr = self.market_data_cache.data[pair]['TR'].ewm(alpha=1/atr_period,min_periods=atr_period).mean().iloc[-1]
            self.market_data_cache.data[pair].loc[table.shape[0]-1,'ATR'] = atr            
            #self.market_data_cache.data[pair]['ATR'].iloc[-1] = atr

            hl2 = (table['High'].iloc[-1] + table['Low'].iloc[-1])/2

            final_upperband = upperband = hl2 + (multiplier*atr)
            final_lowerband = lowerband = hl2 - (multiplier*atr)

            curr = len(table.index)-1
            prev = curr-1
            # if current close price crosses above upperband
            if table['Close'][curr] > table['Final Upper Band'][prev]:
                supertrend = True
            # if current close price crosses below lowerband
            elif table['Close'][curr] < table['Final Lower Band'][prev]:
                supertrend = False
            # else, the trend continues
            else:
                supertrend = table['Supertrend'][prev]
            # adjustment to the final bands
            if supertrend and table['Final Lower Band'][curr] < table['Final Lower Band'][prev]:
                final_lowerband = table['Final Lower Band'][prev]
            if not supertrend and table['Final Upper Band'][curr] > table['Final Upper Band'][prev]:
                final_upperband = table['Final Upper Band'][prev]
            
            self.market_data_cache.data[pair].loc[curr,'Supertrend'] = supertrend
            self.market_data_cache.data[pair].loc[curr,'Lower Band'] = lowerband
            self.market_data_cache.data[pair].loc[curr,'Final Lower Band'] = final_lowerband
            self.market_data_cache.data[pair].loc[curr,'Upper Band'] = upperband
            self.market_data_cache.data[pair].loc[curr,'Final Upper Band'] = final_upperband

    
    def make_decision(self, portfolio):
        for pair in self.pairs:
            if not self.in_position and self.market_data_cache.data[pair]['Supertrend'].iloc[-1]:                
                no_tokens = math.floor((portfolio.positions['USDT']['quantity']/self.market_data_cache.data[pair]['Close'].iloc[-1])*100)/100
                close_time = self.market_data_cache.data[pair]['Close time'].iloc[-1]
                close_price = self.market_data_cache.data[pair]['Close'].iloc[-1]
                portfolio.buy_currency(pair[:-4], close_time, quantity=no_tokens, trade_price=close_price)
                self.in_position = True
                msg_price = round(self.market_data_cache.data[pair]['Close'].iloc[-1],2)
                print(f'Buy {no_tokens} {pair[:-4]} tokens at {msg_price} at {close_time}')
                
            elif self.in_position and not self.market_data_cache.data[pair]['Supertrend'].iloc[-1]:
                quantity_of_token_held = portfolio.positions[pair[:-4]]['quantity']
                close_time = self.market_data_cache.data[pair]['Close time'].iloc[-1]
                close_price = self.market_data_cache.data[pair]['Close'].iloc[-1]
                portfolio.buy_usdt(pair[:-4], close_time, quantity=quantity_of_token_held, trade_price=close_price)
                self.in_position = False
                msg_price = round(self.market_data_cache.data[pair]['Close'].iloc[-1],2)
                print(f'Sell {quantity_of_token_held} {pair[:-4]} tokens at {msg_price} at {close_time}')
