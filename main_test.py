from backtester import Backtest

from binance.spot import Spot as Client



backtest_client = Client()
start = 1609459200000 #1/1/2021 00:00:00 UTC 
end = 1640908800000 #31/12/2021 00:00:00 UTC (beginning of final candle)
symbol = ['BTC']
interval = '1d'
lookback = 20
principal_amount = 100000.0

backtest_test1 = Backtest(client = backtest_client, 
                            start_timestamp=start, 
                            end_timestamp=end, 
                            symbols = symbol, 
                            interval = interval,
                            lookback= lookback,
                            principle_amount = principal_amount)

