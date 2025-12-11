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
    
    return database_url or 'sqlite:///' + os.path.join(basedir, 'mectofitness.db')


class Config:
    """Base configuration."""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = get_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Session
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # Set to True in production with HTTPS
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # API Integration
    GOOGLE_CALENDAR_CREDENTIALS = os.path.join(basedir, 'credentials', 'google_credentials.json')
    OUTLOOK_CLIENT_ID = os.environ.get('OUTLOOK_CLIENT_ID')
    OUTLOOK_CLIENT_SECRET = os.environ.get('OUTLOOK_CLIENT_SECRET')
    
    # Zoom Integration
    ZOOM_CLIENT_ID = os.environ.get('ZOOM_CLIENT_ID')
    ZOOM_CLIENT_SECRET = os.environ.get('ZOOM_CLIENT_SECRET')
    ZOOM_ACCOUNT_ID = os.environ.get('ZOOM_ACCOUNT_ID')
    
    # Stripe Payment Integration
    STRIPE_SECRET_KEY = os.environ.get('STRIPE_SECRET_KEY')
    STRIPE_PUBLISHABLE_KEY = os.environ.get('STRIPE_PUBLISHABLE_KEY')
    STRIPE_WEBHOOK_SECRET = os.environ.get('STRIPE_WEBHOOK_SECRET')
    
    # OpenAI Integration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    
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
