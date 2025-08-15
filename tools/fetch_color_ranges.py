import numpy as np
import pandas as pd
import os
import argparse
import json

file_arr = [
    "median_household_income.csv",
    "vehicles_per_household.csv",
    "car_commuter_percentage.csv",
    "college_attainment.csv",
    "home_ownership_rate.csv",
    "median_rooms_per_household.csv",
    "car_commute_time.csv",
    "vehicle_usage_rate.csv",
    "car_transport_emissions_per_household.csv",
]


def parse_args():
    parser = argparse.ArgumentParser(
        description="fetch census data for any county for any year"
    )
    parser.add_argument("--state", default="06", help="State FIPS code (default: 06)")
    parser.add_argument("--county", required=True, help="County FIPS code (e.g., 037)")
    return parser.parse_args()


def calculate_color_ranges(state_number, county_number):
    results = {}

    for x in file_arr:
        file_path = f"data/census/{state_number}{county_number}/{state_number}{county_number}_{x}"
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        try:
            df = pd.read_csv(file_path)

            clean_data = pd.to_numeric(df.iloc[:, 0], errors="coerce")
            clean_data = clean_data[clean_data >= 0]
            clean_data = clean_data.dropna()

            average = clean_data.mean()
            percentiles = np.linspace(0, 1, 13)[1:-1]
            breaks = clean_data.quantile(percentiles).round(2)

            metric_name = x.replace(".csv", "")
            results[metric_name] = {
                "breaks": breaks.tolist(),
                "average": round(average, 2),
                "clean_count": len(clean_data),
                "total_count": len(df),
            }

            print(
                f"Processed {metric_name}: {len(clean_data)}/{len(df)} records, avg: {average:.2f}"
            )

        except Exception as e:
            print(f"Error processing {file_path}: {e}")

    output_dir = f"data/census/{state_number}{county_number}"
    os.makedirs(output_dir, exist_ok=True)

    output_file = f"{output_dir}/color_ranges_{state_number}{county_number}.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nColor ranges saved to {output_file}")


if __name__ == "__main__":
    args = parse_args()
    calculate_color_ranges(args.state, args.county)
