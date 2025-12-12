# Railway Database Connection Setup

## ⚠️ Issue: `trolley.proxy.rlwy.net` Connection Failures

The `trolley.proxy.rlwy.net` URL is Railway's **public proxy** for database access. Connection issues are common because:
- External network instability
- Proxy server timeouts
- SSL handshake issues

## ✅ Solution: Use PRIVATE URL (Internal Railway Network)

### Step 1: Check Your Railway Project Structure

You should have **TWO services**:
1. **PostgreSQL Database** (the database service)
2. **Web Service** (your Flask app)

### Step 2: Configure Database Connection in Web Service

Go to your **Web Service** (Flask app) → **Variables** tab:

#### Option A: Use Reference Variables (BEST)
```bash
DATABASE_URL=${{Postgres.DATABASE_PRIVATE_URL}}
```
This automatically uses Railway's internal network (`postgres.railway.internal`)

#### Option B: Copy Private URL
```bash
DATABASE_URL=postgresql://postgres:PASSWORD@postgres.railway.internal:5432/railway
```

#### Option C: Use Public URL (Only if external access needed)
```bash
DATABASE_URL=postgresql://postgres:PASSWORD@trolley.proxy.rlwy.net:PORT/railway
```

### Step 3: Where to Find These URLs

1. Go to **Railway Dashboard**
2. Click on your **PostgreSQL** service
3. Go to **Variables** tab or **Connect** tab
4. You'll see:
   - `DATABASE_URL` - Public URL (external)
   - `DATABASE_PRIVATE_URL` - Private URL (internal) ⭐ **USE THIS**
   - `DATABASE_PUBLIC_URL` - Public URL (external)

### Step 4: Update Your Web Service

1. Click your **Web Service** (Flask app)
2. Go to **Variables** tab
3. Add or update:
   ```
   DATABASE_URL=${{Postgres.DATABASE_PRIVATE_URL}}
   ```
4. Click **Save**
5. Railway will automatically redeploy

### Step 5: Verify Connection

After redeployment:
1. Check logs: `railway logs`
2. Look for: "Database connection successful"
3. Visit: `https://your-app.railway.app/health`

Should return:
```json
{
  "status": "healthy",
  "database": "connected"
}
```

## 🔍 Troubleshooting

### How to Check Which URL You're Using

```bash
# In Railway Shell or logs
railway run printenv DATABASE_URL
```

### If Still Using `trolley.proxy.rlwy.net`:

**Problem**: Your DATABASE_URL is using the public proxy
**Solution**: Change to private URL in Railway Variables

### If Using `postgres.railway.internal`:

**Problem**: Might be DNS resolution issue
**Solution**: Railway should handle this automatically, check service status

### Common Mistakes:

❌ **Don't hardcode** the URL in your code
❌ **Don't use** `DATABASE_PUBLIC_URL` unless you need external access
❌ **Don't commit** database credentials to git

✅ **Do use** Railway variable references: `${{Postgres.DATABASE_PRIVATE_URL}}`
✅ **Do use** environment variables
✅ **Do restart** service after changing variables

## 📊 Connection Performance Comparison

| URL Type | Network | Speed | Stability | Use Case |
|----------|---------|-------|-----------|----------|
| `postgres.railway.internal` | Private | ⚡ Fast | 🟢 Stable | Production (recommended) |
| `trolley.proxy.rlwy.net` | Public | 🐢 Slow | 🟡 Unstable | External tools only |

## 🚀 Quick Fix Commands

### Check current configuration:
```bash
railway variables
```

### Set to private URL:
```bash
railway variables set DATABASE_URL=\${{Postgres.DATABASE_PRIVATE_URL}}
```

### Restart service:
```bash
railway up
```

### View logs:
```bash
railway logs --follow
```

## 🔐 Security Note

The private URL (`postgres.railway.internal`) is:
- Only accessible within Railway's internal network
- More secure (not exposed to internet)
- Faster (no proxy overhead)
- More stable (no external network issues)

## 📞 Still Having Issues?

1. ✅ Verify PostgreSQL service is running
2. ✅ Check both services are in same Railway project
3. ✅ Ensure DATABASE_URL uses `${{Postgres.DATABASE_PRIVATE_URL}}`
4. ✅ Restart web service after variable changes
5. ✅ Check logs for connection errors
6. ✅ Visit `/health` endpoint to verify

If issue persists, the problem might be:
- PostgreSQL service crashed
- Wrong database credentials
- Network configuration issue in Railway project

Contact Railway support: https://discord.gg/railway
