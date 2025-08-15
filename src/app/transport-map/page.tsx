import TransportMap from '@/components/transport-map'

export default function MapPage() {
  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-center">
        2023 LA County Transportation Data Map
      </h1>
      <TransportMap key="transport-map-page" />
    </main>
  )
}
