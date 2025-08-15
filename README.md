# Census Tract Mapping Application
## Authors: Maxwell Bonham & Charles DeLapa
### [LIVE WEB APP](https://emissions-dashboard-chi.vercel.app/)
An interactive web application for visualizing census tract data with emissions overlays across California counties.

## Overview

This project creates interactive maps displaying census tract boundaries with various demographic and transportation metrics, including car commuter emissions data. Users can explore different data layers and visualize patterns across census tracts within California counties.

## Tech Stack

- **Framework**: Next.js with App Router
- **Package Manager**: Yarn
- **Styling**: Tailwind CSS
- **Mapping**: Mapbox GL JS
- **Dev Server**: Turbopack 

## Project Structure

```
my-mapbox-app/
├── src/
│   ├── app/           # Next.js pages
│   └── components/    # React components
├── public/            # Holds all data ready to be used via web app
├── data/            
│   ├── census/        # Census data CSVs and color ranges (this data is not seen on GitHub)
│   ├── processed/     # GeoJSON files
│   └── raw/           # Raw shapefiles
├── tools/             # Data processing scripts
├── notebooks/         # Jupyter notebooks for data analysis
└── .env               # Environment variables
```

## Features

- Interactive census tract mapping
- Multiple data overlays (income, commute times, emissions, etc.)
- Dynamic color coding based on data percentiles
- County-specific data visualization

## Data Sources & Methodology 

This project utilizes emissions methodology developed by **EcoDataLab's Consumption-Based Emissions Inventory (CBEI)**

Census tract boundaries and demographic data are sourced from the U.S. Census Bureau's American Community Survey and TIGER/Line Shapefiles.

### CO2 Emissions Calculation

Our transportation emissions estimates are calculated using the following methodology:

```python
total_co2 = (
    merged_df["car_avg_travel_time"] 
    * merged_df["total_car_commuters"] 
    * 0.1  # Conversion factor: tons CO2 per commuter-minute per year
)
```

**Calculation Breakdown:**
- **Base emission rate**: 400g CO2 per mile (based on EPA vehicle emission standards)
- **Average speed**: 30 mph (typical urban commuting speed)
- **Round trips**: 2 trips per day (to and from work)
- **Working days**: 250 days per year (typical work year)
- **Unit conversion**: Grams to metric tons (÷ 1,000,000)

**Formula derivation:**
```
400g CO2/mile × (30 mph ÷ 60 min/hour) × 2 trips/day × 250 days/year ÷ 1,000,000g/ton
= 400g CO2/mile × 0.5 miles/min × 2 trips/day × 250 days/year ÷ 1,000,000g/ton  
= 0.1 tons CO2 per commuter-minute per year
```

### Note on Latch Emissions
So we used LATCH est_vmiles (2017) data and used the same formula to come up with LATCH car emission data
to compare to our car commute CO2 estimates. As you can see from the web app, the tracts change
quite a bit and we think that is because of these reasons:
- LATCH is an estimate of all car travel mileage not just commute miles (Census is just commute miles)
- Typically high-income areas have less commute miles since they tend to have more felxibility in when and how they commute
- High-income areas tend to travel more miles outside of work than low-income areas



### Data Processing

The project includes automated scripts for processing census data:

**Process census tracts and fetch data**:
```bash
./tools/fetch_all_data.sh
```

This script will:
- Extract census tract GeoJSON files for specified counties
- Fetch demographic and transportation data from Census API
- Generate color range configurations for data visualization

### Adding New Counties

Edit the counties array in your processing script:
```bash
declare -A counties=(
    ["los_angeles"]="037"
    ["orange"]="059"
    ["san_diego"]="073"
    # Add more counties as needed
)
```

### Available Data Layers

- Median Household Income
- Vehicles Per Household
- Car Commuter Percentage
- College Attainment Rate
- Home Ownership Rate
- Median Rooms Per Household
- Average Car Commute Time
- Car Commuter Percentage 
- Car Transport Emissions Per Household

## Credits

- **Methodology**: EcoDataLab's Consumption-Based Emissions Inventory (CBEI)
- **Census Data**: U.S. Census Bureau American Community Survey
- **Mapping**: Mapbox GL JS
- **Geographic Boundaries**: U.S. Census Bureau TIGER/Line Shapefiles
