"""Database models for MectoFitness Backend API."""
from datetime import datetime
from app import db


class Lead(db.Model):
    """Model for capturing user leads from the landing page."""
    
    __tablename__ = 'leads'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    phone = db.Column(db.String(50), nullable=True)
    business_type = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=True)
    source = db.Column(db.String(100), default='landing_page')
    status = db.Column(db.String(50), default='new')  # new, contacted, converted, etc.
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Lead {self.email}>'
    
    def to_dict(self):
        """Convert model to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'business_type': self.business_type,
            'message': self.message,
            'source': self.source,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }
