import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, Optional


class RateFuncer:
    def __init__(self, rates_file: str = "rates.txt"):
        # Parse the rates file
        with open(rates_file, "r") as file:
            data = file.read()

        data = data.split("\n")
        data = [line.split(",") for line in data if line.strip()]
        assert len(data[0]) == len(data[1])

        # Parse base date (when rates were measured) - first column is date string
        self.base_date = datetime.strptime(data[1][0], "%m/%d/%Y")

        # Convert string rates to float values (skip the date column)
        rates_row = [float(rate) for rate in data[1][1:]]

        # Create dictionary mapping maturity to rate (skip the date column)
        self.rates = {data[0][i]: rates_row[i - 1] for i in range(1, len(data[0]))}

        # Create maturity mapping in months
        self.maturity_months = {
            "1m": 1,
            "1.5m": 1.5,
            "2m": 2,
            "3m": 3,
            "4m": 4,
            "6m": 6,
            "1y": 12,
            "2y": 24,
            "3y": 36,
            "5y": 60,
            "7y": 84,
            "10y": 120,
            "20y": 240,
            "30y": 360,
        }

    def get_rate_for_expiration(self, expiration_date: str) -> Optional[float]:
        """
        Get the appropriate treasury rate for an option expiration date.

        Args:
            expiration_date: Option expiration date in YYYY-MM-DD format

        Returns:
            Treasury rate as decimal (e.g., 0.0377 for 3.77%)
        """
        try:
            # Parse expiration date
            exp_date = datetime.strptime(expiration_date, "%Y-%m-%d")

            # Calculate time to expiration in months
            time_diff = exp_date - self.base_date
            months_to_expiration = time_diff.days / 30.44  # Average days per month

            # Handle negative time (expiration before base date)
            if months_to_expiration < 0:
                return None

            # Find the closest available maturity
            return self._find_closest_rate(months_to_expiration)

        except ValueError as e:
            print(f"Error parsing date {expiration_date}: {e}")
            return None

    def _find_closest_rate(self, months: float) -> float:
        """
        Find the closest treasury rate for a given number of months.

        Args:
            months: Time to expiration in months

        Returns:
            Treasury rate as decimal
        """
        # Find the closest maturity
        closest_maturity = min(
            self.maturity_months.keys(),
            key=lambda k: abs(self.maturity_months[k] - months),
        )

        # Get the rate and convert to decimal
        rate_percent = self.rates[closest_maturity]
        return rate_percent / 100.0

    def get_interpolated_rate(self, expiration_date: str) -> Optional[float]:
        """
        Get an interpolated treasury rate for better accuracy.

        Args:
            expiration_date: Option expiration date in YYYY-MM-DD format

        Returns:
            Interpolated treasury rate as decimal
        """
        try:
            # Parse expiration date
            exp_date = datetime.strptime(expiration_date, "%Y-%m-%d")

            # Calculate time to expiration in months
            time_diff = exp_date - self.base_date
            months_to_expiration = time_diff.days / 30.44

            # Handle negative time
            if months_to_expiration < 0:
                return None

            # Find surrounding maturities for interpolation
            return self._interpolate_rate(months_to_expiration)

        except ValueError as e:
            print(f"Error parsing date {expiration_date}: {e}")
            return None

    def _interpolate_rate(self, months: float) -> float:
        """
        Linear interpolation between two treasury rates with extrapolation for edge cases.

        Args:
            months: Time to expiration in months

        Returns:
            Interpolated/extrapolated treasury rate as decimal
        """
        # Sort maturities by months
        sorted_maturities = sorted(self.maturity_months.items(), key=lambda x: x[1])

        # Find the two surrounding maturities
        lower_maturity = None
        upper_maturity = None

        for maturity, maturity_months in sorted_maturities:
            if maturity_months <= months:
                lower_maturity = (maturity, maturity_months)
            elif maturity_months > months and upper_maturity is None:
                upper_maturity = (maturity, maturity_months)
                break

        # Handle edge cases with extrapolation
        if lower_maturity is None:
            # For expirations <1 month, extrapolate forward from 1m rate
            if months < 1:
                rate_percent = self.rates[sorted_maturities[0][0]]
                # Linear extrapolation: rate = 1m_rate + slope * (months - 1m_in_months)
                # Estimate slope from first few maturities if available
                if len(sorted_maturities) >= 2:
                    first_maturity_months = sorted_maturities[0][1]
                    second_maturity_months = sorted_maturities[1][1]
                    if first_maturity_months != 0:
                        slope = (
                            self.rates[sorted_maturities[1][0]]
                            - self.rates[sorted_maturities[0][0]]
                        ) / (second_maturity_months - first_maturity_months)
                        rate_percent = self.rates[sorted_maturities[0][0]] + slope * (
                            months - 1
                        )
                return rate_percent / 100.0
            else:
                return self.rates[sorted_maturities[0][0]] / 100.0

        if upper_maturity is None:
            # For expirations >30 years, extrapolate forward from 30y rate
            if months > 30:
                rate_percent = self.rates[sorted_maturities[-1][0]]
                # Linear extrapolation: rate = 30y_rate + slope * (months - 30y_in_months)
                # Estimate slope from last few maturities if available
                if len(sorted_maturities) >= 2:
                    second_last_maturity_months = sorted_maturities[-2][1]
                    last_maturity_months = sorted_maturities[-1][1]
                    if second_last_maturity_months != last_maturity_months:
                        slope = (
                            self.rates[sorted_maturities[-1][0]]
                            - self.rates[second_last_maturity_months]
                        ) / (last_maturity_months - second_last_maturity_months)
                        rate_percent = self.rates[sorted_maturities[-1][0]] + slope * (
                            months - 30
                        )
                return rate_percent / 100.0
            else:
                return self.rates[sorted_maturities[-1][0]] / 100.0

        # Linear interpolation between two treasury rates
        lower_rate = self.rates[lower_maturity[0]] / 100.0
        upper_rate = self.rates[upper_maturity[0]] / 100.0

        weight = (months - lower_maturity[1]) / (upper_maturity[1] - lower_maturity[1])

        return lower_rate + weight * (upper_rate - lower_rate)

    def process_options_file(self, options_file_path: str) -> pd.DataFrame:
        """
        Process an options file and add appropriate treasury rates.

        Args:
            options_file_path: Path to the options CSV file

        Returns:
            DataFrame with added 'treasury_rate' column
        """
        # Read options file
        df = pd.read_csv(options_file_path)

        # Add treasury rate column
        df["treasury_rate"] = df["Expiration"].apply(self.get_interpolated_rate)

        return df

    def add_stock_data_to_options(
        self,
        options_df: pd.DataFrame,
        stock_calculator: "StockPriceVolatilityCalculator",
    ) -> pd.DataFrame:
        """
        Add stock price and volatility data to options DataFrame.

        Args:
            options_df: DataFrame with options data
            stock_calculator: StockPriceVolatilityCalculator instance

        Returns:
            Enhanced DataFrame with stock price and volatility columns
        """
        # Get unique tickers from options
        option_tickers = options_df["Ticker"].unique()

        # Create mapping of ticker to stock data
        stock_data_map = {}
        for ticker in option_tickers:
            stock_data_map[ticker] = stock_calculator.process_ticker_data(ticker)

        # Add current price column
        options_df["current_stock_price"] = options_df["Ticker"].map(
            lambda x: stock_data_map.get(x, {}).get("current_price")
        )

        # Add volatility column
        options_df["historical_volatility"] = options_df["Ticker"].map(
            lambda x: stock_data_map.get(x, {}).get("volatility")
        )

        return options_df


