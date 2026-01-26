# Gemini Code Assistant Context

This document provides context for the AI assistant to understand the project structure, goals, and conventions.

## Project Overview

This project is a collection of Python scripts designed to fetch financial data, primarily stock and options data, for analysis. The main goal is to acquire data for both American and European options to study their characteristics and test trading strategies.

**Key Technologies:**

*   **Python:** The primary language for all scripts.
*   **yfinance:** Used to fetch stock data and options chains from Yahoo Finance.
*   **pandas:** Used for data manipulation and storage in CSV format.
*   **OpenBB Platform:** An alternative data source, with a Docker setup provided for easy deployment.
*   **Nix:** A `nix-shell` command is provided for setting up a consistent development environment.

**Project Structure:**

The project consists of several Python scripts for fetching different types of data:

*   `stock_fetcher.py`: A simple script to fetch daily stock prices.
*   `options_fetcher_final.py`: The main script for fetching full American and European option chains.
*   `european_options_fetcher.py`: A script for generating sample European options data.
*   Test scripts (`test_*.py`): Scripts for testing different data sources and functionalities.

## Building and Running

There are multiple ways to run the scripts in this project, depending on the goal.

### 1. Using the Python Virtual Environment

A virtual environment is provided in `venv3.11`.

**To activate the environment:**

```bash
source venv3.11/bin/activate
```

**To run the main options fetcher:**

```bash
# Fetch default American and European options
python options_fetcher_final.py

# Fetch European options for custom indices
python options_fetcher_final.py <index1> <index2>
```

### 2. Using the Nix Shell

A Nix shell configuration is provided for a reproducible environment.

**To start the Nix shell:**

```bash
nix-shell -p python311 python311Packages.pip python311Packages.venv
```

Once in the shell, you can create a virtual environment and install dependencies.

### 3. Using Docker for OpenBB

The project includes a Docker setup for running the OpenBB platform, which can be used as an alternative data source.

**To start the OpenBB container:**

```bash
docker-compose up
```

This will start the OpenBB API on `http://localhost:8080`.

## Development Conventions

*   **Data Format:** All fetched data is saved in CSV format.
*   **File Naming:** Output files are timestamped (e.g., `stock_data_YYYY-MM-DD.csv`).
*   **Modularity:** The scripts are designed to be modular and run independently. `options_fetcher_final.py` can be run with or without command-line arguments to change its behavior.
*   **Error Handling:** The scripts include error handling and rate limiting to prevent issues with the data sources.
