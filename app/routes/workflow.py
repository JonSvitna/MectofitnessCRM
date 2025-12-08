"""Workflow and automation routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.flow import WorkflowTemplate, WorkflowExecution, AutomationRule
from datetime import datetime
import json

bp = Blueprint('workflow', __name__, url_prefix='/workflow')


@bp.route('/')
@login_required
def dashboard():
    """Workflow dashboard."""
    templates = WorkflowTemplate.query.filter_by(
        trainer_id=current_user.id,
        is_active=True
    ).count()
    
    active_executions = WorkflowExecution.query.filter_by(
        trainer_id=current_user.id,
        status='active'
    ).count()
    
    automation_rules = AutomationRule.query.filter_by(
        trainer_id=current_user.id,
        is_active=True
    ).count()
    
    recent_executions = WorkflowExecution.query.filter_by(
        trainer_id=current_user.id
    ).order_by(WorkflowExecution.started_at.desc()).limit(10).all()
    
    return render_template('workflow/dashboard.html',
                         templates_count=templates,
                         active_executions=active_executions,
                         automation_rules=automation_rules,
                         recent_executions=recent_executions)


# Workflow Templates
@bp.route('/templates')
@login_required
def list_templates():
    """List workflow templates."""
    templates = WorkflowTemplate.query.filter_by(
        trainer_id=current_user.id
    ).order_by(WorkflowTemplate.created_at.desc()).all()
    return render_template('workflow/templates.html', templates=templates)


@bp.route('/templates/create', methods=['GET', 'POST'])
@login_required
def create_template():
    """Create workflow template."""
    if request.method == 'POST':
        template = WorkflowTemplate(
            trainer_id=current_user.id,
            name=request.form.get('name'),
            description=request.form.get('description'),
            category=request.form.get('category'),
            trigger_type=request.form.get('trigger_type'),
            is_active=True
        )
        
        # Parse workflow steps from form
        steps_json = request.form.get('steps_json')
        if steps_json:
            template.steps = steps_json
        
        db.session.add(template)
        db.session.commit()
        
        flash('Workflow template created!', 'success')
        return redirect(url_for('workflow.view_template', template_id=template.id))
    
    return render_template('workflow/create_template.html')


@bp.route('/templates/<int:template_id>')
@login_required
def view_template(template_id):
    """View workflow template."""
    template = WorkflowTemplate.query.filter_by(
        id=template_id,
        trainer_id=current_user.id
    ).first_or_404()
    
    executions = WorkflowExecution.query.filter_by(
        workflow_template_id=template.id
    ).order_by(WorkflowExecution.started_at.desc()).limit(20).all()
    
    return render_template('workflow/view_template.html',
                         template=template,
                         executions=executions)


# Automation Rules
@bp.route('/automation')
@login_required
def list_automation():
    """List automation rules."""
    rules = AutomationRule.query.filter_by(
        trainer_id=current_user.id
    ).order_by(AutomationRule.created_at.desc()).all()
    return render_template('workflow/automation.html', rules=rules)


@bp.route('/automation/create', methods=['GET', 'POST'])
@login_required
def create_automation():
    """Create automation rule."""
    if request.method == 'POST':
        rule = AutomationRule(
            trainer_id=current_user.id,
            name=request.form.get('name'),
            description=request.form.get('description'),
            trigger_event=request.form.get('trigger_event'),
            action_type=request.form.get('action_type'),
            is_active=True
        )
        
        # Parse conditions and actions from form
        conditions_json = request.form.get('trigger_conditions')
        if conditions_json:
            rule.trigger_conditions = conditions_json
        
        action_config_json = request.form.get('action_config')
        if action_config_json:
            rule.action_config = action_config_json
        
        db.session.add(rule)
        db.session.commit()
        
        flash('Automation rule created!', 'success')
        return redirect(url_for('workflow.list_automation'))
    
    return render_template('workflow/create_automation.html')


@bp.route('/automation/<int:rule_id>/toggle', methods=['POST'])
@login_required
def toggle_automation(rule_id):
    """Toggle automation rule on/off."""
    rule = AutomationRule.query.filter_by(
        id=rule_id,
        trainer_id=current_user.id
    ).first_or_404()
    
    rule.is_active = not rule.is_active
    db.session.commit()
    
    status = 'activated' if rule.is_active else 'deactivated'
    flash(f'Automation rule {status}!', 'success')
    return redirect(url_for('workflow.list_automation'))


# Workflow Executions
@bp.route('/executions')
@login_required
def list_executions():
    """List workflow executions."""
    page = request.args.get('page', 1, type=int)
    executions = WorkflowExecution.query.filter_by(
        trainer_id=current_user.id
    ).order_by(WorkflowExecution.started_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('workflow/executions.html', executions=executions)


@bp.route('/executions/<int:execution_id>')
@login_required
def view_execution(execution_id):
    """View workflow execution details."""
    execution = WorkflowExecution.query.filter_by(
        id=execution_id,
        trainer_id=current_user.id
    ).first_or_404()
    
    return render_template('workflow/view_execution.html', execution=execution)
