"""Payment and billing models."""
from datetime import datetime, timezone
from app import db
import json


class PaymentPlan(db.Model):
    """Payment plan/package offered by trainer."""
    
    __tablename__ = 'payment_plans'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Plan Details
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    plan_type = db.Column(db.String(50))  # single_session, package, monthly, annual
    
    # Pricing
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    
    # Session Details (if applicable)
    sessions_included = db.Column(db.Integer)
    session_duration_minutes = db.Column(db.Integer)
    
    # Billing
    billing_frequency = db.Column(db.String(20))  # one_time, monthly, weekly, annual
    trial_period_days = db.Column(db.Integer, default=0)
    
    # Features
    features = db.Column(db.Text)  # JSON array of included features
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    is_public = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    trainer = db.relationship('User', backref='payment_plans')
    
    def get_features(self):
        """Parse features from JSON."""
        if self.features:
            return json.loads(self.features)
        return []
    
    def __repr__(self):
        return f'<PaymentPlan {self.name}>'


class Subscription(db.Model):
    """Client subscription to a payment plan."""
    
    __tablename__ = 'subscriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    payment_plan_id = db.Column(db.Integer, db.ForeignKey('payment_plans.id'), nullable=False)
    
    # Subscription Details
    status = db.Column(db.String(20), default='active')  # active, paused, cancelled, expired
    
    # Dates
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date)
    next_billing_date = db.Column(db.Date)
    cancelled_at = db.Column(db.DateTime)
    
    # Usage
    sessions_used = db.Column(db.Integer, default=0)
    sessions_remaining = db.Column(db.Integer)
    
    # Payment Integration
    stripe_subscription_id = db.Column(db.String(200))
    stripe_customer_id = db.Column(db.String(200))
    
    # Notes
    cancellation_reason = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    client = db.relationship('Client', backref='subscriptions')
    payment_plan = db.relationship('PaymentPlan', backref='subscriptions')
    
    def __repr__(self):
        return f'<Subscription {self.id} - {self.status}>'


class Payment(db.Model):
    """Payment transactions."""
    
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    subscription_id = db.Column(db.Integer, db.ForeignKey('subscriptions.id'))
    
    # Payment Details
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    payment_method = db.Column(db.String(50))  # card, bank_transfer, cash, stripe
    
    # Status
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    
    # Payment Gateway
    stripe_payment_intent_id = db.Column(db.String(200))
    stripe_charge_id = db.Column(db.String(200))
    
    # Metadata
    description = db.Column(db.Text)
    receipt_url = db.Column(db.String(500))
    
    # Refund
    refund_amount = db.Column(db.Float)
    refund_reason = db.Column(db.Text)
    refunded_at = db.Column(db.DateTime)
    
    # Timestamps
    payment_date = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Relationships
    client = db.relationship('Client', backref='payments')
    subscription = db.relationship('Subscription', backref='payments')
    
    def __repr__(self):
        return f'<Payment {self.id} - {self.amount} {self.currency}>'


class Invoice(db.Model):
    """Invoice for services."""
    
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    
    # Invoice Details
    invoice_number = db.Column(db.String(50), unique=True, nullable=False)
    invoice_date = db.Column(db.Date, nullable=False)
    due_date = db.Column(db.Date)
    
    # Amounts
    subtotal = db.Column(db.Float, nullable=False)
    tax_amount = db.Column(db.Float, default=0)
    discount_amount = db.Column(db.Float, default=0)
    total_amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='USD')
    
    # Line Items
    items = db.Column(db.Text)  # JSON array of invoice items
    
    # Status
    status = db.Column(db.String(20), default='draft')  # draft, sent, paid, overdue, cancelled
    paid_at = db.Column(db.DateTime)
    
    # Payment
    payment_id = db.Column(db.Integer, db.ForeignKey('payments.id'))
    
    # Notes
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    trainer = db.relationship('User', backref='invoices')
    client = db.relationship('Client', backref='invoices')
    payment = db.relationship('Payment', backref='invoice', uselist=False)
    
    def get_items(self):
        """Parse invoice items from JSON."""
        if self.items:
            return json.loads(self.items)
        return []
    
    def __repr__(self):
        return f'<Invoice {self.invoice_number}>'
