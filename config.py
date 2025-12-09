"""Configuration for MectoFitness CRM application."""
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


def get_database_uri():
    """Get database URI and ensure compatibility with SQLAlchemy 2.x."""
    # Try DATABASE_PRIVATE_URL first (Railway internal network - most stable)
    # Then fall back to DATABASE_URL, then DATABASE_PUBLIC_URL (least stable)
    database_url = (
        os.environ.get('DATABASE_PRIVATE_URL') or 
        os.environ.get('DATABASE_URL') or 
        os.environ.get('DATABASE_PUBLIC_URL')
    )
    
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
        # Determine if using Railway's public proxy (less stable) or internal network
        is_public_proxy = 'rlwy.net' in database_uri or 'railway.app' in database_uri
        
        base_options = {
            # Connection Pool Settings (reduced for Railway public proxy stability)
            'pool_size': 3,  # Fewer permanent connections for public proxy
            'pool_recycle': 180,  # Recycle every 3 minutes (before Railway timeout)
            'pool_pre_ping': True,  # Always test connections before use
            'pool_timeout': 60,  # Longer wait time for public proxy
            'max_overflow': 5,  # Limit overflow connections
        }
        
        # Add connection args based on network type
        if is_public_proxy:
            # Public proxy needs more aggressive settings
            base_options['connect_args'] = {
                'connect_timeout': 30,  # Longer timeout for public proxy
                'keepalives': 1,
                'keepalives_idle': 60,  # Less aggressive to avoid proxy issues
                'keepalives_interval': 30,
                'keepalives_count': 3,
                'options': '-c statement_timeout=30000'  # 30 second statement timeout
            }
        else:
            # Internal network can use standard settings
            base_options['connect_args'] = {
                'connect_timeout': 10,
                'keepalives': 1,
                'keepalives_idle': 20,
                'keepalives_interval': 10,
                'keepalives_count': 5,
            }
        
        return base_options
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
