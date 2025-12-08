"""Training session model."""
from datetime import datetime
from app import db


class Session(db.Model):
    """Training session model."""
    
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    # Session details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    session_type = db.Column(db.String(50))  # personal, group, online, assessment
    location = db.Column(db.String(200))
    
    # Scheduling
    scheduled_start = db.Column(db.DateTime, nullable=False)
    scheduled_end = db.Column(db.DateTime, nullable=False)
    actual_start = db.Column(db.DateTime)
    actual_end = db.Column(db.DateTime)
    
    # Status
    status = db.Column(db.String(20), default='scheduled')  # scheduled, completed, cancelled, no-show
    
    # Session data
    exercises_performed = db.Column(db.Text)
    notes = db.Column(db.Text)
    client_feedback = db.Column(db.Text)
    trainer_notes = db.Column(db.Text)
    
    # Calendar sync
    google_event_id = db.Column(db.String(200))
    outlook_event_id = db.Column(db.String(200))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trainer = db.relationship('User', back_populates='sessions')
    client = db.relationship('Client', back_populates='sessions')
    
    def __repr__(self):
        return f'<Session {self.title} - {self.scheduled_start}>'
