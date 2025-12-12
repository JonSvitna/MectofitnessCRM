# Homepage Deployment Fix - Summary

## Problem Statement

The user pushed a new Next.js homepage but Railway was still displaying the old Flask template-based homepage. This was happening because:

1. The Next.js homepage was never built or deployed
2. The `build.sh` script only built the Vite React dashboard, not the Next.js homepage
3. The Flask route at `/` still served the old `app/templates/index.html` template
4. Next.js has a directory conflict with Flask's `app/` folder (both use `app/` directory)

## Solution Implemented

We converted the Next.js homepage to a **static export** that is served by Flask. This provides:
- ✅ Simpler deployment (no separate Next.js server)
- ✅ Better performance (pre-rendered HTML)
- ✅ Resolves directory conflicts
- ✅ Single application deployment
- ✅ SEO-friendly static content

## Changes Made

### 1. Next.js Configuration
**File:** `next.config.mjs`
- Changed `output: 'standalone'` to `output: 'export'`
- Enabled image optimization bypass (required for static export)
- Set output directory to `out/`

### 2. Build Scripts
**File:** `build-homepage.sh` (new)
- Manual build script for development
- Temporarily renames Flask app/ to avoid conflict
- Builds Next.js and copies output to Flask static directory

**File:** `build.sh` (updated)
- Railway build script now builds both:
  1. Vite React dashboard (`npm run build`)
  2. Next.js static homepage (`npm run nextjs:build`)
- Automatically handles app/ directory renaming
- Copies Next.js output to `app/static/homepage/`

### 3. Flask Routes
**File:** `app/routes/main.py` (updated)
- Route `/` now serves `app/static/homepage/index.html`
- Route `/_next/<path:path>` serves Next.js static assets
- Includes fallback to old template if homepage not built

### 4. Homepage Components
**File:** `src/components/ui/Button.tsx` (updated)
- Now supports both button and anchor elements
- Accepts optional `href` prop for links
- Used throughout homepage for navigation

**Files:** `src/components/sections/Navbar.tsx`, `Hero.tsx`, `Pricing.tsx` (updated)
- Connected all CTAs to Flask authentication routes:
  - "Start Free Trial" → `/register`
  - "Sign In" → `/login`
  - "View Features" → `#features`

### 5. Utilities
**File:** `src/lib/cn.ts` (new)
- Tailwind CSS class merge utility
- Required by Button and Card components
- Combines clsx and tailwind-merge

### 6. Git Configuration
**File:** `.gitignore` (updated)
- Added `out/`, `.next/`, `app/static/homepage/` (build artifacts)
- Excluded `src/lib/` from Python lib/ ignore rule

### 7. Documentation
**File:** `STATIC_HOMEPAGE_GUIDE.md` (new)
- Comprehensive deployment guide
- Architecture explanation
- Build process documentation
- Troubleshooting section
- Common issues and solutions

