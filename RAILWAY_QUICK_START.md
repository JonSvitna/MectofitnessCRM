# Railway Deployment - Quick Start Guide

## 🚀 You Now Have TWO Deployment Options!

### Option 1: Simple Deployment (Existing)
**One Service = Everything Together**

```
┌─────────────────────────────────┐
│   Railway Service (Port 5000)  │
│                                 │
│   Backend (Flask CRM)          │
│   + Frontend (Next.js)         │
│   + PostgreSQL Database        │
└─────────────────────────────────┘
```

**Use:** `railway.toml` (default)

---

### Option 2: Separated Deployment (NEW!) ⭐

**Two Services = Independent Deployment & Scaling**

```
┌──────────────────────────────────────────┐
│         Your Railway Project             │
│                                          │
│  ┌─────────────────┐  ┌──────────────┐  │
│  │   Backend       │  │  Frontend    │  │
│  │   (Flask CRM)   │◄─│  (Next.js)   │  │
│  │   Port: 5000    │  │  Port: 3000  │  │
│  └────────┬────────┘  └──────────────┘  │
│           │                              │
│  ┌────────▼────────┐                    │
│  │   PostgreSQL    │                    │
│  │    Database     │                    │
│  └─────────────────┘                    │
└──────────────────────────────────────────┘
```

**Backend uses:** `railway.backend.toml`
**Frontend uses:** `railway.frontend.toml`

---

## 📋 How to Deploy (Separated Setup)

### Step 1: Create Railway Project
1. Go to https://railway.app
2. Create "New Project"
3. Choose "Deploy from GitHub Repo"
4. Select your repository

### Step 2: Configure Backend Service
The first service Railway creates will be your backend:

1. Rename it to **"Backend"** or **"CRM Backend"**
2. Go to **Settings** → **Advanced**
3. Set **"Railway Config File"** to: `railway.backend.toml`
4. Add PostgreSQL database (click "+ New" → "Database" → "PostgreSQL")

**Required Environment Variables:**
```bash
SECRET_KEY=<generate-random-32-char-hex>
FLASK_ENV=production
```

**For CORS (after frontend is deployed):**
```bash
CORS_ORIGINS=https://your-frontend.railway.app
```

### Step 3: Create Frontend Service
1. In your Railway project, click **"+ New"**
2. Select **"GitHub Repo"**
3. Choose the **SAME repository**
4. Rename to **"Frontend"**
5. Go to **Settings** → **Advanced**
6. Set **"Railway Config File"** to: `railway.frontend.toml`

**Environment Variables (optional):**
```bash
NODE_ENV=production
NEXT_PUBLIC_API_URL=https://your-backend.railway.app
```

### Step 4: Test!
- Backend: `https://your-backend.railway.app/auth/login`
- Frontend: `https://your-frontend.railway.app`

---

## 🎯 When to Use Which Option?

### Use Simple Deployment (Option 1) When:
- ✅ Just getting started
- ✅ Testing the app
- ✅ Cost is a concern (1 service = lower cost)
- ✅ You don't need separate domains

### Use Separated Deployment (Option 2) When:
- ✅ Need independent scaling (scale backend/frontend separately)
- ✅ Want separate domains (api.example.com, www.example.com)
- ✅ Production deployment
- ✅ Following microservices architecture
- ✅ Frontend and backend teams work independently

---

## 💰 Cost Comparison

| Deployment | Services | Estimated Monthly Cost |
|------------|----------|----------------------|
| **Simple** | 1 Web + 1 Database | ~$10-20/month |
| **Separated** | 2 Web + 1 Database | ~$15-30/month |

Both options include Railway's $5 free credit/month.

---

## 🔑 Key Files Reference

| File | Purpose |
|------|---------|
| `railway.toml` | Simple deployment config (default) |
| `railway.backend.toml` | Backend-only config ⭐ NEW |
| `railway.frontend.toml` | Frontend-only config ⭐ NEW |
| `start.sh` | Starts everything (simple deployment) |
| `start-backend.sh` | Starts backend only ⭐ NEW |

---

## 📚 Documentation

**Essential Guides:**
1. **[RAILWAY_SPLIT_DEPLOYMENT.md](docs/deployment/RAILWAY_SPLIT_DEPLOYMENT.md)** - Step-by-step separated deployment
2. **[RAILWAY_CONFIGURATION_REFERENCE.md](docs/deployment/RAILWAY_CONFIGURATION_REFERENCE.md)** - Detailed config explanation
3. **[RAILWAY_README.md](RAILWAY_README.md)** - Quick reference

**Other Docs:**
- [RAILWAY_DEPLOY.md](docs/deployment/RAILWAY_DEPLOY.md) - Original simple deployment guide
- [.env.example](.env.example) - Environment variables reference

---

## 🆘 Common Issues

### "Which railway.toml file is used?"
Railway uses the file you specify in **Settings → Advanced → Railway Config File**.

If not set, it defaults to `railway.toml` (simple deployment).

### "CORS errors in browser console"
Set `CORS_ORIGINS` in your backend service:
```bash
CORS_ORIGINS=https://your-frontend.railway.app
```

### "Build fails"
Check you're using the right config file:
- Backend needs Python dependencies (requirements.txt)
- Frontend needs Node.js dependencies (package.json)

### "Service won't start"
Verify the start command matches your config:
- `railway.backend.toml` → Uses `start-backend.sh`
- `railway.frontend.toml` → Uses `npx serve out`

---

## 🎓 Pro Tips

1. **Custom Domains**: You can add custom domains to each service separately
   - Backend: `api.yourdomain.com`
   - Frontend: `www.yourdomain.com`

2. **Save Costs**: Deploy frontend to Vercel/Netlify (free) and only backend to Railway

3. **Environment Variables**: Use Railway's variable references to link services:
   ```bash
   CORS_ORIGINS=${{Frontend.RAILWAY_PUBLIC_DOMAIN}}
   ```

4. **Rollback**: You can switch between simple and separated deployments by just changing the Railway Config File setting

---

## ✅ Success Checklist

For **Separated Deployment**, verify:

- [ ] Backend service is running
- [ ] PostgreSQL database is connected to backend
- [ ] Backend environment variables are set (SECRET_KEY, FLASK_ENV)
- [ ] Frontend service is running
- [ ] CORS_ORIGINS is set on backend with frontend URL
- [ ] Can access backend at: `https://backend.railway.app/auth/login`
- [ ] Can access frontend at: `https://frontend.railway.app`

---

## 🎉 You're All Set!

Your repository is now configured for both:
- ✅ **Simple deployment** (existing `railway.toml`)
- ✅ **Separated deployment** (new `railway.backend.toml` + `railway.frontend.toml`)

Choose the option that fits your needs and follow the guides above!

**Need help?** Check the comprehensive documentation in `docs/deployment/`.

---

**Built with ❤️ for MectoFitness CRM**
