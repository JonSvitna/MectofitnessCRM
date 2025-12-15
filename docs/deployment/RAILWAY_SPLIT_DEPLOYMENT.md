# Railway Split Deployment Guide

This guide explains how to deploy the MectoFitness CRM with **separate Railway services** for the backend (Flask CRM) and frontend (Next.js marketing site).

## Architecture Overview

```
┌─────────────────────────────────────────┐
│          Railway Project                │
│                                         │
│  ┌──────────────┐    ┌──────────────┐  │
│  │   Backend    │    │   Frontend   │  │
│  │  (Flask CRM) │    │  (Next.js)   │  │
│  │              │◄───│              │  │
│  │  Port: 5000  │    │  Port: 3000  │  │
│  └──────┬───────┘    └──────────────┘  │
│         │                               │
│         │                               │
│  ┌──────▼───────┐                       │
│  │  PostgreSQL  │                       │
│  │   Database   │                       │
│  └──────────────┘                       │
│                                         │
└─────────────────────────────────────────┘
```

## Prerequisites

1. Railway account (sign up at https://railway.app)
2. GitHub repository connected to Railway
3. Basic understanding of environment variables

## Deployment Steps

### Part 1: Create Railway Project

1. Go to https://railway.app/dashboard
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `MectofitnessCRM` repository
5. Railway will create an initial service - we'll configure this as the backend

### Part 2: Deploy Backend Service (Flask CRM)

#### Step 1: Configure Backend Service

1. In your Railway project, select the initial service
2. Rename it to **"Backend"** or **"CRM Backend"**
3. Go to **Settings** → **Service Settings**

#### Step 2: Set Build Configuration

In the **Settings** tab:
- **Build Command**: Leave empty (handled by nixpacks)
- **Start Command**: `./start-backend.sh`
- **Root Directory**: `/` (leave as default)
- **Watch Paths**: Leave as default

#### Step 3: Set Railway Config File

In the **Settings** tab, under **Advanced**:
- **Railway Config File**: `railway.backend.toml`

This tells Railway to use the backend-specific configuration.

#### Step 4: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"PostgreSQL"**
3. Railway will automatically create and link the database
4. The `DATABASE_URL` variable will be auto-populated in your backend service

#### Step 5: Configure Environment Variables

Go to **Variables** tab in your backend service and add:

**Required:**
```
SECRET_KEY=<generate-with-command-below>
FLASK_ENV=production
```

Generate SECRET_KEY:
```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

**Optional (for CORS - set to frontend URL):**
```
CORS_ORIGINS=https://your-frontend.railway.app
```

**Optional (for features):**
```
# Calendar Integration
GOOGLE_CALENDAR_CREDENTIALS=<your-credentials>
OUTLOOK_CLIENT_ID=<your-client-id>
OUTLOOK_CLIENT_SECRET=<your-client-secret>

# Communications
TWILIO_ACCOUNT_SID=<your-sid>
TWILIO_AUTH_TOKEN=<your-token>
TWILIO_PHONE_NUMBER=<your-number>
SENDGRID_API_KEY=<your-api-key>

# Payments
STRIPE_PUBLIC_KEY=<your-public-key>
STRIPE_SECRET_KEY=<your-secret-key>

# Video Conferencing
ZOOM_CLIENT_ID=<your-client-id>
ZOOM_CLIENT_SECRET=<your-client-secret>
```

#### Step 6: Deploy Backend

Railway will automatically deploy. Watch the logs for:
- ✅ Python virtual environment setup
- ✅ Dependencies installation
- ✅ Database initialization
- ✅ Gunicorn server start

Your backend API will be available at: `https://your-backend.railway.app`

### Part 3: Deploy Frontend Service (Next.js Marketing Site)

#### Step 1: Add Frontend Service

1. In your Railway project, click **"+ New"**
2. Select **"GitHub Repo"**
3. Choose the **same repository** (`MectofitnessCRM`)
4. Railway will create a second service from the same repo

#### Step 2: Configure Frontend Service

1. Rename the new service to **"Frontend"** or **"Marketing Site"**
2. Go to **Settings** → **Service Settings**

#### Step 3: Set Build Configuration

In the **Settings** tab:
- **Build Command**: `npm run nextjs:build`
- **Start Command**: `npm run nextjs:start`
- **Root Directory**: `/` (leave as default)

#### Step 4: Set Railway Config File

In the **Settings** tab, under **Advanced**:
- **Railway Config File**: `railway.frontend.toml`

This tells Railway to use the frontend-specific configuration.

#### Step 5: Configure Environment Variables

Go to **Variables** tab in your frontend service and add:

**Required:**
```
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
NODE_ENV=production
```

Replace `your-backend.railway.app` with your actual backend URL from Part 2.

**Optional:**
```
# Analytics
NEXT_PUBLIC_GA_ID=<google-analytics-id>

# Any other frontend-specific variables
```

#### Step 6: Deploy Frontend

Railway will automatically deploy. Watch the logs for:
- ✅ Node.js dependencies installation
- ✅ Next.js build
- ✅ Production server start

Your frontend will be available at: `https://your-frontend.railway.app`

### Part 4: Configure CORS (Important!)

Since frontend and backend are on different domains, you need to configure CORS:

1. Go to your **Backend** service in Railway
2. Navigate to **Variables**
3. Update `CORS_ORIGINS` with your frontend URL:
   ```
   CORS_ORIGINS=https://your-frontend.railway.app
   ```
4. For multiple origins (e.g., staging + production), use comma-separated values:
   ```
   CORS_ORIGINS=https://your-frontend.railway.app,https://staging-frontend.railway.app
   ```

The backend is pre-configured to use the `CORS_ORIGINS` environment variable. See `app/__init__.py` for the CORS configuration.

## Configuration Files Reference

### Backend Configuration: `railway.backend.toml`

- Uses Python 3.11 and PostgreSQL
- Installs Python dependencies only
- Runs `start-backend.sh` script
- Excludes frontend build steps

### Frontend Configuration: `railway.frontend.toml`

- Uses Node.js 20
- Installs npm dependencies
- Builds Next.js app
- Runs Next.js production server

## Environment Variables Summary

### Backend Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `DATABASE_URL` | ✅ Yes | PostgreSQL connection (auto-set by Railway) | `postgresql://...` |
| `SECRET_KEY` | ✅ Yes | Flask secret key | `abc123...` |
| `FLASK_ENV` | ✅ Yes | Flask environment | `production` |
| `CORS_ORIGINS` | ⚠️ Recommended | Allowed frontend origins | `https://frontend.railway.app` |
| `PORT` | Auto-set | Server port (Railway sets this) | `5000` |

### Frontend Environment Variables

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | ✅ Yes | Backend API URL | `https://backend.railway.app` |
| `NODE_ENV` | ✅ Yes | Node environment | `production` |
| `PORT` | Auto-set | Server port (Railway sets this) | `3000` |

## Custom Domains (Optional)

### Backend Custom Domain

1. Go to your backend service in Railway
2. Click **Settings** → **Networking**
3. Click **"Generate Domain"** or **"Add Custom Domain"**
4. Follow Railway's instructions for DNS configuration

### Frontend Custom Domain

1. Go to your frontend service in Railway
2. Click **Settings** → **Networking**
3. Click **"Generate Domain"** or **"Add Custom Domain"**
4. Update `NEXT_PUBLIC_API_URL` in frontend if using custom backend domain
5. Update `CORS_ORIGINS` in backend with custom frontend domain

## Monitoring & Logs

### View Backend Logs
1. Select Backend service in Railway
2. Click **"Deployments"** tab
3. Click on the latest deployment
4. View real-time logs

### View Frontend Logs
1. Select Frontend service in Railway
2. Click **"Deployments"** tab
3. Click on the latest deployment
4. View real-time logs

## Troubleshooting

### Backend Issues

**Database Connection Errors:**
- Verify PostgreSQL service is running
- Check `DATABASE_URL` is set correctly
- Ensure database is linked to backend service

**CORS Errors:**
- Update `CORS_ORIGINS` with correct frontend URL
- Restart backend service after changing CORS settings
- Check browser console for specific CORS errors

**Build Failures:**
- Check Python dependencies in `requirements.txt`
- Verify `start-backend.sh` is executable
- Review Railway build logs

### Frontend Issues

**API Connection Errors:**
- Verify `NEXT_PUBLIC_API_URL` is set correctly
- Check backend is running and accessible
- Verify CORS is configured on backend

**Build Failures:**
- Check Node.js dependencies in `package.json`
- Verify Next.js configuration in `next.config.mjs`
- Review Railway build logs

**Deployment Not Starting:**
- Verify `railway.frontend.toml` is selected
- Check start command is correct
- Review logs for errors

## Cost Estimate

Railway pricing (as of 2024):

- **Starter Plan**: $5 free credit/month
- **Backend Service**: ~$5-10/month
- **Frontend Service**: ~$5-10/month  
- **PostgreSQL**: ~$5-10/month
- **Total**: ~$15-30/month for both services

## Rollback Strategy

If you need to rollback to the monolithic deployment:

1. In your main service, change Railway config file to `railway.toml`
2. Update start command to `./start.sh`
3. Remove or disable the separate frontend service
4. Redeploy

## Next Steps

1. ✅ Deploy backend with PostgreSQL
2. ✅ Deploy frontend with correct API URL
3. ✅ Configure CORS between services
4. ✅ Test the application end-to-end
5. ✅ Set up custom domains (optional)
6. ✅ Configure monitoring and alerts
7. ✅ Set up CI/CD with GitHub Actions (optional)

## Support

For Railway-specific issues:
- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway

For MectoFitness CRM issues:
- GitHub Issues: https://github.com/JonSvitna/MectofitnessCRM/issues

---

**Note**: This deployment separates the backend CRM system from the frontend marketing site. The React dashboard (Vite app in `app/static/`) is still served by the backend and doesn't need separate deployment.
