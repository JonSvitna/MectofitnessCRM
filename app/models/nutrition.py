"""Nutrition and habit tracking models."""
from datetime import datetime
from app import db
import json


class NutritionPlan(db.Model):
    """Nutrition plan for clients."""
    
    __tablename__ = 'nutrition_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Plan Details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    goal = db.Column(db.String(100))  # weight_loss, muscle_gain, maintenance, performance
    
    # Macros
    daily_calories = db.Column(db.Integer)
    protein_grams = db.Column(db.Integer)
    carbs_grams = db.Column(db.Integer)
    fat_grams = db.Column(db.Integer)
    
    # Meal Structure
    meals_per_day = db.Column(db.Integer, default=3)
    meal_plan_data = db.Column(db.Text)  # JSON structure of meals
    
    # Guidelines
    dietary_preferences = db.Column(db.Text)  # JSON array
    foods_to_avoid = db.Column(db.Text)  # JSON array
    supplements = db.Column(db.Text)
    hydration_target = db.Column(db.Integer)  # ml per day
    
    # Schedule
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # Status
    status = db.Column(db.String(20), default='active')  # active, completed, paused
    
    # AI Generated
    is_ai_generated = db.Column(db.Boolean, default=False)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = db.relationship('Client', backref='nutrition_plans')
    trainer = db.relationship('User', backref='nutrition_plans_created')
    
    def get_meal_plan(self):
        """Parse meal plan from JSON."""
        if self.meal_plan_data:
            return json.loads(self.meal_plan_data)
        return {}
    
    def __repr__(self):
        return f'<NutritionPlan {self.name}>'


class FoodLog(db.Model):
    """Daily food logging for clients."""
    
    __tablename__ = 'food_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    # Date and Meal
    log_date = db.Column(db.Date, nullable=False, index=True)
    meal_type = db.Column(db.String(20))  # breakfast, lunch, dinner, snack
    meal_time = db.Column(db.Time)
    
    # Food Details
    food_name = db.Column(db.String(200), nullable=False)
    serving_size = db.Column(db.String(100))
    quantity = db.Column(db.Float)
    
    # Nutrition Info
    calories = db.Column(db.Integer)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)
    fat = db.Column(db.Float)
    fiber = db.Column(db.Float)
    
    # Photo
    photo_url = db.Column(db.String(500))
    
    # Notes
    notes = db.Column(db.Text)
    
    # Timestamps
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    client = db.relationship('Client', backref='food_logs')
    
    def __repr__(self):
        return f'<FoodLog {self.food_name} on {self.log_date}>'


class Habit(db.Model):
    """Habit definition for tracking."""
    
    __tablename__ = 'habits'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Habit Details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # fitness, nutrition, sleep, wellness, custom
    
    # Frequency
    target_frequency = db.Column(db.String(20))  # daily, weekly, custom
    target_count = db.Column(db.Integer)  # times per period
    
    # Schedule
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)
    
    # Reminder
    reminder_enabled = db.Column(db.Boolean, default=False)
    reminder_time = db.Column(db.Time)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    client = db.relationship('Client', backref='habits')
    trainer = db.relationship('User', backref='habits_created')
    
    def __repr__(self):
        return f'<Habit {self.name}>'


class HabitLog(db.Model):
    """Daily habit tracking log."""
    
    __tablename__ = 'habit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habits.id'), nullable=False)
    
    # Log Details
    log_date = db.Column(db.Date, nullable=False, index=True)
    completed = db.Column(db.Boolean, default=False)
    completion_count = db.Column(db.Integer, default=0)
    
    # Notes
    notes = db.Column(db.Text)
    
    # Timestamps
    logged_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    habit = db.relationship('Habit', backref='logs')
    
    def __repr__(self):
        return f'<HabitLog {self.habit_id} on {self.log_date}>'
