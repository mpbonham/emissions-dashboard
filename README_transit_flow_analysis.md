# Transit Flow Analysis with OD, Bus, Rail, and Waze Data

## Project Concept

This project aims to identify transit flow issues by analyzing the alignment (or mismatch) between commuter demand and public transportation coverage. By using a combination of:

- Origin-Destination (OD) commute data (e.g., from LODES or ACS)
- Bus stop and rail station locations (from GTFS or city open data)
- Optionally, real-time congestion data (e.g., Waze)

we can pinpoint areas where:
- High volumes of commuters travel between origin and destination pairs, but
- No frequent public transit options exist, leading to car dependence, congestion, and equity issues

## Data Inputs

### 1. LODES or ACS OD Data
- Provides anonymized, aggregated commuter flows from home to work at the block group or tract level
- Key field: `S000` (number of commuters for each OD pair)

### 2. Bus Stops and Rail Stations
- Sourced from GTFS feeds or open municipal datasets
- Includes location, route frequency, and mode (bus, metro, rail, etc.)

### 3. (Optional) Waze for Cities Data
- Real-time traffic jams, road closures, speed, and congestion alerts
- Indicates where traffic congestion exists in real time

## Methodology

1. Filter OD pairs for heavy commuter volumes (e.g., `S000 ≥ 10`)
2. Map origins and destinations to determine if they are within walking distance (e.g., 0.5 miles) of:
   - A high-frequency bus route
   - A rail station
3. Flag OD pairs where:
   - Both ends are far from transit
   - Flow volume is high (indicating an underserved commuter corridor)
4. Optionally, overlay Waze congestion data to find roads that:
   - Are consistently congested
   - Lack parallel public transit infrastructure

## Limitations

### Limitations of OD and Transit Coverage Data Alone
- LODES and ACS data are static and may be 1–3 years old
- They do not capture the actual mode of transportation
- Temporal variation (e.g., rush hour vs mid-day) is not represented
- Transit proximity alone does not capture service quality (frequency, reliability, transfers)
- Ride-sharing, biking, and walking patterns are not included

## Notebook Limitations and Current Scope

The accompanying notebook currently uses **only LODES OD data** to simulate heavy commuter flows. It was originally intended to integrate GTFS-based bus and rail data for Los Angeles, as well as real-time congestion data via Waze. However, due to technical constraints with shapefile handling and API availability, these components were not included in the initial version.

The LODES dataset, while useful, is **limited** in that:
- It is several years old and updated infrequently
- It does not account for mode of transportation or congestion
- It only shows **home-to-work flows**, not return or multi-stop trips

As such, the map produced by the notebook offers a simplified view of regional commuter demand that should be augmented with other datasets to identify true transit gaps.

## Using Waze to Improve Understanding of Traffic Flow in Los Angeles

Waze for Cities offers an opportunity to enrich this analysis by providing **real-time traffic conditions** across the LA region. By integrating Waze data into the workflow, we can:

- Identify **chronically congested roads** even if they are not captured by OD data
- Prioritize corridors where **car reliance is highest and transit is lacking**
- Detect **temporal patterns** in traffic delays that might inform peak service scheduling

To apply Waze data in Los Angeles:
1. Apply to Waze for Cities and request access to the LA GeoRSS or JSON feed
2. Overlay congestion hotspots on top of OD flow maps
3. Cross-reference jam locations with GTFS routes to find **congested but underserved areas**
4. Recommend new bus or micro-mobility routes based on both volume and delay indicators

This kind of hybrid approach combining OD, transit, and real-time congestion data can power more responsive, data-driven transportation planning.

## Future Work

- Integrate GTFS trip frequency and real-time schedule adherence
- Estimate time savings and mode shift potential from proposed transit improvements
- Incorporate mobile device data or ride-hailing patterns for finer resolution
- Layer in demographic and equity indicators to prioritize underserved communities

## Example Output

- Interactive map showing:
   - High-volume commute corridors
   - Areas with poor transit access
   - Congested zones from Waze data
- Ranked list of priority corridors for intervention

## Intended Users

- City transportation planners
- Transit agencies
- Sustainability and climate offices
- Urban data teams
- Academic researchers

## Contact

This project welcomes collaboration, especially with agencies or organizations interested in real-world deployment and policy impact.
