# Render Deployment Guide for MectoFitness CRM

## Why Render?

✅ **All features supported** - ML libraries, Celery workers, Redis, large dependencies
✅ **PostgreSQL included** - Free managed database
✅ **Background workers** - Perfect for Celery tasks
✅ **Persistent storage** - Unlike serverless platforms
✅ **Free tier available** - Great for testing

## Deployment Options

### Option 1: Blueprint Deployment (Recommended - Easiest)

This uses the `render.yaml` file to automatically set up everything.

1. **Push your code to GitHub** (if not already done)

2. **Go to Render Dashboard**
   - Visit: https://dashboard.render.com
   - Sign up/Login with GitHub

3. **Create New Blueprint**
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Render will automatically detect `render.yaml`
   - Click "Apply"

4. **Wait for deployment** (5-10 minutes)
   - Database will be created automatically
   - Environment variables will be set
   - App will build and deploy

### Option 2: Manual Deployment

1. **Create PostgreSQL Database**
   - Dashboard → "New +" → "PostgreSQL"
   - Name: `mectofitness-db`
   - Plan: Free
   - Copy the "Internal Database URL"

2. **Create Web Service**
   - Dashboard → "New +" → "Web Service"
   - Connect your repository
   - Configure:
     - **Name**: `mectofitness-crm`
     - **Region**: Choose closest to your users
     - **Branch**: `main`
     - **Root Directory**: Leave blank
     - **Runtime**: Python 3
     - **Build Command**: `pip install -r requirements.txt && npm install && npm run build`
     - **Start Command**: `gunicorn run:app`
     - **Plan**: Free (or Starter for better performance)

3. **Set Environment Variables**
   - In the web service settings, add:
     - `DATABASE_URL`: Paste the database URL from step 1
     - `SECRET_KEY`: Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
     - `FLASK_ENV`: `production`
     - Add other optional variables (see below)

4. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete

## Environment Variables

### Required:
- `SECRET_KEY` - Flask secret (auto-generated in blueprint)
- `DATABASE_URL` - PostgreSQL connection (auto-set from database)
- `FLASK_ENV` - Set to `production`

### Optional (Feature-specific):

#### Calendar Integration:
- `GOOGLE_CALENDAR_CREDENTIALS` - Base64 encoded JSON credentials
- `OUTLOOK_CLIENT_ID`
- `OUTLOOK_CLIENT_SECRET`

#### Communications:
- `TWILIO_ACCOUNT_SID`
- `TWILIO_AUTH_TOKEN`
- `TWILIO_PHONE_NUMBER`
- `SENDGRID_API_KEY`

#### Payments:
- `STRIPE_PUBLIC_KEY`
- `STRIPE_SECRET_KEY`

#### Background Jobs (if using Celery):
- `REDIS_URL` - Redis connection string

## Adding Background Workers (Celery)

If you need background jobs (automated emails, scheduled tasks):

1. **Uncomment Redis and Worker sections in `render.yaml`**

2. **Or manually create**:
   - Create Redis instance: "New +" → "Redis"
   - Create Worker: "New +" → "Background Worker"
     - Build Command: `pip install -r requirements.txt`
     - Start Command: `celery -A app.celery worker --loglevel=info`
     - Add same environment variables as web service
     - Add `REDIS_URL` from Redis instance

## Database Migrations

After first deployment:

```bash
# Install Render CLI
npm install -g render-cli

# Login
render login

# Connect to your service shell
render shell <your-service-name>

# Run migrations
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
```

Or use Render Shell in the dashboard:
- Go to your service → "Shell" tab
- Run migration commands directly

## Monitoring & Logs

- **Logs**: Service page → "Logs" tab
- **Metrics**: Service page → "Metrics" tab (CPU, memory, requests)
- **Health Checks**: Automatic at `/` endpoint
- **Alerts**: Configure in service settings

## Custom Domain

1. Go to service settings → "Custom Domain"
2. Add your domain
3. Update DNS records as shown
4. SSL certificate auto-generated

