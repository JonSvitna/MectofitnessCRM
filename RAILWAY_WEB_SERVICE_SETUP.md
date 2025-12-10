# Railway Web Service Setup Instructions

## Problem
You currently only have a **Postgres service** on Railway. You need to add a **Web Service** to run your Flask application.

## Solution: Create Web Service on Railway

### Option 1: Create from GitHub (Recommended)

1. **Go to Railway Dashboard**
   - Visit https://railway.app/dashboard
   - Select your project: "outstanding-alignment"

2. **Add New Service**
   - Click **"+ New"** button
   - Select **"GitHub Repo"**
   - Choose your repository: **JonSvitna/MectofitnessCRM**
   - Click **"Add Service"**

3. **Configure Service**
   - Railway will automatically detect `nixpacks.toml` and `start.sh`
   - Wait for initial build (2-3 minutes)

4. **Link Database**
   - In the new web service settings
   - Go to **"Variables"** tab
   - Click **"+ New Variable"** → **"Add Reference"**
   - Select your Postgres service
   - Choose **DATABASE_URL**
   - Save

5. **Generate Domain**
   - Go to **"Settings"** tab
   - Scroll to **"Networking"**
   - Click **"Generate Domain"**
   - Copy the generated URL (e.g., `yourapp-production-xxxx.up.railway.app`)

6. **Verify Deployment**
   - Visit your new domain
   - You should see the marketing homepage
   - Test signup at `/auth/register`
   - Test login at `/auth/login`

### Option 2: Deploy via Railway CLI

```bash
# Switch to web service (create if doesn't exist)
railway link

# Deploy
railway up

# Generate domain
railway domain
```

## Expected Result

After setup, you'll have TWO services:
1. **Postgres** - Your database
2. **Web** - Your Flask application (accessible via domain)

## Current State

Your code is **100% correct**:
- ✅ Homepage at `/` is public (no login required)
- ✅ Registration at `/auth/register` is public
- ✅ Login at `/auth/login` is public
- ✅ Login redirects work properly
- ✅ Auto-creates organization on signup
- ✅ All navigation links work

The issue is **only** that you don't have a web service deployed on Railway.

## Verify Locally

Your app works perfectly locally:
```bash
# Test locally
python run.py

# Visit in browser:
# http://localhost:5000/          - Should show marketing homepage
# http://localhost:5000/auth/register - Should show registration form
# http://localhost:5000/auth/login    - Should show login form
```

## Railway CLI Commands Reference

```bash
# Check current service
railway status

# List all services in project
# (No direct command - use dashboard)

# Link to different service
railway link

# See logs
railway logs

# Get domain
railway domain

# Deploy current code
railway up
```

## Need Help?

If you're still having issues:
1. Check Railway dashboard for build errors
2. Check Railway logs for runtime errors
3. Verify DATABASE_URL is linked to web service
4. Verify domain is generated and pointing to web service
