import pandas as pd

STATE_NUMBER = "06"  # Cali
COUNTY_NUMBER = "037"  # LA
YEAR = "2017"


# Load the CSV
df = pd.read_csv("data/raw/latch_2017-b.csv")

# Check the column names and structure
print("Columns:", df.columns.tolist())
print("\nFirst few rows:")
print(df.head())

# Look for geographic columns (common names)
geo_columns = [
    col
    for col in df.columns
    if any(
        term in col.lower() for term in ["geoid", "state", "county", "tract", "fips"]
    )
]
print("\nGeographic columns found:", geo_columns)

df["geocode"] = df["geocode"].astype(str).str.zfill(11)

# Filter for LA County (FIPS 06037)
la_county_data = df[df["geocode"].str.startswith("06037")]
print(f"LA County records: {len(la_county_data)}")

vmiles_df = la_county_data[["geocode", "est_vmiles"]].copy()

# Rename columns for consistency with your other datasets
vmiles_df.rename(columns={"geocode": "GEOID", "est_vmiles": "est_vmiles"}, inplace=True)

# Check the result
print("Shape:", vmiles_df.shape)
print("\nFirst few rows:")
print(vmiles_df.head())

vmiles_df_clean = vmiles_df.dropna(subset=["est_vmiles"])

# Reset the index to start from 0
vmiles_df_clean = vmiles_df_clean.reset_index(drop=True)

print("Original rows:", len(vmiles_df))
print("Clean rows:", len(vmiles_df_clean))
print("\nCleaned data:")
print(vmiles_df_clean)

vmiles_df_clean["co2_metric_tons_per_household"] = (
    vmiles_df_clean["est_vmiles"] * 400 * 250 / 1000000
).round(3)

# Check the results
print("CO2 Emissions Statistics:")
print(vmiles_df_clean["co2_metric_tons_per_household"].describe())

print("\nSample data:")
print(vmiles_df_clean[["GEOID", "est_vmiles", "co2_metric_tons_per_household"]].head())

# Save the results
vmiles_df_clean[["co2_metric_tons_per_household", "GEOID"]].to_csv(
    f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_latch_emissions.csv", index=False
)
