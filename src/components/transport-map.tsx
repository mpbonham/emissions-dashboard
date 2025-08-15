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
    id: 'travel-time',
    title: 'Avg. Travel Time to Work (Minutes)',
    dataFile: '/data/census/06037_travel_time.csv',
    propertyName: 'avg_travel_time',
    colorBrackets: [
      { min: 0, max: 26.79, color: '#08306b' },
      { min: 26.79, max: 28.85, color: '#2171b5' },
      { min: 28.85, max: 30.27, color: '#6baed6' },
      { min: 30.27, max: 31.34, color: '#c6dbef' },
      { min: 31.34, max: 32.41, color: '#ffffcc' },
      { min: 32.41, max: 33.44, color: '#fed976' },
      { min: 33.44, max: 34.49, color: '#feb24c' },
      { min: 34.49, max: 35.41, color: '#fd8d3c' },
      { min: 35.41, max: 36.65, color: '#f03b20' },
      { min: 36.65, max: 38.13, color: '#d12f2f' },
      { min: 38.13, max: 40.7, color: '#bd0026' },
      { min: 40.7, max: Infinity, color: '#7a0177' },
    ],
    formatValue: (value: number) =>
      value === Infinity ? `>${(40.7).toFixed(1)}` : value.toFixed(1),
  },
  {
    id: 'car-commute-time',
    title: 'Average Car Commute Time (Minutes)',
    dataFile: '/data/census/06037_car_commute_time.csv',
    propertyName: 'car_avg_travel_time',
    colorBrackets: [
      { min: 0, max: 26.28, color: '#08306b' },
      { min: 26.28, max: 28.15, color: '#2171b5' },
      { min: 28.15, max: 29.51, color: '#6baed6' },
      { min: 29.51, max: 30.47, color: '#c6dbef' },
      { min: 30.47, max: 31.3, color: '#ffffcc' },
      { min: 31.3, max: 32.12, color: '#fed976' },
      { min: 32.12, max: 33.01, color: '#feb24c' },
      { min: 33.01, max: 33.92, color: '#fd8d3c' },
      { min: 33.92, max: 35.05, color: '#f03b20' },
      { min: 35.05, max: 36.38, color: '#d12f2f' },
      { min: 36.38, max: 38.57, color: '#bd0026' },
      { min: 38.57, max: Infinity, color: '#7a0177' },
    ],
    formatValue: (value: number) =>
      value === Infinity ? `>${(38.57).toFixed(1)}` : `${value.toFixed(1)}`,
  },
  {
    id: 'car-commuter-percentage',
    title: 'Car Commuter Percentage (%)',
    dataFile: '/data/census/06037_car_commuter_percentage.csv',
    propertyName: 'car_commuter_percentage',
    colorBrackets: [
      { min: 0, max: 0.55, color: '#08306b' },
      { min: 0.55, max: 0.62, color: '#2171b5' },
      { min: 0.62, max: 0.67, color: '#6baed6' },
      { min: 0.67, max: 0.72, color: '#c6dbef' },
      { min: 0.72, max: 0.75, color: '#ffffcc' },
      { min: 0.75, max: 0.78, color: '#fed976' },
      { min: 0.78, max: 0.8, color: '#feb24c' },
      { min: 0.8, max: 0.83, color: '#fd8d3c' },
      { min: 0.83, max: 0.85, color: '#f03b20' },
      { min: 0.85, max: 0.87, color: '#d12f2f' },
      { min: 0.87, max: 0.9, color: '#bd0026' },
      { min: 0.9, max: Infinity, color: '#7a0177' },
    ],
    formatValue: (value: number) =>
      value === Infinity
        ? `>${(0.9 * 100).toFixed(0)}`
        : `${(value * 100).toFixed(0)}%`,
  },
  {
    id: 'car-transport-emissions',
    title: 'Car Commute Emissions (metric tons CO2e per household)',
    dataFile: '/data/census/06037_car_transport_emissions_per_household.csv',
    propertyName: 'car_co2_metric_tons_per_household',
    colorBrackets: [
      { min: 0, max: 1.61, color: '#08306b' },
      { min: 1.61, max: 2.06, color: '#2171b5' },
      { min: 2.06, max: 2.44, color: '#6baed6' },
      { min: 2.44, max: 2.7, color: '#c6dbef' },
      { min: 2.7, max: 3.02, color: '#ffffcc' },
      { min: 3.02, max: 3.33, color: '#fed976' },
      { min: 3.33, max: 3.59, color: '#feb24c' },
      { min: 3.59, max: 3.88, color: '#fd8d3c' },
      { min: 3.88, max: 4.2, color: '#f03b20' },
      { min: 4.2, max: 4.55, color: '#d12f2f' },
      { min: 4.55, max: 5.12, color: '#bd0026' },
      { min: 5.12, max: Infinity, color: '#7a0177' },
    ],
    formatValue: (value: number) =>
      value === Infinity ? `>${(5.12).toFixed(1)}` : `${value.toFixed(1)} `,
  },
  {
    id: 'latch-emissions',
    title: 'LATCH Transport Emissions per Household',
    dataFile: '/data/census/06037_latch_emissions.csv',
    propertyName: 'co2_metric_tons_per_household',
    colorBrackets: [
      { min: 0, max: 2.76, color: '#08306b' },
      { min: 2.76, max: 3.07, color: '#2171b5' },
      { min: 3.07, max: 3.28, color: '#6baed6' },
      { min: 3.28, max: 3.42, color: '#c6dbef' },
      { min: 3.42, max: 3.56, color: '#ffffcc' },
      { min: 3.56, max: 3.71, color: '#fed976' },
      { min: 3.71, max: 3.85, color: '#feb24c' },
      { min: 3.85, max: 4.0, color: '#fd8d3c' },
      { min: 4.0, max: 4.16, color: '#f03b20' },
      { min: 4.16, max: 4.32, color: '#d12f2f' },
      { min: 4.32, max: 4.58, color: '#bd0026' },
      { min: 4.58, max: Infinity, color: '#7a0177' },
    ],
    formatValue: (value: number) =>
      value === Infinity
        ? `>${(4.58).toFixed(2)} tons`
        : `${value.toFixed(2)} `,
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

export default function TravelTimeMap() {
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<mapboxgl.Map | null>(null)
  const [overlayData, setOverlayData] = useState<
    Map<string, Map<string, number>>
  >(new Map())
  const [activeOverlay, setActiveOverlay] = useState<string>('travel-time')
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
    if (!map.current || !map.current.getLayer('tract-travel-time-fill')) return

    const config = overlayConfigs.find(c => c.id === overlayId)
    if (!config) return

    const colorExpression = createColorExpression(config)
    map.current.setPaintProperty(
      'tract-travel-time-fill',
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
            id: 'tract-travel-time-fill',
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
      <div className="relative">
        <div
          ref={mapContainer}
          className="w-full h-[40rem] 2xl:h-[48rem] rounded-lg shadow-lg"
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
