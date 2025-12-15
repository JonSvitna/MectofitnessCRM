# 🚀 Quick Deploy Guide

## Deploy Frontend to Vercel

```bash
# Option 1: Vercel CLI
vercel --prod

# Option 2: GitHub Integration (Recommended)
# 1. Visit https://vercel.com
# 2. Import repository
# 3. Deploy (auto-configured)
```

**URL**: `https://your-app.vercel.app`

---

## Deploy Backend to Railway

```bash
# Option 1: Web UI (Recommended)
# 1. Visit https://railway.app
# 2. New Project → Deploy from GitHub
# 3. Select repository
# 4. Add PostgreSQL database
# 5. Set env vars:
#    - SECRET_KEY
#    - FLASK_ENV=production
# 6. Deploy

# Option 2: Railway CLI
railway login
railway init
railway up
```

**URL**: `https://your-app.up.railway.app`

---

## Environment Variables

### Vercel (Frontend)
- None required for static site
- Optional: `NEXT_PUBLIC_API_URL` (if connecting to backend)

### Railway (Backend)
- `DATABASE_URL` - Auto-set by Railway PostgreSQL
- `SECRET_KEY` - Flask secret key (**required**)
- `FLASK_ENV` - Set to `production` (**required**)

---

## Local Development

### Run Frontend
```bash
npm install
npm run nextjs:dev
# Visit http://localhost:3000
```

### Run Backend
```bash
pip install -r requirements.txt
npm install
npm run build  # Build React dashboard
python run.py
# Visit http://localhost:5000
```

---

## Build Commands

### Vercel Build (Automated)
```bash
./build-nextjs-vercel.sh
# Output: out/ directory
```

### Railway Build (Automated)
```bash
pip install -r requirements.txt
npm install
npm run build
# Output: app/static/dist/ directory
```

---

## Documentation

- **Complete Guide**: `/DEPLOYMENT.md`
- **Summary**: `/DEPLOYMENT_SUMMARY.md`
- **Status**: `docs/deployment/DEPLOYMENT_STATUS.md`
- **Vercel**: `docs/deployment/VERCEL_DEPLOYMENT.md`
- **Railway**: `docs/deployment/RAILWAY_*.md`

---

## Troubleshooting

**Vercel build fails?**
→ Check `docs/deployment/VERCEL_DEPLOYMENT.md`

**Railway database issues?**
→ Check `docs/deployment/RAILWAY_DB_TROUBLESHOOTING.md`

**General deployment issues?**
→ Check `/DEPLOYMENT.md`

---

## Architecture

```
Frontend (Vercel)          Backend (Railway)
    ↓                           ↓
Next.js Homepage     Flask CRM + React Dashboard
    +                           +
Static Export              PostgreSQL
```

---

**Ready to deploy! 🎉**