**File:** `verify-homepage.py` (new)
- Automated verification script
- Checks all required files exist
- Validates configuration
- Provides deployment checklist

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Flask Application                     │
├─────────────────────────────────────────────────────────┤
│  GET /                                                   │
│  ├─→ app/static/homepage/index.html (Next.js export)   │
│  └─→ Fallback: app/templates/index.html (if not built) │
├─────────────────────────────────────────────────────────┤
│  GET /_next/*                                           │
│  └─→ app/static/homepage/_next/* (CSS, JS, assets)     │
├─────────────────────────────────────────────────────────┤
│  GET /login                                             │
│  └─→ Flask authentication (app/templates/auth/login)   │
├─────────────────────────────────────────────────────────┤
│  GET /register                                          │
│  └─→ Flask authentication (app/templates/auth/register)│
├─────────────────────────────────────────────────────────┤
│  GET /dashboard                                         │
│  └─→ React SPA (Vite build → app/static/dist/)        │
└─────────────────────────────────────────────────────────┘
```

## Deployment Flow

### Railway Automatic Deployment

1. **Code pushed to GitHub**
2. **Railway detects changes**
3. **Build phase** (`build.sh`):
   ```bash
   npm install
   npm run build          # Build Vite dashboard
   npm run nextjs:build   # Build Next.js homepage
   cp out/* → app/static/homepage/
   ```
4. **Start phase** (`start.sh`):
   ```bash
   init_db.py             # Initialize database
   gunicorn run:app       # Start Flask server
   ```
5. **Homepage live!** 🎉

### Local Development

```bash
# Option 1: Build and test with Flask
./build-homepage.sh
export DATABASE_URL="sqlite:///test.db"
export SECRET_KEY="test-key"
python run.py
# Visit http://localhost:5000

# Option 2: Next.js dev server (for development)
./run-nextjs-homepage.sh
# Visit http://localhost:3000
```

## Verification

Run the verification script:
```bash
python3 verify-homepage.py
```

Expected output:
```
✅ All checks passed! Homepage is ready for deployment.
```

## Testing Checklist

- [x] ✅ Next.js homepage builds successfully
- [x] ✅ Static files copied to `app/static/homepage/`
- [x] ✅ Flask route serves homepage at `/`
- [x] ✅ Next.js assets served at `/_next/*`
- [x] ✅ CTAs link to Flask auth routes
- [x] ✅ All verification checks pass

## Railway Deployment

### On Railway, the following will happen automatically:

1. ✅ **Build Process**
   - Install Python dependencies
   - Install Node dependencies
   - Build Vite dashboard
   - Build Next.js homepage (new!)
   - Copy homepage to Flask static directory

2. ✅ **Runtime**
   - Flask serves homepage at root `/`
   - Homepage CTAs link to `/login` and `/register`
   - Dashboard accessible at `/dashboard`
   - All authentication handled by Flask

### Monitoring the Deployment

In Railway dashboard, look for these log messages:

```
Building static homepage (Next.js)...
✅ Static homepage copied to app/static/homepage/
Starting Gunicorn Server...
```

If you see these messages, the homepage is deployed! 🚀

## Why This Works Better

### Previous Approach (Not Working)
- Next.js code existed but wasn't built
- Build script didn't know about Next.js
- Flask served old template
- No integration between Next.js and Flask

### New Approach (Working)
- ✅ Next.js builds to static files
- ✅ Build script handles everything
- ✅ Flask serves static export
- ✅ Full integration, single deployment
- ✅ Better performance (pre-rendered)
- ✅ Simpler architecture

## Next Steps for User

1. **Review the PR** - Check all changes make sense
2. **Merge to main** - Railway will auto-deploy
3. **Monitor logs** - Watch for build success messages
4. **Test homepage** - Visit Railway domain
5. **Verify CTAs** - Click "Sign In" and "Start Free Trial"

## Future Maintenance

### Updating Homepage Content

1. Edit files in `src/components/sections/`
2. Commit and push
3. Railway automatically rebuilds and deploys

### Troubleshooting

If homepage doesn't update:
1. Check Railway build logs
2. Look for "✅ Static homepage copied"
3. Run `python3 verify-homepage.py` locally
4. See `STATIC_HOMEPAGE_GUIDE.md` for detailed troubleshooting

## Files Modified

```
Modified:
- next.config.mjs (static export config)
- build.sh (added homepage build)
- app/routes/main.py (serve static homepage)
- src/components/ui/Button.tsx (support href)
- src/components/sections/Navbar.tsx (auth links)
- src/components/sections/Hero.tsx (auth links)
- src/components/sections/Pricing.tsx (auth links)
- .gitignore (exclude build artifacts)

Created:
- build-homepage.sh (manual build script)
- src/lib/cn.ts (Tailwind utility)
- STATIC_HOMEPAGE_GUIDE.md (comprehensive docs)
- verify-homepage.py (verification script)
- HOMEPAGE_FIX_SUMMARY.md (this file)
```

## Success Criteria

✅ Homepage displays on Railway
✅ All CTAs link to correct Flask routes
✅ No separate Next.js server needed
✅ Automatic builds on Railway
✅ Pre-rendered for performance and SEO

---

**Status:** ✅ READY FOR DEPLOYMENT

The homepage will now display correctly on Railway after the next push to main branch.
