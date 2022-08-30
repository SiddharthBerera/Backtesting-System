# Backtesting-System
Event-driven, object oriented backtesting software for custom trading strategies.

## Logic of the program

Makes use of the python-binance api connector to retrieve historical price data for the N th minute of the backtest period, then in the stragey object calculates the relevant metrics. Based on these metrics decides whether or not to create a trade signal. If a signal is created, it is sent to the portfolio class which contains the current holdings and these holdings are updated. 
The backtester object then continues to the N+1 th minute of the backtest period until the strategy has been tested on the whole period.
Such a backtesting software tests the strategy in the order in which a live trading strategy would work and minimises any lookahead bias.

## How to use it

The main Backtest object (backtest.py) is intilised in the main_test.py file and the parameters for the backtest can be edited in this file.
The strategy file operates using the supertrend strategy, however this can be swapped out for any strategy by editing the indicators_historical_data, indicators and
make_decisions functions in the Strategy class.

## The output

The outputs produced when this software is run consist of a csv file containing all market data for the backtest period given and a quantstats tearsheet containing 
all relevant performance metrics of the strategy. 

<img width="485" alt="image" src="https://user-images.githubusercontent.com/71666566/187538425-16740d00-1d72-4558-b7a1-ac63edb7522f.png">
