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
    // IMPORTANT: Set NEXT_PUBLIC_API_URL in Railway environment variables
    // This placeholder should be replaced with your actual backend URL
    // Example: https://mecto-backend-xyz.railway.app
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'https://SET-BACKEND-URL-IN-RAILWAY-ENV.railway.app',
  },
}

export default nextConfig
