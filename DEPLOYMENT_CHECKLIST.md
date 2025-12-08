# Vercel Deployment Checklist

## ✅ Pre-Deployment Checklist

- [ ] Install Vercel CLI: `npm install -g vercel`
- [ ] Build frontend locally to test: `npm run build`
- [ ] Verify `api/index.py` exists
- [ ] Check `vercel.json` configuration
- [ ] Review `requirements-vercel.txt` (no ML libraries)

## 🗄️ Database Setup (REQUIRED)

Vercel is serverless - you MUST use an external database:

- [ ] Choose a database provider:
  - [ ] Vercel Postgres (easiest, $0.25/GB)
  - [ ] Supabase (free tier available)
  - [ ] PlanetScale (free tier available)
  - [ ] ElephantSQL (free tier available)

- [ ] Get your `DATABASE_URL` connection string
- [ ] Add to Vercel environment variables

## 🔐 Environment Variables

Set these in Vercel Dashboard (Settings → Environment Variables):

### Required:
- [ ] `SECRET_KEY` - Generate with `python -c "import secrets; print(secrets.token_hex(32))"`
- [ ] `DATABASE_URL` - PostgreSQL connection string

### Optional (based on features you need):
- [ ] `GOOGLE_CALENDAR_CREDENTIALS` - For Google Calendar sync
- [ ] `OUTLOOK_CLIENT_ID` - For Outlook Calendar sync
- [ ] `OUTLOOK_CLIENT_SECRET`
- [ ] `TWILIO_ACCOUNT_SID` - For SMS
- [ ] `TWILIO_AUTH_TOKEN`
- [ ] `TWILIO_PHONE_NUMBER`
- [ ] `SENDGRID_API_KEY` - For email
- [ ] `STRIPE_PUBLIC_KEY` - For payments
- [ ] `STRIPE_SECRET_KEY`

## 🚀 Deploy

### First Time:

```bash
vercel
```

Follow the prompts:
- Set up and deploy? **Yes**
- Which scope? Choose your account
- Link to existing project? **No**
- What's your project's name? **mectofitness-crm**
- In which directory is your code? **./**
- Want to override settings? **No**

### Subsequent Deploys:

```bash
vercel --prod
```

## 🧪 Testing After Deployment

1. [ ] Visit your Vercel URL
2. [ ] Test login/registration
3. [ ] Check database connections
4. [ ] Verify static assets load
5. [ ] Test API endpoints

## ⚠️ Known Limitations on Vercel

❌ **Not Available** (due to serverless/size limits):
- ML features (client churn prediction)
- Celery background workers
- Redis caching
- Large file uploads (>4.5MB)

✅ **Available**:
- All CRUD operations
- Calendar sync (Google/Outlook)
- Email/SMS notifications
- Payment processing
- Client management
- Session tracking
- Program management

## 🔧 Troubleshooting

### Build Fails:

```bash
# Test locally
vercel dev

# Check logs
vercel logs [deployment-url]
```

### "Function too large":
- Verify using `requirements-vercel.txt`
- Check `.vercelignore` excludes unnecessary files
- Remove any unused dependencies

### Database Connection Error:
- Ensure `DATABASE_URL` starts with `postgresql://` not `postgres://`
- Test connection string locally
- Check database allows connections from Vercel IPs

### Static Files 404:
- Run `npm run build` locally
- Check `app/static/dist/` directory exists
- Verify routes in `vercel.json`

## 🎯 Alternative: Full Feature Deployment

If you need ALL features (ML, Celery, Redis), deploy to:

**Railway** (Recommended):
```bash
npm install -g @railway/cli
railway login
railway init
railway up
```

**Render**:
- Visit https://render.com
- Connect GitHub repo
- Create Web Service
- Use full `requirements.txt`

## 📚 Resources

- [Vercel Python Documentation](https://vercel.com/docs/functions/serverless-functions/runtimes/python)
- [Flask on Vercel](https://vercel.com/guides/using-flask-with-vercel)
- [Vercel Environment Variables](https://vercel.com/docs/concepts/projects/environment-variables)
