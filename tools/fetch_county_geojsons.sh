#!/bin/bash

# Navigate to the directory containing the project root
cd "$(dirname "$0")/.."

# Create output directory if it doesn't exist
mkdir -p data/processed

# State and County codes
STATE="06"  # California
declare -A counties=(
    ["sf"]="075"
    ["la"]="037" 
    ["sd"]="073"
    ["santa_clara"]="085"  # San Jose is in Santa Clara County
    ["sacramento"]="067"
)

# Process each county
for county_name in "${!counties[@]}"; do
    fips=${counties[$county_name]}
    echo "Processing $county_name (FIPS: ${STATE}${fips})..."
    
    yarn mapshaper data/raw/tl_2023_06_tract.shp \
        -filter "COUNTYFP == '$fips'" \
        -simplify 0.5 keep-shapes \
        -o "data/processed/${STATE}_${fips}_${county_name}_census_tracts.geojson"
    
    echo "✓ Saved data/processed/${STATE}_${fips}_${county_name}_census_tracts.geojson"

done


echo "All counties processed!"

for county_name in "$[!counties[@]}"; do 
    fips=${counties[$county_name]}
    echo ""