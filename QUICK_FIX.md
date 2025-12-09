# 🚨 QUICK FIX: Stop Using trolley.proxy.rlwy.net

## The Problem
You're using: `trolley.proxy.rlwy.net` (unstable public proxy)
You need: `postgres.railway.internal` (stable private network)

## The Solution (2 minutes)

### Step 1: Go to Railway Dashboard
https://railway.app/dashboard

### Step 2: Click Your PostgreSQL Database Service
(The one with the database icon, NOT your Flask app)

### Step 3: Copy the PRIVATE URL
Look for a variable called:
- `DATABASE_PRIVATE_URL` or
- `POSTGRES_PRIVATE_URL`

It will look like:
```
postgresql://postgres:YOUR_PASSWORD@postgres.railway.internal:5432/railway
```

### Step 4: Click Your Web Service (Flask App)
(The one running your Python backend)

### Step 5: Go to Variables Tab
Click "+ New Variable" or edit existing `DATABASE_URL`

### Step 6: Add This Variable
```
Name: DATABASE_URL
Value: ${{Postgres.DATABASE_PRIVATE_URL}}
```

**OR** paste the full private URL you copied:
```
Name: DATABASE_URL
Value: postgresql://postgres:YOUR_PASSWORD@postgres.railway.internal:5432/railway
```

### Step 7: Save & Wait
- Click "Add" or "Update"
- Railway will redeploy (takes 2-3 minutes)
- Watch the logs for "Database connection successful"

## Verify It Worked

1. Check logs for: `postgres.railway.internal` (not `trolley.proxy.rlwy.net`)
2. Visit: `https://your-app.railway.app/health`
3. Should return: `{"status": "healthy", "database": "connected"}`

## Why This Fixes It

| What You're Using Now | What You Need |
|----------------------|---------------|
| `trolley.proxy.rlwy.net` | `postgres.railway.internal` |
| Public internet proxy | Private Railway network |
| Unstable, times out | Stable, fast |
| External connection | Internal connection |
| ❌ Keeps failing | ✅ Works reliably |

## Still Failing?

If you still see `trolley.proxy.rlwy.net` in logs after this change:
1. The environment variable didn't update
2. Service didn't restart
3. Try manual restart: Railway dashboard → Service → "Restart"

## Need the Exact Steps?

1. Railway dashboard: https://railway.app/dashboard
2. Find your project
3. You should see TWO services:
   - One is PostgreSQL (database icon)
   - One is Web Service (your Flask app)
4. Click PostgreSQL → Variables → Copy `DATABASE_PRIVATE_URL`
5. Click Web Service → Variables → Set `DATABASE_URL` = value from step 4
6. Save
7. Done!
