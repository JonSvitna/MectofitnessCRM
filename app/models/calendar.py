"""Calendar integration model."""
from datetime import datetime, timezone
from app import db


class CalendarIntegration(db.Model):
    """Calendar integration settings for users."""
    
    __tablename__ = 'calendar_integrations'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Integration type
    provider = db.Column(db.String(20), nullable=False)  # google, outlook
    
    # Auth tokens (encrypted in production)
    access_token = db.Column(db.Text)
    refresh_token = db.Column(db.Text)
    token_expiry = db.Column(db.DateTime)
    
    # Calendar settings
    calendar_id = db.Column(db.String(200))
    sync_enabled = db.Column(db.Boolean, default=True)
    auto_sync = db.Column(db.Boolean, default=True)
    last_sync = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    user = db.relationship('User', back_populates='calendar_integrations')
    
    def __repr__(self):
        return f'<CalendarIntegration {self.provider} for User {self.user_id}>'
