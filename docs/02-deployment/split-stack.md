# Split Stack Deployment Guide
## Backend (Render) + Static Assets (Vercel)

This guide shows you how to deploy your MectoFitness CRM with the backend on Render and optionally serve static assets through Vercel's CDN for better performance.

## Architecture

```
┌─────────────┐      ┌──────────────┐
│   Vercel    │      │    Render    │
│  (Static)   │◄────►│  (Backend)   │
│   CDN       │      │   Flask App  │
└─────────────┘      └──────────────┘
     CSS/JS              HTML/API
     Assets              Database
```

## Quick Start: Render Only (Recommended to Start)

If you just want to get deployed quickly, **deploy everything to Render first**:

### Step 1: Deploy to Render
```bash
# Already done! Your code is on GitHub
# Just go to: https://dashboard.render.com
# Click "New +" → "Blueprint" → Select your repo
# Wait 10 minutes for deployment
```

That's it! Your app will be fully functional at `https://mectofitness-api.onrender.com`

---

## Advanced: Add Vercel CDN for Static Assets (Optional)

Once your Render deployment works, you can optionally move static assets to Vercel's CDN for faster global delivery.

### Benefits:
- ⚡ Faster static asset loading globally
- 🌍 Edge caching worldwide
- 💰 Free tier covers most usage
- 📦 Automatic compression and optimization

### Step 1: Deploy Static Assets to Vercel

1. **Install Vercel CLI**:
   ```bash
   npm install -g vercel
   ```

2. **Login to Vercel**:
   ```bash
   vercel login
   ```

3. **Deploy Static Assets**:
   ```bash
   vercel --prod
   ```

4. **Note your Vercel URL**: e.g., `https://mectofitness-static.vercel.app`

### Step 2: Configure Render to Use Vercel CDN

1. Go to your Render dashboard
2. Select your `mectofitness-api` service
3. Go to **Environment** tab
4. Add new environment variable:
   - **Key**: `STATIC_CDN_URL`
   - **Value**: `https://your-vercel-deployment.vercel.app`

5. Click **Save Changes** (app will redeploy)

### Step 3: Update Templates (Optional)

To use the CDN URL in your templates, replace:
```html
<link rel="stylesheet" href="{{ url_for('static', filename='dist/assets/main.css') }}">
```

With:
```html
{% if cdn_url %}
<link rel="stylesheet" href="{{ cdn_url }}/assets/main.css">
{% else %}
<link rel="stylesheet" href="{{ url_for('static', filename='dist/assets/main.css') }}">
{% endif %}
```

---

## Deploy Everything to Render (Simpler Alternative)

**Honestly, this is the easiest approach:**

Your `render.yaml` already builds both frontend and backend:
```yaml
buildCommand: "pip install -r requirements.txt && npm install && npm run build"
```

This means:
- ✅ One deployment
- ✅ No CORS issues
- ✅ Simpler configuration
- ✅ Everything works together

The only downside is static assets aren't on a CDN, but for most apps, Render's performance is perfectly fine.

---

## Troubleshooting

### Vercel Build Fails
```bash
# Test build locally first
npm run build
# Check if dist/assets/ folder is created
ls -la app/static/dist/assets/
```

### Static Assets Not Loading from Vercel
1. Check `STATIC_CDN_URL` is set correctly in Render
2. Verify Vercel deployment succeeded
3. Check browser console for CORS errors
4. Ensure Vercel URL ends without trailing slash

### CORS Issues
If you get CORS errors when loading from Vercel, add to `app/__init__.py`:
```python
from flask_cors import CORS
CORS(app, resources={r"/static/*": {"origins": "*"}})
```

---

## Cost Comparison

### Render Only:
- **Web Service**: $7/month (Starter)
- **Database**: $7/month (Starter)
- **Total**: $14/month

### Render + Vercel:
- **Render Web**: $7/month
- **Render DB**: $7/month
- **Vercel**: FREE (hobby tier)
- **Total**: $14/month + slightly better performance

**Verdict**: Start with Render-only. Add Vercel later if you need CDN performance.

---

## What's Already Configured

✅ `vercel.json` - Configured for static asset deployment
✅ `vite.config.js` - Builds to correct output directory
✅ `config.py` - Supports `STATIC_CDN_URL` environment variable
✅ `app/__init__.py` - Template helper for CDN URLs
✅ `render.yaml` - Builds frontend during deployment

---

## Next Steps

1. **Deploy to Render first** (see DEPLOY_NOW.md)
2. **Test your app** - Make sure everything works
3. **Optional**: Add Vercel CDN later if needed
4. **Monitor**: Check Render dashboard for performance

---

## Quick Commands

```bash
# Build frontend locally
npm run build

# Deploy to Vercel (after Render works)
vercel --prod

# Check build output
ls -la app/static/dist/assets/

# Test locally with production build
FLASK_ENV=production python run.py
```
