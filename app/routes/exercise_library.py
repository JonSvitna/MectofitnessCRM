"""Exercise library and program builder routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.exercise_library import ExerciseLibrary, ProgramTemplate
from app.models.program import Program, Exercise
from app.models.client import Client
import json

bp = Blueprint('exercise_library', __name__, url_prefix='/exercise-library')


@bp.route('/')
@login_required
def index():
    """Exercise library home."""
    # Get search and filter parameters
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    difficulty = request.args.get('difficulty', '')
    equipment = request.args.get('equipment', '')
    
    query = ExerciseLibrary.query.filter_by(is_active=True)
    
    # Apply filters
    if search:
        query = query.filter(ExerciseLibrary.name.ilike(f'%{search}%'))
    if category:
        query = query.filter_by(category=category)
    if difficulty:
        query = query.filter_by(difficulty_level=difficulty)
    if equipment:
        query = query.filter(ExerciseLibrary.equipment_required.like(f'%{equipment}%'))
    
    page = request.args.get('page', 1, type=int)
    exercises = query.order_by(ExerciseLibrary.name).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('exercise_library/index.html', exercises=exercises)


@bp.route('/<int:exercise_id>')
@login_required
def view_exercise(exercise_id):
    """View exercise details."""
    exercise = ExerciseLibrary.query.filter_by(id=exercise_id, is_active=True).first_or_404()
    exercise.increment_usage()
    db.session.commit()
    
    return render_template('exercise_library/view.html', exercise=exercise)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_exercise():
    """Create custom exercise."""
    if request.method == 'POST':
        exercise = ExerciseLibrary(
            name=request.form.get('name'),
            description=request.form.get('description'),
            category=request.form.get('category'),
            difficulty_level=request.form.get('difficulty_level'),
            exercise_type=request.form.get('exercise_type'),
            setup_instructions=request.form.get('setup_instructions'),
            is_custom=True,
            created_by_trainer_id=current_user.id,
            is_public=request.form.get('is_public') == 'on'
        )
        
        # Handle JSON fields
        primary_muscles = request.form.getlist('primary_muscles')
        if primary_muscles:
            exercise.primary_muscle_groups = json.dumps(primary_muscles)
        
        equipment = request.form.getlist('equipment')
        if equipment:
            exercise.equipment_required = json.dumps(equipment)
        
        db.session.add(exercise)
        db.session.commit()
        
        flash('Custom exercise created!', 'success')
        return redirect(url_for('exercise_library.view_exercise', exercise_id=exercise.id))
    
    return render_template('exercise_library/create.html')


# Program Builder
@bp.route('/program-builder')
@login_required
def program_builder():
    """Enhanced program builder interface."""
    clients = Client.query.filter_by(
        trainer_id=current_user.id,
        is_active=True
    ).order_by(Client.last_name, Client.first_name).all()
    
    templates = ProgramTemplate.query.filter(
        (ProgramTemplate.is_public == True) |
        (ProgramTemplate.created_by_trainer_id == current_user.id)
    ).filter_by(is_active=True).all()
    
    return render_template('exercise_library/program_builder.html',
                         clients=clients,
                         templates=templates)


@bp.route('/program-builder/exercises', methods=['GET'])
@login_required
def get_exercises_json():
    """Get exercises as JSON for program builder."""
    category = request.args.get('category')
    difficulty = request.args.get('difficulty')
    
    query = ExerciseLibrary.query.filter_by(is_active=True)
    
    if category:
        query = query.filter_by(category=category)
    if difficulty:
        query = query.filter_by(difficulty_level=difficulty)
    
    exercises = query.limit(100).all()
    
    result = []
    for ex in exercises:
        result.append({
            'id': ex.id,
            'name': ex.name,
            'category': ex.category,
            'difficulty': ex.difficulty_level,
            'equipment': ex.get_equipment(),
            'muscles': ex.get_primary_muscles(),
            'image_url': ex.image_url
        })
    
    return jsonify(result)


@bp.route('/program-builder/save', methods=['POST'])
@login_required
def save_program_from_builder():
    """Save program created in program builder."""
    data = request.get_json()
    
    program = Program(
        trainer_id=current_user.id,
        client_id=data.get('client_id'),
        name=data.get('name'),
        description=data.get('description'),
        goal=data.get('goal'),
        duration_weeks=data.get('duration_weeks'),
        difficulty_level=data.get('difficulty_level'),
        status='active'
    )
    
    db.session.add(program)
    db.session.flush()
    
    # Add exercises
    exercises_data = data.get('exercises', [])
    for ex_data in exercises_data:
        exercise = Exercise(
            program_id=program.id,
            name=ex_data.get('name'),
            description=ex_data.get('description'),
            exercise_type=ex_data.get('exercise_type'),
            muscle_group=ex_data.get('muscle_group'),
            sets=ex_data.get('sets'),
            reps=ex_data.get('reps'),
            day_number=ex_data.get('day_number'),
            order_in_day=ex_data.get('order_in_day')
        )
        db.session.add(exercise)
    
    db.session.commit()
    
    return jsonify({
        'success': True,
        'program_id': program.id,
        'message': 'Program created successfully!'
    })


# Program Templates
@bp.route('/templates')
@login_required
def list_templates():
    """List program templates."""
    templates = ProgramTemplate.query.filter(
        (ProgramTemplate.is_public == True) |
        (ProgramTemplate.created_by_trainer_id == current_user.id)
    ).filter_by(is_active=True).order_by(ProgramTemplate.name).all()
    
    return render_template('exercise_library/templates.html', templates=templates)


@bp.route('/templates/<int:template_id>')
@login_required
def view_template(template_id):
    """View program template."""
    template = ProgramTemplate.query.filter_by(id=template_id, is_active=True).first_or_404()
    return render_template('exercise_library/view_template.html', template=template)


@bp.route('/templates/<int:template_id>/use', methods=['POST'])
@login_required
def use_template(template_id):
    """Create program from template."""
    template = ProgramTemplate.query.filter_by(id=template_id, is_active=True).first_or_404()
    client_id = request.form.get('client_id', type=int)
    
    if not client_id:
        flash('Please select a client.', 'warning')
        return redirect(url_for('exercise_library.view_template', template_id=template.id))
    
    # Create program from template
    program = Program(
        trainer_id=current_user.id,
        client_id=client_id,
        name=template.name,
        description=template.description,
        goal=template.target_goal,
        duration_weeks=template.duration_weeks,
        difficulty_level=template.target_level,
        status='active'
    )
    
    db.session.add(program)
    db.session.flush()
    
    # Add exercises from template
    template_data = template.get_template_data()
    exercises_data = template_data.get('exercises', [])
    
    for ex_data in exercises_data:
        exercise = Exercise(
            program_id=program.id,
            name=ex_data.get('name'),
            description=ex_data.get('description', ''),
            exercise_type=ex_data.get('exercise_type', ''),
            muscle_group=ex_data.get('muscle_group', ''),
            sets=ex_data.get('sets'),
            reps=ex_data.get('reps', ''),
            day_number=ex_data.get('day_number', 1),
            order_in_day=ex_data.get('order_in_day', 1)
        )
        db.session.add(exercise)
    
    template.usage_count += 1
    db.session.commit()
    
    flash(f'Program created from template: {template.name}', 'success')
    return redirect(url_for('programs.view_program', program_id=program.id))
