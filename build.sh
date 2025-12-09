#!/bin/bash
# Railway build script

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Node dependencies..."
npm install

echo "Building frontend..."
npm run build

echo "Build complete!"
