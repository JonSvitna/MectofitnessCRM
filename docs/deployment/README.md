# Deployment Documentation

This directory contains deployment-specific documentation for MectoFitness CRM.

## Quick Start

📖 **Start here**: [`/DEPLOYMENT.md`](../../DEPLOYMENT.md) - Complete deployment guide for the split-stack architecture

## Current Architecture

MectoFitness CRM uses a **split-stack deployment**:
- **Frontend (Next.js)** → Vercel
- **Backend (Flask CRM + React Dashboard)** → Railway

## Documentation Index

### Getting Started
- **[DEPLOYMENT_STATUS.md](DEPLOYMENT_STATUS.md)** - Current deployment status and quick start guide

### Platform-Specific Guides

#### Vercel (Frontend)
- **[VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)** - Deploy Next.js marketing homepage to Vercel

#### Railway (Backend)
- **[RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)** - Quick Railway deployment guide
- **[RAILWAY_SETUP.md](RAILWAY_SETUP.md)** - Detailed Railway setup instructions
- **[RAILWAY_WEB_SERVICE_SETUP.md](RAILWAY_WEB_SERVICE_SETUP.md)** - Railway web service configuration
- **[RAILWAY_DB_FIX.md](RAILWAY_DB_FIX.md)** - Database connection troubleshooting
- **[RAILWAY_DB_TROUBLESHOOTING.md](RAILWAY_DB_TROUBLESHOOTING.md)** - Advanced database troubleshooting

## Deployment Flow

```
┌─────────────────────┐         ┌──────────────────────┐
│   Vercel (Frontend) │         │  Railway (Backend)   │
│                     │         │                      │
│  Next.js Marketing  │         │  Flask CRM App       │
│  Homepage (src/)    │         │  + React Dashboard   │
│                     │         │  + PostgreSQL        │
└─────────────────────┘         └──────────────────────┘
```

### Deploy Frontend to Vercel
```bash
# Option 1: CLI
vercel --prod

# Option 2: GitHub Integration (recommended)
# Connect repository at vercel.com
```

### Deploy Backend to Railway
```bash
# Option 1: Web UI (recommended)
# Visit railway.app and connect GitHub repo

# Option 2: CLI
railway login
railway up
```

## Environment Variables

### Vercel (Frontend)
- None required for static site
- Optional: `NEXT_PUBLIC_API_URL` if connecting to backend API

### Railway (Backend)
- `DATABASE_URL` - Auto-set by Railway PostgreSQL
- `SECRET_KEY` - Flask secret key (required)
- `FLASK_ENV` - Set to `production`

## Configuration Files

### Root Directory
- `/vercel.json` - Vercel deployment configuration
- `/railway.toml` - Railway deployment configuration
- `/nixpacks.toml` - Railway build configuration
- `/build-nextjs-vercel.sh` - Vercel build script
- `/build.sh` - Railway build script
- `/start.sh` - Railway startup script

### Exclusion Files
- `/.vercelignore` - Excludes backend from Vercel deployment
- `/.gitignore` - Excludes build artifacts from git

## Troubleshooting

- **Vercel build fails**: Check [VERCEL_DEPLOYMENT.md](VERCEL_DEPLOYMENT.md)
- **Railway database issues**: Check [RAILWAY_DB_TROUBLESHOOTING.md](RAILWAY_DB_TROUBLESHOOTING.md)
- **Railway deployment fails**: Check [RAILWAY_DEPLOY.md](RAILWAY_DEPLOY.md)

## Archived Documentation

Older deployment guides have been moved to [`../archive/deployment/`](../archive/deployment/) for reference. These include:
- Render deployment guides
- Monolithic deployment approaches
- Earlier split-stack iterations

See [`../archive/deployment/README.md`](../archive/deployment/README.md) for details.

## Support

For deployment issues:
1. Check the troubleshooting sections in platform-specific guides
2. Review platform logs (Vercel dashboard or Railway dashboard)
3. Refer to platform documentation:
   - [Vercel Docs](https://vercel.com/docs)
   - [Railway Docs](https://docs.railway.app)
