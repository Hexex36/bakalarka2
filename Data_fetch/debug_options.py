#!/usr/bin/env python3
"""
Debug Options Data Fetcher - Test with one ticker to see column structure
"""

import yfinance as yf
import pandas as pd
import time

def debug_ticker(ticker_symbol):
    """Debug one ticker to see column structure"""
    print(f"Debugging {ticker_symbol}...")
    
    ticker = yf.Ticker(ticker_symbol)
    expirations = ticker.options
    print(f"Expirations found: {len(expirations)}")
    print(f"First expiration: {expirations[0] if expirations else 'None'}")
    
    if expirations:
        # Get first option chain
        option_chain = ticker.option_chain(expirations[0])
        
        print("\nCalls columns:")
        print(option_chain.calls.columns.tolist())
        
        print("\nFirst few rows of calls:")
        print(option_chain.calls.head())
        
        print("\nPuts columns:")
        print(option_chain.puts.columns.tolist())
        
        print("\nFirst few rows of puts:")
        print(option_chain.puts.head())

if __name__ == "__main__":
    debug_ticker("TSLA")