#!/bin/bash
# Deploy static assets to Vercel

echo "🚀 Deploying MectoFitness Static Assets to Vercel"
echo ""

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Build the frontend
echo "📦 Building frontend assets..."
npm run build

# Check if build succeeded
if [ ! -d "app/static/dist/assets" ]; then
    echo "❌ Build failed! app/static/dist/assets not found"
    exit 1
fi

echo "✅ Build succeeded!"
echo ""

# Deploy to Vercel
echo "🌍 Deploying to Vercel..."
vercel --prod

echo ""
echo "✅ Deployment complete!"
echo ""
echo "📝 Next steps:"
echo "   1. Note the Vercel URL from above"
echo "   2. Add STATIC_CDN_URL environment variable in Render"
echo "   3. Set it to your Vercel URL (e.g., https://your-app.vercel.app)"
echo "   4. Your backend will now use Vercel CDN for static assets!"
