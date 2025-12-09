"""Configuration for MectoFitness CRM application."""
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


def get_database_uri():
    """Get database URI and ensure compatibility with SQLAlchemy 2.x."""
    # Try DATABASE_PUBLIC_URL first (for Railway public access), then DATABASE_URL
    database_url = os.environ.get('DATABASE_PUBLIC_URL') or os.environ.get('DATABASE_URL')
    
    # Fix for Vercel Postgres and other providers that use deprecated postgres://
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql://', 1)
    
    # Add SSL mode for Railway/Render if using PostgreSQL
    if database_url and database_url.startswith('postgresql://'):
        # Railway requires SSL, add if not already present
        if '?sslmode=' not in database_url and '&sslmode=' not in database_url:
            separator = '&' if '?' in database_url else '?'
            database_url = f"{database_url}{separator}sslmode=require"
    
    return database_url or 'sqlite:///' + os.path.join(basedir, 'mectofitness.db')


def get_engine_options():
    """Get SQLAlchemy engine options based on database type."""
    database_uri = get_database_uri()
    
    # PostgreSQL-specific connection pooling settings
    if database_uri and 'postgresql' in database_uri:
        return {
            # Connection Pool Settings
            'pool_size': 5,  # Number of permanent connections to maintain
            'pool_recycle': 240,  # Recycle connections after 4 minutes (Railway closes idle connections after approximately 300s)
            'pool_pre_ping': True,  # Test connections before using them to avoid stale connections
            'pool_timeout': 30,  # Timeout for getting connection from pool
            'max_overflow': 10,  # Additional connections beyond pool_size when needed
            
            # Connection Options (PostgreSQL-specific)
            'connect_args': {
                'connect_timeout': 10,  # Timeout for establishing new connections
                'keepalives': 1,  # Enable TCP keepalive
                'keepalives_idle': 20,  # Seconds before starting keepalive probes (more aggressive)
                'keepalives_interval': 10,  # Interval between keepalive probes
                'keepalives_count': 5,  # Max keepalive probes before giving up
            }
        }
    else:
        # SQLite settings (simpler, no keepalives needed)
        return {
            'pool_pre_ping': True,  # Still useful for detecting issues
        }


class Config:
    """Base configuration."""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # SQLAlchemy Engine Options for robust connection handling
    # Automatically configured based on database type (PostgreSQL vs SQLite)
    SQLALCHEMY_ENGINE_OPTIONS = get_engine_options()
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # API Integration
    GOOGLE_CALENDAR_CREDENTIALS = os.path.join(basedir, 'credentials', 'google_credentials.json')
    OUTLOOK_CLIENT_ID = os.environ.get('OUTLOOK_CLIENT_ID')
    OUTLOOK_CLIENT_SECRET = os.environ.get('OUTLOOK_CLIENT_SECRET')
    
    # AI Model
    AI_MODEL_PATH = os.path.join(basedir, 'models')
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    
    # SEO
    SITE_NAME = 'MectoFitness'
    SITE_DESCRIPTION = 'Professional personal training software for fitness coaches. Manage clients, build programs, and grow your business.'
    SITE_KEYWORDS = 'personal trainer software, fitness CRM, client management, workout builder, training software, gym management, fitness coaching'
    
    # Branding Colors (Professional Fitness Software Theme - TrueCoach/Trainerize Inspired)
    PRIMARY_COLOR = '#367588'  # Teal Blue (Professional, Trustworthy)
    SECONDARY_COLOR = '#1E566C'  # Dark Blue (Grounded, Stable)
    ACCENT_COLOR = '#FFC107'  # Yellow/Gold (Energetic, Action)


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
