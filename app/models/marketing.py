"""Marketing automation models."""
from datetime import datetime
from app import db
import json


class EmailTemplate(db.Model):
    """Email template for marketing campaigns."""
    
    __tablename__ = 'email_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(200), nullable=False)
    subject = db.Column(db.String(300), nullable=False)
    body = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50))  # welcome, reminder, promotion, follow_up
    
    # AI Generation
    is_ai_generated = db.Column(db.Boolean, default=False)
    ai_prompt = db.Column(db.Text)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trainer = db.relationship('User', backref='email_templates')
    
    def __repr__(self):
        return f'<EmailTemplate {self.name}>'


class SMSTemplate(db.Model):
    """SMS template for marketing campaigns."""
    
    __tablename__ = 'sms_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(200), nullable=False)
    message = db.Column(db.String(320), nullable=False)  # SMS limit: 160 chars (single), 320 chars (concatenated)
    category = db.Column(db.String(50))  # reminder, promotion, welcome, follow_up
    
    # AI Generation
    is_ai_generated = db.Column(db.Boolean, default=False)
    ai_prompt = db.Column(db.Text)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trainer = db.relationship('User', backref='sms_templates')
    
    def validate_message_length(self):
        """Validate SMS message length."""
        if self.message and len(self.message) > 320:
            raise ValueError(f"SMS message exceeds 320 character limit (current: {len(self.message)} chars)")
        return True
    
    def get_message_segments(self):
        """Calculate number of SMS segments required."""
        if not self.message:
            return 0
        length = len(self.message)
        if length <= 160:
            return 1
        return (length + 152) // 153  # Concatenated SMS uses 153 chars per segment
    
    def __repr__(self):
        return f'<SMSTemplate {self.name}>'


class MarketingCampaign(db.Model):
    """Marketing campaign for email/SMS flows."""
    
    __tablename__ = 'marketing_campaigns'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    campaign_type = db.Column(db.String(20))  # email, sms, both
    
    # Target Audience
    target_segment = db.Column(db.String(50))  # all_clients, new_clients, inactive_clients, custom
    target_client_ids = db.Column(db.Text)  # JSON array of client IDs
    
    # Schedule
    trigger_type = db.Column(db.String(50))  # immediate, scheduled, event_based
    scheduled_date = db.Column(db.DateTime)
    trigger_event = db.Column(db.String(100))  # client_signup, session_completed, program_end
    
    # Content
    email_template_id = db.Column(db.Integer, db.ForeignKey('email_templates.id'))
    sms_template_id = db.Column(db.Integer, db.ForeignKey('sms_templates.id'))
    
    # Status
    status = db.Column(db.String(20), default='draft')  # draft, active, paused, completed
    
    # Metrics
    sent_count = db.Column(db.Integer, default=0)
    delivered_count = db.Column(db.Integer, default=0)
    opened_count = db.Column(db.Integer, default=0)
    clicked_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    launched_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    
    # Relationships
    trainer = db.relationship('User', backref='campaigns')
    email_template = db.relationship('EmailTemplate')
    sms_template = db.relationship('SMSTemplate')
    
    def get_target_clients(self):
        """Parse target client IDs from JSON."""
        if self.target_client_ids:
            return json.loads(self.target_client_ids)
        return []
    
    def set_target_clients(self, client_ids):
        """Set target client IDs as JSON."""
        self.target_client_ids = json.dumps(client_ids)
    
    def __repr__(self):
        return f'<MarketingCampaign {self.name}>'


class CommunicationLog(db.Model):
    """Log of sent communications."""
    
    __tablename__ = 'communication_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('marketing_campaigns.id'))
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    communication_type = db.Column(db.String(20))  # email, sms
    recipient = db.Column(db.String(200))  # email address or phone number
    subject = db.Column(db.String(300))
    content = db.Column(db.Text)
    
    # Status
    status = db.Column(db.String(20))  # sent, delivered, failed, opened, clicked
    error_message = db.Column(db.Text)
    
    # Engagement
    opened_at = db.Column(db.DateTime)
    clicked_at = db.Column(db.DateTime)
    
    # Timestamps
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    campaign = db.relationship('MarketingCampaign', backref='communications')
    client = db.relationship('Client', backref='communications')
    
    def __repr__(self):
        return f'<CommunicationLog {self.communication_type} to {self.recipient}>'
