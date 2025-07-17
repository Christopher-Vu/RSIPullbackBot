import pandas as pd
import yfinance as yf
import ta
from concurrent.futures import ThreadPoolExecutor, as_completed

tickers = pd.read_csv('sp500_companies.csv')['Symbol'].tolist()

print(tickers)

def rsi_pullback(ticker):
    try:
        data = yf.download(ticker, period='1y', interval="1d")

        close = data['Close'].squeeze()

        sma_200 = close.rolling(200).mean()
        rsi_10 = ta.momentum.RSIIndicator(close, window=10).rsi()

        if close.iloc[-1] > sma_200.iloc[-1] and rsi_10.iloc[-1] < 30:
            return ticker

    except Exception as e:
        print(f"Error processing {ticker}: {e}")
    return None

trades = []

rsi_pullback("AAPL")

print("\nStocks above 200-day SMA and RSI(10) < 30:")
print(trades)