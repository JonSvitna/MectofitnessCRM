# Deployment Overview

Guide to deploying MectoFitness CRM to production.

## Deployment Options

Choose the platform that best fits your needs:

### 🏆 Render (Recommended for Full Features)

**Best for:** Production deployments with all features

**Pros:**
- ✅ All features supported (ML, background workers, large dependencies)
- ✅ Free PostgreSQL database included
- ✅ Background workers for Celery tasks
- ✅ Persistent storage
- ✅ Free tier available
- ✅ Easy setup with Blueprint (`render.yaml`)

**Cons:**
- Slower cold starts on free tier
- Limited resources on free tier

**Guide:** [Render Deployment](render.md)

### 🚂 Railway

**Best for:** Modern deployment with internal networking

**Pros:**
- ✅ All features supported
- ✅ Fast internal networking
- ✅ GitHub integration
- ✅ Simple environment variable management
- ✅ Good free tier ($5/month credit)

**Cons:**
- Requires credit card for free tier
- Can be expensive beyond free tier

**Guide:** [Railway Deployment](railway.md)

### ⚡ Vercel (Frontend Only)

**Best for:** Static frontend deployment (React/Vite build)

**Pros:**
- ✅ Lightning-fast CDN
- ✅ Automatic preview deployments
- ✅ Free tier generous
- ✅ Perfect for static sites

**Cons:**
- ❌ Serverless only (no ML, Celery, Redis)
- ❌ Function size limits
- ❌ Requires external database
- ❌ Not suitable for full backend

**Guide:** [Vercel Deployment](vercel.md)

### 🔀 Split Stack Deployment

**Best for:** Separating frontend and backend for scalability

**Setup:**
- Frontend: Vercel (CDN + static assets)
- Backend: Render or Railway (API + database)

**Pros:**
- ✅ Best performance (CDN for static assets)
- ✅ Scalable architecture
- ✅ Independent deployment

**Cons:**
- More complex setup
- CORS configuration needed
- Multiple deployments to manage

**Guide:** [Split Stack Deployment](split-stack.md)

## Quick Comparison

| Feature | Render | Railway | Vercel | Split Stack |
|---------|--------|---------|--------|-------------|
| All Features | ✅ | ✅ | ❌ | ✅ |
| Free Tier | ✅ | ✅ ($5 credit) | ✅ | ✅ |
| Database Included | ✅ | ✅ | ❌ | ✅ |
| Background Workers | ✅ | ✅ | ❌ | ✅ |
| ML Features | ✅ | ✅ | ❌ | ✅ |
| Setup Complexity | Easy | Easy | Medium | Complex |
| Performance | Good | Good | Excellent (frontend) | Excellent |

## Deployment Architecture

### Monolithic (Render/Railway)

```
┌─────────────────────────┐
│   Render/Railway        │
│  ┌──────────────────┐   │
│  │   Flask App      │   │
│  │   + Static Files │   │
│  └──────────────────┘   │
│  ┌──────────────────┐   │
│  │   PostgreSQL     │   │
│  └──────────────────┘   │
└─────────────────────────┘
```

**Pros:** Simple, all-in-one  
**Cons:** Less scalable

### Split Stack (Vercel + Render)

```
┌──────────────────┐      ┌──────────────────┐
│   Vercel         │      │   Render         │
│  ┌────────────┐  │      │  ┌────────────┐  │
│  │   React    │  │◄────►│  │  Flask API │  │
│  │   Static   │  │ API  │  └────────────┘  │
│  └────────────┘  │      │  ┌────────────┐  │
└──────────────────┘      │  │ PostgreSQL │  │
     CDN                  │  └────────────┘  │
                          └──────────────────┘
```

**Pros:** Better performance, scalable  
**Cons:** More complex, CORS setup

## Pre-Deployment Checklist

Before deploying to any platform, complete these steps:

### 1. Environment Configuration

- [ ] Create production `.env` file with all required variables
- [ ] Generate secure `SECRET_KEY`: `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] Set `FLASK_ENV=production`
- [ ] Configure database connection string

### 2. Database Setup

- [ ] Choose database provider (PostgreSQL recommended)
- [ ] Create production database
- [ ] Run database migrations: `python init_db.py`
- [ ] Set up database backups

### 3. Security

- [ ] Use HTTPS (all platforms provide this automatically)
- [ ] Set `SESSION_COOKIE_SECURE=True`
- [ ] Review CORS settings if using split stack
- [ ] Set up proper authentication
- [ ] Review file upload restrictions

### 4. Dependencies

- [ ] Test all dependencies install: `pip install -r requirements.txt`
- [ ] Build frontend: `npm run build` (if using React)
- [ ] Verify no development dependencies in production

### 5. Testing

- [ ] Test locally with production settings
- [ ] Run database tests: `python test_db.py`
- [ ] Verify setup: `python verify_setup.py`
- [ ] Test all critical user flows

### 6. Monitoring & Logging

- [ ] Set up application logging
- [ ] Configure error tracking (optional: Sentry)
- [ ] Set up uptime monitoring (optional: UptimeRobot)
- [ ] Configure database connection pooling

See the complete [Deployment Checklist](checklist.md) for more details.

## Required Environment Variables

### Essential (All Deployments)

```bash
# Application
SECRET_KEY=your-secret-key-here
FLASK_ENV=production

# Database
DATABASE_URL=postgresql://user:password@host:5432/database
```

### Optional (Feature-Specific)

```bash
# Calendar Integration
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
OUTLOOK_CLIENT_ID=your-outlook-client-id
OUTLOOK_CLIENT_SECRET=your-outlook-client-secret

