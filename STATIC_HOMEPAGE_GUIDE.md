# Static Homepage Deployment Guide

## Overview

The MectoFitness homepage is built with Next.js and exported as static HTML/CSS/JS files. These static files are served by Flask at the root route (`/`), providing a modern, performant homepage while keeping the CRM dashboard as a React SPA.

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Flask Application                     │
├─────────────────────────────────────────────────────────┤
│  Route: /                                               │
│  → Serves: app/static/homepage/index.html              │
│  → Assets: app/static/homepage/_next/*                 │
├─────────────────────────────────────────────────────────┤
│  Route: /dashboard                                      │
│  → Serves: React SPA (Vite build)                      │
│  → Assets: app/static/dist/*                           │
└─────────────────────────────────────────────────────────┘
```

## Why Static Export?

**Benefits:**
- ✅ **No separate Next.js server needed** - Flask serves everything
- ✅ **Better performance** - Pre-rendered HTML, instant page loads
- ✅ **Simpler deployment** - Single application to deploy
- ✅ **No directory conflicts** - Next.js app/ conflict resolved
- ✅ **Lower hosting costs** - Static files are cheap to serve
- ✅ **SEO-friendly** - Pre-rendered content for search engines

**Trade-offs:**
- ❌ No Next.js API routes (use Flask API instead)
- ❌ No server-side rendering at request time (SSR)
- ❌ No incremental static regeneration (ISR)

For a marketing homepage, these trade-offs are acceptable and the benefits outweigh them.

## Build Process

### Local Development

To work on the homepage locally:

```bash
# Option 1: Run Next.js dev server (best for development)
./run-nextjs-homepage.sh

# Option 2: Build and test with Flask
./build-homepage.sh
python run.py
# Visit http://localhost:5000
```

### Production Build (Automatic)

The `build.sh` script handles everything automatically during Railway deployment:

1. **Install dependencies** - npm install
2. **Build dashboard** - npm run build (Vite)
3. **Build homepage** - npm run nextjs:build
4. **Copy to static** - out/* → app/static/homepage/

```bash
# This runs automatically on Railway
./build.sh
```

## File Structure

```
/home/runner/work/MectofitnessCRM/MectofitnessCRM/
├── src/                          # Next.js source files
│   ├── app/                      # Next.js App Router
│   │   ├── layout.tsx           # Root layout with SEO metadata
│   │   ├── page.tsx             # Homepage (imports sections)
│   │   └── globals.css          # Tailwind styles
│   ├── components/
│   │   ├── ui/                  # Reusable UI components
│   │   └── sections/            # Homepage sections
│   └── lib/
│       └── cn.ts                # Tailwind class merger utility
├── out/                          # Next.js build output (gitignored)
├── app/static/homepage/          # Served by Flask (NOW TRACKED IN GIT)
│   ├── index.html               # Homepage HTML
│   ├── 404.html                 # 404 page
│   └── _next/                   # Next.js static assets
│       ├── static/              # CSS, JS chunks
│       └── [build-id]/          # Build-specific assets
└── build-homepage.sh            # Manual build script
```

## Flask Route Configuration

The Flask routes in `app/routes/main.py` handle serving the static homepage:

```python
@bp.route('/')
def index():
    """Landing page - serves Next.js static homepage."""
    homepage_path = os.path.join(current_app.static_folder, 'homepage', 'index.html')
    if os.path.exists(homepage_path):
        return send_from_directory(
            os.path.join(current_app.static_folder, 'homepage'),
            'index.html'
        )
    else:
        # Fallback to old template if Next.js homepage not built
        return render_template('index.html')

@bp.route('/_next/<path:path>')
def serve_next_assets(path):
    """Serve Next.js static assets."""
    return send_from_directory(
        os.path.join(current_app.static_folder, 'homepage', '_next'),
        path
    )
```

## Next.js Configuration

The `next.config.mjs` is configured for static export:

```javascript
const nextConfig = {
  reactStrictMode: true,
  output: 'export',           // Enable static export
  images: {
    unoptimized: true,        // Required for static export
  },
  distDir: 'out',             // Output directory
}
```

## Deployment on Railway

### First-Time Setup

1. Push your code to GitHub
2. Railway automatically:
   - Detects the repository
   - Runs `build.sh`
   - Starts Flask with `start.sh`
3. Homepage is live at your Railway domain

### Updating the Homepage

1. Edit files in `src/app/` or `src/components/`
2. Commit and push to GitHub
3. Railway automatically:
   - Runs build process
   - Rebuilds homepage
   - Deploys new version

No manual steps required!

## Common Issues

### Issue: Homepage shows old Flask template

**Cause:** Next.js homepage wasn't built during deployment

**Solution:**
```bash
# Build and commit the homepage files
./build-homepage.sh
git add app/static/homepage
git commit -m "Add built homepage"
git push
```

**Note:** As of December 2024, `app/static/homepage/` has been removed from `.gitignore` to allow the built homepage files to be committed to the repository. This ensures the homepage is available even if the build process fails during deployment. The homepage files are now tracked in Git and will be pushed with your code.

### Issue: 404 on Next.js assets

**Cause:** `_next` route not configured in Flask

**Solution:** Ensure the `serve_next_assets` route is present in `app/routes/main.py` (already done)

### Issue: Styles not loading

**Cause:** CSS files not found in `_next/static/css/`

**Solution:**
```bash
# Verify build output
ls -la app/static/homepage/_next/static/css/

# If empty, rebuild
./build-homepage.sh
```

### Issue: "app directory not found" during build

**Cause:** Previous build failed and didn't restore the Flask app directory

**Solution:**
```bash
# Restore the directory
mv flask_app_temp app
```

## Testing

### Test Locally

```bash
# 1. Build the homepage
./build-homepage.sh

# 2. Verify files exist
python test_homepage_serve.py

# 3. Start Flask (requires DATABASE_URL)
export DATABASE_URL="sqlite:///test.db"
export SECRET_KEY="test-secret-key"
python run.py

# 4. Visit http://localhost:5000
```

### Test on Railway

1. Check build logs in Railway dashboard
2. Look for "✅ Static homepage copied to app/static/homepage/"
3. Visit your Railway domain
4. Verify homepage loads with correct styles

## Maintenance

### Updating Homepage Content

1. Edit React components in `src/components/sections/`
2. Edit styles in `src/app/globals.css`
3. Commit and push - Railway handles the rest

### Updating Homepage SEO

Edit metadata in `src/app/layout.tsx`:

```typescript
export const metadata = {
  title: 'Your New Title',
  description: 'Your new description',
  // ... other meta tags
}
```

### Adding New Sections

1. Create component in `src/components/sections/NewSection.tsx`
2. Import in `src/app/page.tsx`
3. Add to the page component
4. Commit and push

## Performance

The static export provides excellent performance:

- **First Contentful Paint:** < 1s
- **Largest Contentful Paint:** < 2s
- **Time to Interactive:** < 3s
- **Lighthouse Score:** 90+ typically

Pre-rendered HTML means:
- No client-side rendering delay
- Instant content display
- Better SEO crawlability
- Lower server load

## Future Enhancements

Possible improvements:

1. **CDN Deployment** - Deploy static files to Cloudflare/Vercel for global edge caching
2. **Image Optimization** - Add sharp/next-image-export-optimizer for optimized images
3. **Split Deployment** - Separate homepage (Vercel) from CRM (Railway)
4. **Analytics** - Add Google Analytics/Plausible for usage tracking
5. **A/B Testing** - Test different homepage variations

## Troubleshooting

**Problem:** Homepage doesn't update after code changes

**Solution:** 
- Clear browser cache
- Check Railway build logs
- Verify build completed successfully

**Problem:** Broken links to /login or /register

**Solution:**
- Ensure Flask auth routes are registered
- Check that auth blueprint is loaded

**Problem:** Mixed content warnings (http/https)

**Solution:**
- Update all URLs to use relative paths
- Ensure all assets use HTTPS in production

## Summary

This static export approach gives you:
- Modern Next.js development experience
- Simple Flask deployment
- Excellent performance
- Easy maintenance

The homepage is now a static asset served by Flask, making deployment straightforward and performant. 🚀
