import Map from '@/components/map'

export default function MapPage() {
  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-center">
        2023 LA County Tract Map
      </h1>
      <Map key="map-page" />
    </main>
  )
}
