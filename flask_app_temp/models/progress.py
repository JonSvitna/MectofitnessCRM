"""Progress tracking models."""
from datetime import datetime, timezone
from app import db
import json


class ProgressPhoto(db.Model):
    """Client progress photos."""
    
    __tablename__ = 'progress_photos'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Photo Information
    photo_url = db.Column(db.String(500), nullable=False)
    thumbnail_url = db.Column(db.String(500))
    photo_type = db.Column(db.String(20))  # front, back, side, custom
    
    # Context
    caption = db.Column(db.Text)
    weight_at_time = db.Column(db.Float)
    body_fat_at_time = db.Column(db.Float)
    
    # Privacy
    is_visible_to_client = db.Column(db.Boolean, default=True)
    is_public = db.Column(db.Boolean, default=False)
    
    # Timestamps
    taken_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    uploaded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    client = db.relationship('Client', backref='progress_photos')
    trainer = db.relationship('User', backref='uploaded_photos')
    
    def __repr__(self):
        return f'<ProgressPhoto {self.id} for Client {self.client_id}>'


class CustomMetric(db.Model):
    """Custom metrics definition for tracking."""
    
    __tablename__ = 'custom_metrics'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Metric Definition
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    unit = db.Column(db.String(20))  # kg, lbs, cm, inches, reps, seconds, etc.
    metric_type = db.Column(db.String(20))  # numeric, percentage, boolean, text
    
    # Display
    display_format = db.Column(db.String(50))
    chart_type = db.Column(db.String(20))  # line, bar, area
    
    # Validation
    min_value = db.Column(db.Float)
    max_value = db.Column(db.Float)
    
    # Goal tracking
    is_goal_metric = db.Column(db.Boolean, default=False)
    goal_direction = db.Column(db.String(20))  # increase, decrease, maintain
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    trainer = db.relationship('User', backref='custom_metrics')
    
    def __repr__(self):
        return f'<CustomMetric {self.name}>'


class ProgressEntry(db.Model):
    """Progress tracking entries for clients."""
    
    __tablename__ = 'progress_entries'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Entry Date
    entry_date = db.Column(db.Date, nullable=False, index=True)
    
    # Standard Metrics
    weight = db.Column(db.Float)
    body_fat_percentage = db.Column(db.Float)
    muscle_mass = db.Column(db.Float)
    
    # Body Measurements (cm or inches)
    chest = db.Column(db.Float)
    waist = db.Column(db.Float)
    hips = db.Column(db.Float)
    thigh = db.Column(db.Float)
    arm = db.Column(db.Float)
    
    # Custom Metrics (JSON)
    custom_metrics_data = db.Column(db.Text)  # JSON: {metric_id: value}
    
    # Notes
    notes = db.Column(db.Text)
    mood_rating = db.Column(db.Integer)  # 1-10
    energy_level = db.Column(db.Integer)  # 1-10
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    client = db.relationship('Client', backref='progress_entries')
    trainer = db.relationship('User', backref='tracked_progress')
    
    def get_custom_metrics(self):
        """Parse custom metrics from JSON."""
        if self.custom_metrics_data:
            return json.loads(self.custom_metrics_data)
        return {}
    
    def set_custom_metric(self, metric_id, value):
        """Set a custom metric value."""
        metrics = self.get_custom_metrics()
        metrics[str(metric_id)] = value
        self.custom_metrics_data = json.dumps(metrics)
    
    def __repr__(self):
        return f'<ProgressEntry {self.entry_date} for Client {self.client_id}>'
