# Deployment Guide - MectoFitness CRM

## Overview

This guide covers deploying MectoFitness CRM with:
- **Frontend**: Vercel (static assets and CDN)
- **Backend**: Render (API and application logic)
- **Database**: PostgreSQL on Render

## Prerequisites

- GitHub account
- Vercel account (free tier available)
- Render account (free tier available)
- Domain name (optional)

## Backend Deployment on Render

### Step 1: Create PostgreSQL Database

1. Log in to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Configure database:
   - **Name**: `mectofitness-db`
   - **Database**: `mectofitness`
   - **User**: `mectofitness_user`
   - **Region**: Choose closest to your users
   - **Plan**: Free (or paid for production)
4. Click "Create Database"
5. Save the **Internal Database URL** (starts with `postgresql://`)

### Step 2: Deploy Backend Application

1. In Render Dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Configure service:
   - **Name**: `mectofitness-api`
   - **Environment**: Python 3
   - **Region**: Same as database
   - **Branch**: `main` or your deployment branch
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn -w 4 -b 0.0.0.0:$PORT run:app`
4. Add environment variables:
   ```
   FLASK_ENV=production
   SECRET_KEY=<generate-strong-random-key>
   DATABASE_URL=<your-postgres-internal-url>
   GOOGLE_CLIENT_ID=<your-google-client-id>
   GOOGLE_CLIENT_SECRET=<your-google-client-secret>
   OUTLOOK_CLIENT_ID=<your-outlook-client-id>
   OUTLOOK_CLIENT_SECRET=<your-outlook-client-secret>
   ```
5. Click "Create Web Service"

### Step 3: Run Database Migrations

1. Once deployed, go to your service's "Shell" tab
2. Run migrations:
   ```bash
   flask db upgrade
   ```
3. Or manually create tables:
   ```bash
   python
   >>> from app import create_app, db
   >>> app = create_app('production')
   >>> with app.app_context():
   >>>     db.create_all()
   ```

## Frontend Deployment on Vercel

### Option 1: Monolithic Deployment (Simpler)

If you want to serve everything from one place, deploy the entire Flask app to Render and skip Vercel.

### Option 2: Separate Frontend/Backend (Advanced)

For better performance and scalability, serve static assets from Vercel CDN:

1. Create a `frontend` directory in your project
2. Move static assets:
   ```bash
   mkdir -p frontend/public
   cp -r app/static/* frontend/public/
   cp -r app/templates frontend/
   ```

3. Create `vercel.json` in frontend directory:
   ```json
   {
     "version": 2,
     "builds": [
       {
         "src": "public/**",
         "use": "@vercel/static"
       }
     ],
     "routes": [
       {
         "src": "/static/(.*)",
         "dest": "/public/$1"
       },
       {
         "src": "/(.*)",
         "dest": "https://your-render-backend.onrender.com/$1"
       }
     ]
   }
   ```

4. Deploy to Vercel:
   ```bash
   cd frontend
   vercel --prod
   ```

## Post-Deployment Configuration

### 1. Update CORS Settings

In `config.py`, update CORS settings for production:

```python
class ProductionConfig(Config):
    CORS_ORIGINS = [
        'https://your-domain.com',
        'https://your-vercel-app.vercel.app'
    ]
```

### 2. Configure OAuth Redirect URLs

Update redirect URLs in:
- **Google Cloud Console**: Add `https://your-domain.com/calendar/google/callback`
- **Azure Portal**: Add `https://your-domain.com/calendar/outlook/callback`

### 3. Set Up Custom Domain (Optional)

**On Render:**
1. Go to service settings → "Custom Domains"
2. Add your domain (e.g., `api.yourdomain.com`)
3. Update DNS records as instructed

**On Vercel:**
1. Go to project settings → "Domains"
2. Add your domain (e.g., `yourdomain.com`)
3. Update DNS records as instructed

### 4. Enable HTTPS

Both Render and Vercel provide automatic HTTPS with Let's Encrypt certificates.

Update `config.py`:
```python
SESSION_COOKIE_SECURE = True  # Requires HTTPS
```

## Environment Variables Reference

### Required for Backend (Render)

```env
# Flask
FLASK_ENV=production
SECRET_KEY=<strong-random-key>

# Database
DATABASE_URL=postgresql://user:pass@host/database

# Google Calendar (Optional)
GOOGLE_CLIENT_ID=<your-client-id>
GOOGLE_CLIENT_SECRET=<your-client-secret>

# Microsoft Outlook (Optional)
OUTLOOK_CLIENT_ID=<your-client-id>
OUTLOOK_CLIENT_SECRET=<your-client-secret>

# Twilio SMS (Optional)
TWILIO_ACCOUNT_SID=<your-account-sid>
TWILIO_AUTH_TOKEN=<your-auth-token>
TWILIO_PHONE_NUMBER=<your-phone-number>

# SendGrid Email (Optional)
SENDGRID_API_KEY=<your-api-key>
SENDGRID_FROM_EMAIL=<your-from-email>
```

## Monitoring and Maintenance

### Health Checks

Render automatically monitors your service. The `/` endpoint serves as health check.

### Logs

View logs in Render Dashboard → Your Service → "Logs"

### Database Backups

- **Free Tier**: No automatic backups
- **Paid Tiers**: Automatic daily backups
- **Manual Backups**: Use `pg_dump` via Render Shell

### Scaling

**Horizontal Scaling:**
- Render: Increase number of web service instances
- Vercel: Automatic CDN scaling

**Vertical Scaling:**
- Upgrade Render plan for more resources
- Upgrade PostgreSQL plan for more storage/connections

## Troubleshooting

### Database Connection Issues

1. Check `DATABASE_URL` is correct
2. Verify database is running
3. Check firewall/security groups
4. Test connection from Render Shell:
   ```bash
   psql $DATABASE_URL
   ```

### Static Files Not Loading

1. Verify paths in templates
2. Check CORS configuration
3. Clear browser cache
4. Check network tab in browser DevTools

### OAuth Failures

1. Verify redirect URLs match exactly
2. Check API credentials are set
3. Ensure HTTPS is enabled for production

### Performance Issues

1. Check database query performance
2. Add database indexes for frequently queried fields
3. Enable caching (Redis)
4. Use CDN for static assets (Vercel)

## Production Checklist

- [ ] Database backups configured
- [ ] HTTPS enabled
- [ ] Environment variables set
- [ ] OAuth redirect URLs updated
- [ ] CORS settings configured
- [ ] Custom domain configured (if applicable)
- [ ] Session cookie secure flag enabled
- [ ] Debug mode disabled
- [ ] Error tracking enabled (e.g., Sentry)
- [ ] Monitoring set up
- [ ] API rate limiting configured
- [ ] Email/SMS integrations tested
- [ ] Database migrations run
- [ ] Admin user created

## Cost Estimates

### Free Tier (Development)
- **Render**: Free web service + free PostgreSQL (limited)
- **Vercel**: Free for personal projects
- **Total**: $0/month

### Production (Recommended)
- **Render**: 
  - Web Service: $7/month (starter)
  - PostgreSQL: $7/month (starter)
- **Vercel**: Free for hobby projects or $20/month for Pro
- **Total**: ~$14-34/month

### Additional Services
- **Twilio SMS**: Pay-as-you-go (~$0.0075 per SMS)
- **SendGrid Email**: Free up to 100 emails/day, then pay-as-you-go

## Support

For deployment issues:
- Render: [Render Documentation](https://render.com/docs)
- Vercel: [Vercel Documentation](https://vercel.com/docs)
- GitHub Issues: Report bugs or request help

---

**Last Updated**: December 2024
