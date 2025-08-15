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
        df["GEOID"] = df["state"] + df["county"] + df["tract"]

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
        df["GEOID"] = df["state"] + df["county"] + df["tract"]

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

        df["GEOID"] = df["state"] + df["county"] + df["tract"]

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


def fetch_car_commute_time():
    if not os.path.exists(
        f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_car_commute_time.csv"
    ):
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            "get": "B08134_011E,B08134_012E,B08134_013E,B08134_014E,B08134_015E,B08134_016E,B08134_017E,B08134_018E,B08134_019E,B08134_020E",
            "for": "tract:*",
            "in": f"state:{STATE_NUMBER} county:{COUNTY_NUMBER}",
        }
        response = requests.get(url, params=params)
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        df["GEOID"] = df["state"] + df["county"] + df["tract"]

        # Convert to numeric
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

        # Assign midpoint values for each time range (in minutes)
        time_midpoints = {
            "B08134_012E": 7.5,  # Less than 10 minutes -> 7.5
            "B08134_013E": 12,  # 10 to 14 minutes -> 12
            "B08134_014E": 17,  # 15 to 19 minutes -> 17
            "B08134_015E": 22,  # 20 to 24 minutes -> 22
            "B08134_016E": 27,  # 25 to 29 minutes -> 27
            "B08134_017E": 32,  # 30 to 34 minutes -> 32
            "B08134_018E": 39.5,  # 35 to 44 minutes -> 39.5
            "B08134_019E": 52,  # 45 to 59 minutes -> 52
            "B08134_020E": 75,  # 60+ minutes -> 75 (estimate)
        }

        # Calculate weighted average travel time for car commuters
        total_weighted_time = 0
        total_car_commuters = df["B08134_011E"]  # Total car commuters

        for col, midpoint in time_midpoints.items():
            total_weighted_time += df[col] * midpoint

        # Calculate average travel time (avoid division by zero)
        df["car_avg_travel_time"] = (
            total_weighted_time / total_car_commuters.replace(0, 1)
        ).round(2)

        # Handle cases where no car commuters
        df.loc[total_car_commuters == 0, "car_avg_travel_time"] = 0

        # Keep only GEOID and car travel time
        final_df = df[["car_avg_travel_time", "GEOID"]].copy()

        os.makedirs("data/census", exist_ok=True)
        final_df.to_csv(
            f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_car_commute_time.csv",
            index=False,
        )
    else:
        print("car commute time data exists")
    return None


# TODO Rename by car commute percentage
def fetch_vehicle_usage_rate():
    # B08301_001E is total commuters
    # B08301_002E is car, truck, or van commuters
    if not os.path.exists(
        f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_car_commuter_percentage.csv"
    ):
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            "get": "B08301_001E,B08301_002E",
            "for": "tract:*",
            "in": f"state:{STATE_NUMBER} county:{COUNTY_NUMBER}",
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
            f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_car_commuter_percentage.csv",
            index=False,
        )
    else:
        print("vehicle usage rate data exists")
    return None


def fetch_car_transport_emissions_per_household():
    if not os.path.exists(
        f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_car_transport_emissions_per_household.csv"
    ):
        # Fetch total households from API (we don't need commuters since B08134_011E gives us car commuters)
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            "get": "B25001_001E,B08134_011E",  # Total households + total car commuters
            "for": "tract:*",
            "in": f"state:{STATE_NUMBER} county:{COUNTY_NUMBER}",
        }
        response = requests.get(url, params=params)
        data = response.json()
        df = pd.DataFrame(data[1:], columns=data[0])
        df["GEOID"] = df["state"] + df["county"] + df["tract"]

        # Convert to numeric
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
            f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_car_commute_time.csv",
            dtype={"GEOID": str},
        )

        # Convert GEOID to string
        households_df["GEOID"] = households_df["GEOID"].astype(str)

        # Merge datasets
        merged_df = households_df.merge(car_time_df, on="GEOID", how="inner")

        # Calculate total CO2 emissions in metric tons
        # Formula: car_avg_travel_time * total_car_commuters * 0.1 (already accounts for 100% vehicle usage)
        total_co2 = (
            merged_df["car_avg_travel_time"]
            * merged_df["total_car_commuters"]
            * 0.1  # 400g CO2/mile * 30mph * 2 trips * 250 days / 1M = 0.1 tons/year per minute
        )

        # Calculate CO2 per household (avoid division by zero)
        merged_df["car_co2_metric_tons_per_household"] = (
            total_co2 / merged_df["total_households"].replace(0, 1)
        ).round(3)

        # Keep only GEOID and emissions per household
        final_df = merged_df[["car_co2_metric_tons_per_household", "GEOID"]].copy()

        os.makedirs("data/census", exist_ok=True)
        final_df.to_csv(
            f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_car_transport_emissions_per_household.csv",
            index=False,
        )
    else:
        print("car transport emissions per household data exists")
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
    fetch_car_commute_time()
    fetch_vehicle_usage_rate()
    fetch_car_transport_emissions_per_household()

    print("All census data fetch complete!")


if __name__ == "__main__":
    fetch_all_data()
