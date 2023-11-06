import yfinance as yf

def fetch_historical_data(ticker, start_date, end_date, data_interval):
    try:
        df = yf.download(ticker, start=start_date, end=end_date, interval=data_interval, progress=False)
        return df
    except Exception as e:
        print(f"Error fetching data for {ticker}: {str(e)}")
        return None
    
