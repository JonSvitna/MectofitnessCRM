#!/bin/bash
# Railway build script

echo "Installing Backend Python dependencies..."
cd backend
pip install -r requirements.txt
cd ..

echo "Installing Frontend Node dependencies..."
cd frontend
npm install
cd ..

echo "Building frontend static website (Next.js)..."
cd frontend
npm run build
cd ..

echo "Building backend dashboard (React/Vite)..."
cd backend
npm install
npm run build
cd ..

echo "Build complete!"
