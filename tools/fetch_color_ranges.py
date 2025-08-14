import numpy as np
import pandas as pd
import os

STATE_NUMBER = "06"  # Cali
COUNTY_NUMBER = "037"  # LA
YEAR = "2023"

file_arr = [
    "median_household_income.csv",
    "vehicles_per_household.csv",
    "avg_household_size.csv",
    "college_attainment.csv",
    "home_ownership_rate.csv",
    "median_rooms_per_household.csv",
]


def calculate_color_ranges():
    for x in file_arr:
        file_path = f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_{x}"

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        try:
            df = pd.read_csv(file_path)

            # Convert to numeric and filter out negative values
            clean_data = pd.to_numeric(df.iloc[:, 0], errors="coerce")
            clean_data = clean_data[clean_data >= 0]  # Remove negative values
            clean_data = clean_data.dropna()  # Remove NaN values

            # Calculate average and percentiles with clean data
            average = clean_data.mean()
            percentiles = np.linspace(0, 1, 13)[1:-1]  # 11 breaks for 12 color bands
            breaks = clean_data.quantile(percentiles).round(2)

            print("----------------------------------------------------------")
            print(f" Percentile-based color breaks for {x}:")
            print(breaks.tolist())
            print(f"Average: {average:.2f}")
            print(f"Clean data count: {len(clean_data)} / {len(df)} records")

        except Exception as e:
            print(f" Error processing {file_path}: {e}")


if __name__ == "__main__":
    calculate_color_ranges()
