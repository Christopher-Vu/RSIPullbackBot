from tkinter.constants import E
import pandas as pd
import yfinance as yf
import ta
from concurrent.futures import ThreadPoolExecutor, as_completed

tickers = pd.read_csv('sp500_companies.csv')['Symbol'].tolist()

filtered_tickers = [ticker for ticker in tickers]

result = []
non_matches, errors = 0, 0

def check_conditions(ticker):
    try:
        df = yf.download(ticker, period="1y", progress=False, auto_adjust=True)
        if len(df) < 200:
            return None
        
        if isinstance(df.columns, pd.MultiIndex):
            if ('Close', ticker) not in df.columns:
                return None
            close_prices = df[('Close', ticker)]
        else:
            if 'Close' not in df.columns:
                return None
            close_prices = df['Close']
        
        close_prices = close_prices.dropna()
        
        if len(close_prices) < 200:
            return None
        
        df['RSI_10'] = ta.momentum.rsi(close_prices, window=10)
        df['SMA_200'] = ta.trend.sma_indicator(close_prices, window=200)
        
        rsi_latest = df['RSI_10'].iloc[-1]
        sma_latest = df['SMA_200'].iloc[-1]
        close_latest = close_prices.iloc[-1]
        # Check for valid values
        if pd.isna(rsi_latest) or pd.isna(sma_latest) or pd.isna(close_latest):
            return None
        
        print(f"{ticker}: RSI={rsi_latest:.1f}, Close={close_latest:.1f}, SMA200={sma_latest:.1f}")
        
        if rsi_latest < 35 and close_latest > (sma_latest * 0.95):
            return ticker
        
    except Exception as e:
        print(f"Error with ticker {ticker}: {e}")
        errors += 1
        return None

    print(f"No error, no match with ticker {ticker}")
    non_matches += 1
    return None

test_tickers = filtered_tickers[:20]  

"""
with ThreadPoolExecutor(max_workers=10) as executor:
    futures = [executor.submit(check_conditions, ticker) for ticker in test_tickers]
    for future in as_completed(futures):
        res = future.result()
        if res is not None:
            result.append(res)
"""

for ticker in tickers:
    if check_conditions(ticker) is not None:
        result.append(ticker)

print(f"\nStocks found: {result}")
print(f"Matches: {len(result)}, Non Matches: {str(non_matches)}, Errors: {str(errors)}")