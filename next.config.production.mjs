/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  // For Railway deployment, use standalone mode for optimal performance
  output: 'standalone',
  // Enable image optimization
  images: {
    unoptimized: false,
  },
  // Environment variables for frontend
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5000',
  },
}

export default nextConfig
