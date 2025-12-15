#!/bin/bash

# Script to run the Next.js homepage

echo "🚀 Starting Mectofitness Next.js Homepage..."
echo ""

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo "❌ Error: Frontend directory not found"
    exit 1
fi

cd frontend

echo "📦 Installing dependencies (if needed)..."
npm install

echo "🌐 Starting development server..."
echo "   Visit: http://localhost:3000"
echo ""
echo "   Press Ctrl+C to stop the server"
echo ""

# Start dev server
npm run dev
