import os
import requests
import numpy as np
import pandas as pd
import argparse


def parse_args():
    parser = argparse.ArgumentParser(
        description="fetch census data for any county for any year"
    )
    parser.add_argument("--state", default="06", help="State FIPS code (default: 06)")
    parser.add_argument("--county", required=True, help="County FIPS code (e.g., 037)")
    parser.add_argument("--year", default="2023", help="Census year (default: 2023)")
    return parser.parse_args()


def fetch_median_household_income(state_number, county_number, year):
    if not os.path.exists(
        f"data/census/{state_number}{county_number}/{state_number}{county_number}_median_household_income.csv"
    ):
        # Median Household Income in the Past 12 Months (in 2023 Inflation-Adjusted Dollars)
        # ['B19013_001E', 'NAME', 'state', 'county', 'tract']
        url = f"https://api.census.gov/data/{year}/acs/acs5"
        params = {
            "get": "B19013_001E",
            "for": "tract:*",
            "in": f"state:{state_number} county:{county_number}",
        }

        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])
        df["GEOID"] = df["state"] + df["county"] + df["tract"]

        df = df.drop(["state", "county", "tract"], axis=1)

        df.to_csv(
            f"data/census/{state_number}{county_number}/{state_number}{county_number}_median_household_income.csv",
            index=False,
        )
    else:
        print("Median income data exists")

    return None


def fetch_avg_household_size(state_number, county_number, year):
    if not os.path.exists(
        f"data/census/{state_number}{county_number}/{state_number}{county_number}_avg_household_size.csv"
    ):
        # Average Household Size of Occupied Housing Units by Tenure
        # ["B25010_001E","NAME","state","county","tract"]
        url = f"https://api.census.gov/data/{year}/acs/acs5"
        params = {
            "get": "B25010_001E",
            "for": "tract:*",
            "in": f"state:{state_number} county:{county_number}",
        }

        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])
        df["GEOID"] = df["state"] + df["county"] + df["tract"]

        df = df.drop(["state", "county", "tract"], axis=1)
        df.to_csv(
            f"data/census/{state_number}{county_number}/{state_number}{county_number}_avg_household_size.csv",
            index=False,
        )

    else:
        print("Average household size data exists")

    return None


def fetch_vehicles_per_household(state_number, county_number, year):
    if not os.path.exists(
        f"data/census/{state_number}{county_number}/{state_number}{county_number}_vehicles_per_household.csv"
    ):
        # B25044_001E is total occupied households
        # 004E  1 vehicle and same logic through 008E which is 5+ vehicles and same for renting 1-5+
        url = f"https://api.census.gov/data/{year}/acs/acs5"
        params = {
            "get": "B25044_001E,B25044_004E,B25044_005E,B25044_006E,B25044_007E,B25044_008E,B25044_011E,B25044_012E,B25044_013E,B25044_014E,B25044_015E",
            "for": "tract:*",
            "in": f"state:{state_number} county:{county_number}",
        }
        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])

        df["GEOID"] = df["state"] + df["county"] + df["tract"]

        numeric_cols = [
            "B25044_001E",
            "B25044_004E",
            "B25044_005E",
            "B25044_006E",
            "B25044_007E",
            "B25044_008E",
            "B25044_011E",
            "B25044_012E",
            "B25044_013E",
            "B25044_014E",
            "B25044_015E",
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df["total_vehicles"] = (
            1 * df["B25044_004E"]
            + 2 * df["B25044_005E"]
            + 3 * df["B25044_006E"]
            + 4 * df["B25044_007E"]
            + 5 * df["B25044_008E"]
            + 1 * df["B25044_011E"]
            + 2 * df["B25044_012E"]
            + 3 * df["B25044_013E"]
            + 4 * df["B25044_014E"]
            + 5 * df["B25044_015E"]
        )

        df["avg_vehicles_per_household"] = (
            df["total_vehicles"] / df["B25044_001E"]
        ).round(2)

        df["avg_vehicles_per_household"] = df["avg_vehicles_per_household"].fillna(0)

        final_df = df[["avg_vehicles_per_household", "GEOID"]].copy()

        os.makedirs("data/census", exist_ok=True)
        final_df.to_csv(
            f"data/census/{state_number}{county_number}/{state_number}{county_number}_vehicles_per_household.csv",
            index=False,
        )

    else:
        print("Vehicles per household data already exists ")
    return None


def fetch_rooms_per_household(state_number, county_number, year):
    if not os.path.exists(
        f"data/census/{state_number}{county_number}/{state_number}{county_number}_median_rooms_per_household.csv"
    ):
        # B25018_001E Median number of rooms
        url = f"https://api.census.gov/data/{year}/acs/acs5"
        params = {
            "get": "B25018_001E",
            "for": "tract:*",
            "in": f"state:{state_number} county:{county_number}",
        }
        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])

        df["GEOID"] = df["state"] + df["county"] + df["tract"]

        df = df.drop(["state", "county", "tract"], axis=1)

        df.to_csv(
            f"data/census/{state_number}{county_number}/{state_number}{county_number}_median_rooms_per_household.csv",
            index=False,
        )
    else:
        print("Rooms per household data exists")


