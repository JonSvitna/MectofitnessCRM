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
    // Must be set in Railway environment variables for production
    // This fallback should only be used in development
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://your-backend.railway.app',
  },
}

export default nextConfig
