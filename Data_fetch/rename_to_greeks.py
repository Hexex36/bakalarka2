#!/usr/bin/env python3
"""
Script to rename columns in options CSV files to Greek notation.
Only renames existing columns that represent Greek-like concepts.
"""

import pandas as pd
import os


def rename_columns_to_greek_notation(df: pd.DataFrame) -> pd.DataFrame:
    """
    Rename columns to Greek notation while preserving non-Greek columns.

    Args:
        df: Input DataFrame with original column names

    Returns:
        DataFrame with Greek notation column names
    """
    # Define column renaming mapping
    # Only rename columns that represent Greek-like concepts
    column_mapping = {
        "historical_volatility": "sigma",  # σ - volatility
        "treasury_rate": "r",  # r - risk-free rate
        "current_stock_price": "S",  # S - current stock price
        "strike": "K",  # K - strike price
        "lastPrice": "option_price",  # option price (not a Greek but standard notation)
        "bid": "bid_price",
        "ask": "ask_price",
        "volume": "volume",
        "openInterest": "open_interest",
        "Ticker": "ticker",
        "Expiration": "expiration",
        "Type": "option_type",
    }

    # Create a copy to avoid modifying original
    df_renamed = df.copy()

    # Rename columns using the mapping
    df_renamed = df_renamed.rename(columns=column_mapping)

    return df_renamed


def process_options_file(input_file: str, output_file: str) -> None:
    """
    Process an options CSV file and rename columns to Greek notation.

    Args:
        input_file: Path to input CSV file
        output_file: Path to output CSV file with Greek column names
    """
    print(f"Processing {input_file}...")

    # Read the CSV file
    df = pd.read_csv(input_file)
    print(f"Original columns: {list(df.columns)}")

    # Rename columns to Greek notation
    df_renamed = rename_columns_to_greek_notation(df)
    print(f"Renamed columns: {list(df_renamed.columns)}")

    # Save to new file
    df_renamed.to_csv(output_file, index=False)
    print(f"Saved to {output_file}")

    # Show sample data
    print(f"\nSample data (first 3 rows):")
    print(df_renamed.head(3))

    print(f"\nProcessed {len(df_renamed)} records")


def main():
    """Main function to process both American and European options files."""

    # Define input and output files
    files_to_process = [
        {
            "input": "./american_options_2026-02-27_enhanced.csv",
            "output": "./american_options_2026-02-27_greeks.csv",
        },
        {
            "input": "./european_options_2026-02-27_enhanced.csv",
            "output": "./european_options_2026-02-27_greeks.csv",
        },
    ]

    print("=" * 60)
    print("RENAMING COLUMNS TO GREEK NOTATION")
    print("=" * 60)

    for file_info in files_to_process:
        if os.path.exists(file_info["input"]):
            print(f"\n{'-' * 40}")
            process_options_file(file_info["input"], file_info["output"])
            print(f"{'-' * 40}")
        else:
            print(f"Warning: {file_info['input']} not found, skipping...")

    print(f"\n{'=' * 60}")
    print("COLUMN RENAMING COMPLETE")
    print("=" * 60)


if __name__ == "__main__":
    main()
