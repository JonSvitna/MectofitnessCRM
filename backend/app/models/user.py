"""User model for personal trainers."""
from datetime import datetime, timezone
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db


class User(UserMixin, db.Model):
    """Personal trainer user model."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    
    # Organization & RBAC
    organization_id = db.Column(db.Integer, db.ForeignKey('organizations.id'), nullable=True)
    role = db.Column(db.String(20), default='trainer')  # owner, admin, trainer, client
    
    first_name = db.Column(db.String(64))
    last_name = db.Column(db.String(64))
    phone = db.Column(db.String(20))
    specialization = db.Column(db.String(200))
    certification = db.Column(db.String(200))
    bio = db.Column(db.Text)
    profile_image = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    clients = db.relationship('Client', back_populates='trainer', lazy='dynamic')
    sessions = db.relationship('Session', back_populates='trainer', lazy='dynamic')
    programs = db.relationship('Program', back_populates='trainer', lazy='dynamic')
    calendar_integrations = db.relationship('CalendarIntegration', back_populates='user', lazy='dynamic')
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check password against hash."""
        return check_password_hash(self.password_hash, password)
    
    @property
    def full_name(self):
        """Return full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    # RBAC Permission Checks
    def is_owner(self):
        """Check if user is organization owner."""
        return self.role == 'owner'
    
    def is_admin(self):
        """Check if user is admin or owner."""
        return self.role in ['owner', 'admin']
    
    def is_trainer(self):
        """Check if user is trainer, admin, or owner."""
        return self.role in ['owner', 'admin', 'trainer']
    
    def is_client_user(self):
        """Check if user is a client (read-only access)."""
        return self.role == 'client'
    
    def can_manage_organization(self):
        """Check if user can manage organization settings."""
        return self.role == 'owner'
    
    def can_manage_users(self):
        """Check if user can manage other users."""
        return self.role in ['owner', 'admin']
    
    def can_access_client_data(self, client_id):
        """Check if user can access specific client data."""
        if self.is_admin():
            # Admins can access all clients in their organization
            from app.models.client import Client
            client = Client.query.get(client_id)
            if client:
                trainer = User.query.get(client.trainer_id)
                return trainer and trainer.organization_id == self.organization_id
        elif self.is_trainer():
            # Trainers can only access their own clients
            from app.models.client import Client
            client = Client.query.get(client_id)
            return client and client.trainer_id == self.id
        return False
    
    # CRUD Methods
    @classmethod
    def create_user(cls, username, email, password, **kwargs):
        """
        Create a new user with proper error handling.
        
        Args:
            username: Unique username
            email: Unique email address
            password: Plain text password (will be hashed)
            **kwargs: Additional user attributes (first_name, last_name, etc.)
        
        Returns:
            tuple: (User object or None, error message or None)
        """
        try:
            # Validate required fields
            if not username or not email or not password:
                return None, "Username, email, and password are required"
            
            # Check if username already exists
            if cls.query.filter_by(username=username).first():
                return None, "Username already exists"
            
            # Check if email already exists
            if cls.query.filter_by(email=email).first():
                return None, "Email already registered"
            
            # Create new user
            user = cls(username=username, email=email, **kwargs)
            user.set_password(password)
            
            db.session.add(user)
            db.session.commit()
            
            return user, None
            
        except Exception as e:
            db.session.rollback()
            return None, f"Failed to create user: {str(e)}"
    
    @classmethod
    def get_by_id(cls, user_id):
        """
        Get user by ID with error handling.
        
        Args:
            user_id: User ID
        
        Returns:
            User object or None
        """
        try:
            return db.session.get(cls, user_id)
        except Exception:
            return None
    
    @classmethod
    def get_by_username(cls, username):
        """
        Get user by username with error handling.
        
        Args:
            username: Username to search for
        
        Returns:
            User object or None
        """
        try:
            return cls.query.filter_by(username=username).first()
        except Exception:
            return None
    
    @classmethod
    def get_by_email(cls, email):
        """
        Get user by email with error handling.
        
        Args:
            email: Email to search for
        
        Returns:
            User object or None
        """
        try:
            return cls.query.filter_by(email=email).first()
        except Exception:
            return None
    
    @classmethod
    def authenticate(cls, username, password):
        """
        Authenticate user with username and password.
        
        Args:
            username: Username or email
            password: Plain text password
        
        Returns:
            tuple: (User object or None, error message or None)
        """
        try:
            # Try to find user by username or email
            user = cls.query.filter(
                (cls.username == username) | (cls.email == username)
            ).first()
            
            if not user:
                return None, "Invalid username or password"
            
            if not user.is_active:
                return None, "Account is disabled"
            
            if not user.check_password(password):
                return None, "Invalid username or password"
            
            return user, None
            
        except Exception as e:
            return None, f"Authentication failed: {str(e)}"
    
    # Fields that cannot be updated via update_profile
    PROTECTED_FIELDS = ['id', 'password_hash', 'created_at']
    
    def update_profile(self, **kwargs):
        """
        Update user profile with error handling.
        
        Args:
            **kwargs: Attributes to update
        
        Returns:
            tuple: (success boolean, error message or None)
        """
        try:
            for key, value in kwargs.items():
                if hasattr(self, key) and key not in self.PROTECTED_FIELDS:
                    setattr(self, key, value)
            
            self.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to update profile: {str(e)}"
    
    def change_password(self, old_password, new_password):
        """
        Change user password with validation.
        
        Args:
            old_password: Current password
            new_password: New password
        
        Returns:
            tuple: (success boolean, error message or None)
        """
        try:
            if not self.check_password(old_password):
                return False, "Current password is incorrect"
            
            if len(new_password) < 8:
                return False, "New password must be at least 8 characters"
            
            self.set_password(new_password)
            self.updated_at = datetime.now(timezone.utc)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to change password: {str(e)}"
    
    def delete_user(self):
        """
        Delete user with error handling.
        
        Returns:
            tuple: (success boolean, error message or None)
        """
        try:
            db.session.delete(self)
            db.session.commit()
            return True, None
            
        except Exception as e:
            db.session.rollback()
            return False, f"Failed to delete user: {str(e)}"
    
    def __repr__(self):
        return f'<User {self.username}>'
