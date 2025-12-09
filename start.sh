#!/bin/bash
# Railway startup script - Initialize database and start app

set -e  # Exit on any error

echo "========================================" 
echo "MectoFitness CRM - Railway Startup"
echo "========================================"
echo ""

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
echo "Initializing Database..."
$PYTHON init_db.py || {
    echo "❌ Database initialization failed"
    exit 1
}

echo ""
echo "========================================"
echo "Starting Gunicorn Server on port $PORT"
echo "========================================"
exec $PYTHON -m gunicorn run:app --workers 4 --timeout 120 --bind 0.0.0.0:$PORT --log-level info
