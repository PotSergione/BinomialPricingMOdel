# BinomialPricingModel
Prices American and European options using a simple binomial tree model up to 150 steps into the future. 

## Use example
From command line execute main.py [--ticker TICKER] [--start_date START_DATE] [--end_date END_DATE]
               [--data_interval {1m,2m,5m,15m,30m,60m,90m,1h,1d,5d,1wk,1mo,3mo}] [--n N] [--dt DT] [--r R] [--K K]
               [--option_type OPTION_TYPE] [--discount {continuous,simple}]
### Example

>python main.py --ticker RACE --start_date 2023-01-01 --n 3 --K=315 --r 0.01 --option_type call

The code fetches the (default) monthly historical data for Ferrari and prices both a 3 months European and a 3 months American call options with strike price 315. 
The risk free interest rate can be modified (--r 0.01). 
The volatility is estimated from the historical data and used to estimate the risk neutral probabilities (Bernstein/Cox). 
