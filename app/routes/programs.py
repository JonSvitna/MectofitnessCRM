"""Training program routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.program import Program, Exercise
from app.models.client import Client
from datetime import datetime
import json

bp = Blueprint('programs', __name__, url_prefix='/programs')


@bp.route('/')
@login_required
def list_programs():
    """List all programs."""
    page = request.args.get('page', 1, type=int)
    programs = Program.query.filter_by(
        trainer_id=current_user.id
    ).order_by(Program.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('programs/list.html', programs=programs)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_program():
    """Add new program."""
    if request.method == 'POST':
        program = Program(
            trainer_id=current_user.id,
            client_id=request.form.get('client_id'),
            name=request.form.get('name'),
            description=request.form.get('description'),
            goal=request.form.get('goal'),
            duration_weeks=request.form.get('duration_weeks', type=int),
            difficulty_level=request.form.get('difficulty_level'),
            status='active'
        )
        
        db.session.add(program)
        db.session.commit()
        
        flash('Program created successfully!', 'success')
        return redirect(url_for('programs.view_program', program_id=program.id))
    
    # Get clients for dropdown
    clients = Client.query.filter_by(
        trainer_id=current_user.id,
        is_active=True
    ).order_by(Client.last_name, Client.first_name).all()
    
    return render_template('programs/add.html', clients=clients)


@bp.route('/<int:program_id>')
@login_required
def view_program(program_id):
    """View program details."""
    program = Program.query.filter_by(id=program_id, trainer_id=current_user.id).first_or_404()
    exercises = program.exercises.order_by(Exercise.day_number, Exercise.order_in_day).all()
    return render_template('programs/view.html', program=program, exercises=exercises)


@bp.route('/<int:program_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_program(program_id):
    """Edit program details."""
    program = Program.query.filter_by(id=program_id, trainer_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        program.name = request.form.get('name')
        program.description = request.form.get('description')
        program.goal = request.form.get('goal')
        program.duration_weeks = request.form.get('duration_weeks', type=int)
        program.difficulty_level = request.form.get('difficulty_level')
        program.status = request.form.get('status')
        program.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Program updated successfully!', 'success')
        return redirect(url_for('programs.view_program', program_id=program.id))
    
    return render_template('programs/edit.html', program=program)


@bp.route('/<int:program_id>/generate-ai', methods=['POST'])
@login_required
def generate_ai_program(program_id):
    """Generate AI-based training program."""
    program = Program.query.filter_by(id=program_id, trainer_id=current_user.id).first_or_404()
    
    # Placeholder for AI generation
    # In production, this would call the AI model
    flash('AI program generation is being implemented. This feature will use your knowledge base to create customized programs.', 'info')
    
    return redirect(url_for('programs.view_program', program_id=program.id))


@bp.route('/<int:program_id>/exercises/add', methods=['POST'])
@login_required
def add_exercise(program_id):
    """Add exercise to program."""
    program = Program.query.filter_by(id=program_id, trainer_id=current_user.id).first_or_404()
    
    exercise = Exercise(
        program_id=program.id,
        name=request.form.get('name'),
        description=request.form.get('description'),
        exercise_type=request.form.get('exercise_type'),
        muscle_group=request.form.get('muscle_group'),
        sets=request.form.get('sets', type=int),
        reps=request.form.get('reps'),
        day_number=request.form.get('day_number', type=int),
        order_in_day=request.form.get('order_in_day', type=int)
    )
    
    db.session.add(exercise)
    db.session.commit()
    
    flash('Exercise added successfully!', 'success')
    return redirect(url_for('programs.view_program', program_id=program.id))
