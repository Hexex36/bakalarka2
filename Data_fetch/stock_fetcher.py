#!/usr/bin/env python3
"""
Stock Data Fetcher for S&P 500 Options Study
Fetches daily stock prices for recommended stocks and saves to CSV
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

def fetch_stock_data(ticker, period='1y'):
    """Fetch daily stock data for a given ticker"""
    try:
        print(f"Fetching data for {ticker}...")
        stock = yf.Ticker(ticker)
        data = stock.history(period=period)
        
        if data.empty:
            print(f"No data found for {ticker}")
            return None
            
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
    
    all_data = []
    
    for category, tickers in STOCKS.items():
        print(f"\n=== {category} ===")
        
        for ticker in tickers:
            data = fetch_stock_data(ticker)
            
            if data is not None:
                all_data.append(data)
                print(f"✓ Successfully fetched {len(data)} days of data for {ticker}")
            else:
                print(f"✗ Failed to fetch data for {ticker}")
            
            # Rate limiting
            time.sleep(1)
    
    if all_data:
        # Combine all data
        combined_data = pd.concat(all_data)
        
        # Reorder columns
        cols = ['Ticker', 'Volatility_Category', 'Open', 'High', 'Low', 'Close', 'Volume']
        combined_data = combined_data[cols]
        
        # Save to CSV
        filename = f"stock_data_{datetime.now().strftime('%Y-%m-%d')}.csv"
        combined_data.to_csv(filename, index=True)
        print(f"\n✓ Data saved to {filename}")
        print(f"Total records: {len(combined_data)}")
        print(f"Date range: {combined_data.index.min()} to {combined_data.index.max()}")
        
    else:
        print("No data was successfully fetched.")

if __name__ == "__main__":
    main()