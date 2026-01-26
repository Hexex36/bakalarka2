#!/usr/bin/env python3
"""
Fast Options Data Fetcher - Minimal Progress Reporting
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import time
import sys

# American stocks
AMERICAN_STOCKS = ['TSLA', 'NVDA', 'AMD', 'AAPL', 'MSFT', 'GOOGL', 'JNJ', 'PG', 'KO']

# European indices
EUROPEAN_INDICES = ['SPX', 'XSP']

def fetch_ticker_options(ticker_symbol, is_european=False):
    """Fetch options for a single ticker"""
    print(f"Fetching {ticker_symbol}...")
    
    try:
        ticker = yf.Ticker(ticker_symbol)
        expirations = ticker.options
        
        if not expirations:
            print(f"No expirations for {ticker_symbol}")
            return pd.DataFrame()
        
        all_data = []
        
        for exp_date in expirations:
            try:
                option_chain = ticker.option_chain(exp_date)
                
                # Process calls
                calls = option_chain.calls.copy()
                calls['Type'] = 'Call'
                calls['Ticker'] = ticker_symbol
                calls['Expiration'] = exp_date
                if is_european:
                    calls['ExerciseStyle'] = 'European'
                
                # Process puts
                puts = option_chain.puts.copy()
                puts['Type'] = 'Put'
                puts['Ticker'] = ticker_symbol
                puts['Expiration'] = exp_date
                if is_european:
                    puts['ExerciseStyle'] = 'European'
                
                # Combine
                combined = pd.concat([calls, puts], ignore_index=True)
                all_data.append(combined)
                
                time.sleep(0.3)  # Reduced rate limit for speed
                
            except:
                continue
        
        if all_data:
            final_data = pd.concat(all_data, ignore_index=True)
            
            # Select columns
            if is_european:
                desired_cols = ['Ticker', 'Expiration', 'strike', 'Type', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest', 'ExerciseStyle']
            else:
                desired_cols = ['Ticker', 'Expiration', 'strike', 'Type', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest']
            
            final_cols = [col for col in desired_cols if col in final_data.columns]
            final_data = final_data[final_cols]
            final_data = final_data.sort_values(['Ticker', 'Expiration', 'strike', 'Type'])
            
            print(f"✓ {ticker_symbol}: {len(final_data)} contracts")
            return final_data
            
    except Exception as e:
        print(f"❌ Error {ticker_symbol}: {e}")
        sys.exit(1)

def main():
    print("Options Data Fetcher - FAST MODE")
    print(f"Start: {datetime.now().strftime('%H:%M:%S')}")
    
    start_time = time.time()
    
    # Fetch American options
    print("\n=== AMERICAN OPTIONS ===")
    american_data = []
    for ticker in AMERICAN_STOCKS:
        data = fetch_ticker_options(ticker, is_european=False)
        if not data.empty:
            american_data.append(data)
        time.sleep(0.5)  # Rate limit between tickers
    
    # Fetch European options
    print("\n=== EUROPEAN OPTIONS ===")
    european_data = []
    for ticker in EUROPEAN_INDICES:
        data = fetch_ticker_options(ticker, is_european=True)
        if not data.empty:
            european_data.append(data)
        time.sleep(0.5)  # Rate limit between tickers
    
    # Save American options
    if american_data:
        final_american = pd.concat(american_data, ignore_index=True)
        timestamp = datetime.now().strftime('%Y-%m-%d')
        filename = f"american_options_{timestamp}.csv"
        final_american.to_csv(filename, index=False)
        print(f"\n✅ American saved: {filename} ({len(final_american):,} contracts)")
    
    # Save European options
    if european_data:
        final_european = pd.concat(european_data, ignore_index=True)
        timestamp = datetime.now().strftime('%Y-%m-%d')
        filename = f"european_options_{timestamp}.csv"
        final_european.to_csv(filename, index=False)
        print(f"✅ European saved: {filename} ({len(final_european):,} contracts)")
    
    # Summary
    total_time = time.time() - start_time
    total_contracts = (len(final_american) if american_data else 0) + (len(final_european) if european_data else 0)
    print(f"\n🎉 COMPLETE in {total_time:.1f}s - {total_contracts:,} total contracts")

if __name__ == "__main__":
    main()