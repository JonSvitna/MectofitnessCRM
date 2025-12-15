# Railway Configuration Reference

Quick reference guide for Railway deployment files and their usage.

## Configuration Files Overview

| File | Purpose | Used For |
|------|---------|----------|
| `railway.toml` | **Monolithic deployment** | Single service with Flask + Next.js together |
| `railway.backend.toml` | **Backend service** | Flask CRM API (separate deployment) |
| `railway.frontend.toml` | **Frontend service** | Next.js marketing site (separate deployment) |
| `start.sh` | Monolithic startup | Builds frontend + starts backend |
| `start-backend.sh` | Backend-only startup | Starts backend without frontend build |
| `Procfile` | Default process | Used by monolithic deployment |
| `Procfile.backend` | Backend process | Alternative for backend service |
| `Procfile.frontend` | Frontend process | Alternative for frontend service |
| `.railwayignore` | Deployment exclusions | Excludes docs, tests, etc. from builds |

## Deployment Options Comparison

### Option 1: Monolithic Deployment

**Files needed:**
- `railway.toml` (main config)
- `start.sh` (startup script)
- `Procfile` (optional)

**How to deploy:**
1. Create Railway project from GitHub repo
2. Add PostgreSQL database
3. Deploy automatically (Railway uses `railway.toml` by default)

**Pros:**
- ✅ Simple setup
- ✅ Single service (lower cost)
- ✅ No CORS configuration needed
- ✅ Easier to manage

**Cons:**
- ❌ Cannot scale frontend/backend independently
- ❌ Single domain for both services
- ❌ Frontend build included in backend startup time

### Option 2: Split Deployment (Backend + Frontend)

**Files needed for Backend:**
- `railway.backend.toml` (backend config)
- `start-backend.sh` (backend startup)
- `Procfile.backend` (optional)

**Files needed for Frontend:**
- `railway.frontend.toml` (frontend config)
- `Procfile.frontend` (optional)
- `next.config.mjs` (Next.js config)

**How to deploy:**
1. Create Railway project
2. Deploy backend service:
   - Set "Railway Config File" to `railway.backend.toml`
   - Add PostgreSQL database
3. Deploy frontend service:
   - Create new service from same repo
   - Set "Railway Config File" to `railway.frontend.toml`
4. Configure CORS between services

**Pros:**
- ✅ Independent scaling
- ✅ Separate domains (api.example.com, www.example.com)
- ✅ Independent deployments
- ✅ Better for microservices architecture
- ✅ Frontend doesn't wait for backend build

**Cons:**
- ❌ More complex setup
- ❌ Two services (higher cost)
- ❌ CORS configuration required
- ❌ More environment variables to manage

## Railway Config File Settings

### Backend Service Settings

**In Railway Dashboard → Settings → Advanced:**
```
Railway Config File: railway.backend.toml
```

**Or override with:**
```
Start Command: ./start-backend.sh
Build Command: (leave empty)
```

### Frontend Service Settings

**In Railway Dashboard → Settings → Advanced:**
```
Railway Config File: railway.frontend.toml
```

**Or override with:**
```
Start Command: npx serve out -l $PORT
Build Command: npm run nextjs:build
```

## Environment Variables by Service

### Backend Service

| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `DATABASE_URL` | ✅ Yes | `postgresql://...` | Auto-set by Railway |
| `SECRET_KEY` | ✅ Yes | `abc123...` | Generate random string |
| `FLASK_ENV` | ✅ Yes | `production` | Set environment |
| `PORT` | Auto | `5000` | Railway sets this |
| `CORS_ORIGINS` | Recommended | `https://frontend.railway.app` | For split deployment |
| `OPENAI_API_KEY` | Optional | `sk-...` | For AI features |
| `STRIPE_SECRET_KEY` | Optional | `sk_...` | For payments |
| `ZOOM_CLIENT_ID` | Optional | `...` | For video calls |

### Frontend Service

| Variable | Required | Example | Notes |
|----------|----------|---------|-------|
| `NODE_ENV` | ✅ Yes | `production` | Set environment |
| `PORT` | Auto | `3000` | Railway sets this |
| `NEXT_PUBLIC_API_URL` | Optional | `https://backend.railway.app` | If frontend needs API |

## Nixpacks Configuration

### Backend (`railway.backend.toml`)

```toml
[nixpacks]
nixPkgs = ["python311", "postgresql"]  # Python + PostgreSQL client
```

- Installs Python 3.11
- Installs PostgreSQL client libraries
- Installs Python dependencies from `requirements.txt`
- Does NOT install Node.js or build frontend

### Frontend (`railway.frontend.toml`)

