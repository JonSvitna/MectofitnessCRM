# Installation Guide

Complete setup instructions for MectoFitness CRM.

## System Requirements

- Python 3.8 or higher
- 100 MB free disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for calendar integration)

## Installation Steps

### 1. Install Python

**Windows:**
1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run installer and check "Add Python to PATH"
3. Verify installation: `python --version`

**macOS:**
```bash
brew install python3
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### 2. Clone and Setup

```bash
# Clone the repository
git clone https://github.com/JonSvitna/MectofitnessCRM.git
cd MectofitnessCRM

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Application

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your settings
nano .env  # or use any text editor
```

**Important Settings:**
- `SECRET_KEY`: Generate a secure random key
- `FLASK_ENV`: Set to 'production' for live deployment
- `DATABASE_URL`: Database connection string (see [Database Setup](database-setup.md))

### 4. Verify Setup (Recommended)

```bash
python verify_setup.py
```

This checks:
- ✓ Environment variables
- ✓ Database connection
- ✓ Table creation
- ✓ User operations

### 5. Initialize Database

```bash
# Run the application (this creates the database)
python run.py
```

The database will be created automatically. For SQLite, this creates `mectofitness.db`.

### 6. Access the Application

1. Open your web browser
2. Navigate to: `http://localhost:5000`
3. Register your first trainer account
4. Start adding clients and sessions!

## Calendar Integration Setup

### Google Calendar Integration

#### Step 1: Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project: "MectoFitness CRM"
3. Enable Google Calendar API:
   - Navigate to "APIs & Services" > "Library"
   - Search for "Google Calendar API"
   - Click "Enable"

#### Step 2: Create OAuth Credentials

1. Go to "APIs & Services" > "Credentials"
2. Click "Create Credentials" > "OAuth client ID"
3. Choose "Web application"
4. Add authorized redirect URI: `http://localhost:5000/calendar/google/callback`
5. Download the JSON credentials file

#### Step 3: Configure Application

1. Create `credentials` directory if it doesn't exist
2. Save downloaded JSON as `credentials/google_credentials.json`
3. Add credentials to `.env`:
   ```
   GOOGLE_CLIENT_ID=your-client-id
   GOOGLE_CLIENT_SECRET=your-client-secret
   ```

### Outlook Calendar Integration

#### Step 1: Register Application in Azure

1. Go to [Azure Portal](https://portal.azure.com/)
2. Navigate to "Azure Active Directory" > "App registrations"
3. Click "New registration"
4. Name: "MectoFitness CRM"
5. Supported account types: "Accounts in any organizational directory and personal Microsoft accounts"
6. Redirect URI: `http://localhost:5000/calendar/outlook/callback`

#### Step 2: Configure Permissions

1. Go to "API permissions"
2. Add these permissions:
   - Calendars.ReadWrite
   - User.Read
3. Grant admin consent

#### Step 3: Create Client Secret

1. Go to "Certificates & secrets"
2. Create new client secret
3. Copy the secret value (shown only once!)

#### Step 4: Configure Application

Add to `.env`:
```
OUTLOOK_CLIENT_ID=your-application-id
OUTLOOK_CLIENT_SECRET=your-client-secret
```

## Troubleshooting

### Database Issues

**Problem**: "Database is locked"  
**Solution**: SQLite doesn't handle high concurrency well. Consider PostgreSQL for production.

**Problem**: "Table doesn't exist"  
**Solution**: Run `python run.py` to create tables

**Problem**: "relation 'users' does not exist"  
**Solution**: Tables weren't created. Run `python run.py` to create them automatically.

### Calendar Integration Issues

**Problem**: "Invalid credentials"  
**Solution**: Verify credentials in `.env` and check redirect URIs match exactly.

**Problem**: "Access denied"  
**Solution**: Ensure proper permissions are granted in Google Cloud Console or Azure Portal.

### Port Already in Use

```bash
# Find process using port 5000
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Kill the process or use different port
python run.py --port 5001
```

### Module Not Found Errors

**Problem**: "No module named 'psycopg2'"  
**Solution**:
```bash
pip install psycopg2-binary
```

**Problem**: Missing dependencies  
**Solution**:
```bash
pip install -r requirements.txt
```

## Security Checklist

- [ ] Change SECRET_KEY in production
- [ ] Use HTTPS (set SESSION_COOKIE_SECURE=True)
- [ ] Keep dependencies updated: `pip install -U -r requirements.txt`
- [ ] Restrict file upload types and sizes
- [ ] Use environment variables for sensitive data
- [ ] Enable CSRF protection (included in Flask-WTF)
- [ ] Regular database backups

## What's Next?

After successful setup:

1. **Add Clients**: Navigate to Clients → Add New Client
2. **Schedule Sessions**: Create training sessions
3. **Build Programs**: Create workout programs
4. **Set Up Calendar**: Connect Google Calendar or Outlook
5. **Explore Features**: Check out all the [CRM features](../03-features/overview.md)

## Getting Help

- Check the [Quick Start Guide](quickstart.md) for faster setup
- Review [Database Setup](database-setup.md) for database configuration
- See [Deployment Guide](../02-deployment/overview.md) for production deployment
- Open an issue on GitHub for bugs

---

Ready to go? Run `python run.py` and start managing your fitness business! 💪
