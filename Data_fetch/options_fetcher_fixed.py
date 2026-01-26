#!/usr/bin/env python3
"""
Options Data Fetcher for S&P500 Stocks
Fetches full options chains for American and European options using yfinance
"""

import yfinance as yf
import pandas as pd
from datetime import datetime
import time
import sys
import os

# American stocks (individual equity options)
AMERICAN_STOCKS = {
    'High Volatility': ['TSLA', 'NVDA', 'AMD'],
    'Moderate Volatility': ['AAPL', 'MSFT', 'GOOGL'],
    'Low Volatility': ['JNJ', 'PG', 'KO']
}

# European indices (index options)
EUROPEAN_INDICES = ['SPX', 'XSP']

def fetch_american_options():
    """Fetch all American options for individual stocks"""
    print("Fetching American Options (Individual Stocks)...")
    print("=" * 50)
    
    all_american_data = []
    
    for category, tickers in AMERICAN_STOCKS.items():
        print(f"\n--- {category} ---")
        
        for ticker_symbol in tickers:
            print(f"Fetching {ticker_symbol} options...")
            
            try:
                ticker = yf.Ticker(ticker_symbol)
                
                # Get all expiration dates
                expirations = ticker.options
                if not expirations:
                    print(f"⚠️  No expirations found for {ticker_symbol}")
                    continue
                
                print(f"  Found {len(expirations)} expirations")
                
                # Fetch each expiration's option chain
                for i, exp_date in enumerate(expirations):
                    try:
                        option_chain = ticker.option_chain(exp_date)
                        
                        # Process calls
                        calls = option_chain.calls.copy()
                        calls['Type'] = 'Call'
                        calls['Ticker'] = ticker_symbol
                        calls['Expiration'] = exp_date
                        
                        # Process puts
                        puts = option_chain.puts.copy()
                        puts['Type'] = 'Put'
                        puts['Ticker'] = ticker_symbol
                        puts['Expiration'] = exp_date
                        
                        # Combine calls and puts
                        combined = pd.concat([calls, puts], ignore_index=True)
                        all_american_data.append(combined)
                        
                        if (i + 1) % 5 == 0:
                            print(f"    Processed {i + 1}/{len(expirations)} expirations")
                        
                        # Rate limiting
                        time.sleep(0.5)
                        
                    except Exception as e:
                        print(f"⚠️  Error processing {ticker_symbol} {exp_date}: {e}")
                        continue
                
                # Success message
                total_contracts = len([x for x in all_american_data if any(x['Ticker'] == ticker_symbol)])
                print(f"  ✓ {ticker_symbol}: {total_contracts} contracts fetched")
                
            except Exception as e:
                print(f"❌ CRITICAL ERROR fetching {ticker_symbol}: {e}")
                print("Failing entirely as requested...")
                sys.exit(1)
            
            # Rate limiting between tickers
            time.sleep(1)
    
    if all_american_data:
        final_american_data = pd.concat(all_american_data, ignore_index=True)
        
        # Select and reorder columns (use actual column names from yfinance)
        desired_cols = ['Ticker', 'Expiration', 'strike', 'Type', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest']
        
        # Only include columns that exist
        final_cols = []
        for col in desired_cols:
            if col in final_american_data.columns:
                final_cols.append(col)
        
        final_american_data = final_american_data[final_cols]
        
        # Sort for readability
        final_american_data = final_american_data.sort_values(by=['Ticker', 'Expiration', 'strike', 'Type'])
        
        return final_american_data
    else:
        return pd.DataFrame()

def fetch_european_options():
    """Fetch European options for indices"""
    print("\nFetching European Options (Indices)...")
    print("=" * 50)
    
    all_european_data = []
    
    for ticker_symbol in EUROPEAN_INDICES:
        print(f"Fetching {ticker_symbol} options...")
        
        try:
            ticker = yf.Ticker(ticker_symbol)
            
            # Get all expiration dates
            expirations = ticker.options
            if not expirations:
                print(f"⚠️  No expirations found for {ticker_symbol}")
                continue
            
            print(f"  Found {len(expirations)} expirations")
            
            # Fetch each expiration's option chain
            for i, exp_date in enumerate(expirations):
                try:
                    option_chain = ticker.option_chain(exp_date)
                    
                    # Process calls
                    calls = option_chain.calls.copy()
                    calls['Type'] = 'Call'
                    calls['Ticker'] = ticker_symbol
                    calls['Expiration'] = exp_date
                    calls['ExerciseStyle'] = 'European'
                    
                    # Process puts
                    puts = option_chain.puts.copy()
                    puts['Type'] = 'Put'
                    puts['Ticker'] = ticker_symbol
                    puts['Expiration'] = exp_date
                    puts['ExerciseStyle'] = 'European'
                    
                    # Combine calls and puts
                    combined = pd.concat([calls, puts], ignore_index=True)
                    all_european_data.append(combined)
                    
                    if (i + 1) % 5 == 0:
                        print(f"    Processed {i + 1}/{len(expirations)} expirations")
                    
                    # Rate limiting
                    time.sleep(0.5)
                    
                except Exception as e:
                    print(f"⚠️  Error processing {ticker_symbol} {exp_date}: {e}")
                    continue
            
            # Success message
            total_contracts = len([x for x in all_european_data if any(x['Ticker'] == ticker_symbol)])
            print(f"  ✓ {ticker_symbol}: {total_contracts} contracts fetched")
            
        except Exception as e:
            print(f"❌ CRITICAL ERROR fetching {ticker_symbol}: {e}")
            print("Failing entirely as requested...")
            sys.exit(1)
        
        # Rate limiting between tickers
        time.sleep(1)
    
    if all_european_data:
        final_european_data = pd.concat(all_european_data, ignore_index=True)
        
        # Select and reorder columns
        desired_cols = ['Ticker', 'Expiration', 'strike', 'Type', 'bid', 'ask', 'lastPrice', 'volume', 'openInterest', 'ExerciseStyle']
        
        # Only include columns that exist
        final_cols = []
        for col in desired_cols:
            if col in final_european_data.columns:
                final_cols.append(col)
        
        final_european_data = final_european_data[final_cols]
        
        # Sort for readability
        final_european_data = final_european_data.sort_values(by=['Ticker', 'Expiration', 'strike', 'Type'])
        
        return final_european_data
    else:
        return pd.DataFrame()

def save_options_data(data, filename_prefix):
    """Save options data to CSV with timestamp"""
    if data.empty:
        print(f"No data to save for {filename_prefix}")
        return
    
    timestamp = datetime.now().strftime('%Y-%m-%d')
    filename = f"{filename_prefix}_{timestamp}.csv"
    
    # Save to CSV
    data.to_csv(filename, index=False)
    
    # Summary statistics
    print(f"\n📊 {filename_prefix} Summary:")
    print(f"   File: {filename}")
    print(f"   Total contracts: {len(data):,}")
    
    # Count by ticker
    ticker_counts = data['Ticker'].value_counts()
    print(f"   Contracts per ticker:")
    for ticker, count in ticker_counts.items():
        print(f"     {ticker}: {count:,}")
    
    # Count by type
    type_counts = data['Type'].value_counts()
    print(f"   Calls vs Puts: {type_counts.get('Call', 0):,} Calls, {type_counts.get('Put', 0):,} Puts")
    
    # Show sample of data
    print(f"\n   Sample data (first 3 rows):")
    print(data.head(3).to_string(index=False))

def main():
    print("Options Data Fetcher - Starting")
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    start_time = time.time()
    
    try:
        # Fetch American options
        american_data = fetch_american_options()
        if not american_data.empty:
            save_options_data(american_data, 'american_options')
        else:
            print("No American options data fetched")
        
        # Fetch European options  
        european_data = fetch_european_options()
        if not european_data.empty:
            save_options_data(european_data, 'european_options')
        else:
            print("No European options data fetched")
        
        # Final summary
        total_time = time.time() - start_time
        print(f"\n✅ COMPLETE - Total time: {total_time:.1f} seconds")
        print(f"   American contracts: {len(american_data):,}")
        print(f"   European contracts: {len(european_data):,}")
        print(f"   Total contracts: {len(american_data) + len(european_data):,}")
        
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ UNEXPECTED ERROR: {e}")
        print("Failing entirely as requested...")
        sys.exit(1)

if __name__ == "__main__":
    main()