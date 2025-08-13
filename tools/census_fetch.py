import os
import requests

import pandas as pd

STATE_NUMBER = '06' # Cali
COUNTY_NUMBER = '037' # LA
YEAR = '2023' 

def fetch_median_household_income():
    if not os.path.exists(f'data/census/{STATE_NUMBER}{COUNTY_NUMBER}_median_household_income.csv'):
        # Median Household Income in the Past 12 Months (in 2023 Inflation-Adjusted Dollars)
        # ['B19013_001E', 'NAME', 'state', 'county', 'tract']
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            'get': 'B19013_001E',
            'for': 'tract:*',
            'in': f'state:{STATE_NUMBER} county:{COUNTY_NUMBER}'
        }
        
        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])
        df['geoid'] = df['state'] + df['county'] + df['tract']

        df = df.drop(['state', 'county', 'tract'], axis=1)
        
        df.to_csv(f'data/census/{STATE_NUMBER}{COUNTY_NUMBER}_median_household_income.csv', index=False)
    else:
        print("Median income data exists")
    
    return None

def fetch_avg_household_size():
    if not os.path.exists(f'data/census/{STATE_NUMBER}{COUNTY_NUMBER}_avg_household_size.csv'):
        # Average Household Size of Occupied Housing Units by Tenure
         # ["B25010_001E","NAME","state","county","tract"]
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            'get': 'B25010_001E',
            'for': 'tract:*',
            'in': f'state:{STATE_NUMBER} county:{COUNTY_NUMBER}'
        }

        response = requests.get(url, params=params)
        data = response.json()

        df = pd.DataFrame(data[1:], columns=data[0])
        df['geoid'] = df['state'] + df['county'] + df['tract']

        df = df.drop([ 'state', 'county', 'tract'], axis=1)
        df.to_csv(f'data/census/{STATE_NUMBER}{COUNTY_NUMBER}_avg_household_size.csv', index=False)
       
    else:
        print("Average household size data exists")
    
    return None

def fetch_vehicles_per_household():
    if not os.path.exists(f'data/census/{STATE_NUMBER}{COUNTY_NUMBER}_vehicles_per_household.csv'):
        # B25044_001E is total occupied households
        # 004E is owned with 1 vehicle and same logic through 008E which is 5+ vehicles owned 
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            'get': 'B25044_001E,B25044_004E,B25044_005E,B25044_006E,B25044_007E,B25044_008E,B25044_011E,B25044_012E,B25044_013E,B25044_014E,B25044_015E',
            'for': 'tract:*',
            'in': f'state:{STATE_NUMBER} county:{COUNTY_NUMBER}'
        }
        response = requests.get(url, params=params)
        data = response.json()
        
        df = pd.DataFrame(data[1:], columns=data[0])
        
      
        df['GEOID'] = df['state'] + df['county'] + df['tract']
        
       
        numeric_cols = ['B25044_001E', 'B25044_004E', 'B25044_005E', 'B25044_006E', 
                    'B25044_007E', 'B25044_008E', 'B25044_011E', 'B25044_012E', 
                    'B25044_013E', 'B25044_014E', 'B25044_015E']
        
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df['total_vehicles'] = (
            1 * df['B25044_004E'] + 2 * df['B25044_005E'] + 3 * df['B25044_006E'] + 
            4 * df['B25044_007E'] + 5 * df['B25044_008E'] +
            1 * df['B25044_011E'] + 2 * df['B25044_012E'] + 3 * df['B25044_013E'] + 
            4 * df['B25044_014E'] + 5 * df['B25044_015E']
        )
        
       
        df['avg_vehicles_per_household'] = (df['total_vehicles'] / df['B25044_001E']).round(2)
      
        df['avg_vehicles_per_household'] = df['avg_vehicles_per_household'].fillna(0)
        
        final_df = df[['avg_vehicles_per_household', 'GEOID']].copy()
      
        os.makedirs(f'data/census', exist_ok=True)
        final_df.to_csv(f'data/census/{STATE_NUMBER}{COUNTY_NUMBER}_vehicles_per_household.csv', index=False)
        

    else:
        print("Vehicles per household data already exists ")
    return None

