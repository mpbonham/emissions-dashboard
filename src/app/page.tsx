import Link from 'next/link'

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
      <div className="text-center p-8">
        <h1 className="text-4xl md:text-6xl font-bold text-gray-900 mb-4">
          Census Tract Explorer
        </h1>
        <p className="text-lg md:text-xl text-gray-600 mb-8 max-w-2xl">
          Explore demographic data across California census tracts with
          interactive maps and detailed overlays.
        </p>
        <div className="flex gap-4">
          <Link
            href="/transport-map"
            className="flex-1 inline-block bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-md font-semibold transition-colors shadow-lg"
          >
            Explore Transport Map →
          </Link>
          <Link
            href="/map"
            className="flex-1 inline-block bg-blue-600 hover:bg-blue-700 text-white px-8 py-4 rounded-lg text-md font-semibold transition-colors shadow-lg"
          >
            Explore Household Data Map →
          </Link>
        </div>
        <a
          href="https://github.com/mpbonham/emissions-dashboard"
          className="block mt-8 bg-purple-500 hover:bg-purple-600 text-black px-6 py-3 rounded-lg font-semibold transition-colors"
        >
          GitHub
        </a>
      </div>
    </div>
  )
}
