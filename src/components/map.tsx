'use client'
import { useEffect, useRef, useState } from 'react'
import mapboxgl, { ExpressionSpecification } from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

interface OverlayConfig {
  id: string
  title: string
  dataFile: string
  propertyName: string
  colorBrackets: Array<{
    min: number
    max: number
    color: string
  }>
  formatValue: (value: number) => string
}

const overlayConfigs: OverlayConfig[] = [
  {
    id: 'income',
    title: 'Median Household Income',
    dataFile: '/data/census/06037_median_household_income.csv',
    propertyName: 'median_income',
    colorBrackets: [
      { min: 0, max: 49000, color: '#08306b' },
      { min: 49000, max: 58000, color: '#2171b5' },
      { min: 58000, max: 65000, color: '#6baed6' },
      { min: 65000, max: 72000, color: '#c6dbef' },
      { min: 72000, max: 79000, color: '#ffffcc' },
      { min: 79000, max: 87000, color: '#fed976' },
      { min: 87000, max: 94000, color: '#feb24c' },
      { min: 94000, max: 103000, color: '#fd8d3c' },
      { min: 103000, max: 112000, color: '#f03b20' },
      { min: 112000, max: 126000, color: '#d12f2f' },
      { min: 126000, max: 151000, color: '#bd0026' },
      { min: 151000, max: Infinity, color: '#7a0177' },
    ],
    formatValue: (value: number) =>
      value === Infinity
        ? `>$${(151000 / 1000).toFixed(0)}k`
        : `$${(value / 1000).toFixed(0)}k`,
  },
  {
    id: 'vehicles',
    title: 'Average Vehicles per Household',
    dataFile: '/data/census/06037_vehicles_per_household.csv',
    propertyName: 'avg_vehicles',
    colorBrackets: [
      { min: 0, max: 1.2, color: '#08306b' },
      { min: 1.2, max: 1.39, color: '#2171b5' },
      { min: 1.39, max: 1.54, color: '#6baed6' },
      { min: 1.54, max: 1.66, color: '#c6dbef' },
      { min: 1.66, max: 1.77, color: '#ffffcc' },
      { min: 1.77, max: 1.87, color: '#fed976' },
      { min: 1.87, max: 1.96, color: '#feb24c' },
      { min: 1.96, max: 2.08, color: '#fd8d3c' },
      { min: 2.08, max: 2.18, color: '#f03b20' },
      { min: 2.18, max: 2.31, color: '#d12f2f' },
      { min: 2.31, max: 2.47, color: '#bd0026' },
      { min: 2.47, max: Infinity, color: '#7a0177' },
    ],
    formatValue: (value: number) =>
      value === Infinity ? `>${(2.47).toFixed(1)}` : value.toFixed(1),
  },
  {
    id: 'homeownership',
    title: 'Home Ownership Rate',
    dataFile: 'data/census/06037_home_ownership_rate.csv',
    propertyName: 'home_ownership_rate',
    colorBrackets: [
      { min: 0, max: 0.07, color: '#08306b' },
      { min: 0.07, max: 0.16, color: '#2171b5' },
      { min: 0.16, max: 0.24, color: '#6baed6' },
      { min: 0.24, max: 0.31, color: '#c6dbef' },
      { min: 0.31, max: 0.37, color: '#ffffcc' },
      { min: 0.37, max: 0.45, color: '#fed976' },
      { min: 0.45, max: 0.53, color: '#feb24c' },
      { min: 0.53, max: 0.61, color: '#fd8d3c' },
      { min: 0.61, max: 0.69, color: '#f03b20' },
      { min: 0.69, max: 0.77, color: '#d12f2f' },
      { min: 0.77, max: 0.85, color: '#bd0026' },
      { min: 0.85, max: Infinity, color: '#7a0177' },
    ],
    formatValue: (value: number) =>
      value === Infinity
        ? `>${(0.85).toFixed(2)}`
        : `${(value * 100).toFixed(1)}%`,
  },
  {
    id: 'college',
    title: 'College Attainment Rate',
    dataFile: '/data/census/06037_college_attainment.csv',
    propertyName: 'college_attainment',
    colorBrackets: [
      { min: 0, max: 0.08, color: '#08306b' },
      { min: 0.08, max: 0.12, color: '#2171b5' },
      { min: 0.12, max: 0.16, color: '#6baed6' },
      { min: 0.16, max: 0.2, color: '#c6dbef' },
      { min: 0.2, max: 0.25, color: '#ffffcc' },
      { min: 0.25, max: 0.31, color: '#fed976' },
      { min: 0.31, max: 0.37, color: '#feb24c' },
      { min: 0.37, max: 0.44, color: '#fd8d3c' },
      { min: 0.44, max: 0.51, color: '#f03b20' },
      { min: 0.51, max: 0.61, color: '#d12f2f' },
      { min: 0.61, max: 0.7, color: '#bd0026' },
      { min: 0.7, max: Infinity, color: '#7a0177' },
    ],
    formatValue: (value: number) =>
      value === Infinity
        ? `>${(0.7).toFixed(2)}`
        : `${(value * 100).toFixed(1)}%`,
  },
  {
    id: 'rooms',
    title: 'Median Rooms per Household',
    dataFile: 'data/census/06037_median_rooms_per_household.csv',
    propertyName: 'median_rooms',
    colorBrackets: [
      { min: 0, max: 3.2, color: '#08306b' },
      { min: 3.2, max: 3.6, color: '#2171b5' },
      { min: 3.6, max: 3.9, color: '#6baed6' },
      { min: 3.9, max: 4.1, color: '#c6dbef' },
      { min: 4.1, max: 4.3, color: '#ffffcc' },
      { min: 4.3, max: 4.5, color: '#fed976' },
      { min: 4.5, max: 4.8, color: '#feb24c' },
      { min: 4.8, max: 5.1, color: '#fd8d3c' },
      { min: 5.1, max: 5.4, color: '#f03b20' },
      { min: 5.4, max: 5.8, color: '#d12f2f' },
      { min: 5.8, max: 6.3, color: '#bd0026' },
      { min: 6.3, max: Infinity, color: '#7a0177' },
    ],
    formatValue: (value: number) =>
      value === Infinity ? `>${(6.3).toFixed(1)}` : value.toFixed(1),
  },
  {
    id: 'householdsize',
    title: 'Average Household Size',
    dataFile: '/data/census/06037_avg_household_size.csv',
    propertyName: 'avg_household_size',
    colorBrackets: [
      { min: 0, max: 1.95, color: '#08306b' },
      { min: 1.95, max: 2.22, color: '#2171b5' },
      { min: 2.22, max: 2.46, color: '#6baed6' },
      { min: 2.46, max: 2.63, color: '#c6dbef' },
      { min: 2.63, max: 2.78, color: '#ffffcc' },
      { min: 2.78, max: 2.93, color: '#fed976' },
      { min: 2.93, max: 3.09, color: '#feb24c' },
      { min: 3.09, max: 3.24, color: '#fd8d3c' },
      { min: 3.24, max: 3.46, color: '#f03b20' },
      { min: 3.46, max: 3.71, color: '#d12f2f' },
      { min: 3.71, max: 4.01, color: '#bd0026' },
      { min: 4.01, max: Infinity, color: '#7a0177' },
    ],
    formatValue: (value: number) =>
      value === Infinity ? `>${(4.01).toFixed(2)}` : value.toFixed(2),
  },
]

