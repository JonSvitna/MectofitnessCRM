#!/bin/bash
# Build Next.js homepage as static export
# This script temporarily renames the Flask app directory to avoid conflicts

set -e

echo "========================================" 
echo "Building Next.js Static Homepage"
echo "========================================"
echo ""

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Error: Node.js not found"
    exit 1
fi

# Check if app directory exists
if [ ! -d "app" ]; then
    echo "❌ Error: Flask app directory not found"
    exit 1
fi

echo "Step 1: Temporarily renaming Flask app directory..."
mv app flask_app_temp

echo "Step 2: Building Next.js homepage..."
npm run nextjs:build

echo "Step 3: Restoring Flask app directory..."
mv flask_app_temp app

echo "Step 4: Copying static files to Flask static directory..."
# Remove old homepage files if they exist
rm -rf app/static/homepage

# Create homepage directory
mkdir -p app/static/homepage

# Copy Next.js build output
cp -r out/* app/static/homepage/

echo ""
echo "✅ Homepage build complete!"
echo "   Static files copied to: app/static/homepage/"
echo ""
