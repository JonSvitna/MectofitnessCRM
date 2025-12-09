# Railway Deployment Guide

## Quick Deploy to Railway

### Step 1: Sign Up & Create Project
1. Go to https://railway.app
2. Sign in with GitHub
3. Click "New Project"
4. Select "Deploy from GitHub repo"
5. Choose `JonSvitna/MectofitnessCRM`

### Step 2: Add PostgreSQL Database
1. In your project, click "+ New"
2. Select "Database" → "PostgreSQL"
3. Railway will create a database automatically

### Step 3: Configure Environment Variables
Railway auto-detects most settings, but add these:

**Required:**
- `SECRET_KEY` - Generate with: `python -c "import secrets; print(secrets.token_hex(32))"`
- `DATABASE_URL` - Auto-populated by Railway from your Postgres service

**Railway will automatically set:**
- `PORT` - Railway assigns this
- `PYTHONUNBUFFERED=1`
- `FLASK_ENV=production`

### Step 4: Deploy
Railway automatically deploys! Watch the logs for:
- ✅ Installing Python dependencies
- ✅ Installing npm packages
- ✅ Building frontend with Vite
- ✅ Starting Gunicorn server

Your app will be live at: `https://your-app.up.railway.app`

## What's Configured

✅ `railway.json` - Railway configuration
✅ `railway.toml` - Alternative Railway config
✅ `requirements.txt` - Python dependencies
✅ `package.json` - Frontend build
✅ Auto-deploys on git push

## Railway Features

- ✅ **$5 free credit/month** (starter allowance)
- ✅ **PostgreSQL included** (pay-as-you-go)
- ✅ **No cold starts** (always running)
- ✅ **Auto SSL/HTTPS**
- ✅ **Automatic deploys** from GitHub
- ✅ **Built-in metrics** and logs
- ✅ **Easy scaling**

## Cost Estimate

Railway charges based on usage:
- **Starter plan**: $5 credit/month (free)
- **Web service**: ~$5-10/month (depends on usage)
- **PostgreSQL**: ~$5-10/month (depends on storage)
- **Total**: Usually $5-15/month for small apps

## Quick Commands

```bash
# Install Railway CLI (optional)
npm install -g @railway/cli

# Login
railway login

# Link to project
railway link

# Deploy manually
railway up

# View logs
railway logs

# Open in browser
railway open
```

## Database Migrations

After first deployment, run migrations:

1. Go to Railway dashboard
2. Select your web service
3. Click "Settings" → "Variables"
4. Make sure `DATABASE_URL` is set
5. Your app auto-runs migrations on startup (if configured)

Or use Railway CLI:
```bash
railway run flask db upgrade
```

## Environment Variables (Optional)

Add these in Railway dashboard for additional features:

**Calendar Integration:**
- `GOOGLE_CALENDAR_CREDENTIALS`
- `OUTLOOK_CLIENT_ID`
- `OUTLOOK_CLIENT_SECRET`

**Communications:**
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `SENDGRID_API_KEY`

**Payments:**
- `STRIPE_PUBLIC_KEY`
- `STRIPE_SECRET_KEY`

## Troubleshooting

### Build Fails
- Check logs in Railway dashboard
- Verify `requirements.txt` and `package.json` are valid
- Ensure Python 3.11+ compatibility

### App Won't Start
- Check that `DATABASE_URL` is set
- Verify `SECRET_KEY` is configured
- Check Gunicorn logs

### Database Connection Issues
- Ensure PostgreSQL service is running
- Verify `DATABASE_URL` format: `postgresql://...`
- Check database variables are linked

## Next Steps

1. ✅ Deploy to Railway
2. ✅ Add PostgreSQL database
3. ✅ Configure environment variables
4. ✅ Test your app
5. ✅ Set up custom domain (optional)

---

**Railway Dashboard:** https://railway.app/dashboard
**Docs:** https://docs.railway.app
