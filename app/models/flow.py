"""Workflow and flow management models."""
from datetime import datetime, timezone
from app import db
import json


class WorkflowTemplate(db.Model):
    """Workflow template for automation."""
    
    __tablename__ = 'workflow_templates'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    category = db.Column(db.String(50))  # onboarding, training, follow_up, retention
    
    # Trigger Configuration
    trigger_type = db.Column(db.String(50))  # client_signup, intake_complete, session_complete, program_end
    trigger_config = db.Column(db.Text)  # JSON configuration
    
    # Workflow Steps
    steps = db.Column(db.Text)  # JSON array of workflow steps
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    trainer = db.relationship('User', backref='workflow_templates')
    
    def get_steps(self):
        """Parse workflow steps from JSON."""
        if self.steps:
            return json.loads(self.steps)
        return []
    
    def set_steps(self, steps):
        """Set workflow steps as JSON."""
        self.steps = json.dumps(steps)
    
    def __repr__(self):
        return f'<WorkflowTemplate {self.name}>'


class WorkflowExecution(db.Model):
    """Active workflow execution instance."""
    
    __tablename__ = 'workflow_executions'
    
    id = db.Column(db.Integer, primary_key=True)
    workflow_template_id = db.Column(db.Integer, db.ForeignKey('workflow_templates.id'), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # Execution State
    current_step = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='active')  # active, paused, completed, cancelled
    
    # Step History
    completed_steps = db.Column(db.Text)  # JSON array of completed step IDs with timestamps
    
    # Timestamps
    started_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    completed_at = db.Column(db.DateTime)
    next_step_at = db.Column(db.DateTime)
    
    # Relationships
    workflow_template = db.relationship('WorkflowTemplate', backref='executions')
    client = db.relationship('Client', backref='workflow_executions')
    trainer = db.relationship('User', backref='workflow_executions')
    
    def get_completed_steps(self):
        """Parse completed steps from JSON."""
        if self.completed_steps:
            return json.loads(self.completed_steps)
        return []
    
    def add_completed_step(self, step_id):
        """Add a completed step."""
        steps = self.get_completed_steps()
        steps.append({
            'step_id': step_id,
            'completed_at': datetime.now(timezone.utc).isoformat()
        })
        self.completed_steps = json.dumps(steps)
    
    def __repr__(self):
        return f'<WorkflowExecution {self.id} - {self.status}>'


class AutomationRule(db.Model):
    """Automation rules for triggering actions."""
    
    __tablename__ = 'automation_rules'
    
    id = db.Column(db.Integer, primary_key=True)
    trainer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Trigger Conditions
    trigger_event = db.Column(db.String(100))  # session_no_show, client_inactive, program_complete
    trigger_conditions = db.Column(db.Text)  # JSON object with conditions
    
    # Actions
    action_type = db.Column(db.String(50))  # send_email, send_sms, create_task, assign_program
    action_config = db.Column(db.Text)  # JSON configuration for the action
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    
    # Execution History
    last_triggered_at = db.Column(db.DateTime)
    trigger_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationships
    trainer = db.relationship('User', backref='automation_rules')
    
    def get_trigger_conditions(self):
        """Parse trigger conditions from JSON."""
        if self.trigger_conditions:
            return json.loads(self.trigger_conditions)
        return {}
    
    def get_action_config(self):
        """Parse action configuration from JSON."""
        if self.action_config:
            return json.loads(self.action_config)
        return {}
    
    def __repr__(self):
        return f'<AutomationRule {self.name}>'