def fetch_college_degree_attainment(state_number, county_number, year):
    if not os.path.exists(
        f"data/census/{state_number}{county_number}/{state_number}{county_number}_college_attainment.csv"
    ):
        # B15003_001E is total number of 25 year olds in tract
        # rest of the codes are highest degree attained, bachelors, masters, etc.
        # Educational attainment refers to the highest level of education that an individual has completed.
        # This is distinct from the level of schooling that an individual is attending.

        url = f"https://api.census.gov/data/{year}/acs/acs5"
        params = {
            "get": "B15003_001E,B15003_022E,B15003_023E,B15003_024E,B15003_025E",
            "for": "tract:*",
            "in": f"state:{state_number} county:{county_number}",
        }
        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])

        df["GEOID"] = df["state"] + df["county"] + df["tract"]

        numeric_cols = [
            "B15003_001E",
            "B15003_022E",
            "B15003_023E",
            "B15003_024E",
            "B15003_025E",
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df["total_college_degrees"] = (
            df["B15003_022E"]
            + df["B15003_023E"]
            + df["B15003_024E"]
            + df["B15003_025E"]
        )

        df["college_attainment_rate"] = (
            df["total_college_degrees"] / df["B15003_001E"]
        ).round(2)

        df["college_attainment_rate"] = df["college_attainment_rate"].fillna(0)

        final_df = df[["college_attainment_rate", "GEOID"]].copy()

        final_df.to_csv(
            f"data/census/{state_number}{county_number}/{state_number}{county_number}_college_attainment.csv",
            index=False,
        )
    else:
        print("college attainment data exists")
    return None


def fetch_home_ownership_rate(state_number, county_number, year):
    # B25003_001E is total number of occupied housing units
    # B25003_002E is owner occupied units
    if not os.path.exists(
        f"data/census/{state_number}{county_number}/{state_number}{county_number}_home_ownership_rate.csv"
    ):
        url = f"https://api.census.gov/data/{year}/acs/acs5"
        params = {
            "get": "B25003_001E,B25003_002E",
            "for": "tract:*",
            "in": f"state:{state_number} county:{county_number}",
        }
        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])

        df["GEOID"] = df["state"] + df["county"] + df["tract"]

        numeric_cols = ["B25003_001E", "B25003_002E"]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        df["home_ownership_rate"] = (df["B25003_002E"] / df["B25003_001E"]).round(2)

        df["home_ownership_rate"] = df["home_ownership_rate"].fillna(0)

        final_df = df[["home_ownership_rate", "GEOID"]].copy()

        os.makedirs("data/census", exist_ok=True)
        final_df.to_csv(
            f"data/census/{state_number}{county_number}/{state_number}{county_number}_home_ownership_rate.csv",
            index=False,
        )
    else:
        print("home ownership rate data exists")
    return None


def fetch_car_commute_time(state_number, county_number, year):
    if not os.path.exists(
        f"data/census/{state_number}{county_number}/{state_number}{county_number}_car_commute_time.csv"
    ):
        url = f"https://api.census.gov/data/{year}/acs/acs5"
        params = {
            "get": "B08134_011E,B08134_012E,B08134_013E,B08134_014E,B08134_015E,B08134_016E,B08134_017E,B08134_018E,B08134_019E,B08134_020E",
            "for": "tract:*",
            "in": f"state:{state_number} county:{county_number}",
        }
        response = requests.get(url, params=params)
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        df["GEOID"] = df["state"] + df["county"] + df["tract"]

        travel_time_cols = [
            "B08134_011E",
            "B08134_012E",
            "B08134_013E",
            "B08134_014E",
            "B08134_015E",
            "B08134_016E",
            "B08134_017E",
            "B08134_018E",
            "B08134_019E",
            "B08134_020E",
        ]

        for col in travel_time_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
            df[col] = df[col].fillna(0)

   
        time_midpoints = {
            "B08134_012E": 7.5,  
            "B08134_013E": 12, 
            "B08134_014E": 17,  
            "B08134_015E": 22,  
            "B08134_016E": 27, 
            "B08134_017E": 32, 
            "B08134_018E": 39.5,  
            "B08134_019E": 52,  
            "B08134_020E": 75,  
        }

        total_weighted_time = 0
        total_car_commuters = df["B08134_011E"]

        for col, midpoint in time_midpoints.items():
            total_weighted_time += df[col] * midpoint

        df["car_avg_travel_time"] = (
            total_weighted_time / total_car_commuters.replace(0, 1)
        ).round(2)

        df.loc[total_car_commuters == 0, "car_avg_travel_time"] = 0

        final_df = df[["car_avg_travel_time", "GEOID"]].copy()

        os.makedirs("data/census", exist_ok=True)
        final_df.to_csv(
            f"data/census/{state_number}{county_number}/{state_number}{county_number}_car_commute_time.csv",
            index=False,
        )
    else:
        print("car commute time data exists")
    return None


