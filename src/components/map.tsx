'use client'
import { useEffect, useRef, useState } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

// Define income brackets and colors
const incomeColors = [
  { min: 0, max: 46000, color: '#08306b' }, // <46k - dark blue
  { min: 46000, max: 63000, color: '#2171b5' }, // 46-63k - medium blue
  { min: 63000, max: 77000, color: '#6baed6' }, // 63-77k - light blue
  { min: 77000, max: 90000, color: '#c6dbef' }, // 77-90k - very light blue
  { min: 90000, max: 102000, color: '#ffffcc' }, // 90-102k - light yellow
  { min: 102000, max: 114000, color: '#fed976' }, // 102-114k - yellow-orange
  { min: 114000, max: 129000, color: '#feb24c' }, // 114-129k - orange
  { min: 129000, max: 148000, color: '#fd8d3c' }, // 129-148k - dark orange
  { min: 148000, max: 174000, color: '#f03b20' }, // 148-174k - red-orange
  { min: 174000, max: 200000, color: '#d12f2f' }, // 174-200k - red
  { min: 200000, max: 246000, color: '#bd0026' }, // 200-246k - dark red
  { min: 246000, max: Infinity, color: '#7a0177' }, // >246k - dark purple
]

function getIncomeColor(income: number): string {
  const bracket = incomeColors.find(b => income >= b.min && income < b.max)
  return bracket?.color || '#808080' // default gray for missing data
}

export default function IncomeMap() {
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<mapboxgl.Map | null>(null)
  const [incomeData, setIncomeData] = useState<Map<string, number>>(new Map())

  // Load CSV data
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
    if (map.current || !incomeData.size) return

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

            feature.properties.median_income = income || null
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
                '#ffffff', // <= 0 values appear white
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
                '#7a0177', // >246k
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
  }, [incomeData])

  return (
    <div className="relative">
      <div
        ref={mapContainer}
        className="w-full h-[48rem] rounded-lg shadow-lg"
      />

      <div className="absolute bottom-4 left-4 bg-white p-4 rounded-lg shadow-lg">
        <h3 className="text-sm font-semibold mb-2 text-black">
          Median Household Income
        </h3>
        <div className="space-y-1 text-xs">
          {incomeColors.map((bracket, index) => (
            <div key={index} className="flex items-center">
              <div
                className="w-4 h-4 mr-2 border border-gray-300"
                style={{ backgroundColor: bracket.color }}
              />
              <span className="text-black">
                {bracket.max === Infinity
                  ? `>$${(bracket.min / 1000).toFixed(0)}k`
                  : `$${(bracket.min / 1000).toFixed(0)}k - $${(bracket.max / 1000).toFixed(0)}k`}
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
