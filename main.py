from PricingBinaryTree import PricingBinaryTree
from data_getter import fetch_historical_data
from argparse import ArgumentParser
import warnings
warnings.filterwarnings("ignore")

allowed_dates = ['1m', '2m', '5m', '15m', '30m', '60m', '90m', '1h', '1d', '5d', '1wk', '1mo', '3mo']

parser = ArgumentParser()
parser.add_argument('--ticker', type=str, help='Ticker of the stock of interest', default='GOOGL')
parser.add_argument('--start_date', type=str, help='Starting date of the historical period', default='2023-01-01')
parser.add_argument('--end_date', type=str, help='Ending date of historical period')
parser.add_argument('--data_interval', type=str, help='Step interval', choices=allowed_dates, default='1mo')
parser.add_argument('--n', type=int, help='Number of steps of the simulation', default=6)
parser.add_argument('--dt', type=float, help='Time step of the simulation', default=1/12)
parser.add_argument('--r', type=float, help='Risk free interest rate', default=0.005)
parser.add_argument('--K', type=float, help='Strike price', default=130)
parser.add_argument('--option_type', type=str, help='Kind of option', default='call')
parser.add_argument('--discount', type=str, help='Type of discount', default='continuous', choices=['continuous', 'simple'])


args = parser.parse_args()

ticker = args.ticker
start_date, end_date =args.start_date, args.end_date

data = fetch_historical_data(ticker, start_date, end_date, args.data_interval)
df = data['Adj Close'].pct_change()

s = df.std()
n = args.n
dt = args.dt
r = args.r
s0 = data['Adj Close'].values[-1]
K = args.K
option_type = args.option_type

b = PricingBinaryTree(ticker=ticker, dt=dt, r=r, sigma=s, s0=s0, n=n, K=K, option_type=option_type, discount=args.discount)
b.european_option_price_dynamics(n)
b.american_option_price_dynamics(n)

b.print_results()
b.plot_results(data['Adj Close'])
