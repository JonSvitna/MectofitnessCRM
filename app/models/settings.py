"""Settings and configuration models."""
from datetime import datetime
from app import db
import json


class TrainerSettings(db.Model):
    """Trainer-specific settings and preferences."""
    
    __tablename__ = 'trainer_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # API Rate Limiting
    api_calls_per_day = db.Column(db.Integer, default=1000)
    current_api_calls = db.Column(db.Integer, default=0)
    api_calls_reset_at = db.Column(db.DateTime)
    
    # Feature Toggles
    enable_ai_programs = db.Column(db.Boolean, default=True)
    enable_email_marketing = db.Column(db.Boolean, default=True)
    enable_sms_marketing = db.Column(db.Boolean, default=True)
    enable_calendar_sync = db.Column(db.Boolean, default=True)
    enable_workflow_automation = db.Column(db.Boolean, default=True)
    
    # Integration Settings
    twilio_enabled = db.Column(db.Boolean, default=False)
    twilio_account_sid = db.Column(db.String(200))
    twilio_auth_token = db.Column(db.String(200))
    twilio_phone_number = db.Column(db.String(20))
    
    sendgrid_enabled = db.Column(db.Boolean, default=False)
    sendgrid_api_key = db.Column(db.String(200))
    sendgrid_from_email = db.Column(db.String(200))
    
    # Notification Preferences
    notify_new_client = db.Column(db.Boolean, default=True)
    notify_session_reminder = db.Column(db.Boolean, default=True)
    notify_intake_complete = db.Column(db.Boolean, default=True)
    notification_email = db.Column(db.String(200))
    
    # Business Settings
    business_name = db.Column(db.String(200))
    business_logo_url = db.Column(db.String(300))
    business_website = db.Column(db.String(200))
    business_phone = db.Column(db.String(20))
    business_address = db.Column(db.Text)
    
    # Branding
    primary_color = db.Column(db.String(7), default='#2ECC71')
    secondary_color = db.Column(db.String(7), default='#27AE60')
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trainer = db.relationship('User', backref='settings', uselist=False)
    
    def increment_api_calls(self):
        """Increment API call counter."""
        self.current_api_calls += 1
    
    def reset_api_calls(self):
        """Reset API call counter."""
        self.current_api_calls = 0
        from datetime import timedelta
        self.api_calls_reset_at = datetime.utcnow() + timedelta(days=1)
    
    def can_make_api_call(self):
        """Check if API call limit is reached."""
        # Check if reset is needed
        if self.api_calls_reset_at and datetime.utcnow() >= self.api_calls_reset_at:
            self.reset_api_calls()
        
        return self.current_api_calls < self.api_calls_per_day
    
    def __repr__(self):
        return f'<TrainerSettings for User {self.trainer_id}>'


class SystemSettings(db.Model):
    """System-wide settings (admin only)."""
    
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    
    key = db.Column(db.String(100), nullable=False, unique=True)
    value = db.Column(db.Text)
    value_type = db.Column(db.String(20))  # string, integer, boolean, json
    description = db.Column(db.Text)
    category = db.Column(db.String(50))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def get_value(self):
        """Parse value based on type."""
        if self.value_type == 'integer':
            return int(self.value)
        elif self.value_type == 'boolean':
            return self.value.lower() == 'true'
        elif self.value_type == 'json':
            return json.loads(self.value)
        return self.value
    
    def set_value(self, value):
        """Set value with type conversion."""
        if self.value_type == 'json':
            self.value = json.dumps(value)
        else:
            self.value = str(value)
    
    def __repr__(self):
        return f'<SystemSettings {self.key}>'