def fetch_rooms_per_household():
    if not os.path.exists(f'data/census/{STATE_NUMBER}{COUNTY_NUMBER}_median_rooms_per_household.csv'):
        # B25018_001E Median number of rooms	
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            'get': 'B25018_001E',
            'for': 'tract:*',
            'in': f'state:{STATE_NUMBER} county:{COUNTY_NUMBER}'
        }
        response = requests.get(url, params=params)
        data = response.json()
        
      
        df = pd.DataFrame(data[1:], columns=data[0])
        
        df['geoid'] = df['state'] + df['county'] + df['tract']

        df = df.drop(['state', 'county', 'tract'], axis=1)
        
        df.to_csv(f'data/census/{STATE_NUMBER}{COUNTY_NUMBER}_median_rooms_per_household.csv', index=False)
    else:
        print("Rooms per household data exists")

def fetch_college_degree_attainment():
    if not os.path.exists(f'data/census/{STATE_NUMBER}{COUNTY_NUMBER}_college_attainment.csv'):
        # B15003_001E is total number of 25 year olds in tract
        # rest of the codes are highest degree attained, bachelors, masters, etc.
        # Educational attainment refers to the highest level of education that an individual has completed. 
        # This is distinct from the level of schooling that an individual is attending.

        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            'get': 'B15003_001E,B15003_022E,B15003_023E,B15003_024E,B15003_025E',
            'for': 'tract:*',
            'in': f'state:{STATE_NUMBER} county:{COUNTY_NUMBER}'
        }
        response = requests.get(url, params=params)
        data = response.json()
        
      
        df = pd.DataFrame(data[1:], columns=data[0])
        
       
        df['GEOID'] = df['state'] + df['county'] + df['tract']
        

        numeric_cols = ['B15003_001E', 'B15003_022E', 'B15003_023E', 'B15003_024E', 'B15003_025E']
        
        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')
        
        
        df['total_college_degrees'] = df['B15003_022E'] + df['B15003_023E'] + df['B15003_024E'] + df['B15003_025E']
        
        df['college_attainment_rate'] = (df['total_college_degrees'] / df['B15003_001E']).round(2)
        
        df['college_attainment_rate'] = df['college_attainment_rate'].fillna(0)
        
 
        final_df = df[['college_attainment_rate', 'GEOID']].copy()
        

        
        final_df.to_csv(f'data/census/{STATE_NUMBER}{COUNTY_NUMBER}_college_attainment.csv', index=False)
    else:
        print("college attainment data exists")
    return None

def fetch_home_ownership_rate():
    #B25003_001E is total number of occupied housing units
    #B25003_002E is owner occupied units
    if not os.path.exists(f'data/census/{STATE_NUMBER}{COUNTY_NUMBER}_home_ownership_rate.csv'):
        url = f"https://api.census.gov/data/{YEAR}/acs/acs5"
        params = {
            'get': 'B25003_001E,B25003_002E',
            'for': 'tract:*',
            'in': f'state:{STATE_NUMBER} county:{COUNTY_NUMBER}'
        }
        response = requests.get(url, params=params)
        data = response.json()

       
        df = pd.DataFrame(data[1:], columns=data[0])

       
        df['GEOID'] = df['state'] + df['county'] + df['tract']

        
        numeric_cols = ['B25003_001E', 'B25003_002E']

        for col in numeric_cols:
            df[col] = pd.to_numeric(df[col], errors='coerce')

       
        df['home_ownership_rate'] = (df['B25003_002E'] / df['B25003_001E']).round(2)

      
        df['home_ownership_rate'] = df['home_ownership_rate'].fillna(0)

       
        final_df = df[['home_ownership_rate', 'GEOID']].copy()

      
        os.makedirs(f'data/census', exist_ok=True)
        final_df.to_csv(f'data/census/{STATE_NUMBER}{COUNTY_NUMBER}_home_ownership_rate.csv', index=False)
    else:
        print("home ownership rate data exists")
    return None


def fetch_all_data():
    """Fetch all census data"""
    print(f"Fetching all census data for county:{COUNTY_NUMBER} in state:{STATE_NUMBER} for year:{YEAR}")
    os.makedirs('data/census', exist_ok=True)
    
    fetch_median_household_income()
    fetch_avg_household_size()
    fetch_vehicles_per_household()
    fetch_rooms_per_household()
    fetch_college_degree_attainment()
    fetch_home_ownership_rate()

    
    print("All census data fetch complete!")

if __name__ == "__main__":
    fetch_all_data()