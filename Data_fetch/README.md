# Stock Data Fetcher

Simple Python script to fetch daily stock price data for S&P 500 stocks recommended for options study.

## Features

- Fetches 1 year of daily stock data for 9 S&P 500 stocks
- Categorizes stocks by volatility (High/Medium/Low)
- Includes rate limiting to avoid API blocks
- Saves data to CSV with timestamp
- Error handling for failed requests

## Requirements

Install the required package:

```bash
pip install yfinance pandas
```

## Usage

```bash
cd Data_fetch
python stock_fetcher.py
```

## Stocks Included

**High Volatility:**
- TSLA (Tesla)
- NVDA (NVIDIA) 
- AMD (Advanced Micro Devices)

**Moderate Volatility:**
- AAPL (Apple)
- MSFT (Microsoft)
- GOOGL (Alphabet)

**Low Volatility:**
- JNJ (Johnson & Johnson)
- PG (Procter & Gamble)
- KO (Coca-Cola)

## Output

Creates a CSV file named `stock_data_YYYY-MM-DD.csv` with columns:
- Date (index)
- Ticker
- Volatility_Category
- Open, High, Low, Close
- Volume

## Notes

- Uses yfinance (Yahoo Finance API) - free and no API key required
- Includes 1-second delays between requests to avoid rate limiting
- Script will retry failed stocks and continue with others