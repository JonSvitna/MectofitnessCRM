# MectoFitness CRM - Deployment Guide

## Architecture Overview

MectoFitness CRM uses a **split-stack deployment architecture**:

```
┌─────────────────────┐         ┌──────────────────────┐
│   Vercel (Frontend) │         │  Railway (Backend)   │
│                     │         │                      │
│  Next.js Marketing  │         │  Flask CRM App       │
│  Homepage (src/)    │         │  + React Dashboard   │
│                     │         │  + PostgreSQL        │
└─────────────────────┘         └──────────────────────┘
   https://your-app            https://your-api
      .vercel.app                 .up.railway.app
```

## What Goes Where

### Vercel (Frontend)
- **Next.js Marketing Homepage** (`/src` directory)
- Modern landing page with:
  - Hero section
  - Features showcase
  - Pricing page
  - FAQ section
  - Fully responsive design

### Railway (Backend)
- **Flask CRM Application** (`/app` directory)
- **React Dashboard** (built with Vite, served by Flask)
- **PostgreSQL Database**
- **API Endpoints**

---

## Deployment Instructions

### Step 1: Deploy Backend to Railway

1. **Connect Repository to Railway**
   ```bash
   # Visit https://railway.app
   # Create new project
   # Connect GitHub repository
   ```

2. **Add PostgreSQL Database**
   - In Railway dashboard, click "New" → "Database" → "PostgreSQL"
   - Railway will automatically set `DATABASE_URL` environment variable

3. **Configure Environment Variables**
   Set these in Railway dashboard:
   ```
   SECRET_KEY=<your-secret-key>
   FLASK_ENV=production
   DATABASE_URL=<automatically-set-by-railway>
   ```

4. **Deploy**
   - Railway will automatically:
     - Install Python dependencies
     - Install Node dependencies
     - Build React dashboard with Vite
     - Start Flask app with Gunicorn
   
   Your backend will be available at: `https://your-app.up.railway.app`

### Step 2: Deploy Frontend to Vercel

1. **Install Vercel CLI** (optional, can use GitHub integration)
   ```bash
   npm install -g vercel
   ```

2. **Deploy via CLI**
   ```bash
   # From repository root
   vercel --prod
   ```
   
   OR

3. **Deploy via GitHub Integration** (Recommended)
   - Visit https://vercel.com
   - Import Git Repository
   - Select your repository
   - Vercel will auto-detect Next.js
   - Click "Deploy"

4. **Configuration**
   Vercel will automatically use:
   - Build Command: `npm run nextjs:build`
   - Output Directory: `out`
   - Framework: Next.js

   Your frontend will be available at: `https://your-app.vercel.app`

---

## Development Workflow

### Running Backend Locally
```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Node dependencies
npm install

# Build React dashboard
npm run build

# Run Flask app
python run.py

# Visit http://localhost:5000
```

### Running Frontend Locally
```bash
# Install dependencies
npm install

# Run Next.js dev server
npm run nextjs:dev

# Visit http://localhost:3000
```

---

## Configuration Files

### Backend (Railway)
- `railway.toml` - Railway configuration
- `nixpacks.toml` - Build configuration
- `start.sh` - Startup script
- `build.sh` - Build script
- `Procfile` - Process definition
- `requirements.txt` - Python dependencies

### Frontend (Vercel)
- `vercel.json` - Vercel configuration
- `.vercelignore` - Files to exclude from deployment
- `next.config.mjs` - Next.js configuration
- `package.json` - Node dependencies (nextjs:* scripts)

---

## Environment Variables

### Railway (Backend)
| Variable | Description | Required |
|----------|-------------|----------|
| `DATABASE_URL` | PostgreSQL connection string | Yes (auto-set) |
| `SECRET_KEY` | Flask secret key for sessions | Yes |
| `FLASK_ENV` | Environment (production/development) | Yes |
| `PORT` | Port to run on | No (defaults to 5000) |

### Vercel (Frontend)
No environment variables required for static Next.js site.

If you need to connect frontend to backend API:
| Variable | Description |
|----------|-------------|
| `NEXT_PUBLIC_API_URL` | Backend API URL (e.g., https://your-api.up.railway.app) |

---

## Troubleshooting

### Backend Issues

**Build fails on Railway:**
- Check Railway logs
- Ensure `requirements.txt` and `package.json` are valid
- Verify Python and Node versions in `nixpacks.toml`

**Database connection fails:**
- Ensure PostgreSQL database is added in Railway
- Check `DATABASE_URL` environment variable is set
- Wait 30-60 seconds after deployment for DB connection

**React dashboard not loading:**
- Ensure `npm run build` completed successfully
- Check `app/static/dist/` directory exists
- Verify Vite build in Railway logs

### Frontend Issues

**Vercel build fails:**
- Ensure `.vercelignore` excludes backend files
- Check Next.js build locally: `npm run nextjs:build`
- Verify `out/` directory is created

**Pages not loading:**
- Check Vercel deployment logs
- Ensure `output: 'export'` in `next.config.mjs`
- Verify static export compatibility

---

## Cost Estimates

### Free Tier
- **Railway**: $5/month (includes 500 execution hours)
- **Vercel**: Free (includes generous bandwidth)
- **PostgreSQL**: Included with Railway

### Production Tier
- **Railway Pro**: $20/month (more resources)
- **Vercel Pro**: $20/month (if needed for team features)

---

## Migration Notes

### Previous Setup (Monolithic)
- Everything deployed together
- Next.js homepage built into Flask static directory
- Complex build scripts to avoid directory conflicts

### Current Setup (Split Stack)
- Frontend and backend deployed separately
- No directory naming conflicts
- Simpler deployment process
- Better performance (CDN for frontend)

### Removed Files
- `build-homepage.sh` - No longer needed
- `run-nextjs-homepage.sh` - No longer needed
- `deploy-vercel.sh` - Replaced by direct Vercel deployment

---

## Additional Resources

- [Railway Documentation](https://docs.railway.app)
- [Vercel Documentation](https://vercel.com/docs)
- [Next.js Static Exports](https://nextjs.org/docs/app/building-your-application/deploying/static-exports)
- [Flask Deployment](https://flask.palletsprojects.com/en/2.3.x/deploying/)

---

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review deployment logs in Railway/Vercel dashboards
3. Refer to platform-specific documentation
4. Open an issue in the repository
