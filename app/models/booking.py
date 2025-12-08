"""Online booking system models."""
from datetime import datetime, time
from app import db
import json


class BookingAvailability(db.Model):
    """Trainer availability for online booking."""
    
    __tablename__ = 'booking_availability'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Day of Week (0=Monday, 6=Sunday)
    day_of_week = db.Column(db.Integer, nullable=False)
    
    # Time Slots
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    
    # Session Details
    session_type = db.Column(db.String(50))  # personal, group, online, assessment
    max_bookings = db.Column(db.Integer, default=1)
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trainer = db.relationship('User', backref='availability_slots')
    
    def __repr__(self):
        return f'<BookingAvailability Day {self.day_of_week} {self.start_time}-{self.end_time}>'


class BookingException(db.Model):
    """Exceptions to regular availability (holidays, vacations, etc)."""
    
    __tablename__ = 'booking_exceptions'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Date Range
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    
    # Exception Type
    exception_type = db.Column(db.String(50))  # unavailable, special_hours, holiday
    
    # Special Hours (if applicable)
    special_start_time = db.Column(db.Time)
    special_end_time = db.Column(db.Time)
    
    # Description
    reason = db.Column(db.String(200))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    trainer = db.relationship('User', backref='booking_exceptions')
    
    def __repr__(self):
        return f'<BookingException {self.start_date} to {self.end_date}>'


class OnlineBooking(db.Model):
    """Client online booking requests."""
    
    __tablename__ = 'online_bookings'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'))
    
    # Guest Booking (for new clients)
    guest_name = db.Column(db.String(200))
    guest_email = db.Column(db.String(200))
    guest_phone = db.Column(db.String(20))
    
    # Booking Details
    requested_date = db.Column(db.Date, nullable=False)
    requested_time = db.Column(db.Time, nullable=False)
    duration_minutes = db.Column(db.Integer, default=60)
    session_type = db.Column(db.String(50))
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, confirmed, declined, cancelled
    
    # Notes
    client_notes = db.Column(db.Text)
    trainer_notes = db.Column(db.Text)
    decline_reason = db.Column(db.Text)
    
    # Converted Session
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id'))
    
    # Timestamps
    requested_at = db.Column(db.DateTime, default=datetime.utcnow)
    confirmed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    
    # Relationships
    trainer = db.relationship('User', backref='booking_requests')
    client = db.relationship('Client', backref='booking_requests')
    session = db.relationship('Session', backref='booking', uselist=False)
    
    @property
    def contact_name(self):
        """Get contact name (client or guest)."""
        if self.client:
            return self.client.full_name
        return self.guest_name
    
    @property
    def contact_email(self):
        """Get contact email (client or guest)."""
        if self.client:
            return self.client.email
        return self.guest_email
    
    def __repr__(self):
        return f'<OnlineBooking {self.id} - {self.status}>'


class BookingSettings(db.Model):
    """Booking system settings for trainers."""
    
    __tablename__ = 'booking_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # General Settings
    enable_online_booking = db.Column(db.Boolean, default=True)
    require_approval = db.Column(db.Boolean, default=True)
    allow_guest_booking = db.Column(db.Boolean, default=True)
    
    # Booking Window
    min_advance_hours = db.Column(db.Integer, default=24)  # Minimum hours in advance
    max_advance_days = db.Column(db.Integer, default=30)  # Maximum days in advance
    
    # Session Settings
    default_session_duration = db.Column(db.Integer, default=60)
    buffer_time_minutes = db.Column(db.Integer, default=15)  # Time between sessions
    
    # Cancellation Policy
    cancellation_hours = db.Column(db.Integer, default=24)
    cancellation_fee_percentage = db.Column(db.Integer, default=0)
    
    # Notifications
    notify_new_booking = db.Column(db.Boolean, default=True)
    notify_cancellation = db.Column(db.Boolean, default=True)
    send_booking_reminders = db.Column(db.Boolean, default=True)
    reminder_hours_before = db.Column(db.Integer, default=24)
    
    # Public Booking Page
    booking_page_slug = db.Column(db.String(100), unique=True)
    booking_page_title = db.Column(db.String(200))
    booking_page_description = db.Column(db.Text)
    booking_page_image_url = db.Column(db.String(500))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trainer = db.relationship('User', backref='booking_settings', uselist=False)
    
    def __repr__(self):
        return f'<BookingSettings for Trainer {self.trainer_id}>'