```toml
[nixpacks]
nixPkgs = ["nodejs_20"]  # Node.js only
```

- Installs Node.js 20
- Installs npm dependencies from `package.json`
- Builds Next.js app
- Does NOT install Python

### Monolithic (`railway.toml`)

```toml
[nixpacks]
nixPkgs = ["python311", "nodejs_20", "postgresql"]  # Everything
```

- Installs Python 3.11, Node.js 20, and PostgreSQL
- Installs both Python and npm dependencies
- Builds frontend and starts backend

## Start Commands Explained

### Monolithic: `./start.sh`
```bash
# 1. Activates Python venv
# 2. Checks environment variables
# 3. Builds React frontend (npm run build)
# 4. Initializes database
# 5. Starts Gunicorn server
```

### Backend Only: `./start-backend.sh`
```bash
# 1. Activates Python venv
# 2. Checks environment variables
# 3. Skips frontend build ← KEY DIFFERENCE
# 4. Initializes database
# 5. Starts Gunicorn server
```

### Frontend: `npx serve out -l $PORT`
```bash
# Serves static files from 'out/' directory
# Created by Next.js static export (npm run nextjs:build)
# Simple HTTP server, no Node.js server rendering
```

## Build Commands Explained

### Backend
```bash
# No build command needed
# Python doesn't require compilation
# Dependencies installed during install phase
```

### Frontend
```bash
npm run nextjs:build
# Runs: next build
# Creates static export in 'out/' directory
# All HTML/CSS/JS pre-generated
```

### Monolithic
```bash
npm run build
# Runs: vite build
# Builds React dashboard for CRM
# Outputs to app/static/dist/
```

## Port Configuration

Railway automatically sets the `PORT` environment variable:

- **Backend**: Gunicorn binds to `$PORT` (default: 5000)
- **Frontend**: Serve binds to `$PORT` (default: 3000)
- **Monolithic**: Gunicorn binds to `$PORT` (default: 5000)

All services must listen on `0.0.0.0:$PORT` to be accessible.

## Database Connection

Only the **backend** needs database access:

```
Backend Service → PostgreSQL Database
```

The frontend is a static site and doesn't connect to the database directly.

## CORS Configuration

When using split deployment:

**Backend must allow frontend origin:**
```bash
# In Backend Service environment variables
CORS_ORIGINS=https://your-frontend.railway.app
```

**Backend CORS config (already in code):**
```python
# app/__init__.py
CORS(app, resources={
    r"/api/*": {
        "origins": cors_origins,  # From CORS_ORIGINS env var
        "methods": ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})
```

## Troubleshooting

### "Which railway.toml is used?"

Railway uses the file specified in:
**Settings → Advanced → Railway Config File**

If not set, it defaults to `railway.toml`.

### "Build fails with missing dependencies"

Check which config file is being used:
- Backend config only installs Python dependencies
- Frontend config only installs Node dependencies
- Monolithic config installs both

### "Service won't start"

Check the start command matches your config:
- `railway.backend.toml` → `./start-backend.sh`
- `railway.frontend.toml` → `npx serve out -l $PORT`
- `railway.toml` → `./start.sh`

### "CORS errors in browser"

1. Check `CORS_ORIGINS` is set on backend
2. Verify frontend URL is correct
3. Check browser console for actual error
4. Test with `curl -H "Origin: https://frontend.railway.app" https://backend.railway.app/api/health`

## Cost Optimization

### Monolithic Deployment
- 1 Web Service: ~$5-10/month
- 1 PostgreSQL: ~$5-10/month
- **Total: ~$10-20/month**

### Split Deployment
- 1 Backend Service: ~$5-10/month
- 1 Frontend Service: ~$5-10/month
- 1 PostgreSQL: ~$5-10/month
- **Total: ~$15-30/month**

**Tip**: Frontend static sites can be deployed to Vercel/Netlify for free, and only deploy backend to Railway to save costs.

## Quick Commands

```bash
# Test backend locally
python run.py

# Test frontend locally
npm run nextjs:dev

# Build frontend locally
npm run nextjs:build

# Serve frontend locally
npx serve out

# Check Python syntax
python -m py_compile run.py

# Check bash syntax
bash -n start-backend.sh

# Generate secret key
python -c "import secrets; print(secrets.token_hex(32))"
```

## See Also

- [Comprehensive Split Deployment Guide](RAILWAY_SPLIT_DEPLOYMENT.md)
- [Quick Reference](../../RAILWAY_README.md)
- [Original Railway Guide](RAILWAY_DEPLOY.md)
- [Railway Documentation](https://docs.railway.app)
