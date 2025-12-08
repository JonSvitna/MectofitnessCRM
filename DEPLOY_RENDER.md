# Quick Start: Deploy to Render

## 1. Push to GitHub

```bash
git add .
git commit -m "Configure for Render deployment"
git push origin main
```

## 2. Deploy to Render

### Option A: Blueprint (Fastest - 1 click)

1. Go to https://dashboard.render.com
2. Click "New +" → "Blueprint"
3. Connect your GitHub repository: `JonSvitna/MectofitnessCRM`
4. Click "Apply Blueprint"
5. Wait 5-10 minutes for deployment

✅ Done! Your app will be at: `https://mectofitness-api.onrender.com`

### Option B: Manual Setup

1. **Create Database**:
   - New + → PostgreSQL
   - Name: `mectofitness-db`
   - Click "Create Database"

2. **Create Web Service**:
   - New + → Web Service
   - Connect repository
   - Configure:
     - Name: `mectofitness-api`
     - Build: `pip install -r requirements.txt && npm install && npm run build`
     - Start: `gunicorn run:app --workers 4 --timeout 120`
   - Add Environment Variables:
     - `DATABASE_URL` → Link to database
     - `FLASK_ENV` → `production`
     - `SECRET_KEY` → Generate a random string
   - Click "Create Web Service"

## 3. Run Database Migrations

After deployment completes:

1. Go to your service → "Shell" tab
2. Run:
```bash
flask db upgrade
# or if not using migrations:
python -c "from run import app, db; app.app_context().push(); db.create_all()"
```

## 4. Test Your App

Visit: `https://mectofitness-api.onrender.com`

## 5. (Optional) Use Vercel for Frontend

Since backend is on Render, use Vercel for faster frontend delivery:

1. **Update vercel.json** - Change `your-render-backend.onrender.com` to your actual Render URL
2. **Deploy**: `vercel --prod`
3. **Result**: Frontend on Vercel CDN, backend on Render

## Environment Variables to Add

### Required:
- ✅ `SECRET_KEY` (auto-generated)
- ✅ `DATABASE_URL` (auto-linked)
- ✅ `FLASK_ENV=production`

### Optional (add as needed):

**Calendar Sync:**
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

**Background Jobs:**
- `REDIS_URL` (if using Celery)

## Troubleshooting

**Build fails?**
- Check logs in Render dashboard
- Verify requirements.txt is up to date

**Can't connect to database?**
- Ensure DATABASE_URL is linked
- Check database is running

**App crashes on startup?**
- Check logs for errors
- Verify all required env vars are set

## Costs

- **Free Tier**: Free for 90 days (web service spins down after 15 min inactivity)
- **Starter**: $7/mo web + $7/mo database = **$14/mo** (recommended for production)

## Next Steps

- [ ] Deploy to Render
- [ ] Run database migrations
- [ ] Add environment variables
- [ ] Test application
- [ ] (Optional) Connect custom domain
- [ ] (Optional) Deploy frontend to Vercel

📚 Full guide: See `RENDER_DEPLOYMENT.md`
