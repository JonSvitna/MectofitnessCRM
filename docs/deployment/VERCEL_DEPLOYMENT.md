# Vercel Deployment Guide for MectoFitness CRM

## Overview

This guide covers deploying the **Next.js marketing homepage** (in `/src` directory) to Vercel.

⚠️ **Important:** Vercel is used **ONLY for the Next.js frontend**. The Flask backend should be deployed to Railway (see `../../DEPLOYMENT.md`).

## Quick Start

### Option 1: GitHub Integration (Recommended)

1. Visit https://vercel.com and sign in with GitHub
2. Click "Add New" → "Project"
3. Import your repository
4. Vercel will auto-detect Next.js configuration
5. Click "Deploy"

### Option 2: Vercel CLI

```bash
npm install -g vercel
vercel --prod
```

## Configuration

The repository is pre-configured for Vercel deployment:

- ✅ `vercel.json` - Deployment configuration
- ✅ `.vercelignore` - Excludes backend files
- ✅ `next.config.mjs` - Next.js static export settings
- ✅ `/src` directory - Next.js app with App Router

## Environment Variables

For a static Next.js site, no environment variables are required.

If you need to connect to your backend API, set:

| Variable | Description | Example |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `https://your-api.up.railway.app` |

Add these in the Vercel dashboard under Project Settings → Environment Variables.

## What Gets Deployed

- **Source**: `/src` directory (Next.js 14 App Router)
- **Build Command**: `npm run nextjs:build`
- **Output**: `/out` directory (static HTML/CSS/JS)
- **Excluded**: All backend files (Flask, Python, database)

## Troubleshooting

### Build Fails

**Test locally first:**
```bash
npm install
npm run nextjs:build
```

Check if `/out` directory is created with static files.

### Pages Not Loading

1. Check Vercel deployment logs
2. Verify `output: 'export'` is set in `next.config.mjs`
3. Ensure all pages are compatible with static export (no server-side features)

### 404 Errors

- Verify `trailingSlash: true` in `next.config.mjs`
- Check that all routes have corresponding files in `/src/app`

### Images Not Loading

- Ensure `images.unoptimized: true` in `next.config.mjs`
- Use standard `<img>` tags or Next.js Image with `unoptimized` prop

## Testing Locally

```bash
# Install dependencies
npm install

# Run Next.js dev server
npm run nextjs:dev

# Visit http://localhost:3000
```

To test production build:
```bash
npm run nextjs:build
npx serve out
```

## Backend Deployment

**Important:** The Flask CRM backend should be deployed separately to Railway.

See the main [DEPLOYMENT.md](../../DEPLOYMENT.md) for complete instructions on deploying both frontend and backend.

## Benefits of Split-Stack Deployment

✅ **Frontend (Vercel)**
- Global CDN for fast loading worldwide
- Automatic HTTPS and SSL
- Free tier with generous limits
- Automatic deployments on push

✅ **Backend (Railway)**
- Full Flask CRM features
- PostgreSQL database
- No size constraints
- Background workers support

This architecture provides the best of both worlds: fast static content delivery and powerful backend capabilities.
