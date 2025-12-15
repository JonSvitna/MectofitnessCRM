# Frontend Deployment - Quick Reference

## Current Setup ✅

Your frontend is **built with Vite + Tailwind CSS** and ready to deploy!

- **Build command**: `npm run build`
- **Output directory**: `app/static/dist/`
- **Assets**: CSS + JS bundles in `app/static/dist/assets/`

---

## Deployment Options

### Option 1: All-in-One on Render (RECOMMENDED) ⭐

**Simplest approach** - Everything in one place:

```bash
# Just deploy to Render - it builds everything automatically!
# Go to: https://dashboard.render.com
# Click "New +" → "Blueprint" → Select your repo
# Wait 10 minutes
# Done! 🎉
```

**Pros:**
- ✅ One deployment
- ✅ No CORS issues
- ✅ No configuration needed
- ✅ Everything works together

**Cons:**
- ⚠️ Static assets not on CDN (but performance is still good)

---

### Option 2: Render (Backend) + Vercel (Static CDN)

**For better performance** - Static assets on global CDN:

#### Step 1: Deploy Backend to Render
```bash
# Follow DEPLOY_NOW.md
# Get your backend running first at: https://mectofitness-api.onrender.com
```

#### Step 2: Deploy Static Assets to Vercel
```bash
# Install Vercel CLI
npm install -g vercel

# Deploy
./deploy-vercel.sh

# Or manually:
vercel --prod
```

#### Step 3: Link Them Together
In Render dashboard:
1. Go to your service → Environment
2. Add: `STATIC_CDN_URL` = `https://your-vercel-app.vercel.app`
3. Save (app redeploys automatically)

**Pros:**
- ⚡ Faster global asset delivery
- 🌍 Edge caching worldwide
- 💰 Vercel free tier included

**Cons:**
- 🔧 More complex setup
- 🔗 Two services to manage

---

## Quick Test

### Test Build Locally:
```bash
npm run build
ls -la app/static/dist/assets/
```

Should show:
```
main-[hash].css  (22KB - your Tailwind styles)
main-[hash].js   (2KB - your JavaScript)
```

### Test Production Mode:
```bash
FLASK_ENV=production python run.py
# Visit http://localhost:5000
# Check browser console - no errors
# CSS should load correctly
```

---

## Files Configured

✅ **vercel.json** - Vercel deployment config (static assets only)
✅ **vite.config.js** - Vite build config (outputs to dist/)
✅ **package.json** - Build scripts
✅ **render.yaml** - Full-stack deployment (includes npm build)
✅ **config.py** - CDN URL support
✅ **deploy-vercel.sh** - One-command Vercel deployment

---

## What Gets Built

When you run `npm run build`:

1. **Vite** bundles your JavaScript (`app/static/src/main.js`)
2. **Tailwind CSS** processes and minifies your styles
3. **Output** goes to `app/static/dist/assets/`
4. **Files** are cache-busted with hashes (e.g., `main-CmgeP6Yw.js`)

---

## Troubleshooting

### Build Fails
```bash
# Check Node.js version
node --version  # Should be 18+

# Clean install
rm -rf node_modules package-lock.json
npm install
npm run build
```

### CSS Not Loading
```bash
# Check build output exists
ls app/static/dist/assets/*.css

# Verify template uses correct path
# In base_vite.html:
# {{ url_for('static', filename='dist/assets/main.css') }}
```

### Vercel Deployment Fails
```bash
# Login first
vercel login

# Check vercel.json is valid
cat vercel.json | python -m json.tool

# Try deployment
vercel --prod
```

---

## Cost Summary

| Option | Cost | Performance |
|--------|------|-------------|
| **Render Only** | $14/month | Good |
| **Render + Vercel** | $14/month | Excellent |

*Vercel free tier covers static assets for most projects*

---

## Recommended Flow

1. ✅ **First**: Deploy everything to Render (use DEPLOY_NOW.md)
2. ✅ **Test**: Make sure your app works end-to-end
3. ✅ **Optional**: Add Vercel CDN later if you need better performance
4. ✅ **Monitor**: Check performance and decide if CDN is worth it

---

## Next Steps

🎯 **Right now**: Deploy to Render first
📖 **Read**: `DEPLOY_NOW.md` for step-by-step instructions
🚀 **Later**: Consider adding Vercel CDN with `deploy-vercel.sh`

---

## Commands Cheat Sheet

```bash
# Build frontend
npm run build

# Deploy all to Render
# (Use Render dashboard with Blueprint)

# Deploy static to Vercel (optional)
./deploy-vercel.sh

# Test locally
npm run dev  # Development mode
FLASK_ENV=production python run.py  # Production mode
```
