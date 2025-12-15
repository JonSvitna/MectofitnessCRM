/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  output: 'export',
  // Disable image optimization for static export
  images: {
    unoptimized: true,
  },
  // Output directory for static export
  distDir: 'out',
  // Trailing slash for better static hosting compatibility
  trailingSlash: true,
}

export default nextConfig
