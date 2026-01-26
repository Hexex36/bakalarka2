#!/usr/bin/env python3
"""
Test full option chain for one expiration
"""

import yfinance as yf
import pandas as pd

def test_full_chain(ticker_symbol):
    """Test getting full option chain"""
    print(f"Testing full chain for {ticker_symbol}...")
    
    ticker = yf.Ticker(ticker_symbol)
    expirations = ticker.options
    print(f"Available expirations: {len(expirations)}")
    
    if expirations:
        # Test first expiration
        exp_date = expirations[0]
        print(f"\nTesting expiration: {exp_date}")
        
        option_chain = ticker.option_chain(exp_date)
        
        print(f"Calls shape: {option_chain.calls.shape}")
        print(f"Puts shape: {option_chain.puts.shape}")
        
        print(f"\nCalls strikes range: {option_chain.calls['strike'].min():.2f} - {option_chain.calls['strike'].max():.2f}")
        print(f"Puts strikes range: {option_chain.puts['strike'].min():.2f} - {option_chain.puts['strike'].max():.2f}")
        
        print(f"\nSample calls (first 10):")
        print(option_chain.calls[['strike', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest']].head(10))
        
        print(f"\nSample puts (first 10):")
        print(option_chain.puts[['strike', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest']].head(10))

if __name__ == "__main__":
    test_full_chain("TSLA")