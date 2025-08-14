import os
import requests
import numpy as np
import pandas as pd

STATE_NUMBER = "06"  # Cali
COUNTY_NUMBER = "037"  # LA
YEAR = "2023"


def fetch_median_household_income():
    if not os.path.exists(
        f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_median_household_income.csv"
    ):
        # Median Household Income in the Past 12 Months (in 2023 Inflation-Adjusted Dollars)
        # ['B19013_001E', 'NAME', 'state', 'county', 'tract']
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            "get": "B19013_001E",
            "for": "tract:*",
            "in": f"state:{STATE_NUMBER} county:{COUNTY_NUMBER}",
        }

        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])
        df["geoid"] = df["state"] + df["county"] + df["tract"]

        df = df.drop(["state", "county", "tract"], axis=1)

        df.to_csv(
            f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_median_household_income.csv",
            index=False,
        )
    else:
        print("Median income data exists")

    return None


def fetch_avg_household_size():
    if not os.path.exists(
        f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_avg_household_size.csv"
    ):
        # Average Household Size of Occupied Housing Units by Tenure
        # ["B25010_001E","NAME","state","county","tract"]
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            "get": "B25010_001E",
            "for": "tract:*",
            "in": f"state:{STATE_NUMBER} county:{COUNTY_NUMBER}",
        }

        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])
        df["geoid"] = df["state"] + df["county"] + df["tract"]

        df = df.drop(["state", "county", "tract"], axis=1)
        df.to_csv(
            f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_avg_household_size.csv",
            index=False,
        )

    else:
        print("Average household size data exists")

    return None


def fetch_vehicles_per_household():
    if not os.path.exists(
        f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_vehicles_per_household.csv"
    ):
        # B25044_001E is total occupied households
        # 004E  1 vehicle and same logic through 008E which is 5+ vehicles and same for renting 1-5+
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            "get": "B25044_001E,B25044_004E,B25044_005E,B25044_006E,B25044_007E,B25044_008E,B25044_011E,B25044_012E,B25044_013E,B25044_014E,B25044_015E",
            "for": "tract:*",
            "in": f"state:{STATE_NUMBER} county:{COUNTY_NUMBER}",
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
            f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_vehicles_per_household.csv",
            index=False,
        )

    else:
        print("Vehicles per household data already exists ")
    return None


def fetch_rooms_per_household():
    if not os.path.exists(
        f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_median_rooms_per_household.csv"
    ):
        # B25018_001E Median number of rooms
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            "get": "B25018_001E",
            "for": "tract:*",
            "in": f"state:{STATE_NUMBER} county:{COUNTY_NUMBER}",
        }
        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])

        df["geoid"] = df["state"] + df["county"] + df["tract"]

        df = df.drop(["state", "county", "tract"], axis=1)

        df.to_csv(
            f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_median_rooms_per_household.csv",
            index=False,
        )
    else:
        print("Rooms per household data exists")


def fetch_college_degree_attainment():
    if not os.path.exists(
        f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_college_attainment.csv"
    ):
        # B15003_001E is total number of 25 year olds in tract
        # rest of the codes are highest degree attained, bachelors, masters, etc.
        # Educational attainment refers to the highest level of education that an individual has completed.
        # This is distinct from the level of schooling that an individual is attending.

        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            "get": "B15003_001E,B15003_022E,B15003_023E,B15003_024E,B15003_025E",
            "for": "tract:*",
            "in": f"state:{STATE_NUMBER} county:{COUNTY_NUMBER}",
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
            f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_college_attainment.csv",
            index=False,
        )
    else:
        print("college attainment data exists")
    return None


def fetch_home_ownership_rate():
    # B25003_001E is total number of occupied housing units
    # B25003_002E is owner occupied units
    if not os.path.exists(
        f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_home_ownership_rate.csv"
    ):
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            "get": "B25003_001E,B25003_002E",
            "for": "tract:*",
            "in": f"state:{STATE_NUMBER} county:{COUNTY_NUMBER}",
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
            f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_home_ownership_rate.csv",
            index=False,
        )
    else:
        print("home ownership rate data exists")
    return None


def fetch_travel_time():
    if not os.path.exists(f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_travel_time.csv"):
        # B08303 Travel Time to Work
        # 001E: Total workers 16 years and over
        # 002E: Less than 5 minutes
        # 003E: 5 to 9 minutes
        # 004E: 10 to 14 minutes
        # 005E: 15 to 19 minutes
        # 006E: 20 to 24 minutes
        # 007E: 25 to 29 minutes
        # 008E: 30 to 34 minutes
        # 009E: 35 to 39 minutes
        # 010E: 40 to 44 minutes
        # 011E: 45 to 59 minutes
        # 012E: 60 to 89 minutes
        # 013E: 90 or more minutes

        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            "get": "B08303_001E,B08303_002E,B08303_003E,B08303_004E,B08303_005E,B08303_006E,B08303_007E,B08303_008E,B08303_009E,B08303_010E,B08303_011E,B08303_012E,B08303_013E",
            "for": "tract:*",
            "in": f"state:{STATE_NUMBER} county:{COUNTY_NUMBER}",
        }

        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])

        df["GEOID"] = df["state"] + df["county"] + df["tract"]

        numeric_cols = [
            "B08303_001E",
            "B08303_002E",
            "B08303_003E",
            "B08303_004E",
            "B08303_005E",
            "B08303_006E",
            "B08303_007E",
            "B08303_008E",
            "B08303_009E",
            "B08303_010E",
            "B08303_011E",
            "B08303_012E",
            "B08303_013E",
        ]

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce")

        # Calculate weighted average travel time in minutes
        # Using midpoints of each time range
        df["weighted_travel_time"] = (
            2.5 * df["B08303_002E"]  # Less than 5 min -> 2.5
            + 7 * df["B08303_003E"]  # 5-9 min -> 7
            + 12 * df["B08303_004E"]  # 10-14 min -> 12
            + 17 * df["B08303_005E"]  # 15-19 min -> 17
            + 22 * df["B08303_006E"]  # 20-24 min -> 22
            + 27 * df["B08303_007E"]  # 25-29 min -> 27
            + 32 * df["B08303_008E"]  # 30-34 min -> 32
            + 37 * df["B08303_009E"]  # 35-39 min -> 37
            + 42 * df["B08303_010E"]  # 40-44 min -> 42
            + 52 * df["B08303_011E"]  # 45-59 min -> 52
            + 74.5 * df["B08303_012E"]  # 60-89 min -> 74.5
            + 105 * df["B08303_013E"]  # 90+ min -> 105 (estimate)
        )

        df["avg_travel_time"] = (df["weighted_travel_time"] / df["B08303_001E"]).round(
            2
        )

        df["avg_travel_time"] = df["avg_travel_time"].fillna(0)

        final_df = df[["avg_travel_time", "GEOID"]].copy()

        os.makedirs("data/census", exist_ok=True)
        final_df.to_csv(
            f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_travel_time.csv",
            index=False,
        )
    else:
        print("Travel time data exists")

    return None


def fetch_all_data():
    """Fetch all census data"""
    print(
        f"Fetching all census data for county:{COUNTY_NUMBER} in state:{STATE_NUMBER} for year:{YEAR}"
    )
    os.makedirs("data/census", exist_ok=True)

    fetch_median_household_income()
    fetch_avg_household_size()
    fetch_vehicles_per_household()
    fetch_rooms_per_household()
    fetch_college_degree_attainment()
    fetch_home_ownership_rate()
    fetch_travel_time()

    print("All census data fetch complete!")


if __name__ == "__main__":
    fetch_all_data()
