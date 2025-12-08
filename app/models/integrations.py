"""Third-party integrations models."""
from datetime import datetime
from app import db
import json


class Integration(db.Model):
    """Third-party integration configuration."""
    
    __tablename__ = 'integrations'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Integration Details
    integration_type = db.Column(db.String(50), nullable=False)  # zoom, stripe, zapier, etc.
    integration_name = db.Column(db.String(100))
    
    # Authentication
    api_key = db.Column(db.String(500))
    api_secret = db.Column(db.String(500))
    access_token = db.Column(db.Text)
    refresh_token = db.Column(db.Text)
    token_expires_at = db.Column(db.DateTime)
    
    # Configuration
    config_data = db.Column(db.Text)  # JSON configuration
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_connected = db.Column(db.Boolean, default=False)
    last_sync_at = db.Column(db.DateTime)
    last_error = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trainer = db.relationship('User', backref='integrations')
    
    def get_config(self):
        """Parse configuration from JSON."""
        if self.config_data:
            return json.loads(self.config_data)
        return {}
    
    def set_config(self, config):
        """Set configuration as JSON."""
        self.config_data = json.dumps(config)
    
    def __repr__(self):
        return f'<Integration {self.integration_type} for Trainer {self.trainer_id}>'


class VideoConference(db.Model):
    """Video conference sessions."""
    
    __tablename__ = 'video_conferences'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Conference Details
    platform = db.Column(db.String(20))  # zoom, google_meet, teams, custom
    meeting_id = db.Column(db.String(200))
    meeting_url = db.Column(db.String(500))
    meeting_password = db.Column(db.String(100))
    
    # Platform-Specific IDs
    zoom_meeting_id = db.Column(db.String(100))
    google_meet_code = db.Column(db.String(100))
    teams_meeting_id = db.Column(db.String(100))
    
    # Status
    status = db.Column(db.String(20), default='scheduled')  # scheduled, started, ended
    
    # Recording
    recording_url = db.Column(db.String(500))
    recording_available = db.Column(db.Boolean, default=False)
    
    # Timestamps
    scheduled_start = db.Column(db.DateTime)
    actual_start = db.Column(db.DateTime)
    actual_end = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    session = db.relationship('Session', backref='video_conference', uselist=False)
    trainer = db.relationship('User', backref='video_conferences')
    
    def __repr__(self):
        return f'<VideoConference {self.platform} for Session {self.session_id}>'


class WebhookEndpoint(db.Model):
    """Webhook endpoints for integrations."""
    
    __tablename__ = 'webhook_endpoints'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Endpoint Details
    name = db.Column(db.String(100), nullable=False)
    url = db.Column(db.String(500), nullable=False)
    secret = db.Column(db.String(100))
    
    # Events to Subscribe
    events = db.Column(db.Text)  # JSON array of event types
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Statistics
    total_calls = db.Column(db.Integer, default=0)
    successful_calls = db.Column(db.Integer, default=0)
    failed_calls = db.Column(db.Integer, default=0)
    last_called_at = db.Column(db.DateTime)
    last_error = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trainer = db.relationship('User', backref='webhooks')
    
    def get_events(self):
        """Parse events from JSON."""
        if self.events:
            return json.loads(self.events)
        return []
    
    def __repr__(self):
        return f'<WebhookEndpoint {self.name}>'


class AppCustomization(db.Model):
    """Branded app customization settings."""
    
    __tablename__ = 'app_customizations'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # App Identity
    app_name = db.Column(db.String(100))
    app_tagline = db.Column(db.String(200))
    app_description = db.Column(db.Text)
    
    # Branding
    logo_url = db.Column(db.String(500))
    icon_url = db.Column(db.String(500))
    splash_screen_url = db.Column(db.String(500))
    
    # Colors
    primary_color = db.Column(db.String(7), default='#2ECC71')
    secondary_color = db.Column(db.String(7), default='#27AE60')
    accent_color = db.Column(db.String(7), default='#1C1C1C')
    background_color = db.Column(db.String(7), default='#FFFFFF')
    text_color = db.Column(db.String(7), default='#1C1C1C')
    
    # Typography
    font_family = db.Column(db.String(100))
    heading_font = db.Column(db.String(100))
    
    # Features
    enabled_features = db.Column(db.Text)  # JSON array
    
    # Custom Content
    welcome_message = db.Column(db.Text)
    terms_and_conditions = db.Column(db.Text)
    privacy_policy = db.Column(db.Text)
    
    # App Store
    ios_app_id = db.Column(db.String(100))
    android_package_name = db.Column(db.String(200))
    app_store_url = db.Column(db.String(500))
    play_store_url = db.Column(db.String(500))
    
    # Status
    is_published = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    published_at = db.Column(db.DateTime)
    
    # Relationships
    trainer = db.relationship('User', backref='app_customization', uselist=False)
    
    def get_enabled_features(self):
        """Parse enabled features from JSON."""
        if self.enabled_features:
            return json.loads(self.enabled_features)
        return []
    
    def __repr__(self):
        return f'<AppCustomization {self.app_name}>'
