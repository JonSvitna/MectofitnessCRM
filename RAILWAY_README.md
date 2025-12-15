# Railway Deployment - Quick Reference

This repository is configured for **two deployment options** on Railway:

## Option 1: Monolithic Deployment (Default)

Deploy everything together in a single Railway service.

**Configuration file**: `railway.toml`

**Use case**: Simple deployment, testing, or if you don't need separate services.

**Setup**:
1. Create new Railway project from this GitHub repo
2. Add PostgreSQL database
3. Set environment variables (see below)
4. Railway will auto-deploy

## Option 2: Split Deployment (Backend + Frontend Separate)

Deploy backend (Flask CRM) and frontend (Next.js marketing) as separate Railway services.

**Configuration files**: 
- Backend: `railway.backend.toml`
- Frontend: `railway.frontend.toml`

**Use case**: Better scalability, independent deployments, separate domains.

**Setup**: See detailed guide in [`docs/deployment/RAILWAY_SPLIT_DEPLOYMENT.md`](docs/deployment/RAILWAY_SPLIT_DEPLOYMENT.md)

**Quick steps**:
1. Create Railway project
2. Deploy backend service (set Railway config file to `railway.backend.toml`)
3. Add PostgreSQL database to backend
4. Deploy frontend service from same repo (set Railway config file to `railway.frontend.toml`)
5. Configure environment variables for both services
6. Set CORS_ORIGINS on backend to frontend URL

## Environment Variables

### Backend (Flask CRM)

**Required:**
- `DATABASE_URL` - Auto-set by Railway when you add PostgreSQL
- `SECRET_KEY` - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
- `FLASK_ENV` - Set to `production`

**For split deployment:**
- `CORS_ORIGINS` - Set to your frontend URL (e.g., `https://frontend.railway.app`)

### Frontend (Next.js)

**Required (for split deployment only):**
- `NEXT_PUBLIC_API_URL` - Your backend URL (e.g., `https://backend.railway.app`)
- `NODE_ENV` - Set to `production`

## Files Reference

| File | Purpose | Used By |
|------|---------|---------|
| `railway.toml` | Monolithic deployment config | Single service deployment |
| `railway.backend.toml` | Backend-only config | Backend service in split deployment |
| `railway.frontend.toml` | Frontend-only config | Frontend service in split deployment |
| `start.sh` | Monolithic startup script | Single service deployment |
| `start-backend.sh` | Backend-only startup script | Backend service in split deployment |

## Architecture Comparison

### Monolithic (railway.toml)
```
┌─────────────────────────────┐
│    Single Railway Service   │
│                             │
│  ┌─────────────────────┐   │
│  │  Flask Backend      │   │
│  │  + Next.js Frontend │   │
│  │  Port: 5000         │   │
│  └──────────┬──────────┘   │
│             │               │
│  ┌──────────▼──────────┐   │
│  │   PostgreSQL DB     │   │
│  └─────────────────────┘   │
└─────────────────────────────┘
```

### Split (railway.backend.toml + railway.frontend.toml)
```
┌────────────────────────────────────┐
│       Railway Project              │
│                                    │
│  ┌──────────┐    ┌──────────┐    │
│  │ Backend  │    │ Frontend │    │
│  │ (Flask)  │◄───│ (Next.js)│    │
│  │ Port:5000│    │ Port:3000│    │
│  └────┬─────┘    └──────────┘    │
│       │                            │
│  ┌────▼─────┐                     │
│  │PostgreSQL│                     │
│  └──────────┘                     │
└────────────────────────────────────┘
```

## When to Use Each Option

### Use Monolithic When:
- ✅ Getting started / testing
- ✅ Simple deployment needs
- ✅ Cost-conscious (one service = lower cost)
- ✅ Don't need separate scaling

### Use Split When:
- ✅ Need independent deployments
- ✅ Want separate domains (api.example.com, www.example.com)
- ✅ Need to scale frontend/backend independently
- ✅ Following microservices architecture
- ✅ Want to use different deployment strategies

## Switching Between Deployments

### From Monolithic to Split:
1. Follow [RAILWAY_SPLIT_DEPLOYMENT.md](docs/deployment/RAILWAY_SPLIT_DEPLOYMENT.md)
2. Keep existing service as backend (change config to `railway.backend.toml`)
3. Add new frontend service (use `railway.frontend.toml`)
4. Configure CORS and API URLs

### From Split to Monolithic:
1. Keep your backend service
2. Change Railway config file to `railway.toml`
3. Change start command to `./start.sh`
4. Remove or pause frontend service
5. Remove CORS_ORIGINS variable (or set to `*`)

## Documentation

- **Comprehensive Split Deployment Guide**: [`docs/deployment/RAILWAY_SPLIT_DEPLOYMENT.md`](docs/deployment/RAILWAY_SPLIT_DEPLOYMENT.md)
- **Original Railway Guide**: [`docs/deployment/RAILWAY_DEPLOY.md`](docs/deployment/RAILWAY_DEPLOY.md)
- **Environment Variables**: [`.env.example`](.env.example)
- **Main README**: [`README.md`](README.md)

## Quick Deploy Commands

Using Railway CLI (optional):

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# For monolithic deployment
railway up

# For split deployment - backend
railway up --config railway.backend.toml

# For split deployment - frontend (in separate service)
railway up --config railway.frontend.toml
```

## Support

- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **Project Issues**: https://github.com/JonSvitna/MectofitnessCRM/issues

---

**Recommended**: For production deployments, use the **Split Deployment** option for better scalability and maintainability.
