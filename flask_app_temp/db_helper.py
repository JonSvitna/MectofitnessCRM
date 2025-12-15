"""Database configuration helper for Vercel deployment."""
import os
import re


def get_database_url():
    """
    Get database URL and ensure it's compatible with SQLAlchemy 2.x.
    
    Vercel Postgres and some providers use 'postgres://' which is deprecated.
    SQLAlchemy 2.x requires 'postgresql://'
    """
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url and database_url.startswith('postgres://'):
        # Replace postgres:// with postgresql://
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    return database_url or 'sqlite:///mectofitness.db'