## Scaling

### Vertical Scaling (More Power):
- Free: 512MB RAM, 0.1 CPU
- Starter ($7/mo): 512MB RAM, 0.5 CPU
- Standard ($25/mo): 2GB RAM, 1 CPU
- Pro ($85/mo): 4GB RAM, 2 CPU

### Horizontal Scaling:
- Add more instances in service settings
- Load balancing automatic

## Performance Optimization

1. **Enable Redis Caching**
   - Uncomment Redis in `render.yaml`
   - Configure in Flask app

2. **Use CDN for Static Files**
   - Deploy `app/static/dist` to Vercel/Netlify
   - Update asset URLs

3. **Database Connection Pooling**
   - Already configured in SQLAlchemy

4. **Gunicorn Workers**
   - Adjust in start command: `gunicorn run:app --workers 4`

## Cost Estimate

### Free Tier:
- Web Service: Free (spins down after 15 min inactivity)
- PostgreSQL: Free (90 days, then $7/mo)
- Redis: $1/mo
- **Total: Free for 90 days, then ~$8/mo**

### Production Tier:
- Web Service Starter: $7/mo
- PostgreSQL Starter: $7/mo
- Redis Starter: $1/mo
- Worker (optional): $7/mo
- **Total: $15-22/mo**

## Troubleshooting

### Build Fails:
```bash
# Check requirements.txt has all dependencies
# Verify Python version in render.yaml
# Check build logs in Render dashboard
```

### Database Connection Error:
```bash
# Verify DATABASE_URL is set
# Check database is running
# Ensure URL uses postgresql:// (auto-handled in config.py)
```

### Static Files Not Loading:
```bash
# Verify npm build runs in Build Command
# Check app/static/dist exists after build
# Review Flask static file configuration
```

### App Times Out:
```bash
# Increase gunicorn timeout
# Start command: gunicorn run:app --timeout 120
# Check for slow database queries
```

## Vercel Frontend (Optional)

Since backend is on Render, you can serve the frontend from Vercel for better performance:

1. **Update `vercel.json`** - Already configured to proxy API calls to Render
2. **Replace `your-render-backend.onrender.com`** with your actual Render URL
3. **Deploy to Vercel**: `vercel --prod`
4. **Benefits**: 
   - Global CDN for static assets
   - Faster page loads worldwide
   - Separate frontend/backend scaling

## Migration from Other Platforms

### From Heroku:
- Export `DATABASE_URL` and other env vars
- Use same Procfile format (Render auto-detects)
- Import database using `pg_dump`/`pg_restore`

### From Railway:
- Similar configuration
- Export environment variables
- Point domain to new Render URL

## Backup & Recovery

1. **Automatic Backups** (Paid plans):
   - Daily snapshots
   - Point-in-time recovery

2. **Manual Backup**:
```bash
# Download database dump
pg_dump $DATABASE_URL > backup.sql

# Restore
psql $DATABASE_URL < backup.sql
```

## CI/CD

Render automatically deploys on git push:
- Push to `main` branch → Auto-deploy
- Configure deploy hooks in settings
- Add deploy notifications (Slack, email)

## Security

✅ **Included**:
- Automatic SSL certificates
- DDoS protection
- Private networking between services
- Environment variable encryption

✅ **Recommended**:
- Enable 2FA on Render account
- Rotate `SECRET_KEY` regularly
- Use strong database passwords
- Keep dependencies updated

## Support

- **Render Docs**: https://render.com/docs
- **Community**: https://community.render.com
- **Status**: https://status.render.com

## Next Steps

1. ✅ Push code to GitHub
2. ✅ Sign up for Render
3. ✅ Deploy using Blueprint (render.yaml)
4. ✅ Set environment variables
5. ✅ Run database migrations
6. ✅ Test your application
7. ✅ (Optional) Point custom domain
8. ✅ (Optional) Deploy frontend to Vercel

Your app will be live at: `https://mectofitness-crm.onrender.com`
