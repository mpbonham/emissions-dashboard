import Map from '@/components/map'

export default function Home() {
  return (
    <main className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-6 text-center">My Mapbox App</h1>
      <Map />
    </main>
  )
}
