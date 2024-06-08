import yfinance as yf
import pandas as pd

def fetch_stock_data(start_date, end_date, ticker, interval):
    ticker_obj = yf.Ticker(ticker)
    stock_data = ticker_obj.history(start=start_date, end=end_date, interval=interval)
    df = pd.concat([stock_data], axis=1)
    return df