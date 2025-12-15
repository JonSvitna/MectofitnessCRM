#!/bin/bash
# Railway startup script for Backend only - Flask CRM
# This version skips frontend build as frontend is deployed separately

set -e  # Exit on any error

echo "========================================" 
echo "MectoFitness CRM Backend - Railway Startup"
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

# Check CORS configuration for separate frontend
if [ -z "$CORS_ORIGINS" ]; then
    echo "⚠  WARNING: CORS_ORIGINS not set"
    echo "   Set this to your frontend URL for production"
    echo "   Example: https://your-frontend.railway.app"
fi

echo ""
echo "Initializing Database..."
echo "Note: Railway PostgreSQL connections may take 30-60 seconds to establish"
$PYTHON scripts/init_db.py || {
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
echo "Backend API will be available for frontend"
echo "Make sure frontend is configured with this backend URL"
echo ""
exec $PYTHON -m gunicorn run:app --config gunicorn_config.py
