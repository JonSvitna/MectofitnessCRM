# Quick Start Guide

Get MectoFitness CRM up and running in 5 minutes!

## Prerequisites

- Python 3.8+ installed
- Git installed (or download ZIP from GitHub)

## 5-Minute Setup

### Step 1: Get the Code (30 seconds)

```bash
git clone https://github.com/JonSvitna/MectofitnessCRM.git
cd MectofitnessCRM
```

### Step 2: Install Dependencies (2 minutes)

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install packages
pip install -r requirements.txt
```

### Step 3: Configure (30 seconds)

```bash
# Copy environment template
cp .env.example .env

# Default SQLite database is ready to go!
# No additional configuration needed for quick start
```

### Step 4: Verify Setup (30 seconds)

```bash
python verify_setup.py
```

Expected output:
```
✓ Environment variables loaded
✓ Database connection successful
✓ Tables created
✓ User operations working
```

### Step 5: Start the App (30 seconds)

```bash
python run.py
```

Expected output:
```
Database tables created successfully!
 * Running on http://127.0.0.1:5000
```

### Step 6: Create Your Account (1 minute)

1. Open browser: http://localhost:5000
2. Click "Register" 
3. Fill in the form:
   - Username: your_username
   - Email: your@email.com
   - Password: secure_password
   - First Name: Your
   - Last Name: Name
4. Click "Register" and login!

## ✅ You're Done!

You can now:
- Add clients
- Schedule training sessions
- Create workout programs
- Track progress

## Database Options

### Option A: SQLite (Default - No Setup Required)

Perfect for:
- Testing and development
- Single-user deployment
- Small businesses (<100 clients)

Already configured! Just run `python run.py`.

### Option B: PostgreSQL (Production Recommended)

Better for:
- Production deployments
- Multiple concurrent users
- Larger client bases

Quick PostgreSQL setup:

```bash
# 1. Install PostgreSQL (if not installed)
# On macOS: brew install postgresql
# On Ubuntu: sudo apt install postgresql

# 2. Create database
psql -U postgres -c "CREATE DATABASE mectofitness_db;"

# 3. Update .env file
DATABASE_URL=postgresql://postgres:password@localhost:5432/mectofitness_db

# 4. Restart app
python run.py
```

See [Database Setup Guide](database-setup.md) for detailed PostgreSQL instructions.

## Troubleshooting

### "500 Internal Server Error" when creating account

Run diagnostics:
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
   sudo systemctl status postgresql  # Linux
   ```

2. Verify DATABASE_URL format:
   ```
   postgresql://username:password@host:port/database
   ```

3. Test connection manually:
   ```bash
   psql -U username -d database_name -h host
   ```

### "Port already in use"

```bash
# Find what's using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Use a different port
python run.py --port 5001
```

## Testing the Setup

### Method 1: Automated Verification (Recommended)
```bash
python verify_setup.py
```

### Method 2: Direct Database Test
```bash
python test_db.py
```

### Method 3: Web Interface Test
1. Start app: `python run.py`
2. Register account: http://localhost:5000/auth/register
3. Login: http://localhost:5000/auth/login

### Method 4: Python Console Test
```python
from dotenv import load_dotenv
load_dotenv()

from app import create_app, db
from app.models.user import User

app = create_app()
with app.app_context():
    # Check connection
    db.engine.connect()
    print("✓ Connected!")
    
    # Count users
    print(f"Users in database: {User.query.count()}")
```

## Optional: React Frontend

The application includes an optional modern React interface. The traditional Flask interface works perfectly without it.

To enable React UI:

```bash
# Install Node.js dependencies
npm install

# Build the React app
npm run build

# Access React interface at /app after logging in
```

See [Frontend Setup Guide](frontend-setup.md) for details.

## Next Steps

### Getting Started
1. **Add Your First Client**
   - Go to Clients → Add New Client
   - Fill in client details
   - Save

2. **Schedule a Session**
   - Go to Sessions → New Session
   - Select client
   - Choose date/time
   - Save

3. **Create a Program**
   - Go to Programs → New Program
   - Add exercises
   - Assign to client

### Advanced Features
- **Calendar Integration**: Connect [Google Calendar or Outlook](installation.md#calendar-integration-setup)
- **AI Features**: Set up [AI Program Generation](../03-features/ai-programs.md)
- **API Access**: Review [API Documentation](../04-api/overview.md)

### Production Deployment
- See [Deployment Overview](../02-deployment/overview.md) for production setup
- Review [Deployment Checklist](../02-deployment/checklist.md) before going live

## Configuration Files

- `.env` - Environment variables (database, secrets)
- `config.py` - Application configuration
- `requirements.txt` - Python dependencies

## Getting Help

If you encounter issues:

1. ✅ Run `python verify_setup.py` first
2. ✅ Check error messages in console
3. ✅ Review [Installation Guide](installation.md) for detailed setup
4. ✅ Check [Database Setup](database-setup.md) for PostgreSQL issues
5. ✅ Open an issue on [GitHub](https://github.com/JonSvitna/MectofitnessCRM/issues)

## Production Considerations

When ready for production:

1. ✅ Set `FLASK_ENV=production` in .env
2. ✅ Generate strong `SECRET_KEY`
3. ✅ Use PostgreSQL (not SQLite)
4. ✅ Use Gunicorn or production WSGI server
5. ✅ Set up HTTPS/SSL
6. ✅ Configure database backups

See [Deployment Guide](../02-deployment/overview.md) for complete production setup.

---

**That's it!** You're ready to start managing your fitness business. 💪

For more detailed information, see the [Complete Installation Guide](installation.md).
