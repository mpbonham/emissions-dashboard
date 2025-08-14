/** @type {import('next').NextConfig} */
const nextConfig = {
  compress: true,
  async headers() {
    return [
      {
        source: '/data/(.*)',
        headers: [
          {
            key: 'Cache-Control', 
            value: 'public, max-age=604800, immutable',
          },
        ],
      },
    ]
  },
}

module.exports = nextConfig