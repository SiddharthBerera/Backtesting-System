import pandas as pd
from binance.client import Client

class Portfolio():

    def __init__(self, symbols: list, pairs: list, principle_amount: float):

        self.symbols = symbols
        self.pairs = pairs
        self.positions = {}
        for symbol in self.symbols:
            self.positions[symbol] = {'latest_trade_timestamp' : 0,
                                    'quantity' : 0.0,  #no of tokens held
                                    'value' : 0.0}     #in USDT
        self.positions['USDT'] = {'latest_trade_timestamp': None,
                                'quantity' : principle_amount,
                                'value' : principle_amount}

        self.trade_history = pd.DataFrame()
        #currenceyA currenceyB with positive quantity means currenceyB used to buy currenceyA 
        #currenceyA currenceyB with negative quantity means currenceyA used to buy currenceyB        
        self.trade_history['symbol'] = []
        self.trade_history['trade_timestamp'] = []
        self.trade_history['direction'] = [] #buy/sell being 1 or -1
        self.trade_history['trade_price'] = []
        self.trade_history['trade_quantity'] = []

        #tracks portfolio value at nth minute at nth index
        self.principal_amount = principle_amount
        self.portfolio_value = []
        self.pnl = []

    def buy_currency(self, 
                    symbol: str,   #currency symbol
                    trade_timestamp: int, 
                    quantity: int,   #quantity of currency
                    trade_price: float   # price of currency in usdt
                    ) -> dict:
        self.positions[symbol]['latest_trade_timestamp'] = trade_timestamp
        self.positions[symbol]['quantity'] += quantity
        self.positions[symbol]['value'] = self.positions[symbol]['quantity']*trade_price #in usdt
        
        self.positions['USDT']['latest_trade_timestamp'] = trade_timestamp
        self.positions['USDT']['quantity'] -= quantity*trade_price
        self.positions['USDT']['value'] = self.positions['USDT']['quantity']*1 #in usdt

        self.trade_history.loc[len(self.trade_history.index)] = [symbol, trade_timestamp, 1, trade_price, quantity]
        
    def buy_usdt(self, 
                    symbol: str,   #currency symbol
                    trade_timestamp: int, 
                    quantity: int,   #quantity of currency
                    trade_price: float   # price of currency in usdt
                    ) -> dict:
        
        self.positions['USDT']['latest_trade_timestamp'] = trade_timestamp
        self.positions['USDT']['quantity'] += quantity*trade_price
        self.positions['USDT']['value'] = self.positions['USDT']['quantity']*1 #in usdt

        self.positions[symbol]['latest_trade_timestamp'] = trade_timestamp
        self.positions[symbol]['quantity'] -= quantity
        self.positions[symbol]['value'] = self.positions[symbol]['quantity']*trade_price #in usdt

        self.trade_history.loc[len(self.trade_history.index)] = [symbol, trade_timestamp, -1, trade_price, quantity]


    def update_position_value(self, symbol, symbol_price):
        #print(self.positions[symbol]['value'])
        self.positions[symbol]['value'] = self.positions[symbol]['quantity']*symbol_price
        #print(self.positions[symbol]['value'])

    def calculate_pnl(self):
        total_portfolio_value = 0
        for symbol in self.symbols:
            total_portfolio_value += self.positions[symbol]['value']
        total_portfolio_value += self.positions['USDT']['value']
        self.portfolio_value.append(total_portfolio_value)
        if len(self.pnl) == 0:
            self.pnl.append(0)
        else:
            current_pnl = ((self.portfolio_value[-1]-self.portfolio_value[-2])/self.portfolio_value[-2])
            self.pnl.append(current_pnl)

            
