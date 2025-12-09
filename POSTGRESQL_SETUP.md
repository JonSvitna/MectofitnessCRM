# PostgreSQL Setup Guide for MectoFitness CRM

This guide will help you set up PostgreSQL for MectoFitness CRM and troubleshoot common issues.

## Prerequisites

- PostgreSQL 12 or higher installed
- Python 3.8 or higher
- psycopg2-binary package (included in requirements.txt)

## Step 1: Create PostgreSQL Database

### Option A: Using psql command line

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

### Option B: Using pgAdmin

1. Open pgAdmin
2. Right-click on "Databases" → "Create" → "Database"
3. Name: `mectofitness_db`
4. Owner: Create a new user or select existing
5. Save

## Step 2: Configure Environment Variables

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

## Step 3: Test Database Connection

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

## Step 4: Initialize Database Tables

Run the application to create all tables:

```bash
python run.py
```

The application will automatically create all necessary tables on first run.

## Troubleshooting Common Issues

### Issue 1: "500 Internal Server Error" when creating account

**Cause**: Database connection issues or missing tables

**Solution**:
1. Verify DATABASE_URL is correct in `.env`
2. Check database credentials
3. Run `python test_db.py` to diagnose
4. Check application logs for specific error

### Issue 2: "psycopg2.OperationalError: could not connect to server"

**Cause**: PostgreSQL server not running or wrong host/port

**Solution**:
1. Check PostgreSQL is running: `sudo systemctl status postgresql` (Linux)
2. Verify host and port in DATABASE_URL
3. Check firewall settings
4. For cloud databases, verify IP whitelist

### Issue 3: "FATAL: password authentication failed"

**Cause**: Wrong username or password

**Solution**:
1. Verify credentials in `.env`
2. Reset password in PostgreSQL:
   ```sql
   ALTER USER mecto_user WITH PASSWORD 'new_password';
   ```

### Issue 4: "relation 'users' does not exist"

**Cause**: Database tables not created

**Solution**:
1. Run `python run.py` to create tables
2. Or use Flask migrations:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

### Issue 5: "postgres:// scheme not supported"

**Cause**: Old postgres:// scheme (Heroku/older services)

**Solution**:
The application automatically converts `postgres://` to `postgresql://`.
If issues persist, manually update DATABASE_URL:
```bash
DATABASE_URL=postgresql://... # Change postgres:// to postgresql://
```

## Verifying Setup

After setup, you should be able to:

1. **Access the application**: http://localhost:5000
2. **Register an account**: Go to /auth/register
3. **Login successfully**: Use your credentials
4. **See dashboard**: Redirected after login

## Environment-Specific Notes

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
```

### Docker
```bash
DATABASE_URL=postgresql://mecto_user:password@db:5432/mectofitness_db
# 'db' is the service name in docker-compose.yml
```

## Database Maintenance

### Backup Database
```bash
pg_dump -U mecto_user mectofitness_db > backup.sql
```

### Restore Database
```bash
psql -U mecto_user mectofitness_db < backup.sql
```

### View Database Size
```sql
SELECT pg_size_pretty(pg_database_size('mectofitness_db'));
```

## Getting Help

If you continue to experience issues:

1. Check the application logs for detailed error messages
2. Run `python test_db.py` and share the output
3. Verify PostgreSQL version: `psql --version`
4. Check PostgreSQL logs for connection attempts

## Additional Resources

- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [SQLAlchemy PostgreSQL Dialect](https://docs.sqlalchemy.org/en/14/dialects/postgresql.html)
