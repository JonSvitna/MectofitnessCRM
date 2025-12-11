# Database Setup Guide

Complete guide for setting up SQLite or PostgreSQL with MectoFitness CRM.

## Database Options

### SQLite (Default)
**Best for:**
- Development and testing
- Single-user deployments
- Small businesses (<100 clients)
- Simple deployment scenarios

**Pros:**
- No installation required
- Zero configuration
- File-based (easy backup)
- Built into Python

**Cons:**
- Limited concurrent access
- Not recommended for production with multiple users

### PostgreSQL (Recommended for Production)
**Best for:**
- Production deployments
- Multiple concurrent users
- Larger client bases (>100 clients)
- High-availability requirements

**Pros:**
- Robust and reliable
- Excellent concurrent access
- Advanced features
- Industry standard

**Cons:**
- Requires separate installation
- More complex setup

## Quick Start with SQLite

SQLite is configured by default. No additional setup needed!

```bash
# Just start the app
python run.py
```

The database file `mectofitness.db` will be created automatically.

## PostgreSQL Setup

### Prerequisites
- PostgreSQL 12 or higher installed
- Python 3.8 or higher
- psycopg2-binary package (included in requirements.txt)

### Step 1: Install PostgreSQL

**macOS:**
```bash
brew install postgresql
brew services start postgresql
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install postgresql postgresql-contrib
sudo systemctl start postgresql
```

