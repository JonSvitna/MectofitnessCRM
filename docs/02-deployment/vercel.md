# Vercel Deployment Guide for MectoFitness CRM

## Issues Fixed

1. **Created `api/index.py`** - Vercel entry point for the Flask application
2. **Updated `vercel.json`** - Proper routing and build configuration
3. **Created `requirements-vercel.txt`** - Lighter dependencies without ML libraries that exceed Vercel limits
4. **Created `.vercelignore`** - Exclude unnecessary files from deployment

## Important Limitations

⚠️ **Vercel Serverless Functions have size constraints** (50MB limit). Your full `requirements.txt` includes:
- `scikit-learn`, `pandas`, `numpy` - Heavy ML libraries
- `celery`, `redis` - Require persistent workers
- `boto3` - Large AWS SDK

These have been **removed from `requirements-vercel.txt`** to make deployment possible.

## Deployment Steps

### Option 1: Deploy to Vercel (Recommended for frontend-heavy apps)

1. **Install Vercel CLI** (if not already installed):
   ```bash
   npm install -g vercel
   ```

2. **Set Environment Variables in Vercel Dashboard**:
   - `SECRET_KEY` - Your Flask secret key
   - `DATABASE_URL` - PostgreSQL connection string (use Vercel Postgres or external DB)
   - `GOOGLE_CALENDAR_CREDENTIALS` - Base64 encoded credentials
   - `OUTLOOK_CLIENT_ID`, `OUTLOOK_CLIENT_SECRET`
   - `TWILIO_ACCOUNT_SID`, `TWILIO_AUTH_TOKEN`, `TWILIO_PHONE_NUMBER`
   - `SENDGRID_API_KEY`
   - `STRIPE_PUBLIC_KEY`, `STRIPE_SECRET_KEY`

3. **Deploy**:
   ```bash
   vercel --prod
   ```

### Option 2: Deploy to Railway/Render (Better for full-stack with ML)

If you need the ML features (client churn prediction, etc.), consider:

**Railway**: Supports larger deployments with full requirements
```bash
# Install Railway CLI
npm install -g @railway/cli

# Deploy
railway login
railway init
railway up
```

**Render**: Free tier available, supports background workers
- Create a new Web Service
- Connect your GitHub repo
- Build Command: `pip install -r requirements.txt && npm run build`
- Start Command: `gunicorn run:app`

## Database Setup

Vercel doesn't provide a persistent file system. You **must** use an external database:

1. **Vercel Postgres** (recommended): Add in Vercel dashboard
2. **Supabase** (free tier): https://supabase.com
3. **PlanetScale** (free tier): https://planetscale.com
4. **ElephantSQL** (free tier): https://www.elephantsql.com

Update `DATABASE_URL` environment variable with the connection string.

## Frontend Build

The Vite build will run automatically during deployment. Ensure:
- `node_modules` are gitignored
- `package.json` has correct build script
- Static files are served from `/app/static/dist/`

## Troubleshooting

### "Function size exceeded"
- Use `requirements-vercel.txt` instead of `requirements.txt`
- Remove unused dependencies

### "Module not found"
- Check that all imports in `api/index.py` work
- Verify Python version (3.9-3.11 supported by Vercel)

### Database connection issues
- Ensure `DATABASE_URL` is set in Vercel environment variables
- Use `postgresql://` not `postgres://` (SQLAlchemy requirement)

### Static files not loading
- Check routes in `vercel.json`
- Verify build output location matches routes
- Run `npm run build` locally to test

## Testing Locally

```bash
# Install dependencies
pip install -r requirements-vercel.txt
npm install

# Build frontend
npm run build

# Run with Vercel dev server
vercel dev
```

## Alternative: Keep Full Features

If you need all features (ML, Celery workers, etc.), Vercel is not ideal. Deploy to:
- **Railway** - $5/month, supports all features
- **Render** - Free tier available, supports workers
- **Heroku** - Classic choice for Python apps
- **DigitalOcean App Platform** - $5/month

These platforms support:
- Persistent storage
- Background workers (Celery)
- Larger dependencies (ML libraries)
- Long-running processes (Redis)
