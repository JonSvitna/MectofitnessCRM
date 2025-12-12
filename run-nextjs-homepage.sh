#!/bin/bash

# Script to run the Next.js homepage
# This script handles the directory conflict between Flask's app/ and Next.js's app router

echo "🚀 Starting Mectofitness Next.js Homepage..."
echo ""

# Check if Flask app directory exists
if [ -d "app" ] && [ ! -d "flask_app" ]; then
    echo "📁 Temporarily renaming Flask app directory..."
    mv app flask_app
    RENAMED=true
else
    RENAMED=false
fi

echo "📦 Installing dependencies (if needed)..."
npm install

echo "🔨 Building Next.js application..."
npm run nextjs:build

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Build successful!"
    echo ""
    echo "🌐 Starting development server..."
    echo "   Visit: http://localhost:3000"
    echo ""
    echo "   Press Ctrl+C to stop the server"
    echo ""
    
    # Start dev server
    npm run nextjs:dev
    
    # When server stops, restore Flask app
    if [ "$RENAMED" = true ]; then
        echo ""
        echo "🔄 Restoring Flask app directory..."
        mv flask_app app
        echo "✅ Flask app restored"
    fi
else
    echo ""
    echo "❌ Build failed"
    
    # Restore Flask app on failure
    if [ "$RENAMED" = true ]; then
        echo "🔄 Restoring Flask app directory..."
        mv flask_app app
        echo "✅ Flask app restored"
    fi
    exit 1
fi
