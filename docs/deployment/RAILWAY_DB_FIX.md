# Railway Database Connection Issues - Troubleshooting Guide

## Error: `server closed the connection unexpectedly`

This error occurs when the PostgreSQL server terminates the connection. Here's how to fix it:

## ✅ Fixes Applied

1. **Connection Pooling** - Added in `config.py`:
   - `pool_pre_ping=True` - Tests connections before using
   - `pool_recycle=300` - Recycles connections every 5 minutes
   - TCP keepalives enabled

2. **SSL Requirements** - Added automatic SSL mode for PostgreSQL
   - Railway requires `sslmode=require`
   - Auto-added to DATABASE_URL if missing

3. **Connection Retry Logic** - Improved error handling
   - Graceful degradation on connection failure
   - Better logging for debugging

4. **Health Check Endpoint** - Added `/health` route
   - Tests database connectivity
   - Returns JSON status

## 🔧 Railway-Specific Configuration

### Step 1: Verify Environment Variables

In your Railway dashboard, ensure these are set:

```bash
DATABASE_URL=postgresql://user:password@host:port/database
# Or use the internal URL (better for Railway)
DATABASE_PRIVATE_URL=postgresql://user:password@postgres.railway.internal:5432/railway
```

**Important**: Railway provides multiple database URLs:
- `DATABASE_URL` - Public URL (external access)
- `DATABASE_PRIVATE_URL` - Internal URL (faster, more stable)
- `DATABASE_PUBLIC_URL` - Public URL with SSL

### Step 2: Update Your Service Environment Variables

Add these in Railway dashboard → Your Service → Variables:

```bash
# Use private URL for better stability
DATABASE_URL=${{Postgres.DATABASE_PRIVATE_URL}}

# Or reference the database service directly
DATABASE_URL=${{Postgres.DATABASE_URL}}
```

### Step 3: Check Database Connection Limits

Railway free tier has connection limits:
- **Free**: 20 connections
- **Hobby**: 100 connections

Our app is configured to use 10 connections max with 20 overflow.

### Step 4: Restart Your Service

After updating variables:
1. Go to Railway dashboard
2. Click your service
3. Click "Restart" or redeploy

## 🐛 Debugging Steps

### 1. Check Logs
```bash
railway logs
```

Look for:
- "Database connection successful" (good)
- "Database connection failed" (shows error details)

### 2. Test Connection Locally

```bash
# Install psql
apt-get update && apt-get install -y postgresql-client

# Test connection (replace with your Railway DATABASE_URL)
psql "postgresql://user:password@trolley.proxy.rlwy.net:47021/railway?sslmode=require"
```

### 3. Check Connection String Format

Your DATABASE_URL should look like:
```
postgresql://postgres:PASSWORD@trolley.proxy.rlwy.net:47021/railway
```

**Common Issues**:
- ❌ `postgres://` instead of `postgresql://` (we auto-fix this)
- ❌ Missing `?sslmode=require` (we auto-add this)
- ❌ Wrong port number
- ❌ Expired credentials

### 4. Verify Database is Running

In Railway dashboard:
- Go to your PostgreSQL service
- Check status (should be "Active")
- Check logs for any errors

## 🔐 SSL Certificate Issues

If you see SSL errors, add to your DATABASE_URL:
```
?sslmode=require
```

Or disable SSL verification (NOT recommended for production):
```
?sslmode=prefer
```

## 📊 Monitor Connection Health

Visit your deployed app:
```
https://your-app.railway.app/health
```

Should return:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

If unhealthy:
```json
{
  "status": "unhealthy",
  "database": "disconnected",
  "error": "error details here"
}
```

## 🚀 Railway Deployment Checklist

- [ ] PostgreSQL service is running
- [ ] Database credentials are correct
- [ ] Environment variables are set in service settings
- [ ] Using `DATABASE_PRIVATE_URL` or `${{Postgres.DATABASE_URL}}`
- [ ] Service has restarted after variable changes
- [ ] Health check endpoint returns 200
- [ ] Logs show "Database connection successful"

## 💡 Common Solutions

### Solution 1: Use Private URL
```bash
# In Railway Variables tab
DATABASE_URL=${{Postgres.DATABASE_PRIVATE_URL}}
```

### Solution 2: Increase Timeout
Already configured in `config.py`:
```python
'connect_timeout': 10
'pool_timeout': 30
```

### Solution 3: Reduce Connection Pool
If hitting connection limits, edit `config.py`:
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 5,        # Reduce from 10
    'max_overflow': 10,    # Reduce from 20
}
```

### Solution 4: Enable Connection Pre-Ping
Already enabled in `config.py`:
```python
'pool_pre_ping': True  # Tests connections before use
```

## 🔄 Still Having Issues?

### Check Railway Status
- Visit: https://railway.app/status
- Check if there are ongoing incidents

### Contact Support
- Railway Discord: https://discord.gg/railway
- Railway Help: https://help.railway.app

### Alternative: Use Render
If Railway issues persist, try Render (includes managed PostgreSQL):
```bash
# Deploy to Render instead
# See RENDER_DEPLOYMENT.md for instructions
```

## 📝 Updated Configuration Files

The following files have been updated to fix connection issues:

1. **config.py**
   - Added connection pooling
   - Added SSL requirement auto-detection
   - Added TCP keepalives
   - Added connection timeouts

2. **app/__init__.py**
   - Added connection testing on startup
   - Added better error logging
   - Added graceful degradation

3. **app/routes/main.py**
   - Added `/health` endpoint
   - Database connectivity check

## 🎯 Quick Fix Commands

```bash
# Commit and push changes
git add .
git commit -m "Fix Railway database connection issues"
git push origin main

# Railway will auto-deploy
# Check logs after deployment
railway logs --follow
```

## 📞 Need Help?

If the issue persists:
1. Check `/health` endpoint output
2. Share the error logs (remove credentials)
3. Verify DATABASE_URL format
4. Ensure PostgreSQL service is running
5. Check Railway service limits