class StockPriceVolatilityCalculator:
    def __init__(self, stock_prices_file: str):
        """
        Initialize with stock prices data.

        Args:
            stock_prices_file: Path to CSV with stock price data
        """
        self.stock_data = pd.read_csv(stock_prices_file)
        self.stock_data["Date"] = pd.to_datetime(self.stock_data["Date"], utc=True)
        self.tickers = self.stock_data["Ticker"].unique()

    def get_current_stock_price(
        self, ticker: str, target_date: str = "2026-02-27"
    ) -> Optional[float]:
        """
        Get the most recent stock price for a ticker as of target date.

        Args:
            ticker: Stock ticker symbol
            target_date: Date to get price as of (YYYY-MM-DD)

        Returns:
            Current stock price or None if not found
        """
        try:
            target_dt = pd.to_datetime(target_date, utc=True)
            ticker_mask = self.stock_data["Ticker"] == ticker
            ticker_data = self.stock_data[ticker_mask]

            if len(ticker_data) == 0:
                return None

            # Get the most recent price up to target date
            recent_mask = ticker_data["Date"] <= target_dt
            recent_data = ticker_data[recent_mask]
            if len(recent_data) == 0:
                return None

            latest_row = recent_data.iloc[-1]
            return float(latest_row["Close"])

        except Exception as e:
            print(f"Error getting stock price for {ticker}: {e}")
            return None

    def calculate_historical_volatility(
        self, ticker: str, lookback_days: int = 252
    ) -> Optional[float]:
        """
        Calculate annualized historical volatility using daily returns.

        Args:
            ticker: Stock ticker symbol
            lookback_days: Number of trading days to use for calculation (default ~1 year)

        Returns:
            Annualized volatility as decimal or None if not found
        """
        try:
            ticker_mask = self.stock_data["Ticker"] == ticker
            ticker_data = self.stock_data[ticker_mask].copy()
            ticker_data = ticker_data.sort_values(by="Date")

            if len(ticker_data) < 2:
                return None

            # Use the last lookback_days of data
            if len(ticker_data) > lookback_days:
                ticker_data = ticker_data.tail(lookback_days)

            # Calculate daily returns
            ticker_data["Daily_Return"] = np.log(
                ticker_data["Close"] / ticker_data["Close"].shift(1)
            )

            # Remove first row with NaN return
            returns = ticker_data["Daily_Return"].dropna()

            if len(returns) < 2:
                return None

            # Calculate annualized volatility
            daily_vol = returns.std()
            annualized_vol = daily_vol * np.sqrt(252)  # 252 trading days per year

            return float(annualized_vol)

        except Exception as e:
            print(f"Error calculating volatility for {ticker}: {e}")
            return None

    def process_ticker_data(
        self, ticker: str, target_date: str = "2026-02-27"
    ) -> Dict[str, Optional[float]]:
        """
        Get current price and volatility for a ticker.

        Args:
            ticker: Stock ticker symbol
            target_date: Date to get price as of (YYYY-MM-DD)

        Returns:
            Dictionary with current_price and volatility
        """
        current_price = self.get_current_stock_price(ticker, target_date)
        volatility = self.calculate_historical_volatility(ticker)

        return {"current_price": current_price, "volatility": volatility}


