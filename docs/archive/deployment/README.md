# Archived Deployment Documentation

This directory contains deployment documentation that has been archived as part of the transition to the split-stack deployment architecture (Vercel + Railway).

## Why These Were Archived

These documents were archived on December 15, 2024, when the project moved to a cleaner split-stack deployment:
- **Frontend (Next.js)** → Vercel
- **Backend (Flask CRM)** → Railway

## Archived Documents

### Outdated Deployment Approaches
- `DEPLOYMENT.md` - Old monolithic deployment guide (replaced by `/DEPLOYMENT.md`)
- `DEPLOYMENT_GUIDE.md` - General deployment guide (consolidated into `/DEPLOYMENT.md`)
- `DEPLOY_RENDER.md` - Render-specific deployment (not primary deployment target)
- `RENDER_DEPLOYMENT.md` - Another Render deployment guide (not primary deployment target)
- `FRONTEND_DEPLOY.md` - Old frontend deployment approach (serving Next.js from Flask)
- `DEPLOY_SPLIT_STACK.md` - Earlier split-stack approach (different architecture)
- `DEPLOYMENT_CHECKLIST.md` - Old deployment checklist (superseded by new docs)

## Current Deployment Documentation

For current deployment instructions, see:
- **Primary Guide**: `/DEPLOYMENT.md` - Complete split-stack deployment guide
- **Status & Quick Start**: `../deployment/DEPLOYMENT_STATUS.md`
- **Vercel Details**: `../deployment/VERCEL_DEPLOYMENT.md`
- **Railway Details**: `../deployment/RAILWAY_*.md` files

## Historical Context

These documents represent various deployment strategies that were tested:
1. **Monolithic deployment** - Everything deployed together to Render/Railway
2. **CDN optimization** - Using Vercel for static assets while keeping backend on Render
3. **Split-stack evolution** - Various approaches to separating concerns

The current architecture simplifies deployment by:
- Deploying Next.js marketing site independently to Vercel
- Deploying Flask CRM + React dashboard to Railway
- Eliminating complex build scripts that managed directory conflicts
- Using platform-native deployment configurations

## Reference Value

These documents are kept for:
- Historical reference
- Understanding evolution of deployment strategy
- Potential future deployment to Render or other platforms
- Troubleshooting legacy deployment issues

---

**Note**: If you need to deploy to Render or use a different architecture, these documents may provide useful starting points, but they will need to be updated to match the current codebase structure.
