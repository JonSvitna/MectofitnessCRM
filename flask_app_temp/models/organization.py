"""Organization model for multi-tenant support."""
from datetime import datetime, timezone
from app import db


class Organization(db.Model):
    """Organization/Tenant model - each trainer/business is an organization."""
    
    __tablename__ = 'organizations'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Organization Details
    name = db.Column(db.String(200), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)  # URL-friendly identifier
    
    # Business Information
    business_type = db.Column(db.String(50))  # personal_trainer, gym, studio, wellness_center
    website = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    
    # Address
    address_line1 = db.Column(db.String(200))
    address_line2 = db.Column(db.String(200))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
    country = db.Column(db.String(100), default='USA')
    
    # Subscription & Limits
    subscription_tier = db.Column(db.String(50), default='free')  # free, basic, pro, enterprise
    max_trainers = db.Column(db.Integer, default=1)  # How many trainers can be in this org
    max_clients = db.Column(db.Integer, default=10)  # Client limit based on tier
    
    # Branding
    logo_url = db.Column(db.String(500))
    primary_color = db.Column(db.String(7))  # Hex color
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    users = db.relationship('User', backref='organization', lazy='dynamic')
    
    def __repr__(self):
        return f'<Organization {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'business_type': self.business_type,
            'subscription_tier': self.subscription_tier,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat()
        }
    
    @property
    def trainer_count(self):
        """Count trainers in organization."""
        return self.users.filter_by(role='trainer').count()
    
    @property
    def client_count(self):
        """Count clients in organization."""
        from app.models.client import Client
        trainer_ids = [u.id for u in self.users.filter(db.or_(
            User.role == 'trainer',
            User.role == 'admin',
            User.role == 'owner'
        )).all()]
        return Client.query.filter(Client.trainer_id.in_(trainer_ids)).count()


# Import User here to avoid circular import
from app.models.user import User
