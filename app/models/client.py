"""Client model for gym members and training clients."""
from datetime import datetime, timezone
from app import db


class Client(db.Model):
    """Client model representing gym members or personal training clients."""
    
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    first_name = db.Column(db.String(64), nullable=False)
    last_name = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(120), nullable=False, index=True)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date)
    gender = db.Column(db.String(20))
    address = db.Column(db.String(200))
    emergency_contact = db.Column(db.String(100))
    emergency_phone = db.Column(db.String(20))
    
    # Fitness data
    fitness_goal = db.Column(db.String(200))
    medical_conditions = db.Column(db.Text)
    fitness_level = db.Column(db.String(50))
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    
    # Membership
    membership_type = db.Column(db.String(50))
    membership_start = db.Column(db.Date)
    membership_end = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True)
    
    # Notes
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    trainer = db.relationship('User', back_populates='clients')
    sessions = db.relationship('Session', back_populates='client', lazy='dynamic')
    programs = db.relationship('Program', back_populates='client', lazy='dynamic')
    
    @property
    def full_name(self):
        """Return full name."""
        return f"{self.first_name} {self.last_name}"
    
    def __repr__(self):
        return f'<Client {self.full_name}>'
