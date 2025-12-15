#!/bin/bash
# Build Next.js homepage as static export

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

# Check if frontend directory exists
if [ ! -d "frontend" ]; then
    echo "❌ Error: Frontend directory not found"
    exit 1
fi

echo "Step 1: Building Next.js homepage..."
cd frontend
npm install
npm run build

echo ""
echo "✅ Homepage build complete!"
echo "   Next.js site ready in frontend/.next/"
echo ""
