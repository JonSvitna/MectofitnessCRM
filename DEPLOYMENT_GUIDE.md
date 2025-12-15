# MectoFitness Railway Deployment Guide

Complete guide for deploying MectoFitness CRM to Railway with three separate services.

## 📋 Prerequisites

- Railway account (sign up at https://railway.app)
- GitHub repository with the code
- Basic understanding of environment variables

## 🏗️ Architecture Overview

```
┌─────────────────┐
│   Frontend      │ ← https://your-frontend.railway.app
│   (Static)      │
└────────┬────────┘
         │
         │ HTTP Requests
         ↓
┌─────────────────┐     ┌──────────────┐
│   Backend API   │ ←──→│  PostgreSQL  │
│   (Flask)       │     │  Database    │
└─────────────────┘     └──────────────┘
https://your-backend.railway.app
```

## 🚀 Deployment Steps

### Step 1: Create Railway Project

1. Log in to [Railway](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Authorize Railway to access your repository
5. Select the `MectofitnessCRM` repository

### Step 2: Deploy PostgreSQL Database

1. In your Railway project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway will automatically provision a PostgreSQL instance
4. Note: The `DATABASE_URL` will be automatically set

**PostgreSQL Configuration:**
- Railway automatically provides:
  - `DATABASE_URL` (private connection string)
  - `DATABASE_PUBLIC_URL` (public connection string)
  - Host, port, username, password, database name

### Step 3: Deploy Backend Service

1. Click "+ New" → "GitHub Repo"
2. Select your repository
3. Configure the service:

**Settings:**
- **Name**: `mectofitness-backend`
- **Root Directory**: `backend/`
- **Build Command**: Detected automatically from `railway.toml`
- **Start Command**: `gunicorn -c gunicorn_config.py run:app`

**Environment Variables:**

Click "Variables" and add:

```env
FLASK_ENV=production
SECRET_KEY=<generate-a-strong-random-key>
CORS_ORIGINS=<will-add-after-frontend-deployment>
```

**Generate SECRET_KEY:**
```python
python -c "import secrets; print(secrets.token_hex(32))"
```

**Connect to Database:**
Railway will automatically inject these variables:
- `DATABASE_URL` (use this)
- `DATABASE_PUBLIC_URL`

The backend `config.py` is already configured to use `DATABASE_URL`.

4. Click "Deploy"
5. Wait for deployment to complete
6. Note your backend URL: `https://mectofitness-backend.up.railway.app` (example)

### Step 4: Deploy Frontend Service

1. Click "+ New" → "GitHub Repo"
2. Select your repository again (yes, same repo)
3. Configure the service:

**Settings:**
- **Name**: `mectofitness-frontend`
- **Root Directory**: `frontend/`
- **Build Command**: `npm install && npm run build`
- **Start Command**: `npx serve -s dist -p $PORT`

**Environment Variables:**

Click "Variables" and add:

```env
VITE_API_URL=https://your-backend-url.up.railway.app/api
```

Replace `your-backend-url` with the actual URL from Step 3.

4. Click "Deploy"
5. Wait for deployment to complete
6. Note your frontend URL: `https://mectofitness-frontend.up.railway.app` (example)

### Step 5: Update Backend CORS

1. Go to your backend service
2. Click "Variables"
3. Update `CORS_ORIGINS`:

```env
CORS_ORIGINS=https://your-frontend-url.up.railway.app
```

Replace with your actual frontend URL from Step 4.

4. Click "Redeploy" or wait for automatic redeploy

### Step 6: Verify Deployment

1. **Test Backend Health:**
   ```bash
   curl https://your-backend-url.up.railway.app/health
   ```
   Should return: `{"status": "healthy", "service": "MectoFitness API"}`

2. **Test Frontend:**
   - Open `https://your-frontend-url.up.railway.app` in browser
   - You should see the landing page
   - Fill out the signup form
   - Check backend logs for lead creation

3. **Test API Integration:**
   - Submit the form on the frontend
   - You should see "Thank you! We'll be in touch soon."
   - Check backend service logs in Railway dashboard

## 🔧 Configuration Details

### Frontend Configuration

**package.json:**
- Dependencies are installed automatically
- Build creates production-optimized bundle

**vite.config.js:**
- Configured for production builds
- Minification enabled

**Environment Variables:**
- `VITE_API_URL` - Backend API URL (required)

### Backend Configuration

**requirements.txt:**
- All dependencies listed
- Railway installs automatically

**gunicorn_config.py:**
- Workers: `(CPU_COUNT * 2) + 1`
- Timeout: 120 seconds
- Binds to `0.0.0.0:$PORT`

**Environment Variables:**
- `DATABASE_URL` - Auto-injected by Railway
- `FLASK_ENV` - Set to `production`
- `SECRET_KEY` - Strong random key
- `CORS_ORIGINS` - Frontend URL
- `PORT` - Auto-injected by Railway

### Database Configuration

**PostgreSQL Settings:**
- Version: Latest stable (14+)
- Storage: Starts at 1GB (auto-scales)
- Backups: Automatic daily backups

**Connection:**
- The backend automatically uses `DATABASE_URL`
- SQLAlchemy handles connection pooling
- `pool_pre_ping=True` ensures stale connections are recycled

## 🔒 Security Checklist

- [ ] `SECRET_KEY` is strong and random
- [ ] `CORS_ORIGINS` is set to specific frontend URL (not `*`)
- [ ] `FLASK_ENV` is set to `production`
- [ ] Database uses strong password (auto-generated by Railway)
- [ ] Environment variables are not committed to git
- [ ] HTTPS is enabled (automatic on Railway)

## 📊 Monitoring

### Railway Dashboard

1. **Metrics:** CPU, Memory, Network usage
2. **Logs:** Real-time logs for each service
3. **Deployments:** History of all deployments

### Health Checks

**Backend:**
```bash
curl https://your-backend-url.railway.app/health
```

**Database:**
- Check Railway dashboard for database metrics
- Connection count, storage usage, etc.

## 🐛 Troubleshooting

### Frontend Issues

**Build Fails:**
```bash
# Check that package.json is valid
# Verify node version (use Node 18+)
# Check build logs in Railway dashboard
```

**Can't Connect to API:**
```bash
# Verify VITE_API_URL is set correctly
# Check CORS_ORIGINS on backend matches frontend URL
# Test API endpoint directly with curl
```

### Backend Issues

**Database Connection Failed:**
```bash
# Check DATABASE_URL is set
# Verify PostgreSQL service is running
# Check connection pool settings in config.py
```

**CORS Errors:**
```bash
# Verify CORS_ORIGINS includes frontend URL
# Check for trailing slashes in URLs
# Ensure preflight requests are handled
```

**500 Errors:**
```bash
# Check backend logs in Railway
# Verify all environment variables are set
# Test with curl to see detailed error
```

### Database Issues

**Connection Pool Exhausted:**
```python
# Increase pool_size in config.py
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 20,  # Increase from 10
    'pool_recycle': 3600,
}
```

**Migrations Not Applied:**
```bash
# SSH into backend service (if Railway supports it)
# Or add migration command to start script
flask db upgrade
```

## 📈 Scaling

### Vertical Scaling

Railway automatically scales resources, but you can also:

1. **Backend Service:**
   - Increase worker count in `gunicorn_config.py`
   - Add more memory/CPU via Railway settings

2. **Database:**
   - Railway auto-scales storage
   - Can upgrade to larger instance if needed

### Horizontal Scaling

For high traffic:

1. **Backend:**
   - Deploy multiple backend instances
   - Use Railway's load balancer

2. **Frontend:**
   - Railway's CDN handles this automatically
   - Static files are cached globally

## 💰 Cost Estimates

Railway pricing (as of 2024):

- **Hobby Plan** (Free):
  - $5 credit/month
  - Good for testing
  
- **Developer Plan** ($5/month):
  - $5 credit + $0.000231/GB-hour
  - Suitable for small deployments

- **Team Plan** ($20/month):
  - $10 credit/month
  - Better for production

**Estimated Monthly Cost:**
- Frontend: ~$2-5
- Backend: ~$5-10
- PostgreSQL: ~$5-10
- **Total: ~$12-25/month**

## 🔄 CI/CD

Railway automatically redeploys when you push to GitHub:

1. Push to repository
2. Railway detects changes
3. Builds and deploys automatically
4. Zero-downtime deployment

**Deployment Triggers:**
- Push to main/production branch
- Manual deploy via Railway dashboard
- API trigger (advanced)

## 📝 Custom Domains

### Add Custom Domain

1. Go to service settings in Railway
2. Click "Settings" → "Networking"
3. Click "Generate Domain" or "Custom Domain"
4. Follow DNS configuration instructions

**Example:**
- Frontend: `app.mectofitness.com`
- Backend: `api.mectofitness.com`

## 🆘 Support Resources

- Railway Docs: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- GitHub Issues: Your repository
- Railway Status: https://status.railway.app

## ✅ Post-Deployment Checklist

- [ ] All three services deployed successfully
- [ ] Frontend loads without errors
- [ ] Backend health check passes
- [ ] Database connection successful
- [ ] Form submission creates lead in database
- [ ] CORS configured correctly
- [ ] Environment variables set properly
- [ ] Logs show no errors
- [ ] Custom domains configured (if applicable)
- [ ] Monitoring enabled
- [ ] Backups verified

## 🎉 Success!

Your MectoFitness CRM is now deployed on Railway!

- Frontend: https://your-frontend.up.railway.app
- Backend: https://your-backend.up.railway.app/api
- Database: PostgreSQL (private)

Next steps: See [ROADMAP.md](./ROADMAP.md) for future development milestones.
