"""Client intake form routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.client import Client
from app.models.intake import ClientIntake
from app.models.program import Program
from app.models.settings import TrainerSettings
from datetime import datetime
import json

bp = Blueprint('intake', __name__, url_prefix='/intake')


@bp.route('/')
@login_required
def list_intakes():
    """List all client intakes."""
    page = request.args.get('page', 1, type=int)
    intakes = ClientIntake.query.filter_by(
        trainer_id=current_user.id
    ).order_by(ClientIntake.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('intake/list.html', intakes=intakes)


@bp.route('/create/<int:client_id>', methods=['GET', 'POST'])
@login_required
def create_intake(client_id):
    """Create new client intake form."""
    client = Client.query.filter_by(id=client_id, trainer_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        intake = ClientIntake(
            client_id=client.id,
            trainer_id=current_user.id,
            age=request.form.get('age', type=int),
            fitness_experience=request.form.get('fitness_experience'),
            current_activity_level=request.form.get('current_activity_level'),
            primary_goal=request.form.get('primary_goal'),
            target_timeline=request.form.get('target_timeline'),
            current_weight=request.form.get('current_weight', type=float),
            target_weight=request.form.get('target_weight', type=float),
            height_cm=request.form.get('height_cm', type=float),
            sessions_per_week=request.form.get('sessions_per_week', type=int),
            preferred_session_duration=request.form.get('preferred_session_duration', type=int),
            preferred_training_time=request.form.get('preferred_training_time'),
            training_location=request.form.get('training_location'),
            medical_conditions=request.form.get('medical_conditions'),
            injuries=request.form.get('injuries'),
            dietary_restrictions=request.form.get('dietary_restrictions'),
            motivation_level=request.form.get('motivation_level', type=int),
            status='pending',
            completed_at=datetime.utcnow()
        )
        
        # Handle equipment as JSON
        equipment = request.form.getlist('equipment')
        intake.set_available_equipment(equipment)
        
        # Handle secondary goals as JSON
        secondary_goals = request.form.getlist('secondary_goals')
        intake.set_secondary_goals(secondary_goals)
        
        db.session.add(intake)
        db.session.commit()
        
        flash(f'Intake form created for {client.full_name}!', 'success')
        return redirect(url_for('intake.view_intake', intake_id=intake.id))
    
    return render_template('intake/create.html', client=client)


@bp.route('/<int:intake_id>')
@login_required
def view_intake(intake_id):
    """View intake form details."""
    intake = ClientIntake.query.filter_by(id=intake_id, trainer_id=current_user.id).first_or_404()
    return render_template('intake/view.html', intake=intake)


@bp.route('/<int:intake_id>/generate-program', methods=['POST'])
@login_required
def generate_program(intake_id):
    """Generate AI program from intake form."""
    intake = ClientIntake.query.filter_by(id=intake_id, trainer_id=current_user.id).first_or_404()
    
    # Check if trainer has AI features enabled
    trainer_settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
    if not trainer_settings or not trainer_settings.enable_ai_programs:
        flash('AI program generation is not enabled. Please enable it in settings.', 'warning')
        return redirect(url_for('intake.view_intake', intake_id=intake.id))
    
    # AI Program Generation Logic (placeholder for actual AI implementation)
    # This would call an AI service to generate a personalized program
    
    program_name = f"AI-Generated Program for {intake.client.full_name}"
    duration_weeks = 12  # Default
    
    # Adjust duration based on target timeline
    if intake.target_timeline == '4_weeks':
        duration_weeks = 4
    elif intake.target_timeline == '8_weeks':
        duration_weeks = 8
    elif intake.target_timeline == '12_weeks':
        duration_weeks = 12
    elif intake.target_timeline == '6_months':
        duration_weeks = 24
    
    program = Program(
        trainer_id=current_user.id,
        client_id=intake.client_id,
        name=program_name,
        description=f"AI-generated program based on intake assessment. Goal: {intake.primary_goal}",
        goal=intake.primary_goal,
        duration_weeks=duration_weeks,
        difficulty_level=intake.fitness_experience,
        is_ai_generated=True,
        ai_model_version='v1.0',
        status='active'
    )
    
    db.session.add(program)
    db.session.flush()
    
    # Link program to intake
    intake.ai_generated_program_id = program.id
    intake.status = 'program_assigned'
    intake.reviewed_at = datetime.utcnow()
    
    # Store AI recommendations
    recommendations = {
        'bmi': intake.calculate_bmi(),
        'recommended_sessions_per_week': intake.sessions_per_week or 3,
        'focus_areas': [intake.primary_goal],
        'considerations': []
    }
    
    if intake.medical_conditions:
        recommendations['considerations'].append('Medical conditions noted')
    if intake.injuries:
        recommendations['considerations'].append('Previous injuries noted')
    
    intake.ai_recommendations = json.dumps(recommendations)
    
    db.session.commit()
    
    flash(f'AI program generated successfully for {intake.client.full_name}!', 'success')
    return redirect(url_for('programs.view_program', program_id=program.id))


@bp.route('/<int:intake_id>/review', methods=['POST'])
@login_required
def review_intake(intake_id):
    """Mark intake as reviewed."""
    intake = ClientIntake.query.filter_by(id=intake_id, trainer_id=current_user.id).first_or_404()
    
    intake.status = 'reviewed'
    intake.reviewed_at = datetime.utcnow()
    db.session.commit()
    
    flash('Intake form marked as reviewed!', 'success')
    return redirect(url_for('intake.view_intake', intake_id=intake.id))
