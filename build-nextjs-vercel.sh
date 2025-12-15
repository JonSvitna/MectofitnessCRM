#!/bin/bash
# Build script for Vercel deployment
# Temporarily renames Flask app directory to avoid Next.js conflict

set -e

echo "🔨 Building Next.js for Vercel deployment..."

# Check if Flask app directory exists
if [ ! -d "app" ]; then
    echo "✅ Flask app directory not present, building normally..."
    npm run nextjs:build
    exit 0
fi

echo "📁 Temporarily renaming Flask app directory..."
mv app flask_app_temp

# Cleanup function to restore app directory
cleanup() {
    if [ -d "flask_app_temp" ]; then
        echo "🔄 Restoring Flask app directory..."
        mv flask_app_temp app
    fi
}

# Set trap to ensure cleanup on exit
trap cleanup EXIT INT TERM

echo "⚙️  Building Next.js..."
npm run nextjs:build

echo "✅ Build complete!"
