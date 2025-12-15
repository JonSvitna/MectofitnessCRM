#!/bin/bash
# Railway build script for backend CRM only

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing Node dependencies..."
npm install

echo "Building React dashboard (Vite)..."
npm run build

echo ""
echo "✅ Backend build complete!"
echo ""
echo "📝 Note: Next.js marketing homepage should be deployed separately to Vercel"
echo "   To deploy frontend: vercel --prod (from repository root)"