def fetch_car_commute_percentage(state_number, county_number, year):
    # B08301_001E is total commuters
    # B08301_002E is car, truck, or van commuters
    if not os.path.exists(
        f"data/census/{state_number}{county_number}/{state_number}{county_number}_car_commuter_percentage.csv"
    ):
        url = f"https://api.census.gov/data/{year}/acs/acs5"
        params = {
            "get": "B08301_001E,B08301_002E",
            "for": "tract:*",
            "in": f"state:{state_number} county:{county_number}",
        }
        response = requests.get(url, params=params)
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        df["GEOID"] = df["state"] + df["county"] + df["tract"]
        numeric_cols = ["B08301_001E", "B08301_002E"]
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df["vehicle_usage_rate"] = (df["B08301_002E"] / df["B08301_001E"]).round(2)
        df["vehicle_usage_rate"] = df["vehicle_usage_rate"].fillna(0)
        final_df = df[["vehicle_usage_rate", "GEOID"]].copy()
        os.makedirs("data/census", exist_ok=True)
        final_df.to_csv(
            f"data/census/{state_number}{county_number}/{state_number}{county_number}_car_commuter_percentage.csv",
            index=False,
        )
    else:
        print("Car commuter data percentage")
    return None


def fetch_car_transport_emissions_per_household(state_number, county_number, year):
    if not os.path.exists(
        f"data/census/{state_number}{county_number}/{state_number}{county_number}_car_transport_emissions_per_household.csv"
    ):
        url = f"https://api.census.gov/data/{year}/acs/acs5"
        params = {
            "get": "B25001_001E,B08134_011E",  # Total households + total car commuters
            "for": "tract:*",
            "in": f"state:{state_number} county:{county_number}",
        }
        response = requests.get(url, params=params)
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        df["GEOID"] = df["state"] + df["county"] + df["tract"]

        df["B25001_001E"] = pd.to_numeric(df["B25001_001E"], errors="coerce")
        df["B08134_011E"] = pd.to_numeric(df["B08134_011E"], errors="coerce")
        df["B25001_001E"] = df["B25001_001E"].fillna(0)
        df["B08134_011E"] = df["B08134_011E"].fillna(0)

        households_df = df[["B25001_001E", "B08134_011E", "GEOID"]].copy()
        households_df.rename(
            columns={
                "B25001_001E": "total_households",
                "B08134_011E": "total_car_commuters",
            },
            inplace=True,
        )

        # Load car commute time CSV
        car_time_df = pd.read_csv(
            f"data/census/{state_number}{county_number}/{state_number}{county_number}_car_commute_time.csv",
            dtype={"GEOID": str},
        )

        households_df["GEOID"] = households_df["GEOID"].astype(str)

        merged_df = households_df.merge(car_time_df, on="GEOID", how="inner")

        total_co2 = (
            merged_df["car_avg_travel_time"]
            * merged_df["total_car_commuters"]
            * 0.1  # 400g CO2/mile * 30mph * 2 trips * 250 days / 1M = 0.1 tons/year per minute
        )

        merged_df["car_co2_metric_tons_per_household"] = (
            total_co2 / merged_df["total_households"].replace(0, 1)
        ).round(3)

        final_df = merged_df[["car_co2_metric_tons_per_household", "GEOID"]].copy()

        os.makedirs("data/census", exist_ok=True)
        final_df.to_csv(
            f"data/census/{state_number}{county_number}/{state_number}{county_number}_car_transport_emissions_per_household.csv",
            index=False,
        )
    else:
        print("car transport emissions per household data exists")
    return None


def fetch_all_data(state_number, county_number, year):
    """Fetch all census data"""

    print(
        f"Fetching all census data for county:{county_number} in state:{state_number} for year:{year}"
    )
    os.makedirs(f"data/census/{state_number}{county_number}", exist_ok=True)

    fetch_median_household_income(state_number, county_number, year)
    fetch_avg_household_size(state_number, county_number, year)
    fetch_vehicles_per_household(state_number, county_number, year)
    fetch_rooms_per_household(state_number, county_number, year)
    fetch_college_degree_attainment(state_number, county_number, year)
    fetch_home_ownership_rate(state_number, county_number, year)
    fetch_car_commute_time(state_number, county_number, year)
    fetch_car_commute_percentage(state_number, county_number, year)
    fetch_car_transport_emissions_per_household(state_number, county_number, year)

    print("All census data fetch complete!")


if __name__ == "__main__":
    args = parse_args()
    fetch_all_data(args.state, args.county, args.year)
