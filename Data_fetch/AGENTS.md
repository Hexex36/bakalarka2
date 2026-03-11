# AGENTS.md - Developer Guidelines for Data_fetch Project

This document provides guidelines for AI agents working on this codebase.

## Project Overview

- **Project name**: data-fetcher
- **Description**: Python project for fetching financial data (stock prices, options chains) from Yahoo Finance
- **Python version**: >=3.11
- **Virtual environment**: `.venv` (use `source .venv/bin/activate`)

## Dependencies

```
yfinance
pandas
toml
tomlkit
```

---

## Build, Lint, and Test Commands

### Running Scripts

```bash
# Activate virtual environment first
source .venv/bin/activate

# Run individual scripts
python stock_fetcher.py
python options_fetcher_final.py
python rate_functioner.py
python price_fetcher.py

# Or using the venv Python directly
.venv/bin/python stock_fetcher.py
```

### Linting with Ruff

This project uses **ruff** for linting and formatting:

```bash
# Check for linting issues
ruff check .

# Auto-fix linting issues
ruff check --fix .

# Format code
ruff format .

# Run with specific rule selection
ruff check --select=E,F,W .

# Show ruff version (installed: 0.12.5)
ruff --version
```

### Virtual Environment

```bash
# Create virtual environment
python -m venv .venv

# Activate (Linux/macOS)
source .venv/bin/activate

# Install dependencies
pip install -e .
pip install yfinance pandas toml tomlkit

# Or using the lock file
pip install -r requirements.txt  # if exists
```

---

## Code Style Guidelines

### General Principles

- **Be Pythonic**: Follow PEP 8 conventions
- **Keep it readable**: Code is read more often than written
- **No comments unless requested**: Avoid adding unnecessary comments

### Imports

- Standard library imports first
- Third-party imports second
- Local imports last
- Separate groups with blank lines
- Sort within groups alphabetically

```python
# Good
import os
import sys
from datetime import datetime

import pandas as pd
import yfinance as yf
import toml

from my_module import my_function
```

### Formatting

- Maximum line length: 88 characters (ruff default)
- Use 4 spaces for indentation (no tabs)
- Use trailing commas in multi-line structures
- Use parentheses for line continuation

```python
# Good
result = some_function(
    arg1,
    arg2,
    arg3,
)

# Good - string concatenation
long_string = (
    "This is a long string that "
    "continues on the next line"
)
```

### Naming Conventions

- **Variables/functions**: `snake_case` (e.g., `my_variable`, `fetch_data`)
- **Classes**: `PascalCase` (e.g., `RateFuncer`, `DataFetcher`)
- **Constants**: `SCREAMING_SNAKE_CASE` (e.g., `MAX_RETRIES`, `API_TIMEOUT`)
- **Private variables**: prefix with underscore (e.g., `_private_var`)

```python
# Good
def fetch_stock_prices(ticker_symbol):
    MAX_RETRIES = 3
    class StockDataCollector:
        def __init__(self):
            self._cache = {}
```

### Types

- Use type hints where beneficial, especially for function signatures
- Prefer explicit types for public APIs
- Can use inline types for obvious cases

```python
# Good
def get_rate_for_expiration(expiration_date: str) -> dict[str, float]:
    """Get closest treasury rate for specific option expiration date."""
    ...

# Good - simpler cases can omit types
def process_options_file(input_path, output_path=None):
```

### Error Handling

- Use specific exception types when possible
- Provide meaningful error messages
- Handle exceptions at the appropriate level

```python
# Good
try:
    data = pd.read_csv(filename)
except FileNotFoundError:
    print(f"Error: File {filename} not found")
    sys.exit(1)
except Exception as e:
    print(f"Unexpected error: {e}")
    raise

# Good - graceful degradation
if not expirations:
    print(f"⚠️  No expirations found for {ticker_symbol}")
    continue
```

### Data Processing (Pandas)

- Use method chaining where readable
- Prefer vectorized operations over loops
- Use meaningful column names

```python
# Good
df = (
    df.assign(Type='Call')
      .assign(Ticker=ticker_symbol)
      .sort_values(['Ticker', 'Expiration', 'strike'])
)

# Good - check columns exist before using
desired_cols = ['Ticker', 'Expiration', 'strike']
final_cols = [col for col in desired_cols if col in df.columns]
df = df[final_cols]
```

### Naming Files

- Use `snake_case.py` for Python modules
- Use descriptive, functional names: `rate_functioner.py`, `stock_fetcher.py`

### Configuration

- Store configuration in `tickers.toml` (used by this project)
- Use TOML format for config files

---

## Testing

This project currently has **no formal test suite**. When adding tests:

```bash
# If using pytest
pytest                          # run all tests
pytest path/to/test_file.py    # run specific file
pytest -k test_name            # run specific test
pytest --tb=short               # shorter traceback

# If using unittest
python -m unittest discover
python -m unittest test_module
```

Recommended testing approach:
- Use **pytest** for new tests
- Place tests in `tests/` directory
- Name test files as `test_*.py` or `*_test.py`
- Use descriptive test function names: `test_function_name_scenario`

---

## Common Patterns in This Codebase

### Rate Limiting

```python
import time
time.sleep(0.5)  # Between API calls
time.sleep(1)   # Between different tickers
```

### CSV Output with Timestamp

```python
from datetime import datetime
timestamp = datetime.now().strftime('%Y-%m-%d')
filename = f"data_{timestamp}.csv"
df.to_csv(filename, index=False)
```

### Loading TOML Config

```python
import toml

with open('tickers.toml', 'r') as f:
    config = toml.load(f)

american_tickers = config.get('american_tickers', {})
```

---

## Notes

- Uses Yahoo Finance API via `yfinance` (free, no API key required)
- Data includes stock prices and options chains
- Rate limiting is essential to avoid API blocks
- Output is saved as CSV files with timestamps

---

## Ruff Configuration

The project uses ruff with default settings (version 0.12.5). Key settings:
- Line length: 88
- Target Python: 3.11
- Auto-fix: enabled for safe rules

For custom rules, add to `pyproject.toml`:

```toml
[tool.ruff]
line-length = 88
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W"]
ignore = []
```
