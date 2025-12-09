#!/bin/bash
# Railway startup script - Initialize database and start app

echo "========================================" 
echo "Railway Startup - MectoFitness CRM"
echo "========================================"
echo ""

# Debug environment variables
echo "Environment Check:"
if [ -z "$DATABASE_URL" ]; then
    echo "❌ ERROR: DATABASE_URL is NOT set!"
    echo "   Please add PostgreSQL database in Railway and link it to this service"
    exit 1
else
    echo "✓ DATABASE_URL is set"
    # Show masked version
    echo "  Connection type: $(echo $DATABASE_URL | cut -d: -f1)"
fi

if [ -z "$PORT" ]; then
    echo "⚠ PORT not set, using default 5000"
    export PORT=5000
else
    echo "✓ PORT: $PORT"
fi

echo ""

# Test database connection
echo "Testing database connection..."
python test_db.py
if [ $? -ne 0 ]; then
    echo "❌ Database connection test failed!"
    exit 1
fi

# Initialize database tables
echo ""
echo "Initializing database..."
python -c "
from app import create_app, db
import os

app = create_app(os.getenv('FLASK_ENV', 'production'))
with app.app_context():
    print('Creating database tables...')
    db.create_all()
    print('✓ Database tables created successfully!')
"

echo ""
echo "========================================"
echo "Starting Gunicorn web server..."
echo "========================================"
exec gunicorn run:app --workers 4 --timeout 120 --bind 0.0.0.0:$PORT
