"""Client intake form model."""
from datetime import datetime
from app import db
import json


class ClientIntake(db.Model):
    """Client intake questionnaire and responses."""
    
    __tablename__ = 'client_intakes'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Basic Health & Fitness Information
    age = db.Column(db.Integer)
    fitness_experience = db.Column(db.String(50))  # beginner, intermediate, advanced
    current_activity_level = db.Column(db.String(50))  # sedentary, lightly_active, moderately_active, very_active
    
    # Goals
    primary_goal = db.Column(db.String(200))
    secondary_goals = db.Column(db.Text)  # JSON array
    target_timeline = db.Column(db.String(50))  # 4_weeks, 8_weeks, 12_weeks, 6_months, 1_year
    
    # Physical Stats
    current_weight = db.Column(db.Float)
    target_weight = db.Column(db.Float)
    height_cm = db.Column(db.Float)
    body_fat_percentage = db.Column(db.Float)
    
    # Availability & Preferences
    sessions_per_week = db.Column(db.Integer)
    preferred_session_duration = db.Column(db.Integer)  # minutes
    preferred_training_time = db.Column(db.String(50))  # morning, afternoon, evening
    training_location = db.Column(db.String(100))  # gym, home, outdoor
    
    # Equipment Access
    available_equipment = db.Column(db.Text)  # JSON array
    
    # Health & Medical
    medical_conditions = db.Column(db.Text)
    injuries = db.Column(db.Text)
    medications = db.Column(db.Text)
    limitations = db.Column(db.Text)
    
    # Exercise Preferences
    preferred_exercises = db.Column(db.Text)  # JSON array
    disliked_exercises = db.Column(db.Text)  # JSON array
    
    # Nutrition
    dietary_restrictions = db.Column(db.Text)
    nutrition_plan_interest = db.Column(db.Boolean, default=False)
    
    # Motivation & Support
    motivation_level = db.Column(db.Integer)  # 1-10
    support_system = db.Column(db.Text)
    previous_challenges = db.Column(db.Text)
    
    # AI Program Generation
    ai_generated_program_id = db.Column(db.Integer, db.ForeignKey('programs.id'))
    ai_recommendations = db.Column(db.Text)  # JSON object with AI insights
    
    # Document Signing
    documents_signed = db.Column(db.Boolean, default=False)
    signature_data = db.Column(db.Text)  # Base64 encoded signature image
    signed_at = db.Column(db.DateTime)
    
    # Progress Photos
    photos_uploaded = db.Column(db.Boolean, default=False)
    photo_front = db.Column(db.String(500))  # File path or URL
    photo_side_left = db.Column(db.String(500))
    photo_side_right = db.Column(db.String(500))
    photo_back = db.Column(db.String(500))
    photos_uploaded_at = db.Column(db.DateTime)
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, form_completed, documents_signed, completed, reviewed, program_assigned
    completed_at = db.Column(db.DateTime)
    reviewed_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = db.relationship('Client', backref='intakes')
    trainer = db.relationship('User', backref='client_intakes')
    generated_program = db.relationship('Program', foreign_keys=[ai_generated_program_id])
    
    def get_secondary_goals(self):
        """Parse secondary goals from JSON."""
        if self.secondary_goals:
            return json.loads(self.secondary_goals)
        return []
    
    def set_secondary_goals(self, goals):
        """Set secondary goals as JSON."""
        self.secondary_goals = json.dumps(goals)
    
    def get_available_equipment(self):
        """Parse equipment from JSON."""
        if self.available_equipment:
            return json.loads(self.available_equipment)
        return []
    
    def set_available_equipment(self, equipment):
        """Set equipment as JSON."""
        self.available_equipment = json.dumps(equipment)
    
    def calculate_bmi(self):
        """Calculate BMI if height and weight are available."""
        if self.height_cm and self.current_weight:
            height_m = self.height_cm / 100
            return round(self.current_weight / (height_m ** 2), 1)
        return None
    
    def __repr__(self):
        return f'<ClientIntake {self.client_id} - {self.status}>'
