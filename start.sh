#!/bin/bash
# Railway startup script - Initialize database and start app

set -e  # Exit on any error

echo "========================================" 
echo "MectoFitness CRM - Railway Startup"
echo "========================================"
echo ""

# Activate virtual environment if it exists
if [ -d "/opt/venv" ]; then
    echo "Activating Python virtual environment..."
    source /opt/venv/bin/activate
fi

# Use Python 3
PYTHON=python3
echo "Python version check:"
$PYTHON --version

# Check critical environment variables
echo ""
echo "Environment Check:"
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL not set!"
    echo "   Add PostgreSQL database in Railway and link it"
    exit 1
fi
echo "✓ DATABASE_URL configured"

if [ -z "$SECRET_KEY" ]; then
    echo "⚠  WARNING: SECRET_KEY not set, using default (insecure)"
fi

if [ -z "$PORT" ]; then
    echo "⚠  PORT not set, defaulting to 5000"
    export PORT=5000
fi

echo ""
echo "Building Frontend..."
if command -v npm &> /dev/null; then
    echo "npm found, building React app..."
    npm run build || {
        echo "⚠  Frontend build failed, continuing with backend only"
    }
else
    echo "⚠  npm not found, skipping frontend build"
fi

echo ""
echo "Initializing Database..."
echo "Note: Railway PostgreSQL connections may take 30-60 seconds to establish"
$PYTHON init_db.py || {
    echo "❌ Database initialization failed"
    echo "   This may be due to:"
    echo "   1. PostgreSQL service not running or not accessible"
    echo "   2. Network connectivity issues"
    echo "   3. Incorrect DATABASE_URL credentials"
    echo "   Please check Railway logs and database status"
    exit 1
}

echo ""
echo "========================================"
echo "Starting Gunicorn Server on port $PORT"
echo "========================================"
echo "Using gunicorn_config.py for worker lifecycle management"
echo "Config includes: workers=4, timeout=120, bind, log-level, and lifecycle hooks"
exec $PYTHON -m gunicorn run:app --config gunicorn_config.py
