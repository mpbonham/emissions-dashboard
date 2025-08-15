#!/bin/bash


cd "$(dirname "$0")/.."

mkdir -p data/processed
mkdir -p data/census

# State and County codes (FIPS codes)
STATE="06"  # California
YEAR=2023

declare -A counties=(
    ["sf"]="075"
    ["la"]="037" 
    ["sd"]="073"
    ["santa_clara"]="085"  
    ["sacramento"]="067"
)

echo "fetching tract shapes"
for county_name in "${!counties[@]}"; do
    fips=${counties[$county_name]}
    echo "Processing $county_name (FIPS: ${STATE}${fips})..."
    
    yarn mapshaper data/raw/tl_2023_06_tract.shp \
        -filter "COUNTYFP == '$fips'" \
        -simplify 0.5 keep-shapes \
        -o "data/processed/${STATE}_${fips}_${county_name}_census_tracts.geojson"
    
    echo "✓ Saved data/processed/${STATE}_${fips}_${county_name}_census_tracts.geojson"

done

echo "fetching relevant csvs"

for county_name in "${!counties[@]}"; do
    fips=${counties[$county_name]}
    echo "Processing $county_name (FIPS: ${STATE}${fips})..."
    
    venv/bin/python tools/census_fetch.py \
        --state "$STATE" \
        --county "$fips" \
        --year "$YEAR"
done

echo "generating color ranges"
for county_name in "${!counties[@]}"; do
    fips=${counties[$county_name]}
    echo "Generating color ranges for $county_name (FIPS: ${STATE}${fips})..."
    venv/bin/python tools/fetch_color_ranges.py \
        --state "$STATE" \
        --county "$fips"
    echo "✓ Generated color ranges for ${STATE}${fips}"
done