class EnhancedOptionsProcessor:
    """
    Combined processor that handles both rates and stock data for options.
    """

    def __init__(
        self,
        rates_file: str = "rates_2026_02_26.txt",
        stock_prices_file: str = "stock_prices_2026-02-27.csv",
    ):
        self.rate_funcer = RateFuncer(rates_file)
        self.stock_calculator = StockPriceVolatilityCalculator(stock_prices_file)

    def process_options_file(self, options_file_path: str) -> pd.DataFrame:
        """
        Process options file and add both treasury rates and stock data.

        Args:
            options_file_path: Path to the options CSV file

        Returns:
            Enhanced DataFrame with rates, stock prices, and volatility
        """
        # Process rates
        df = self.rate_funcer.process_options_file(options_file_path)

        # Add stock data
        df = self.rate_funcer.add_stock_data_to_options(df, self.stock_calculator)

        return df


if __name__ == "__main__":
    # Test the enhanced processor
    processor = EnhancedOptionsProcessor()

    # Test with some sample expiration dates
    test_dates = [
        "2026-02-28",  # 1 day
        "2026-03-27",  # 1 month
        "2026-05-27",  # 3 months
        "2026-08-27",  # 6 months
        "2027-02-27",  # 1 year
        "2028-02-27",  # 2 years
    ]

    print("Testing rate matching:")
    for date in test_dates:
        rate = processor.rate_funcer.get_interpolated_rate(date)
        print(f"Expiration: {date}, Rate: {rate}")

    # Process European options file with enhanced data
    options_df = processor.process_options_file("./european_options_2026-02-27.csv")
    print(f"\nProcessed {len(options_df)} European options")
    print(f"Sample with rates and stock data:")
    sample_cols = [
        "Ticker",
        "Expiration",
        "strike",
        "treasury_rate",
        "current_stock_price",
        "historical_volatility",
    ]
    print(options_df[sample_cols].head(10))

    # Save results to new CSV file
    output_file = "./european_options_2026-02-27_enhanced.csv"
    options_df.to_csv(output_file, index=False)
    print(f"\nSaved enhanced European results to {output_file}")

    # Process American options file with enhanced data
    options_df = processor.process_options_file("./american_options_2026-02-27.csv")
    print(f"\nProcessed {len(options_df)} American options")
    print(f"Sample with rates and stock data:")
    print(options_df[sample_cols].head(10))

    # Save results to new CSV file
    output_file = "./american_options_2026-02-27_enhanced.csv"
    options_df.to_csv(output_file, index=False)
    print(f"\nSaved enhanced American results to {output_file}")

    # Show some summary statistics
    print(f"\nSummary Statistics:")
    print(f"Unique tickers: {options_df['Ticker'].nunique()}")
    print(
        f"Date range: {options_df['Expiration'].min()} to {options_df['Expiration'].max()}"
    )

    for ticker in options_df["Ticker"].unique():
        ticker_data = options_df[options_df["Ticker"] == ticker]
        avg_vol = ticker_data["historical_volatility"].mean()
        current_price = ticker_data["current_stock_price"].iloc[0]
        print(
            f"{ticker}: Current Price=${current_price:.2f}, Avg Volatility={avg_vol:.2%}"
        )
