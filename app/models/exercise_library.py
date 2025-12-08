"""Exercise library for workout program builder."""
from datetime import datetime
from app import db
import json


class ExerciseLibrary(db.Model):
    """Master exercise library with detailed information."""
    
    __tablename__ = 'exercise_library'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # Basic Information
    name = db.Column(db.String(200), nullable=False, index=True)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # strength, cardio, flexibility, balance, mobility
    
    # Targeting
    primary_muscle_groups = db.Column(db.Text)  # JSON array
    secondary_muscle_groups = db.Column(db.Text)  # JSON array
    
    # Classification
    difficulty_level = db.Column(db.String(20))  # beginner, intermediate, advanced
    equipment_required = db.Column(db.Text)  # JSON array
    exercise_type = db.Column(db.String(50))  # compound, isolation, bodyweight, cardio
    
    # Instructions
    setup_instructions = db.Column(db.Text)
    execution_steps = db.Column(db.Text)  # JSON array of steps
    common_mistakes = db.Column(db.Text)  # JSON array
    tips_and_cues = db.Column(db.Text)  # JSON array
    
    # Media
    image_url = db.Column(db.String(300))
    video_url = db.Column(db.String(300))
    animation_url = db.Column(db.String(300))
    
    # Modifications & Alternatives
    easier_variations = db.Column(db.Text)  # JSON array of exercise IDs
    harder_variations = db.Column(db.Text)  # JSON array of exercise IDs
    alternative_exercises = db.Column(db.Text)  # JSON array of exercise IDs
    
    # Safety & Contraindications
    contraindications = db.Column(db.Text)  # JSON array
    injury_considerations = db.Column(db.Text)
    
    # Metrics
    typical_sets = db.Column(db.String(20))  # e.g., "3-4"
    typical_reps = db.Column(db.String(20))  # e.g., "8-12"
    typical_rest_seconds = db.Column(db.Integer)
    
    # Tags for searching
    tags = db.Column(db.Text)  # JSON array
    
    # Popularity & Usage
    usage_count = db.Column(db.Integer, default=0)
    average_rating = db.Column(db.Float)
    
    # Source
    is_custom = db.Column(db.Boolean, default=False)
    created_by_trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_public = db.Column(db.Boolean, default=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='custom_exercises', foreign_keys=[created_by_trainer_id])
    
    def get_primary_muscles(self):
        """Parse primary muscle groups from JSON."""
        if self.primary_muscle_groups:
            return json.loads(self.primary_muscle_groups)
        return []
    
    def get_equipment(self):
        """Parse equipment from JSON."""
        if self.equipment_required:
            return json.loads(self.equipment_required)
        return []
    
    def get_execution_steps(self):
        """Parse execution steps from JSON."""
        if self.execution_steps:
            return json.loads(self.execution_steps)
        return []
    
    def get_tags(self):
        """Parse tags from JSON."""
        if self.tags:
            return json.loads(self.tags)
        return []
    
    def increment_usage(self):
        """Increment usage counter."""
        self.usage_count += 1
    
    def __repr__(self):
        return f'<ExerciseLibrary {self.name}>'


class ProgramTemplate(db.Model):
    """Pre-built program templates for quick program creation."""
    
    __tablename__ = 'program_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Target Audience
    target_level = db.Column(db.String(20))  # beginner, intermediate, advanced
    target_goal = db.Column(db.String(100))  # weight_loss, muscle_gain, strength, endurance
    
    # Program Structure
    duration_weeks = db.Column(db.Integer)
    sessions_per_week = db.Column(db.Integer)
    session_duration_minutes = db.Column(db.Integer)
    
    # Template Data
    template_data = db.Column(db.Text)  # JSON structure of the full program
    
    # Equipment
    required_equipment = db.Column(db.Text)  # JSON array
    
    # Popularity
    usage_count = db.Column(db.Integer, default=0)
    rating = db.Column(db.Float)
    
    # Source
    is_official = db.Column(db.Boolean, default=False)
    created_by_trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    is_public = db.Column(db.Boolean, default=True)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    creator = db.relationship('User', backref='program_templates', foreign_keys=[created_by_trainer_id])
    
    def get_template_data(self):
        """Parse template data from JSON."""
        if self.template_data:
            return json.loads(self.template_data)
        return {}
    
    def __repr__(self):
        return f'<ProgramTemplate {self.name}>'
