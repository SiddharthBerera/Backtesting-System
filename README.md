# Trading Strategy Backtesting System
Event-driven, object oriented backtesting software for custom trading strategies.

## Logic of the program

Makes use of the python-binance api connector to retrieve historical price data for the N th candle of the backtest period, then in the stragey object calculates the relevant metrics. Based on these metrics decides whether or not to create a trade signal. If a signal is created, it is sent to the portfolio class which contains the current holdings and these holdings are updated. 
The backtester object then continues to the N+1 th candle of the backtest period until the strategy has been tested on the whole period.
Such a backtesting software tests the strategy in the order in which a live trading strategy would work and minimises any lookahead bias.

## How to use it

The main Backtest object (backtest.py) is intilised in the main_test.py file and the parameters for the backtest can be edited in this file.
The strategy file operates using the supertrend strategy, however this can be swapped out for any strategy by editing the indicators_historical_data, indicators and
make_decisions functions in the Strategy class.

## The output

The outputs produced when this software is run consist of a csv file (price_data.csv) containing all market data for the backtest period given and a quantstats tearsheet containing all relevant performance metrics of the strategy. 

### Snippet of price_data.csv-

<img width="691" alt="image" src="https://user-images.githubusercontent.com/71666566/187538672-abf8fc83-ab4a-4951-a959-852521430d1f.png">


### Performance Metrics Tearsheet-

<img width="806" alt="image" src="https://user-images.githubusercontent.com/71666566/187539118-d19733a7-9ad0-42f3-ab16-b15c9ed3f6ce.png">
<img width="749" alt="image" src="https://user-images.githubusercontent.com/71666566/187539456-b2549b63-389f-49f1-996b-16810f268604.png">
<img width="772" alt="image" src="https://user-images.githubusercontent.com/71666566/187539548-ace97a95-452e-4c01-b34b-6a6f83ad0591.png">
<img width="794" alt="image" src="https://user-images.githubusercontent.com/71666566/187539664-cbed3a02-d5a6-497c-b3be-c0f219a1419e.png">
<img width="780" alt="image" src="https://user-images.githubusercontent.com/71666566/187539776-9aff4e9d-4e2e-4a73-812d-9e257f9cd424.png">
<img width="758" alt="image" src="https://user-images.githubusercontent.com/71666566/187539870-925d6e37-a567-479d-961c-223427291115.png">
<img width="695" alt="image" src="https://user-images.githubusercontent.com/71666566/187539944-3be469be-aa4e-421d-b7c3-d8d79abae5b3.png">
<img width="635" alt="image" src="https://user-images.githubusercontent.com/71666566/187540065-1110b556-9242-4710-9044-7ca8c3c86e08.png">
<img width="656" alt="image" src="https://user-images.githubusercontent.com/71666566/187540135-565c9c49-a1a3-4d03-859b-1bf14e036081.png">
<img width="653" alt="image" src="https://user-images.githubusercontent.com/71666566/187540170-f63b6cb8-b94d-4219-8ca3-d71dbe9d0710.png">

