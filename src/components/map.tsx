'use client'
import { useEffect, useRef } from 'react'
import mapboxgl from 'mapbox-gl'
import 'mapbox-gl/dist/mapbox-gl.css'

export default function Map() {
  const mapContainer = useRef<HTMLDivElement>(null)
  const map = useRef<mapboxgl.Map | null>(null)

  useEffect(() => {
    if (map.current) return
    
    mapboxgl.accessToken = process.env.NEXT_PUBLIC_MAPBOX_ACCESS_TOKEN!
    
    map.current = new mapboxgl.Map({
      container: mapContainer.current!,
      style: 'mapbox://styles/mapbox/streets-v12',
      center: [-118.2437, 34.0522], // LA County center
      zoom: 8.5
    })

    map.current.on('load', () => {
      // Add the census tracts data source
      map.current!.addSource('la-tracts', {
        type: 'geojson',
        data: '/data/processed/la-county-tracts.geojson'
      })

      // Add tract boundary layer
      map.current!.addLayer({
        id: 'tract-boundaries',
        type: 'line',
        source: 'la-tracts',
        paint: {
          'line-color': '#627BC1',
          'line-width': 1,
          'line-opacity': 0.8
        }
      })




    })

    return () => {
      if (map.current) {
        map.current.remove()
      }
    }
  }, [])

  return (
    <div 
      ref={mapContainer} 
      className="w-full h-[48rem] rounded-lg shadow-lg"
    />
  )
}