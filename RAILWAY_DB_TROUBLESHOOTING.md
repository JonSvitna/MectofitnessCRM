# Railway Database Connection Troubleshooting Guide

## Common Issue: "server closed the connection unexpectedly"

This error occurs when PostgreSQL connections are closed by Railway's infrastructure before SQLAlchemy expects. This guide helps you resolve and prevent this issue.

## Quick Fix Checklist

### 1. Verify Database is Running
```bash
# In Railway dashboard:
# 1. Go to your PostgreSQL service
# 2. Check it's running (green status)
# 3. Verify DATABASE_URL is populated
```

### 2. Check Environment Variables
Ensure these are set in Railway:
- `DATABASE_URL` - Auto-populated by Railway from PostgreSQL service
- `DATABASE_PUBLIC_URL` - Alternative public connection string (optional)
- `SECRET_KEY` - Required for Flask sessions

### 3. Verify Connection String Format
Railway provides: `postgres://user:pass@host:port/db`
Should be: `postgresql://user:pass@host:port/db`

Our config.py automatically converts this, but double-check if issues persist.

## What We've Fixed

### Connection Pool Configuration (config.py)
```python
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 5,              # Maintain 5 connections
    'pool_recycle': 300,         # Recycle after 5 min (Railway timeout)
    'pool_pre_ping': True,       # Test before use (catches stale connections)
    'pool_timeout': 30,          # Wait 30s for connection from pool
    'max_overflow': 10,          # Up to 10 extra connections
    'connect_args': {
        'connect_timeout': 10,   # 10s to establish connection
        'keepalives': 1,         # Enable TCP keepalive
        'keepalives_idle': 30,   # Start keepalive after 30s idle
        'keepalives_interval': 10,  # Send probe every 10s
        'keepalives_count': 5,   # 5 probes before giving up
    }
}
```

**Key Features:**
- `pool_pre_ping`: Tests connections before using them (prevents stale connection errors)
- `pool_recycle`: Recycles connections before Railway closes them (300s = 5 minutes)
- `keepalives`: Keeps connections alive during idle periods
- `connect_timeout`: Fails fast if database is unreachable

### Retry Logic with Exponential Backoff
- Initial retry: 2 seconds
- Second retry: 4 seconds
- Third retry: 8 seconds
- Fourth retry: 16 seconds
- Fifth retry: 32 seconds

This gives Railway time to establish connections during high load or network issues.

### Connection Pool Disposal
On connection failures, we now:
1. Dispose of the entire connection pool
2. Force creation of fresh connections on retry
3. Prevent accumulation of stale connections

## Testing Your Connection

### 1. Health Check Endpoint
```bash
curl https://your-app.railway.app/api/v1/health
```

Response when healthy:
```json
{
  "status": "healthy",
  "database": "connected",
  "response_time_ms": 45.23,
  "user_count": 5,
  "timestamp": "2025-12-09T10:50:27.039Z"
}
```

### 2. Manual Connection Test
```bash
# SSH into Railway (if using CLI)
railway shell

# Test connection
python3 -c "
from app import create_app, db
app = create_app('production')
with app.app_context():
    with db.engine.connect() as conn:
        result = conn.execute(db.text('SELECT version()'))
        print(result.fetchone())
"
```

### 3. Check Database Logs
In Railway dashboard:
1. Select PostgreSQL service
2. Click "View Logs"
3. Look for connection errors or timeouts

## Common Issues & Solutions

### Issue 1: "Could not connect to server"
**Cause:** PostgreSQL service not accessible
**Solution:**
1. Restart PostgreSQL service in Railway
2. Verify DATABASE_URL is set correctly
3. Check Railway service status page

### Issue 2: "Connection timeout"
**Cause:** Network latency or Railway infrastructure issues
**Solution:**
1. Increase `connect_timeout` in config.py (already set to 10s)
2. Check Railway status: https://railway.app/status
3. Consider using DATABASE_PUBLIC_URL for better routing

### Issue 3: "Too many connections"
**Cause:** Connection pool exhausted
**Solution:**
1. Reduce `pool_size` in config.py (currently 5)
2. Reduce `max_overflow` (currently 10)
3. Check for connection leaks in your code

### Issue 4: "SSL connection has been closed unexpectedly"
**Cause:** Railway's SSL configuration
**Solution:**
1. Add `sslmode=require` to DATABASE_URL
2. Verify SSL certificates are valid
3. Check Railway's SSL documentation

## Performance Optimization

### Connection Pool Sizing
Current settings:
- `pool_size=5`: Good for small apps (1-100 concurrent users)
- `max_overflow=10`: Allows spikes up to 15 connections

Adjust based on your traffic:
- Small app (<100 users): pool_size=5, max_overflow=10
- Medium app (100-1000 users): pool_size=10, max_overflow=20
- Large app (>1000 users): pool_size=20, max_overflow=30

### Pool Recycle Timing
Railway typically closes idle connections after ~5 minutes (300s).
Our `pool_recycle=300` matches this to prevent stale connections.

If you still see issues, try:
- `pool_recycle=240` (4 minutes) - More aggressive
- `pool_recycle=180` (3 minutes) - Very aggressive

## Monitoring in Production

### 1. Enable Query Logging (Development Only)
```python
# In config.py (DevelopmentConfig only)
SQLALCHEMY_ECHO = True  # Logs all SQL queries
```

### 2. Track Connection Pool Stats
```python
from app import db

# Get pool status
pool = db.engine.pool
print(f"Pool size: {pool.size()}")
print(f"Checked out: {pool.checked_out_connections}")
print(f"Overflow: {pool.overflow()}")
```

### 3. Monitor Health Endpoint
Set up monitoring (e.g., UptimeRobot) to ping:
```
https://your-app.railway.app/api/v1/health
```

Alert if:
- Response time > 1000ms
- Status != 200
- Database != "connected"

## Alternative: Fallback to SQLite

If PostgreSQL issues persist, you can temporarily use SQLite for development:

```python
# In .env
DATABASE_URL=sqlite:///mectofitness.db
# Comment out or remove DATABASE_URL for SQLite default
```

**Note:** This is for development only. Production should always use PostgreSQL.

## When to Contact Railway Support

Contact Railway support if:
1. Database is showing as "Running" but connections fail consistently
2. Connection issues persist after trying all troubleshooting steps
3. You see errors in PostgreSQL logs that seem infrastructure-related
4. Response times from Railway's proxy are extremely slow (>5 seconds)

## Additional Resources

- [Railway PostgreSQL Documentation](https://docs.railway.app/databases/postgresql)
- [SQLAlchemy Connection Pooling](https://docs.sqlalchemy.org/en/20/core/pooling.html)
- [Railway Status Page](https://railway.app/status)
- [PostgreSQL Connection Management](https://www.postgresql.org/docs/current/runtime-config-connection.html)

## Summary

The improvements made to this application:
1. ✅ Connection pool pre-ping (detects stale connections)
2. ✅ Aggressive connection recycling (prevents Railway timeouts)
3. ✅ TCP keepalives (maintains connection health)
4. ✅ Exponential backoff retry (handles transient failures)
5. ✅ Connection pool disposal on failure (fresh connections on retry)
6. ✅ Enhanced health check endpoint (monitors connection quality)
7. ✅ Better error messages (helps with debugging)

These changes should resolve the "server closed the connection unexpectedly" error in most cases.
