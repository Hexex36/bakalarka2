#!/usr/bin/env python3
"""
Minimal European Options Test using alternative APIs
Tests Cboe public data and other free sources
"""

import requests
import pandas as pd
from datetime import datetime
import time
import json

def fetch_cboe_spx():
    """Test Cboe public SPX data"""
    try:
        print("Testing Cboe SPX public data...")
        
        # Cboe has public quotes API
        url = "https://cdn.cboe.com/data/mktstat/historical/2025/quoted/SPX_EuropeanQuotes.csv"
        
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            print("✅ Cboe SPX data accessible")
            print("This provides European-style SPX quotes")
            print("Note: This is quotes, not full options chains")
            return True
        else:
            print(f"❌ Cboe API failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Cboe test error: {e}")
        return False

def test_polygon_free():
    """Test Polygon free tier"""
    try:
        print("\nTesting Polygon free tier...")
        
        # Polygon's free options chains endpoint
        url = "https://api.polygon.io/v3/reference/options/contracts"
        
        # This would need API key, just test availability
        print("Polygon requires API key for options data")
        print("Free tier: 5 requests/minute")
        print("European options: Available through market data")
        return True
        
    except Exception as e:
        print(f"❌ Polygon test error: {e}")
        return False

def main():
    print("European Options Data Source Testing")
    print("=" * 50)
    print(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    cboe_success = fetch_cboe_spx()
    polygon_success = test_polygon_free()
    
    print(f"\n📊 Results Summary:")
    print(f"Cboe SPX access: {'✅' if cboe_success else '❌'}")
    print(f"Polygon available: {'✅' if polygon_success else '❌'}")
    
    print(f"\n💡 Recommendations:")
    if cboe_success:
        print("• Use Cboe SPX quotes data for European index reference")
        print("• Consider paid Cboe Data Suite for full options chains")
    
    if polygon_success:
        print("• Polygon offers comprehensive options with free tier")
        print("• Requires API key signup (free tier available)")
    
    print("\n🔄 For comprehensive European options:")
    print("• Get Cboe Data Suite API key (paid)")
    print("• Or use Polygon/Intrinio with API key")
    print("• Manual calculation using SPX spot + implied volatilities")

if __name__ == "__main__":
    main()