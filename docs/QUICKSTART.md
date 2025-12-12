# Quick Start Guide - MectoFitness CRM

This guide will help you quickly set up and verify your MectoFitness CRM installation.

## Step 1: Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

## Step 2: Configure Database

### Option A: Use SQLite (Quick Start - Default)

SQLite is perfect for testing and small deployments. No additional setup required!

Just make sure `.env` has:
```bash
DATABASE_URL=sqlite:///mectofitness.db
```

### Option B: Use PostgreSQL (Recommended for Production)

See [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) for detailed PostgreSQL setup instructions.

Quick PostgreSQL setup:
```bash
# 1. Create database
psql -U postgres -c "CREATE DATABASE mectofitness_db;"

# 2. Update .env file
DATABASE_URL=postgresql://username:password@localhost:5432/mectofitness_db
```

## Step 3: Verify Setup

Run the verification script to check everything is configured correctly:

```bash
python verify_setup.py
```

This will check:
- ✓ Environment variables
- ✓ Database connection
- ✓ Table creation
- ✓ User operations

## Step 4: Start Application

```bash
python run.py
```

You should see:
```
Database tables created successfully!
 * Running on http://127.0.0.1:5000
```

## Step 5: Create Your First Account

1. Open browser: http://localhost:5000
2. Click "Register" or go to http://localhost:5000/auth/register
3. Fill in the form:
   - Username: your_username
   - Email: your@email.com
   - Password: secure_password
   - First Name: Your
   - Last Name: Name
4. Click "Register"
5. You'll be redirected to login page
6. Login with your credentials

## Troubleshooting

### "500 Internal Server Error" when creating account

This usually means database connection issues. Run diagnostics:

```bash
python verify_setup.py
```

Common causes:
1. **Database not accessible** - Check DATABASE_URL in .env
2. **Tables not created** - Run `python run.py` once to create tables
3. **Wrong credentials** - Verify PostgreSQL username/password
4. **Database doesn't exist** - Create the database first

### "No module named 'psycopg2'"

```bash
pip install psycopg2-binary
```

### "Could not connect to PostgreSQL server"

1. Check PostgreSQL is running:
   ```bash
   # Linux/Mac
   sudo systemctl status postgresql
   
   # Or check if port 5432 is listening
   netstat -an | grep 5432
   ```

2. Verify DATABASE_URL format:
   ```
   postgresql://username:password@host:port/database
   ```

3. Test connection manually:
   ```bash
   psql -U username -d database_name -h host
   ```

### "relation 'users' does not exist"

Tables weren't created. Solution:
```bash
python run.py
```

This automatically creates all tables on startup.

## Testing the Setup

### Method 1: Use verify_setup.py (Recommended)
```bash
python verify_setup.py
```

### Method 2: Use test_db.py
```bash
python test_db.py
```

### Method 3: Manual Test via Web Interface
1. Start app: `python run.py`
2. Register account: http://localhost:5000/auth/register
3. Login: http://localhost:5000/auth/login

### Method 4: Manual Test via Python
```python
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    # Check connection
    db.engine.connect()
    print("Connected!")
    
    # Count users
    print(f"Users: {User.query.count()}")
```

## What's Next?

After successful setup:

1. **Add Clients**: Navigate to Clients → Add New Client
2. **Schedule Sessions**: Create training sessions
3. **Build Programs**: Create workout programs
4. **Set Up Calendar**: Connect Google Calendar or Outlook
5. **Explore Features**: Check out all the CRM features

## Configuration Files

- `.env` - Environment variables (database, secrets)
- `config.py` - Application configuration
- `requirements.txt` - Python dependencies

## Getting Help

If you encounter issues:

1. ✅ Run `python verify_setup.py` first
2. ✅ Check error messages in console
3. ✅ Review [POSTGRESQL_SETUP.md](POSTGRESQL_SETUP.md) for PostgreSQL issues
4. ✅ Check application logs for detailed errors
5. ✅ Ensure all dependencies are installed: `pip install -r requirements.txt`

## Production Deployment

For production deployment:

1. Set `FLASK_ENV=production` in .env
2. Use a strong `SECRET_KEY`
3. Use PostgreSQL (not SQLite)
4. Use a production WSGI server (gunicorn)
5. Set up HTTPS/SSL
6. Configure proper backups

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed production deployment guide.

---

**Need help?** Open an issue on GitHub with:
- Output from `python verify_setup.py`
- Error messages from console
- Your database type (SQLite/PostgreSQL)
