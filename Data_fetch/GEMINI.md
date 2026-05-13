# Gemini Code Assistant Context

This document provides context for the AI assistant to understand the project structure, goals, and conventions.

## Project Overview

This project is a collection of Python scripts designed to fetch financial data, primarily American stock and options data, for analysis. The main goal is to acquire data for American options to study their characteristics and test trading strategies.

**Key Technologies:**

*   **Python:** The primary language for all scripts.
*   **yfinance:** Used to fetch stock data and options chains from Yahoo Finance.
*   **pandas:** Used for data manipulation and storage in CSV format.
*   **uv:** Preferred tool for package management and virtual environments.
*   **ruff:** Used for linting and code formatting.
*   **pyproject.toml:** Used for project configuration.
*   **Nix:** A `nix-shell` command is provided for setting up a consistent development environment.

**Project Structure:**

The project consists of several Python scripts for fetching different types of data:

*   `price_fetcher.py`: A script to fetch daily stock prices for tickers specified in a TOML file.
*   `options_fetcher_final.py`: The main script for fetching full American option chains.

## Building and Running

There are multiple ways to run the scripts in this project, depending on the goal.

### 1. Using the Python Virtual Environment

A virtual environment is provided in `.venv`.

**To activate the environment:**

```bash
source .venv/bin/activate
```

**To run the main options fetcher:**

```bash
# Fetch American options
python options_fetcher_final.py
```

### 2. Using the Nix Shell

A Nix shell configuration is provided for a reproducible environment.

**To start the Nix shell:**

```bash
nix-shell -p python311 python311Packages.uv python311Packages.venv
```

Once in the shell, you can create a virtual environment and install dependencies.

## Development Conventions

*   **Data Format:** All fetched data is saved in CSV format.
*   **File Naming:** Output files are timestamped (e.g., `stock_data_YYYY-MM-DD.csv`).
*   **Modularity:** The scripts are designed to be modular and run independently.
*   **Error Handling:** The scripts include error handling and rate limiting to prevent issues with the data sources.
