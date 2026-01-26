#!/usr/bin/env python3
"""
Stock Data Fetcher for S&P 500 Options Study
Fetches daily stock prices for recommended stocks and saves to CSV
Can also be used to fetch data for custom tickers passed as arguments.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import time
import sys
import os

# Stock list with volatility categories
STOCKS = {
    'High Volatility': ['TSLA', 'NVDA', 'AMD'],
    'Moderate Volatility': ['AAPL', 'MSFT', 'GOOGL'],
    'Low Volatility': ['JNJ', 'PG', 'KO']
}

def fetch_stock_data(ticker, period='1y', is_custom=False):
    """Fetch daily stock data for a given ticker"""
    try:
        print(f"Fetching data for {ticker}...")
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        
        if data.empty:
            print(f"No data found for {ticker}")
            return None
        
        if not is_custom:
            # Add ticker and volatility info
            for category, tickers in STOCKS.items():
                if ticker in tickers:
                    data['Volatility_Category'] = category
                    break
                
        data['Ticker'] = ticker
        return data
        
    except Exception as e:
        print(f"Error fetching {ticker}: {e}")
        return None

def main():
    print("Starting stock data fetch...")
    
    # Check for custom tickers from command line
    custom_tickers = sys.argv[1:]
    
    all_data = []
    
    if custom_tickers:
        print("Fetching data for custom tickers:", custom_tickers)
        for ticker in custom_tickers:
            data = fetch_stock_data(ticker, is_custom=True)
            if data is not None:
                all_data.append(data)
                print(f"✓ Successfully fetched {len(data)} days of data for {ticker}")
            else:
                print(f"✗ Failed to fetch data for {ticker}")
            time.sleep(1) # Rate limiting
        
        if all_data:
            combined_data = pd.concat(all_data)
            # Reorder columns for custom tickers
            cols = ['Ticker', 'Open', 'High', 'Low', 'Close', 'Volume']
            combined_data = combined_data[cols]
            filename = f"european_indexes_stock_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
        else:
            print("No data was successfully fetched for custom tickers.")
            return

    else:
        print("Fetching data for default stocks...")
        for category, tickers in STOCKS.items():
            print(f"\n=== {category} ===")
            for ticker in tickers:
                data = fetch_stock_data(ticker)
                if data is not None:
                    all_data.append(data)
                    print(f"✓ Successfully fetched {len(data)} days of data for {ticker}")
                else:
                    print(f"✗ Failed to fetch data for {ticker}")
                time.sleep(1) # Rate limiting
        
        if all_data:
            combined_data = pd.concat(all_data)
            # Reorder columns for default stocks
            cols = ['Ticker', 'Volatility_Category', 'Open', 'High', 'Low', 'Close', 'Volume']
            combined_data = combined_data[cols]
            filename = f"stock_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
        else:
            print("No data was successfully fetched for default stocks.")
            return

    # Save to CSV
    combined_data.to_csv(filename, index=True)
    print(f"\n✓ Data saved to {filename}")
    print(f"Total records: {len(combined_data)}")
    print(f"Date range: {combined_data.index.min()} to {combined_data.index.max()}")


if __name__ == "__main__":
    main()