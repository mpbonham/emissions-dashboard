import pandas as pd

STATE_NUMBER = "06"  # Cali
COUNTY_NUMBER = "037"  # LA
YEAR = "2017"


def get_nhts_data():
    df = pd.read_csv("data/raw/latch_2017-b.csv")

    print("Columns:", df.columns.tolist())
    print("\nFirst few rows:")
    print(df.head())

    geo_columns = [
        col
        for col in df.columns
        if any(
            term in col.lower()
            for term in ["geoid", "state", "county", "tract", "fips"]
        )
    ]
    print("\nGeographic columns found:", geo_columns)

    df["geocode"] = df["geocode"].astype(str).str.zfill(11)

    la_county_data = df[df["geocode"].str.startswith("06037")]
    print(f"LA County records: {len(la_county_data)}")

    vmiles_df = la_county_data[["geocode", "est_vmiles"]].copy()

    vmiles_df.rename(
        columns={"geocode": "GEOID", "est_vmiles": "est_vmiles"}, inplace=True
    )

    vmiles_df_clean = vmiles_df.dropna(subset=["est_vmiles"])

    vmiles_df_clean = vmiles_df_clean.reset_index(drop=True)

    vmiles_df_clean["co2_metric_tons_per_household"] = (
        vmiles_df_clean["est_vmiles"] * 400 * 250 / 1000000
    ).round(3)

    vmiles_df_clean[["co2_metric_tons_per_household", "GEOID"]].to_csv(
        f"data/census/{STATE_NUMBER}{COUNTY_NUMBER}_latch_emissions.csv", index=False
    )


if __name__ == "__main__":
    get_nhts_data()