function createColorExpression(config: OverlayConfig): ExpressionSpecification {
  const conditions: ExpressionSpecification = [
    'case',
    ['!=', ['get', config.propertyName], null],
  ]

  const nestedCase: ExpressionSpecification = ['case']

  nestedCase.push(['<=', ['get', config.propertyName], 0])
  nestedCase.push('#808080')

  config.colorBrackets.forEach(bracket => {
    if (bracket.max === Infinity) {
      nestedCase.push(bracket.color)
    } else {
      nestedCase.push(['<', ['get', config.propertyName], bracket.max])
      nestedCase.push(bracket.color)
    }
  })

  conditions.push(nestedCase)
  conditions.push('#808080')

  return conditions
}

export default function IncomeMap() {
  const [showNotification, setShowNotification] = useState(true)

  useEffect(() => {
    const timer = setTimeout(() => {
      setShowNotification(false)
    }, 5000)

    return () => clearTimeout(timer)
  }, [])
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<mapboxgl.Map | null>(null)
  const [overlayData, setOverlayData] = useState<
    Map<string, Map<string, number>>
  >(new Map())
  const [activeOverlay, setActiveOverlay] = useState<string>('income')
  const [dataLoaded, setDataLoaded] = useState(false)

  useEffect(() => {
    const loadAllData = async () => {
      const allData = new Map<string, Map<string, number>>()

      for (const config of overlayConfigs) {
        try {
          const response = await fetch(config.dataFile)
          const csvText = await response.text()
          const lines = csvText.split('\n').slice(1) // Skip header

          const dataMap = new Map<string, number>()
          lines.forEach(line => {
            if (line.trim()) {
              const [value, geoid] = line.split(',')
              if (value && geoid) {
                dataMap.set(geoid.trim(), parseFloat(value))
              }
            }
          })

          allData.set(config.id, dataMap)
        } catch (error) {
          console.error(`Error loading ${config.title} data:`, error)
          allData.set(config.id, new Map()) // Set empty map on error
        }
      }

      setOverlayData(allData)
      setDataLoaded(true)
    }

    loadAllData()
  }, [])

  const updateMapLayer = (overlayId: string) => {
    if (!map.current || !map.current.getLayer('tract-income-fill')) return

    const config = overlayConfigs.find(c => c.id === overlayId)
    if (!config) return

    const colorExpression = createColorExpression(config)
    map.current.setPaintProperty(
      'tract-income-fill',
      'fill-color',
      colorExpression
    )
  }

  useEffect(() => {
    if (map.current || !dataLoaded) return

    const timer = setTimeout(() => {
      mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN!

      map.current = new mapboxgl.Map({
        container: mapContainer.current!,
        style: 'mapbox://styles/mapbox/light-v11',
        center: [-118.2437, 34.0522],
        zoom: 8.0,
      })

      map.current.on('load', async () => {
        try {
          const geoResponse = await fetch(
            '/data/processed/la-county-tracts.geojson'
          )
          const geoData = await geoResponse.json()

          geoData.features.forEach(
            (feature: { properties: Record<string, unknown> }) => {
              const geoid = (feature.properties.GEOID ||
                feature.properties.geoid) as string
              overlayConfigs.forEach(config => {
                const data = overlayData.get(config.id)
                const value = data?.get(geoid)
                feature.properties[config.propertyName] = value || null
              })
            }
          )

          map.current!.addSource('la-tracts', {
            type: 'geojson',
            data: geoData,
          })

          const initialConfig = overlayConfigs[0]
          map.current!.addLayer({
            id: 'tract-income-fill',
            type: 'fill',
            source: 'la-tracts',
            paint: {
              'fill-color': createColorExpression(initialConfig),
              'fill-opacity': 0.7,
            },
          })

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
    }, 200)

    return () => {
      clearTimeout(timer)
      if (map.current) {
        map.current.remove()
        map.current = null
      }
    }
  }, [dataLoaded, overlayData])

  useEffect(() => {
    if (map.current && dataLoaded) {
      updateMapLayer(activeOverlay)
    }
  }, [activeOverlay, dataLoaded])

  const activeConfig = overlayConfigs.find(
    config => config.id === activeOverlay
  )

  return (
    <div>
      {showNotification && (
        <div className="fixed top-4 left-4 bg-blue-500 text-white px-4 py-2 rounded-lg shadow-lg z-50 text-sm">
          <div className="flex items-center justify-between">
            <span>If map is not loading, please refresh the page</span>
            <button
              onClick={() => setShowNotification(false)}
              className="ml-3 text-white hover:text-gray-200"
            >
              -
            </button>
          </div>
        </div>
      )}
      <div className="relative">
        <div
          ref={mapContainer}
          className="w-full h-[34rem] 2xl:h-[44rem] rounded-lg shadow-lg"
        />

        {activeConfig && (
          <div className="absolute bottom-4 left-4 bg-white p-4 rounded-lg shadow-lg">
            <div className="text-sm font-semibold mb-2 text-black">
              {activeConfig.title}
            </div>
            <div className="space-y-1 text-xs">
              {activeConfig.colorBrackets.map((bracket, index) => (
                <div key={index} className="flex items-center">
                  <div
                    className="w-4 h-4 mr-2 border border-gray-300"
                    style={{ backgroundColor: bracket.color }}
                  />
                  <span className="text-black">
                    {bracket.max === Infinity
                      ? activeConfig.formatValue(bracket.max)
                      : `${activeConfig.formatValue(bracket.min)} - ${activeConfig.formatValue(bracket.max)}`}
                  </span>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>

      <div className="mt-10 flex gap-4">
        {overlayConfigs.map(config => (
          <button
            key={config.id}
            className={`flex-1 px-10 py-4 rounded shadow-lg text-sm ${
              activeOverlay === config.id
                ? 'bg-blue-600 text-white'
                : 'bg-gray-100 hover:bg-gray-200 text-black'
            }`}
            onClick={() => setActiveOverlay(config.id)}
          >
            {config.title}
          </button>
        ))}
      </div>
    </div>
  )
}
