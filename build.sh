#!/bin/bash
# Railway build script

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Node dependencies..."
npm install

echo "Building frontend dashboard (React/Vite)..."
npm run build

echo "Building static homepage (Next.js)..."

# Cleanup function to restore app directory
cleanup_app_dir() {
    if [ -d "flask_app_temp" ] && [ ! -d "app" ]; then
        echo "⚠️  Restoring Flask app directory after error..."
        mv flask_app_temp app
    fi
}

# Set trap to ensure cleanup on exit
trap cleanup_app_dir EXIT INT TERM

# Temporarily rename Flask app directory to avoid Next.js conflict
if [ -d "app" ]; then
    mv app flask_app_temp
    npm run nextjs:build
    mv flask_app_temp app
    
    # Copy Next.js build to static directory
    if [ -d "out" ]; then
        rm -rf app/static/homepage
        mkdir -p app/static/homepage
        cp -r out/* app/static/homepage/
        echo "✅ Static homepage copied to app/static/homepage/"
    else
        echo "⚠️  Next.js build output not found, skipping homepage"
    fi
else
    echo "⚠️  Flask app directory not found, skipping homepage build"
fi

echo "Build complete!"