# Communications
TWILIO_ACCOUNT_SID=your-twilio-sid
TWILIO_AUTH_TOKEN=your-twilio-token
TWILIO_PHONE_NUMBER=your-twilio-number
SENDGRID_API_KEY=your-sendgrid-key

# Payments
STRIPE_PUBLIC_KEY=your-stripe-public-key
STRIPE_SECRET_KEY=your-stripe-secret-key

# Background Jobs (if using Celery)
REDIS_URL=redis://user:password@host:port

# AI Features
OPENAI_API_KEY=your-openai-key
```

## Deployment Steps (General)

### 1. Prepare Application

```bash
# Ensure all tests pass
python test_db.py
python verify_setup.py

# Build frontend (if using React)
npm install
npm run build

# Test production build locally
FLASK_ENV=production python run.py
```

### 2. Choose Platform

Select your deployment platform based on needs:
- **Full features needed?** → Render or Railway
- **Frontend only?** → Vercel
- **Maximum performance?** → Split Stack

### 3. Follow Platform Guide

- [Render Deployment Guide](render.md)
- [Railway Deployment Guide](railway.md)
- [Vercel Deployment Guide](vercel.md)
- [Split Stack Guide](split-stack.md)

### 4. Post-Deployment Verification

After deployment:

```bash
# Check health endpoint
curl https://your-app-url.com/api/v1/health

# Expected response:
{
  "status": "healthy",
  "database": "connected",
  "timestamp": "2025-12-11T..."
}

# Test authentication
# Visit https://your-app-url.com/auth/register
# Create account and login

# Verify core features
# - Client management
# - Session scheduling
# - Program creation
```

## Common Issues

### Database Connection Errors

**Symptoms:** 500 errors, "could not connect to database"

**Solutions:**
1. Verify `DATABASE_URL` is correct
2. Check database is running and accessible
3. For cloud databases, verify IP whitelist
4. Ensure using `postgresql://` not `postgres://`

### Build Failures

**Symptoms:** Deployment fails during build

**Solutions:**
1. Test locally: `pip install -r requirements.txt`
2. Check Python version matches deployment (3.8+)
3. Verify all dependencies are in requirements.txt
4. For Vercel: ensure no ML libraries in requirements

### Static Files Not Loading

**Symptoms:** Styles missing, 404 errors for CSS/JS

**Solutions:**
1. Run `npm run build` before deployment
2. Verify `app/static/dist/` directory exists
3. Check static file routes in application
4. Ensure proper asset paths in templates

### Session/Cookie Issues

**Symptoms:** Users logged out immediately, can't stay logged in

**Solutions:**
1. Set `SESSION_COOKIE_SECURE=True` for HTTPS
2. Configure proper `SECRET_KEY`
3. Check session configuration in `config.py`
4. Verify CORS settings for split stack

## Performance Optimization

### Database

```python
# config.py
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

### Caching (Optional)

Add Redis for session storage and caching:

```bash
pip install redis flask-session
```

### Static Assets

- Use CDN for static files (Vercel, Cloudflare)
- Enable gzip compression
- Set proper cache headers

## Monitoring Production

### Application Logs

**Render:**
```bash
# View logs in dashboard or CLI
render logs
```

**Railway:**
```bash
railway logs
```

### Database Health

Monitor regularly:
```bash
curl https://your-app-url.com/api/v1/health
```

### Uptime Monitoring

Consider services like:
- UptimeRobot (free)
- Pingdom
- StatusCake

### Error Tracking

Consider integrating:
- Sentry (Python errors)
- LogRocket (frontend errors)
- Rollbar

## Backup Strategy

### Database Backups

**Automated (Recommended):**
- Render: Automatic backups on paid plans
- Railway: Automatic backups included
- Manual: Use platform's backup features

**Manual Backup:**
```bash
# PostgreSQL
pg_dump -U user database > backup.sql

# Restore
psql -U user database < backup.sql
```

### File Backups

If storing user uploads:
- Use cloud storage (S3, Cloudinary)
- Implement regular backups
- Test restore procedures

## Scaling Considerations

### Horizontal Scaling

For high traffic:
1. Increase worker count (Gunicorn)
2. Add load balancer
3. Use Redis for session storage
4. Consider background job queue (Celery)

### Vertical Scaling

Upgrade resources:
- More RAM for worker processes
- Faster database instance
- Better CPU for ML features

## Security Best Practices

- [ ] Always use HTTPS
- [ ] Keep dependencies updated
- [ ] Use strong SECRET_KEY
- [ ] Enable CSRF protection
- [ ] Restrict file upload types
- [ ] Set proper CORS headers
- [ ] Use environment variables for secrets
- [ ] Regular security audits
- [ ] Implement rate limiting
- [ ] Use secure session cookies

## Getting Help

If you encounter deployment issues:

1. Check platform-specific guide for your chosen platform
2. Review [deployment checklist](checklist.md)
3. Check application logs for errors
4. Verify all environment variables are set
5. Open an issue on [GitHub](https://github.com/JonSvitna/MectofitnessCRM/issues)

## Next Steps

1. Review [Deployment Checklist](checklist.md)
2. Choose your platform and follow its guide
3. Complete pre-deployment tasks
4. Deploy and test thoroughly
5. Set up monitoring and backups

---

Ready to deploy? Choose your platform and follow the guide! 🚀
