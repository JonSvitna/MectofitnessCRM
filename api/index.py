"""Vercel serverless function entry point."""
import os
import sys

# Add the parent directory to the path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app import create_app, db

# Create the Flask app instance
app = create_app(os.getenv('FLASK_ENV', 'production'))

# Initialize database tables (only on first cold start)
# Note: For production, use Flask-Migrate migrations instead
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        # Log error but don't fail - tables might already exist
        print(f"Database initialization note: {e}")

# This is the entry point for Vercel
# Vercel will look for 'app' variable in this file
