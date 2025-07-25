import pandas as pd
import yfinance as yf
import ta
from concurrent.futures import ThreadPoolExecutor, as_completed

tickers = pd.read_csv('sp500_companies.csv')['Symbol'].tolist()

def rsi(close, period):
    period_close = close[-(period + 1):].tolist()
    AvgU, AvgD = 0, 0
    for ind in range(period):
        if period_close[ind] > period_close[ind + 1]: AvgD += (period_close[ind] - period_close[ind + 1])
        if period_close[ind] < period_close[ind + 1]: AvgU += (period_close[ind + 1] - period_close[ind])
    RS = AvgU / AvgD
    return 100 - (100/(1+RS))

def rsi_pullback(ticker):
    try:
        data = yf.download(ticker, period='1y', interval="1d")
        close_200 = pd.Series(data['Close'].to_numpy().flatten())[-200:]
        rsi_10 = rsi(close_200, 10)
        print(rsi_10)
        sma_200 = close_200.mean()
        print(sma_200)
        print(close_200.tolist()[-1])

        if rsi_10 < 30 and close_200.tolist()[-1] > sma_200: return ticker
    except Exception as e:
        print(f"Error processing {ticker}: {e}")
        return "err"
    return "fail"

# ai slop
trades = []

"""
def worker(ticker):
    if rsi_pullback(ticker):
        return ticker
    return None

errors, fails = 0, 0

with ThreadPoolExecutor() as executor:
    futures = [executor.submit(worker, ticker) for ticker in tickers]
    for future in as_completed(futures):
        result = future.result()
        if result == "err": errors += 1
        if result == "fail": fails += 1
        else: trades.append(result)

print(trades, errors, fails)
"""

rsi_pullback("GOOG")