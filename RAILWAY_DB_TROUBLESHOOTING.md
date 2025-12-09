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
    'pool_recycle': 240,         # Recycle after 4 min (more aggressive than Railway's ~5min timeout)
    'pool_pre_ping': True,       # Test before use (catches stale connections)
    'pool_timeout': 30,          # Wait 30s for connection from pool
    'max_overflow': 10,          # Up to 10 extra connections
    'connect_args': {
        'connect_timeout': 10,   # 10s to establish connection
        'keepalives': 1,         # Enable TCP keepalive
        'keepalives_idle': 20,   # Start keepalive after 20s idle (more aggressive)
        'keepalives_interval': 10,  # Send probe every 10s
        'keepalives_count': 5,   # 5 probes before giving up
    }
}
```

**Key Features:**
- `pool_pre_ping`: Tests connections before using them (prevents stale connection errors)
- `pool_recycle=240`: More aggressive recycling (4 min vs Railway's ~5 min timeout)
- `keepalives_idle=20`: Faster keepalive detection (20s vs previous 30s)
- `keepalives`: Keeps connections alive during idle periods
- `connect_timeout`: Fails fast if database is unreachable

### Gunicorn Worker Lifecycle Management (gunicorn_config.py)
**NEW**: Added worker lifecycle hooks to prevent connection sharing between workers:

```python
def post_fork(server, worker):
    """Each worker gets its own connection pool"""
    from app import db
    db.engine.dispose()  # Dispose inherited pool

def child_exit(server, worker):
    """Clean up connections when worker exits"""
    from app import db
    db.engine.dispose()
```

**Why This Matters:**
- Gunicorn spawns multiple worker processes
- Without proper handling, workers can share/inherit connection pools
- This causes "server closed the connection unexpectedly" errors
- Each worker now creates and manages its own connection pool

### Request Cleanup (app/__init__.py)
Added proper session teardown after each request:

```python
@app.teardown_appcontext
def shutdown_session(exception=None):
    if exception:
        db.session.rollback()
    db.session.remove()
```

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
1. Verify each Gunicorn worker has its own pool (check gunicorn_config.py is being used)
2. Reduce `pool_size` in config.py (currently 5 per worker)
3. Reduce `max_overflow` (currently 10)
4. Check for connection leaks in your code
5. Note: With 4 workers, max connections = 4 × (5 + 10) = 60 connections

### Issue 4: "SSL connection has been closed unexpectedly"
**Cause:** Railway's SSL configuration
**Solution:**
1. Add `sslmode=require` to DATABASE_URL
2. Verify SSL certificates are valid
3. Check Railway's SSL documentation

## Performance Optimization

### Connection Pool Sizing
Current settings (per worker):
- `pool_size=5`: Good for small apps (1-100 concurrent users)
- `max_overflow=10`: Allows spikes up to 15 connections per worker
- With 4 workers: Max total connections = 4 × 15 = 60 connections

Adjust based on your traffic:
- Small app (<100 users): pool_size=5, max_overflow=10
- Medium app (100-1000 users): pool_size=10, max_overflow=20
- Large app (>1000 users): pool_size=20, max_overflow=30

**Important**: Remember to multiply by number of Gunicorn workers!

### Pool Recycle Timing
Railway typically closes idle connections after ~5 minutes (300s).
**Current setting**: `pool_recycle=240` (4 minutes) - More aggressive than Railway's timeout.

This was changed from 300s to 240s to be more proactive about refreshing connections.

If you still see issues, try:
- `pool_recycle=180` (3 minutes) - Very aggressive
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
2. ✅ More aggressive connection recycling (240s vs Railway's ~300s timeout)
3. ✅ Faster TCP keepalives (20s idle vs previous 30s)
4. ✅ **Gunicorn worker lifecycle management** (each worker gets own connection pool - prevents sharing issues)
5. ✅ **Request teardown handlers** (proper session cleanup after each request)
6. ✅ Exponential backoff retry (handles transient failures)
7. ✅ Connection pool disposal on failure (fresh connections on retry)
8. ✅ Enhanced health check endpoint (monitors connection quality)
9. ✅ Better error messages (helps with debugging)

These changes should resolve the "server closed the connection unexpectedly" error in most cases by addressing both connection lifetime issues and multi-worker connection management problems.
