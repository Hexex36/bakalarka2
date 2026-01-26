#!/usr/bin/env python3
"""
Stock Price Fetcher
Fetches daily stock prices for tickers specified in a TOML file.
"""

import yfinance as yf
import pandas as pd
import toml
from datetime import datetime
import time
import os

def fetch_stock_prices(tickers):
    """Fetch daily stock prices for a list of tickers."""
    all_stock_data = []
    failed_tickers = []

    for ticker_symbol in tickers:
        print(f"Fetching {ticker_symbol} daily prices...")
        try:
            ticker = yf.Ticker(ticker_symbol)
            hist = ticker.history(period="1y")

            if hist.empty:
                print(f"⚠️  No data found for {ticker_symbol}")
                failed_tickers.append(ticker_symbol)
                continue

            hist['Ticker'] = ticker_symbol
            all_stock_data.append(hist)
            print(f"  ✓ Fetched {len(hist)} days of data for {ticker_symbol}")
            time.sleep(1)  # Rate limiting

        except Exception as e:
            print(f"❌ CRITICAL ERROR fetching {ticker_symbol}: {e}")
            failed_tickers.append(ticker_symbol)
            continue

    if not all_stock_data:
        return pd.DataFrame(), failed_tickers

    final_data = pd.concat(all_stock_data)
    return final_data, failed_tickers

def save_data(data, filename_prefix):
    """Save data to a CSV file with a timestamp."""
    if data.empty:
        print(f"No data to save for {filename_prefix}")
        return

    timestamp = datetime.now().strftime('%Y-%m-%d')
    filename = f"{filename_prefix}_{timestamp}.csv"
    data.to_csv(filename)
    print(f"\n✅ Data saved to {filename}")
    print(f"   Total rows: {len(data):,}")

def main():
    """Main function to run the stock price fetcher."""
    print("Stock Price Fetcher - Starting")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    try:
        with open('tickers.toml', 'r') as f:
            config = toml.load(f)
    except FileNotFoundError:
        print("❌ Error: tickers.toml not found. Please create it.")
        return

    american_tickers = []
    for category in config.get('american_tickers', {}).values():
        american_tickers.extend(category)

    european_tickers = []
    for category in config.get('european_tickers', {}).values():
        european_tickers.extend(category)

    all_tickers = american_tickers + european_tickers

    if not all_tickers:
        print("No tickers found in tickers.toml")
        return

    print(f"Found {len(all_tickers)} tickers to process.")

    start_time = time.time()
    
    all_data, failed = fetch_stock_prices(all_tickers)

    if not all_data.empty:
        save_data(all_data, 'stock_prices')

    total_time = time.time() - start_time
    print(f"\n✅ COMPLETE - Total time: {total_time:.1f} seconds")
    if failed:
        print(f"⚠️  Failed to fetch data for the following tickers: {', '.join(failed)}")

if __name__ == "__main__":
    main()
