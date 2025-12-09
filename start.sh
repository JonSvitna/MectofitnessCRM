#!/bin/bash
# Railway startup script - Initialize database and start app

echo "Checking database connection..."

# Initialize database tables
python -c "
from app import create_app, db
import os

app = create_app(os.getenv('FLASK_ENV', 'production'))
with app.app_context():
    print('Creating database tables...')
    db.create_all()
    print('✓ Database tables created successfully!')
"

echo "Starting Gunicorn..."
exec gunicorn run:app --workers 4 --timeout 120 --bind 0.0.0.0:$PORT
