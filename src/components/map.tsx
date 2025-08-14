'use client'
import { useEffect, useRef, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

// Define income brackets and colors
const incomeColors = [
  { min: 0, max: 49000, color: '#08306b' }, // <49k - dark blue
  { min: 49000, max: 58000, color: '#2171b5' }, // 49-58k - medium blue
  { min: 58000, max: 65000, color: '#6baed6' }, // 58-65k - light blue
  { min: 65000, max: 72000, color: '#c6dbef' }, // 65-72k - very light blue
  { min: 72000, max: 79000, color: '#ffffcc' }, // 72-79k - light yellow
  { min: 79000, max: 87000, color: '#fed976' }, // 79-87k - yellow-orange
  { min: 87000, max: 94000, color: '#feb24c' }, // 87-94k - orange
  { min: 94000, max: 103000, color: '#fd8d3c' }, // 94-103k - dark orange
  { min: 103000, max: 112000, color: '#f03b20' }, // 103-112k - red-orange
  { min: 112000, max: 126000, color: '#d12f2f' }, // 112-126k - red
  { min: 126000, max: 151000, color: '#bd0026' }, // 126-151k - dark red
  { min: 151000, max: Infinity, color: '#7a0177' }, // >151k - dark purple
]

const vehicleColors = [
  { min: 0, max: 1.2, color: '#08306b' }, // 0-1.2 - dark blue
  { min: 1.2, max: 1.39, color: '#2171b5' }, // 1.2-1.39 - medium blue
  { min: 1.39, max: 1.54, color: '#6baed6' }, // 1.39-1.54 - light blue
  { min: 1.54, max: 1.66, color: '#c6dbef' }, // 1.54-1.66 - very light blue
  { min: 1.66, max: 1.77, color: '#ffffcc' }, // 1.66-1.77 - light yellow (middle)
  { min: 1.77, max: 1.87, color: '#fed976' }, // 1.77-1.87 - yellow-orange
  { min: 1.87, max: 1.96, color: '#feb24c' }, // 1.87-1.96 - orange
  { min: 1.96, max: 2.08, color: '#fd8d3c' }, // 1.96-2.08 - dark orange
  { min: 2.08, max: 2.18, color: '#f03b20' }, // 2.08-2.18 - red-orange
  { min: 2.18, max: 2.31, color: '#d12f2f' }, // 2.18-2.31 - red
  { min: 2.31, max: 2.47, color: '#bd0026' }, // 2.31-2.47 - dark red
  { min: 2.47, max: Infinity, color: '#7a0177' }, // 2.47+ - dark purple
]

function getIncomeColor(income: number): string {
  const bracket = incomeColors.find(b => income >= b.min && income < b.max)
  return bracket?.color || '#808080'
}

function getVehicleColor(vehicles: number): string {
  const bracket = vehicleColors.find(b => vehicles >= b.min && vehicles < b.max)
  return bracket?.color || '#808080' // default gray for missing data
}

function getOverlayColor(
  value: number,
  overlayType: 'incomeOverlay' | 'vehicleOverlay'
): string {
  return overlayType === 'incomeOverlay'
    ? getIncomeColor(value)
    : getVehicleColor(value)
}

export default function IncomeMap() {
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<mapboxgl.Map | null>(null)
  const [incomeData, setIncomeData] = useState<Map<string, number>>(new Map())

  const [activeOverlay, setActiveOverlay] = useState<
    'incomeOverlay' | 'vehicleOverlay'
  >('incomeOverlay')
  const [vehicleData, setVehicleData] = useState<Map<string, number>>(new Map())

  useEffect(() => {
    const loadIncomeData = async () => {
      try {
        const response = await fetch(
          '/data/census/06037_median_household_income.csv'
        )
        const csvText = await response.text()
        const lines = csvText.split('\n').slice(1) // Skip header row

        const dataMap = new Map<string, number>()
        lines.forEach(line => {
          if (line.trim()) {
            const [income, geoid] = line.split(',')
            if (income && geoid) {
              dataMap.set(geoid.trim(), parseFloat(income))
            }
          }
        })

        setIncomeData(dataMap)
      } catch (error) {
        console.error('Error loading income data:', error)
      }
    }

    loadIncomeData()
  }, [])

  useEffect(() => {
    const loadVehicleData = async () => {
      try {
        const response = await fetch(
          '/data/census/06037_vehicles_per_household.csv' // Update this path to your actual file
        )
        const csvText = await response.text()
        const lines = csvText.split('\n').slice(1) // Skip header row

        const dataMap = new Map<string, number>()
        lines.forEach(line => {
          if (line.trim()) {
            const [vehicles, geoid] = line.split(',')
            if (vehicles && geoid) {
              dataMap.set(geoid.trim(), parseFloat(vehicles))
            }
          }
        })

        setVehicleData(dataMap)
      } catch (error) {
        console.error('Error loading vehicle data:', error)
      }
    }

    loadVehicleData()
  }, [])
  const updateMapLayer = (overlayType: 'incomeOverlay' | 'vehicleOverlay') => {
    if (!map.current || !map.current.getLayer('tract-income-fill')) return

    const data = overlayType === 'incomeOverlay' ? incomeData : vehicleData
    const propertyName =
      overlayType === 'incomeOverlay' ? 'median_income' : 'avg_vehicles'

    // Update the paint property based on overlay type
    const colorExpression: any =
      overlayType === 'incomeOverlay'
        ? // Income color expression (copy from your existing map layer)
          [
            'case',
            ['!=', ['get', 'median_income'], null],
            [
              'case',
              ['<=', ['get', 'median_income'], 0],
              '#808080',
              ['<', ['get', 'median_income'], 46000],
              '#08306b',
              ['<', ['get', 'median_income'], 63000],
              '#2171b5',
              ['<', ['get', 'median_income'], 77000],
              '#6baed6',
              ['<', ['get', 'median_income'], 90000],
              '#c6dbef',
              ['<', ['get', 'median_income'], 102000],
              '#ffffcc',
              ['<', ['get', 'median_income'], 114000],
              '#fed976',
              ['<', ['get', 'median_income'], 129000],
              '#feb24c',
              ['<', ['get', 'median_income'], 148000],
              '#fd8d3c',
              ['<', ['get', 'median_income'], 174000],
              '#f03b20',
              ['<', ['get', 'median_income'], 200000],
              '#d12f2f',
              ['<', ['get', 'median_income'], 246000],
              '#bd0026',
              '#7a0177',
            ],
            '#808080',
          ]
        : // Vehicle color expression
          [
            'case',
            ['!=', ['get', 'avg_vehicles'], null],
            [
              'case',
              ['<=', ['get', 'median_income'], 0],
              '#808080',
              ['<', ['get', 'median_income'], 49000],
              '#08306b',
              ['<', ['get', 'median_income'], 58000],
              '#2171b5',
              ['<', ['get', 'median_income'], 65000],
              '#6baed6',
              ['<', ['get', 'median_income'], 72000],
              '#c6dbef',
              ['<', ['get', 'median_income'], 79000],
              '#ffffcc',
              ['<', ['get', 'median_income'], 87000],
              '#fed976',
              ['<', ['get', 'median_income'], 94000],
              '#feb24c',
              ['<', ['get', 'median_income'], 103000],
              '#fd8d3c',
              ['<', ['get', 'median_income'], 112000],
              '#f03b20',
              ['<', ['get', 'median_income'], 126000],
              '#d12f2f',
              ['<', ['get', 'median_income'], 151000],
              '#bd0026',
              '#7a0177',
            ],
            '#808080',
          ]

    map.current.setPaintProperty(
      'tract-income-fill',
      'fill-color',
      colorExpression
    )
  }

  useEffect(() => {
    if (map.current || !incomeData.size || !vehicleData.size) return

    mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN!

    map.current = new mapboxgl.Map({
      container: mapContainer.current!,
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [-118.2437, 34.0522], // LA County center
      zoom: 8.5,
    })

    map.current.on('load', async () => {
      try {
        // Load the GeoJSON data
        const geoResponse = await fetch(
          '/data/processed/la-county-tracts.geojson'
        )
        const geoData = await geoResponse.json()

        // Join income data with GeoJSON features
        geoData.features.forEach(
          (feature: { properties: Record<string, unknown> }) => {
            const geoid = (feature.properties.GEOID ||
              feature.properties.geoid) as string
            const income = incomeData.get(geoid)
            const vehicles = vehicleData.get(geoid)

            feature.properties.median_income = income || null
            feature.properties.avg_vehicles = vehicles || null
            feature.properties.income_color = income
              ? getIncomeColor(income)
              : '#808080'
          }
        )

        // Add the enhanced data source
        map.current!.addSource('la-tracts', {
          type: 'geojson',
          data: geoData,
        })

        // Add income fill layer
        map.current!.addLayer({
          id: 'tract-income-fill',
          type: 'fill',
          source: 'la-tracts',
          paint: {
            'fill-color': [
              'case',
              ['!=', ['get', 'median_income'], null],
              [
                'case',
                ['<=', ['get', 'median_income'], 0],
                '#808080',
                ['<', ['get', 'median_income'], 49000],
                '#08306b',
                ['<', ['get', 'median_income'], 58000],
                '#2171b5',
                ['<', ['get', 'median_income'], 65000],
                '#6baed6',
                ['<', ['get', 'median_income'], 72000],
                '#c6dbef',
                ['<', ['get', 'median_income'], 79000],
                '#ffffcc',
                ['<', ['get', 'median_income'], 87000],
                '#fed976',
                ['<', ['get', 'median_income'], 94000],
                '#feb24c',
                ['<', ['get', 'median_income'], 103000],
                '#fd8d3c',
                ['<', ['get', 'median_income'], 112000],
                '#f03b20',
                ['<', ['get', 'median_income'], 126000],
                '#d12f2f',
                ['<', ['get', 'median_income'], 151000],
                '#bd0026',
                '#7a0177',
              ],
              '#00FF00', // null/missing data - gray
            ],
            'fill-opacity': 0.7,
          },
        })

        // Add tract boundary layer on top
        map.current!.addLayer({
          id: 'tract-boundaries',
          type: 'line',
          source: 'la-tracts',
          paint: {
            'line-color': '#ffffff',
            'line-width': 0.5,
            'line-opacity': 0.8,
          },
        })
      } catch (error) {
        console.error('Error loading map data:', error)
      }
    })

    return () => {
      if (map.current) {
        map.current.remove()
      }
    }
  }, [incomeData, vehicleData])

  useEffect(() => {
    if (map.current && incomeData.size > 0 && vehicleData.size > 0) {
      updateMapLayer(activeOverlay)
    }
  }, [activeOverlay, incomeData, vehicleData])

  return (
    <div>
      <div className="relative">
        <div
          ref={mapContainer}
          className="w-full h-[48rem] rounded-lg shadow-lg"
        />

        <div className="absolute bottom-4 left-4 bg-white p-4 rounded-lg shadow-lg">
          <div className="text-sm font-semibold mb-2 text-black">
            {activeOverlay === 'incomeOverlay'
              ? 'Median Household Income'
              : 'Average Vehicles per Household'}
          </div>
          <div className="space-y-1 text-xs">
            {(activeOverlay === 'incomeOverlay'
              ? incomeColors
              : vehicleColors
            ).map((bracket, index) => (
              <div key={index} className="flex items-center">
                <div
                  className="w-4 h-4 mr-2 border border-gray-300"
                  style={{ backgroundColor: bracket.color }}
                />
                <span className="text-black">
                  {activeOverlay === 'incomeOverlay'
                    ? bracket.max === Infinity
                      ? `>$${(bracket.min / 1000).toFixed(0)}k`
                      : `$${(bracket.min / 1000).toFixed(0)}k - $${(bracket.max / 1000).toFixed(0)}k`
                    : bracket.max === Infinity
                      ? `>${bracket.min.toFixed(1)}`
                      : `${bracket.min.toFixed(1)} - ${bracket.max.toFixed(1)}`}
                </span>
              </div>
            ))}
          </div>
        </div>
      </div>
      <div className="mt-10 flex gap-4">
        <button
          className={`flex-1 px-10 py-4 rounded shadow-lg text-sm ${
            activeOverlay === 'incomeOverlay'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 hover:bg-gray-200 text-black'
          }`}
          onClick={() => setActiveOverlay('incomeOverlay')}
        >
          Household Income
        </button>
        <button
          className={`flex-1 px-10 py-4 rounded shadow-lg text-sm ${
            activeOverlay === 'vehicleOverlay'
              ? 'bg-blue-600 text-white'
              : 'bg-gray-100 hover:bg-gray-200 text-black'
          }`}
          onClick={() => setActiveOverlay('vehicleOverlay')}
        >
          Vehicle Ownership
        </button>
      </div>
    </div>
  )
}
