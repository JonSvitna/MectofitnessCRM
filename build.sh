#!/bin/bash
# Railway build script

echo "Installing Python dependencies (Railway optimized)..."
pip install -r requirements-railway.txt

echo "Installing Node dependencies..."
npm install

echo "Building frontend..."
npm run build

echo "Build complete!"
