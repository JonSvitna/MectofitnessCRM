# Database Initialization Guide

This document explains the database initialization system for MectoFitness CRM, which includes robust error handling, retry logic, and CRUD operations to prevent authentication loops and database connection issues.

## Overview

The database initialization system consists of three main components:

1. **init_db.py** - Standalone initialization script with retry logic
2. **User Model CRUD Methods** - Comprehensive database operations with error handling
3. **Database Helpers** - Utility functions for connection management and retries

## Components

### 1. init_db.py - Database Initialization Script

A robust, standalone script that initializes the database with comprehensive error handling.

**Features:**
- Connection retry logic (up to 5 attempts with configurable delays)
- Automatic table creation for all models
- Verification of critical tables (especially `users` table)
- Full CRUD operation testing
- Detailed logging and error reporting

**Usage:**
```bash
# Run the initialization script
python init_db.py

# Or with environment variables
DATABASE_URL=postgresql://user:pass@host:5432/db python init_db.py
```

**What it does:**
1. Waits for database to be available (with retries)
2. Creates all database tables
3. Verifies the users table exists and has correct structure
4. Tests CRUD operations (Create, Read, Update, Delete)
5. Reports success or failure with detailed error messages

### 2. User Model CRUD Methods

The User model now includes comprehensive CRUD methods with proper error handling:

#### Create
```python
user, error = User.create_user(
    username='trainer1',
    email='trainer@example.com',
    password='securepassword',
    first_name='John',
    last_name='Doe'
)
if user:
    print(f"User created: {user.username}")
else:
    print(f"Error: {error}")
```

#### Read
```python
# Get by ID
user = User.get_by_id(1)

# Get by username
user = User.get_by_username('trainer1')

# Get by email
user = User.get_by_email('trainer@example.com')
```

#### Update
```python
success, error = user.update_profile(
    first_name='Jane',
    phone='555-1234'
)
```

#### Delete
```python
success, error = user.delete_user()
```

#### Authentication
```python
user, error = User.authenticate('trainer1', 'password')
if user:
    # User authenticated successfully
    login_user(user)
else:
    # Authentication failed
    flash(error, 'danger')
```

### 3. Database Helpers (app/utils/db_helpers.py)

Utility functions for database connection management:

#### Connection Check
```python
from app.utils.db_helpers import check_db_connection

is_connected, error = check_db_connection()
if is_connected:
    print("Database is available")
else:
    print(f"Database error: {error}")
```

#### Initialize with Retry
```python
from app.utils.db_helpers import init_db_with_retry

if init_db_with_retry(app, max_retries=5, retry_delay=3):
    print("Database initialized successfully")
else:
    print("Failed to initialize database")
```

#### Safe Database Operation Decorator
```python
from app.utils.db_helpers import safe_db_operation

@safe_db_operation(max_retries=3, retry_delay=1)
def my_database_function():
    # Your database operations here
    pass
```

## Health Check Endpoint

A health check endpoint is available to monitor database connectivity:

```bash
# Check database health
curl http://localhost:5000/api/v1/health
```

**Response (healthy):**
```json
{
    "status": "healthy",
    "database": "connected",
    "timestamp": "2025-12-09T10:23:24.211484"
}
```

**Response (unhealthy):**
```json
{
    "status": "unhealthy",
    "database": "disconnected",
    "error": "Database connection failed",
    "timestamp": "2025-12-09T10:23:24.211484"
}
```

## Error Handling

The system includes comprehensive error handling for database issues:

### 1. Connection Errors
- Automatic retry with exponential backoff
- Session rollback on failures
- Detailed error logging

### 2. Constraint Violations
- Proper handling of duplicate usernames/emails
- Clear error messages for users
- No retry (as it's not a transient error)

### 3. Server Errors
- Global error handlers for 500 and database errors
- User-friendly error pages
- JSON responses for API endpoints

## Startup Scripts

### start.sh (Railway/Production)
The startup script now uses `init_db.py`:

```bash
#!/bin/bash
# Initialize Database
python3 init_db.py || {
    echo "❌ Database initialization failed"
    exit 1
}

# Start Gunicorn
exec python3 -m gunicorn run:app --workers 4 --bind 0.0.0.0:$PORT
```

### run.py (Development)
The run script includes retry logic:

```python
from app.utils.db_helpers import init_db_with_retry

if init_db_with_retry(app, max_retries=5, retry_delay=2):
    print("Database tables created successfully!")
else:
    print("Warning: Database initialization failed.")
```

## Testing

### Test Database Initialization
```bash
python init_db.py
```

### Test User CRUD Operations
```bash
python test_user_crud.py
```

### Test Database Connection
```bash
python test_db.py
```

## Troubleshooting

### Issue: "Could not connect to database"
**Solution:**
1. Verify DATABASE_URL is set correctly
2. Check database server is running
3. Verify network connectivity
4. Check firewall rules

### Issue: "Authentication loop"
**Causes:**
- Database connection lost during authentication
- Session not properly rolled back after error
- User table doesn't exist

**Solution:**
1. Run `init_db.py` to ensure tables exist
2. Check health endpoint: `/api/v1/health`
3. Review application logs for specific errors
4. Verify database credentials are correct

### Issue: "Users table not found"
**Solution:**
```bash
# Reinitialize database
python init_db.py

# Or start the application (auto-creates tables)
python run.py
```

## Best Practices

1. **Always use CRUD methods** - Don't use raw SQLAlchemy queries for user operations
2. **Check return values** - CRUD methods return tuples of (result, error)
3. **Log errors** - Use logging instead of printing to console
4. **Handle failures gracefully** - Show user-friendly error messages
5. **Use health checks** - Monitor database connectivity in production
6. **Test initialization** - Run `init_db.py` after database changes

## Migration from Old System

If you're upgrading from the old initialization system:

1. The old system used inline `db.create_all()` with no error handling
2. New system has retry logic and comprehensive error checking
3. User model now has CRUD methods - update code to use them
4. Health check endpoint is available for monitoring

**Migration steps:**
1. Update imports to use new CRUD methods
2. Replace direct User queries with CRUD methods
3. Add error handling for all database operations
4. Test with `init_db.py` and `test_user_crud.py`

## Environment Variables

Required environment variables:

```bash
# Database connection (required for PostgreSQL)
DATABASE_URL=postgresql://user:password@host:5432/database

# Or for Railway (automatic)
DATABASE_PUBLIC_URL=postgresql://user:password@host:5432/database

# Flask environment
FLASK_ENV=production  # or development

# Secret key (required for production)
SECRET_KEY=your-secret-key-here
```

## Monitoring

### Database Health
Monitor the health endpoint regularly:
```bash
# Check every 30 seconds
watch -n 30 curl -s http://localhost:5000/api/v1/health
```

### Application Logs
Check logs for database errors:
```bash
# View logs in production
tail -f /var/log/mectofitness.log

# Or in Railway
railway logs
```

## Support

For issues with database initialization:
1. Check this documentation
2. Run `python init_db.py` for detailed diagnostics
3. Check application logs
4. Review `POSTGRESQL_SETUP.md` for database-specific setup

## Summary

The new database initialization system provides:
- ✓ Robust error handling with retry logic
- ✓ Comprehensive CRUD operations
- ✓ Health check monitoring
- ✓ User-friendly error messages
- ✓ Automatic session rollback
- ✓ Detailed logging and diagnostics

This prevents authentication loops and ensures reliable database operations even with intermittent connectivity issues.
