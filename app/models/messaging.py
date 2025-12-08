"""In-app messaging models."""
from datetime import datetime
from app import db


class Message(db.Model):
    """In-app messaging between trainers and clients."""
    
    __tablename__ = 'messages'
    
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    recipient_type = db.Column(db.String(20), nullable=False)  # trainer, client
    recipient_id = db.Column(db.Integer, nullable=False)  # Can be User or Client ID
    
    # Message Content
    subject = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    message_type = db.Column(db.String(20), default='text')  # text, image, video, file
    attachment_url = db.Column(db.String(500))
    
    # Thread Management
    thread_id = db.Column(db.String(100), index=True)
    parent_message_id = db.Column(db.Integer, db.ForeignKey('messages.id'))
    
    # Status
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    is_archived = db.Column(db.Boolean, default=False)
    is_deleted = db.Column(db.Boolean, default=False)
    
    # Timestamps
    sent_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    sender = db.relationship('User', foreign_keys=[sender_id], backref='sent_messages')
    replies = db.relationship('Message', backref=db.backref('parent', remote_side=[id]))
    
    def mark_as_read(self):
        """Mark message as read."""
        if not self.is_read:
            self.is_read = True
            self.read_at = datetime.utcnow()
    
    def __repr__(self):
        return f'<Message {self.id} from User {self.sender_id}>'


class MessageNotification(db.Model):
    """Notification settings for messages."""
    
    __tablename__ = 'message_notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # Notification Preferences
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)
    sms_notifications = db.Column(db.Boolean, default=False)
    
    # Quiet Hours
    quiet_hours_enabled = db.Column(db.Boolean, default=False)
    quiet_hours_start = db.Column(db.Time)
    quiet_hours_end = db.Column(db.Time)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = db.relationship('User', backref='message_settings', uselist=False)
    
    def __repr__(self):
        return f'<MessageNotification for User {self.user_id}>'
