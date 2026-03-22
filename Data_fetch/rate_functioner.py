import pandas as pd
from datetime import datetime


class RateFuncer:
    def __init__(self, rates_file="rates.txt"):
        with open(rates_file, "r") as file:
            data = file.read().strip().split("\n")

        data = [line.split(",") for line in data]
        assert len(data[0]) == len(data[1])

        # Convert rates to float (skip first column which is date string)
        rates_data = []
        for i, value in enumerate(data[1]):
            if i == 0:  # First column is date
                rates_data.append(value)  # Keep as string
            else:
                rates_data.append(float(value))  # Convert to float

        # Create dictionary mapping
        self.rates = {data[0][i]: rates_data[i] for i in range(len(data[0]))}

        # Parse base date and remove from rates dict
        self.base_date = datetime.strptime(self.rates.pop("date"), "%m/%d/%Y")

        # Initialize maturity mapping (in months)
        self.maturities_months = {
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

    def _calculate_months_until_expiration(self, expiration_date):
        """Convert date difference to months including partial months."""
        exp_date = datetime.strptime(expiration_date, "%Y-%m-%d")
        delta = exp_date - self.base_date
        return delta.days / 30.44  # Average days per month

    def _find_closest_maturity(self, target_months):
        """Find the closest treasury maturity to target months."""
        available_months = list(self.maturities_months.values())
        closest_months = min(available_months, key=lambda x: abs(x - target_months))
        closest_key = next(
            k for k, v in self.maturities_months.items() if v == closest_months
        )
        return closest_key, closest_months

    def get_rate_for_expiration(self, expiration_date):
        """Get closest treasury rate for specific option expiration date."""
        months = self._calculate_months_until_expiration(expiration_date)
        closest_key, closest_months = self._find_closest_maturity(months)
        rate = self.rates[closest_key]

        return {
            "expiration_date": expiration_date,
            "months_to_expiration": round(months, 2),
            "rate": round(rate, 4),
            "used_maturity": closest_key,
            "base_date": self.base_date.strftime("%Y-%m-%d"),
        }

    def process_options_file(self, input_path, output_path=None):
        """Add rates to options CSV and save to NEW file."""
        # Read options data
        options_df = pd.read_csv(input_path)

        # Calculate rate information for each option
        rate_info = options_df["Expiration"].apply(
            lambda exp: self.get_rate_for_expiration(exp)
        )

        # Add new columns
        options_df["rate"] = rate_info.apply(lambda x: x["rate"])
        options_df["months_to_expiration"] = rate_info.apply(
            lambda x: x["months_to_expiration"]
        )
        options_df["used_maturity"] = rate_info.apply(lambda x: x["used_maturity"])
        options_df["base_date"] = rate_info.apply(lambda x: x["base_date"])

        # Determine output path if not specified
        if output_path is None:
            base_name = input_path.replace(".csv", "")
            output_path = f"{base_name}_with_rates.csv"

        # Save to new CSV file
        options_df.to_csv(output_path, index=False)

        return {
            "output_file": output_path,
            "records_processed": len(options_df),
            "columns_added": [
                "rate",
                "months_to_expiration",
                "used_maturity",
                "base_date",
            ],
        }


if __name__ == "__main__":
    # Initialize rate matcher with Feb 27, 2026 rates
    rate_matcher = RateFuncer("rates_2026_02_26.txt")

    # Process European options
    input_file = "european_options_2026-02-27.csv"
    result = rate_matcher.process_options_file(input_file)
    print(f"✅ Successfully processed {result['records_processed']} European options")
    print(f"📁 Output saved to: {result['output_file']}")

    # Process American options
    input_file = "american_options_2026-02-27.csv"
    result = rate_matcher.process_options_file(input_file)
    print(f"✅ Successfully processed {result['records_processed']} American options")
    print(f"📁 Output saved to: {result['output_file']}")
