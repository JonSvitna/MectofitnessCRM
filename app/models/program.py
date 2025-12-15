"""Training program and exercise models."""
from datetime import datetime, timezone
from app import db


class Program(db.Model):
    """Training program model."""
    
    __tablename__ = 'programs'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    # Program details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    goal = db.Column(db.String(200))
    duration_weeks = db.Column(db.Integer)
    difficulty_level = db.Column(db.String(50))  # beginner, intermediate, advanced
    
    # AI-generated flag
    is_ai_generated = db.Column(db.Boolean, default=False)
    ai_model_version = db.Column(db.String(50))
    
    # Status
    status = db.Column(db.String(20), default='active')  # active, completed, paused
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # Content
    program_data = db.Column(db.Text)  # JSON format for detailed program structure
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    trainer = db.relationship('User', back_populates='programs')
    client = db.relationship('Client', back_populates='programs')
    exercises = db.relationship('Exercise', back_populates='program', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Program {self.name}>'


class Exercise(db.Model):
    """Exercise model for training programs."""
    
    __tablename__ = 'exercises'
    
    id = db.Column(db.Integer, primary_key=True)
    program_id = db.Column(db.Integer, db.ForeignKey('programs.id'), nullable=False)
    
    # Exercise details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    exercise_type = db.Column(db.String(50))  # strength, cardio, flexibility, balance
    muscle_group = db.Column(db.String(100))
    equipment = db.Column(db.String(200))
    
    # Exercise parameters
    sets = db.Column(db.Integer)
    reps = db.Column(db.String(50))  # Can be range like "8-12"
    duration_minutes = db.Column(db.Integer)
    rest_seconds = db.Column(db.Integer)
    weight = db.Column(db.String(50))
    
    # Ordering
    day_number = db.Column(db.Integer)
    order_in_day = db.Column(db.Integer)
    
    # Instructions
    instructions = db.Column(db.Text)
    video_url = db.Column(db.String(200))
    image_url = db.Column(db.String(200))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    program = db.relationship('Program', back_populates='exercises')
    
    def __repr__(self):
        return f'<Exercise {self.name}>'
