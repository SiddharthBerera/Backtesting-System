from csv import writer
from re import L
import pandas as pd

from datetime import datetime
import time

from binance.spot import Spot as Client



class DataStreamer():

    def __init__(self, client: Client, start_timestamp, end_timestamp, pairs, interval):
        self.client = client
        self.start_timestamp = start_timestamp
        self.end_timestamp = end_timestamp
        self.interval = interval
        self.pairs = pairs   
        self.current_interval = 1
        self.backtest_complete = False
        self.current_candle = {pair: None for pair in self.pairs}
    
    def get_candle(self):
        with open('price_data.csv', 'a', newline='') as file_object:
            writer_object = writer(file_object)
            for pair in self.pairs:
                current_candle = self.client.klines(symbol=pair, interval=self.interval, startTime=self.start_timestamp, limit=self.current_interval)[-1]
                for i in range(1,6):
                    current_candle[i] = float(current_candle[i])
                self.current_candle[pair] = current_candle
                writer_object.writerow([pair]+self.current_candle[pair])
            self.current_interval+=1
            current_timestamp = self.current_candle[self.pairs[0]][0]
            if current_timestamp >= self.end_timestamp:
                self.backtest_complete = True 
            return self.current_candle
   
#Testing
'''
API_KEY = "YGK6p56Tj9e5r2R1JGjs0xoiWwAnT49EqwuMu3bf0oRgftaE2sAo28ScSMUGAtds"
SECRET_KEY = "Lab6Y51HaC27Sq9RzyrotLdGDpzyENZdqbY1v8Y0FMlDy9vFeIIZ0Vfl8koC9MHw"
client = Client(API_KEY, SECRET_KEY)

ds = DataStreamer(client, ['BTCUSDT','ETHUSDT'],'1m',10)
'''
#print(ds.start_time_unix)



