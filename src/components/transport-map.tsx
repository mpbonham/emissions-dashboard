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
