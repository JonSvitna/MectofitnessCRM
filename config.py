"""Configuration for MectoFitness CRM application."""
import os
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Base configuration."""
    
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'mectofitness.db')
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
    
    # AI Model
    AI_MODEL_PATH = os.path.join(basedir, 'models')
    
    # Pagination
    ITEMS_PER_PAGE = 20
    
    # Upload
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')
    
    # SEO
    SITE_NAME = 'MectoFitness'
    SITE_DESCRIPTION = 'Simple, powerful software for personal trainers to manage clients and grow their fitness business'
    SITE_KEYWORDS = 'personal trainer software, fitness business, client management, workout programs, training software, fitness coaching'
    
    # Branding Colors (Leadership Theme)
    PRIMARY_COLOR = '#FF8C00'  # Amber
    SECONDARY_COLOR = '#FF6600'  # Dark Orange
    ACCENT_COLOR = '#FF4500'  # Lava Red


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