**Windows:**
Download and install from [postgresql.org](https://www.postgresql.org/download/windows/)

### Step 2: Create Database

**Option A: Using psql command line**

```bash
# Connect to PostgreSQL as superuser
psql -U postgres

# Create database
CREATE DATABASE mectofitness_db;

# Create user with password
CREATE USER mecto_user WITH PASSWORD 'your_secure_password';

# Grant privileges
GRANT ALL PRIVILEGES ON DATABASE mectofitness_db TO mecto_user;

# Exit psql
\q
```

**Option B: Using pgAdmin**

1. Open pgAdmin
2. Right-click on "Databases" → "Create" → "Database"
3. Name: `mectofitness_db`
4. Owner: Create a new user or select existing
5. Save

### Step 3: Configure Environment Variables

Edit the `.env` file in the project root:

```bash
# PostgreSQL connection string format:
# postgresql://username:password@host:port/database

DATABASE_URL=postgresql://mecto_user:your_secure_password@localhost:5432/mectofitness_db
```

### Common PostgreSQL Hosts:
- **Local**: `localhost` or `127.0.0.1`
- **Railway**: Provided in Railway dashboard
- **Render**: Provided in Render dashboard
- **Heroku**: Provided as DATABASE_URL environment variable
- **Azure**: `your-server.postgres.database.azure.com`
- **AWS RDS**: `your-instance.region.rds.amazonaws.com`

### Step 4: Test Database Connection

Run the database test script:

```bash
python test_db.py
```

This will:
- ✓ Verify DATABASE_URL is set
- ✓ Test database connection
- ✓ Check if tables exist
- ✓ Test account creation
- ✓ Verify user queries work

### Step 5: Initialize Database Tables

Run the application to create all tables:

```bash
python run.py
```

The application will automatically create all necessary tables on first run.

## Database Initialization System

MectoFitness CRM includes a robust initialization system with:

- Connection retry logic (up to 5 attempts)
- Automatic table creation
- Comprehensive error handling
- CRUD operation verification
- Health check monitoring

### Initialize with Retry Logic

```bash
# Standalone initialization script
python init_db.py
```

This script:
1. Waits for database to be available (with retries)
2. Creates all database tables
3. Verifies the users table exists
4. Tests CRUD operations
5. Reports success or failure with detailed error messages

### Health Check Endpoint

Monitor database connectivity:

```bash
curl http://localhost:5000/api/v1/health
```

**Response (healthy):**
```json
{
    "status": "healthy",
    "database": "connected",
    "timestamp": "2025-12-11T06:00:00.000000"
}
```

## Troubleshooting

### Issue: "500 Internal Server Error" when creating account

**Cause**: Database connection issues or missing tables

**Solution:**
1. Verify DATABASE_URL is correct in `.env`
2. Check database credentials
3. Run `python test_db.py` to diagnose
4. Check application logs for specific error

### Issue: "psycopg2.OperationalError: could not connect to server"

**Cause**: PostgreSQL server not running or wrong host/port

**Solution:**
1. Check PostgreSQL is running: `sudo systemctl status postgresql` (Linux)
2. Verify host and port in DATABASE_URL
3. Check firewall settings
4. For cloud databases, verify IP whitelist

### Issue: "FATAL: password authentication failed"

**Cause**: Wrong username or password

**Solution:**
1. Verify credentials in `.env`
2. Reset password in PostgreSQL:
   ```sql
   ALTER USER mecto_user WITH PASSWORD 'new_password';
   ```

### Issue: "relation 'users' does not exist"

**Cause**: Database tables not created

**Solution:**
Run `python run.py` to create tables automatically.

### Issue: "postgres:// scheme not supported"

**Cause**: Old postgres:// scheme (Heroku/older services)

**Solution:**
The application automatically converts `postgres://` to `postgresql://`.
If issues persist, manually update DATABASE_URL:
```bash
DATABASE_URL=postgresql://...  # Change postgres:// to postgresql://
```

### Issue: "No module named 'psycopg2'"

**Solution:**
```bash
pip install psycopg2-binary
```

## Environment-Specific Configuration

### Local Development
```bash
DATABASE_URL=postgresql://mecto_user:password@localhost:5432/mectofitness_db
FLASK_ENV=development
```

### Production Deployment
```bash
DATABASE_URL=postgresql://user:password@host:5432/database
FLASK_ENV=production
SECRET_KEY=strong-random-secret-key-here
SESSION_COOKIE_SECURE=True
```

### Docker
```bash
DATABASE_URL=postgresql://mecto_user:password@db:5432/mectofitness_db
# 'db' is the service name in docker-compose.yml
```

## Database Maintenance

### Backup Database

**SQLite:**
```bash
cp mectofitness.db mectofitness_backup.db
```

**PostgreSQL:**
```bash
pg_dump -U mecto_user mectofitness_db > backup.sql
```

### Restore Database

**SQLite:**
```bash
cp mectofitness_backup.db mectofitness.db
```

**PostgreSQL:**
```bash
psql -U mecto_user mectofitness_db < backup.sql
```

### View Database Size

**PostgreSQL:**
```sql
SELECT pg_size_pretty(pg_database_size('mectofitness_db'));
```

## Performance Optimization

### Connection Pooling

For production with many users:

```python
# In config.py
SQLALCHEMY_ENGINE_OPTIONS = {
    'pool_size': 10,
    'pool_recycle': 3600,
    'pool_pre_ping': True,
}
```

### Database Indexes

Already included on frequently queried fields:
- User username and email
- Client user_id
- Session client_id and date
- Program client_id

## Verifying Setup

After setup, you should be able to:

1. **Access the application**: http://localhost:5000
2. **Register an account**: Go to /auth/register
3. **Login successfully**: Use your credentials
4. **See dashboard**: Redirected after login

Run verification:
```bash
python verify_setup.py
```

## Getting Help

If you continue to experience issues:

1. Check the application logs for detailed error messages
2. Run `python test_db.py` and share the output
3. Verify PostgreSQL version: `psql --version`
4. Check PostgreSQL logs for connection attempts
5. Review [Installation Guide](installation.md) for general setup

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [SQLAlchemy PostgreSQL Dialect](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html)
- [SQLite Documentation](https://www.sqlite.org/docs.html)

---

**Database configured?** Move on to the [Quick Start Guide](quickstart.md) to begin using the application!
