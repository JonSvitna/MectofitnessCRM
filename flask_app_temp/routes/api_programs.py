"""
RESTful API endpoints for program management.

This module provides comprehensive program management including:
- CRUD operations for training programs
- Exercise management within programs
- Program assignment to clients
- Program templates and cloning
- Progress tracking
"""
from datetime import datetime, date
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, or_
import json
from app import db
from app.models.program import Program, Exercise
from app.models.client import Client
from app.models.exercise_library import ExerciseLibrary

api_programs = Blueprint('api_programs', __name__, url_prefix='/api/v1/programs')


# ============================================================================
# Helper Functions
# ============================================================================

def program_to_dict(program, include_exercises=False, include_client=False):
    """
    Convert a Program object to a dictionary.
    
    Args:
        program: Program object to convert
        include_exercises: Whether to include exercise list
        include_client: Whether to include client details
        
    Returns:
        Dictionary representation of the program
    """
    data = {
        'id': program.id,
        'name': program.name,
        'description': program.description,
        'goal': program.goal,
        'duration_weeks': program.duration_weeks,
        'difficulty_level': program.difficulty_level,
        'is_ai_generated': program.is_ai_generated,
        'ai_model_version': program.ai_model_version,
        'status': program.status,
        'start_date': program.start_date.isoformat() if program.start_date else None,
        'end_date': program.end_date.isoformat() if program.end_date else None,
        'program_data': json.loads(program.program_data) if program.program_data else None,
        'notes': program.notes,
        'created_at': program.created_at.isoformat() if program.created_at else None,
        'updated_at': program.updated_at.isoformat() if program.updated_at else None,
        'trainer_id': program.trainer_id,
        'client_id': program.client_id,
    }
    
    # Include client details if requested
    if include_client and program.client:
        data['client'] = {
            'id': program.client.id,
            'name': program.client.name,
            'email': program.client.email,
            'status': program.client.status
        }
    
    # Include exercises if requested
    if include_exercises:
        exercises = program.exercises.order_by(Exercise.day_number, Exercise.order_in_day).all()
        data['exercises'] = [exercise_to_dict(ex) for ex in exercises]
        data['total_exercises'] = len(exercises)
    
    return data


def exercise_to_dict(exercise):
    """Convert an Exercise object to a dictionary."""
    return {
        'id': exercise.id,
        'program_id': exercise.program_id,
        'name': exercise.name,
        'description': exercise.description,
        'exercise_type': exercise.exercise_type,
        'muscle_group': exercise.muscle_group,
        'equipment': exercise.equipment,
        'sets': exercise.sets,
        'reps': exercise.reps,
        'duration_minutes': exercise.duration_minutes,
        'rest_seconds': exercise.rest_seconds,
        'weight': exercise.weight,
        'day_number': exercise.day_number,
        'order_in_day': exercise.order_in_day,
        'instructions': exercise.instructions,
        'video_url': exercise.video_url,
        'image_url': exercise.image_url,
        'created_at': exercise.created_at.isoformat() if exercise.created_at else None,
        'updated_at': exercise.updated_at.isoformat() if exercise.updated_at else None,
    }


def error_response(message, status_code=400, errors=None):
    """Create a standardized error response."""
    response = {
        'success': False,
        'error': message
    }
    if errors:
        response['errors'] = errors
    return jsonify(response), status_code


def success_response(data=None, message=None, status_code=200):
    """Create a standardized success response."""
    response = {'success': True}
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code


def validate_program_data(data, is_update=False):
    """
    Validate program data from request.
    
    Args:
        data: Dictionary of program data
        is_update: Whether this is an update operation
        
    Returns:
        Tuple of (is_valid, errors_dict)
    """
    errors = {}
    
    # Required fields for creation
    if not is_update:
        if not data.get('name'):
            errors['name'] = 'Program name is required'
        if not data.get('client_id'):
            errors['client_id'] = 'Client ID is required'
    
    # Validate client exists
    if 'client_id' in data:
        client = Client.query.get(data['client_id'])
        if not client:
            errors['client_id'] = f"Client with ID {data['client_id']} not found"
        elif client.trainer_id != current_user.id:
            errors['client_id'] = "You don't have permission to create programs for this client"
    
    # Validate difficulty
    valid_difficulties = ['beginner', 'intermediate', 'advanced']
    if 'difficulty_level' in data and data['difficulty_level']:
        if data['difficulty_level'] not in valid_difficulties:
            errors['difficulty_level'] = f"Invalid difficulty. Must be one of: {', '.join(valid_difficulties)}"
    
    # Validate status
    valid_statuses = ['active', 'completed', 'paused']
    if 'status' in data and data['status']:
        if data['status'] not in valid_statuses:
            errors['status'] = f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
    
    # Validate dates
    if 'start_date' in data and data['start_date']:
        try:
            date.fromisoformat(data['start_date'])
        except (ValueError, AttributeError):
            errors['start_date'] = 'Invalid date format. Use ISO format (YYYY-MM-DD)'
    
    if 'end_date' in data and data['end_date']:
        try:
            date.fromisoformat(data['end_date'])
        except (ValueError, AttributeError):
            errors['end_date'] = 'Invalid date format. Use ISO format (YYYY-MM-DD)'
    
    return len(errors) == 0, errors


# ============================================================================
# Program Endpoints
# ============================================================================

@api_programs.route('', methods=['GET'])
@login_required
def get_programs():
    """
    Get a paginated list of programs with filtering.
    
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 20, max: 100)
        - client_id: Filter by client ID
        - status: Filter by status (active, completed, paused)
        - difficulty: Filter by difficulty (beginner, intermediate, advanced)
        - include_exercises: Include exercise lists (true/false)
        - include_client: Include client details (true/false)
        - sort_by: Sort field (default: created_at)
        - sort_order: Sort order (asc/desc, default: desc)
        
    Returns:
        JSON response with paginated program list
    """
    try:
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # Base query - only programs for current trainer
        query = Program.query.filter_by(trainer_id=current_user.id)
        
        # Filters
        client_id = request.args.get('client_id', type=int)
        if client_id:
            query = query.filter_by(client_id=client_id)
        
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)
        
        difficulty = request.args.get('difficulty')
        if difficulty:
            query = query.filter_by(difficulty_level=difficulty)
        
        # Sorting
        sort_by = request.args.get('sort_by', 'created_at')
        sort_order = request.args.get('sort_order', 'desc').lower()
        
        valid_sort_fields = ['name', 'created_at', 'updated_at', 'start_date', 'status']
        if sort_by not in valid_sort_fields:
            return error_response(f'Invalid sort_by field. Must be one of: {", ".join(valid_sort_fields)}')
        
        sort_column = getattr(Program, sort_by)
        if sort_order == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Execute query with pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Convert to dict
        include_exercises = request.args.get('include_exercises', 'false').lower() == 'true'
        include_client = request.args.get('include_client', 'false').lower() == 'true'
        
        programs = [
            program_to_dict(program, include_exercises=include_exercises, include_client=include_client)
            for program in pagination.items
        ]
        
        return success_response({
            'programs': programs,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total_pages': pagination.pages,
                'total_items': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            }
        })
        
    except Exception as e:
        return error_response(f'Error fetching programs: {str(e)}', 500)


@api_programs.route('/<int:program_id>', methods=['GET'])
@login_required
def get_program(program_id):
    """
    Get a single program by ID.
    
    Query Parameters:
        - include_exercises: Include exercise list (true/false)
        - include_client: Include client details (true/false)
        
    Returns:
        JSON response with program details
    """
    try:
        program = Program.query.get(program_id)
        
        if not program:
            return error_response('Program not found', 404)
        
        # Check permission
        if program.trainer_id != current_user.id:
            return error_response('You do not have permission to view this program', 403)
        
        include_exercises = request.args.get('include_exercises', 'true').lower() == 'true'
        include_client = request.args.get('include_client', 'false').lower() == 'true'
        
        return success_response(
            program_to_dict(program, include_exercises=include_exercises, include_client=include_client)
        )
        
    except Exception as e:
        return error_response(f'Error fetching program: {str(e)}', 500)


@api_programs.route('', methods=['POST'])
@login_required
def create_program():
    """
    Create a new training program.
    
    Request Body (JSON):
        - name (required): Program name
        - client_id (required): ID of the client
        - description: Program description
        - goal: Training goal
        - duration_weeks: Program duration in weeks
        - difficulty_level: Difficulty (beginner, intermediate, advanced)
        - status: Status (active, completed, paused) - default: active
        - start_date: Start date (ISO format)
        - end_date: End date (ISO format)
        - program_data: Structured program data (JSON)
        - notes: Trainer notes
        
    Returns:
        JSON response with created program details
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        # Validate data
        is_valid, errors = validate_program_data(data)
        if not is_valid:
            return error_response('Validation failed', 400, errors)
        
        # Create program
        program = Program(
            trainer_id=current_user.id,
            client_id=data['client_id'],
            name=data['name'],
            description=data.get('description'),
            goal=data.get('goal'),
            duration_weeks=data.get('duration_weeks'),
            difficulty_level=data.get('difficulty_level', 'intermediate'),
            status=data.get('status', 'active'),
            start_date=date.fromisoformat(data['start_date']) if data.get('start_date') else None,
            end_date=date.fromisoformat(data['end_date']) if data.get('end_date') else None,
            program_data=json.dumps(data['program_data']) if data.get('program_data') else None,
            notes=data.get('notes')
        )
        
        db.session.add(program)
        db.session.commit()
        
        return success_response(
            program_to_dict(program, include_exercises=True, include_client=True),
            'Program created successfully',
            201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating program: {str(e)}', 500)


@api_programs.route('/<int:program_id>', methods=['PUT', 'PATCH'])
@login_required
def update_program(program_id):
    """
    Update an existing program.
    
    Request Body (JSON):
        Any program fields to update (partial updates supported with PATCH)
        
    Returns:
        JSON response with updated program details
    """
    try:
        program = Program.query.get(program_id)
        
        if not program:
            return error_response('Program not found', 404)
        
        # Check permission
        if program.trainer_id != current_user.id:
            return error_response('You do not have permission to update this program', 403)
        
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        # Validate data
        is_valid, errors = validate_program_data(data, is_update=True)
        if not is_valid:
            return error_response('Validation failed', 400, errors)
        
        # Update simple fields
        simple_fields = [
            'name', 'description', 'goal', 'duration_weeks',
            'difficulty_level', 'status', 'notes'
        ]
        
        for field in simple_fields:
            if field in data:
                setattr(program, field, data[field])
        
        # Update dates
        if 'start_date' in data and data['start_date']:
            program.start_date = date.fromisoformat(data['start_date'])
        if 'end_date' in data and data['end_date']:
            program.end_date = date.fromisoformat(data['end_date'])
        
        # Update program_data
        if 'program_data' in data:
            program.program_data = json.dumps(data['program_data'])
        
        # Allow client reassignment
        if 'client_id' in data:
            program.client_id = data['client_id']
        
        program.updated_at = datetime.utcnow()
        db.session.commit()
        
        return success_response(
            program_to_dict(program, include_exercises=True, include_client=True),
            'Program updated successfully'
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating program: {str(e)}', 500)


@api_programs.route('/<int:program_id>', methods=['DELETE'])
@login_required
def delete_program(program_id):
    """
    Delete a program.
    
    Query Parameters:
        - permanent: If true, permanently delete. Otherwise mark as paused.
        
    Returns:
        JSON response confirming deletion
    """
    try:
        program = Program.query.get(program_id)
        
        if not program:
            return error_response('Program not found', 404)
        
        # Check permission
        if program.trainer_id != current_user.id:
            return error_response('You do not have permission to delete this program', 403)
        
        permanent = request.args.get('permanent', 'false').lower() == 'true'
        
        if permanent:
            db.session.delete(program)
            db.session.commit()
            return success_response(message='Program permanently deleted')
        else:
            # Soft delete - mark as paused
            program.status = 'paused'
            program.updated_at = datetime.utcnow()
            db.session.commit()
            return success_response(
                program_to_dict(program),
                'Program paused successfully'
            )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error deleting program: {str(e)}', 500)


@api_programs.route('/<int:program_id>/clone', methods=['POST'])
@login_required
def clone_program(program_id):
    """
    Clone an existing program to a new client.
    
    Request Body (JSON):
        - client_id (required): ID of the new client
        - name: Optional new name (default: "Copy of {original_name}")
        
    Returns:
        JSON response with cloned program details
    """
    try:
        original_program = Program.query.get(program_id)
        
        if not original_program:
            return error_response('Program not found', 404)
        
        # Check permission
        if original_program.trainer_id != current_user.id:
            return error_response('You do not have permission to clone this program', 403)
        
        data = request.get_json()
        
        if not data or not data.get('client_id'):
            return error_response('client_id is required')
        
        # Validate client
        client = Client.query.get(data['client_id'])
        if not client:
            return error_response(f"Client with ID {data['client_id']} not found", 404)
        if client.trainer_id != current_user.id:
            return error_response("You don't have permission to assign programs to this client", 403)
        
        # Clone program
        new_program = Program(
            trainer_id=current_user.id,
            client_id=data['client_id'],
            name=data.get('name', f"Copy of {original_program.name}"),
            description=original_program.description,
            goal=original_program.goal,
            duration_weeks=original_program.duration_weeks,
            difficulty_level=original_program.difficulty_level,
            status='active',
            program_data=original_program.program_data,
            notes=original_program.notes
        )
        
        db.session.add(new_program)
        db.session.flush()  # Get the new program ID
        
        # Clone exercises
        original_exercises = original_program.exercises.all()
        for orig_ex in original_exercises:
            new_exercise = Exercise(
                program_id=new_program.id,
                name=orig_ex.name,
                description=orig_ex.description,
                exercise_type=orig_ex.exercise_type,
                muscle_group=orig_ex.muscle_group,
                equipment=orig_ex.equipment,
                sets=orig_ex.sets,
                reps=orig_ex.reps,
                duration_minutes=orig_ex.duration_minutes,
                rest_seconds=orig_ex.rest_seconds,
                weight=orig_ex.weight,
                day_number=orig_ex.day_number,
                order_in_day=orig_ex.order_in_day,
                instructions=orig_ex.instructions,
                video_url=orig_ex.video_url,
                image_url=orig_ex.image_url
            )
            db.session.add(new_exercise)
        
        db.session.commit()
        
        return success_response(
            program_to_dict(new_program, include_exercises=True, include_client=True),
            'Program cloned successfully',
            201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error cloning program: {str(e)}', 500)


@api_programs.route('/stats', methods=['GET'])
@login_required
def get_program_stats():
    """
    Get program statistics for the current trainer.
    
    Query Parameters:
        - client_id: Filter stats by client
        
    Returns:
        JSON response with program statistics
    """
    try:
        # Base query
        query = Program.query.filter_by(trainer_id=current_user.id)
        
        # Client filtering
        client_id = request.args.get('client_id', type=int)
        if client_id:
            query = query.filter_by(client_id=client_id)
        
        # Calculate stats
        total_programs = query.count()
        
        status_breakdown = db.session.query(
            Program.status,
            func.count(Program.id)
        ).filter(
            Program.trainer_id == current_user.id
        )
        
        if client_id:
            status_breakdown = status_breakdown.filter(Program.client_id == client_id)
        
        status_breakdown = status_breakdown.group_by(Program.status).all()
        
        difficulty_breakdown = db.session.query(
            Program.difficulty_level,
            func.count(Program.id)
        ).filter(
            Program.trainer_id == current_user.id
        )
        
        if client_id:
            difficulty_breakdown = difficulty_breakdown.filter(Program.client_id == client_id)
        
        difficulty_breakdown = difficulty_breakdown.group_by(Program.difficulty_level).all()
        
        stats = {
            'total_programs': total_programs,
            'by_status': {status: count for status, count in status_breakdown if status},
            'by_difficulty': {diff: count for diff, count in difficulty_breakdown if diff}
        }
        
        return success_response(stats)
        
    except Exception as e:
        return error_response(f'Error calculating stats: {str(e)}', 500)


# ============================================================================
# Exercise Management Endpoints
# ============================================================================

@api_programs.route('/<int:program_id>/exercises', methods=['GET'])
@login_required
def get_program_exercises(program_id):
    """
    Get all exercises for a program, grouped by day.
    
    Returns:
        JSON response with exercises grouped by day
    """
    try:
        program = Program.query.get(program_id)
        
        if not program:
            return error_response('Program not found', 404)
        
        # Check permission
        if program.trainer_id != current_user.id:
            return error_response('You do not have permission to view this program', 403)
        
        # Get exercises grouped by day
        exercises = program.exercises.order_by(Exercise.day_number, Exercise.order_in_day).all()
        
        # Group by day
        exercises_by_day = {}
        for ex in exercises:
            day = ex.day_number or 0
            if day not in exercises_by_day:
                exercises_by_day[day] = []
            exercises_by_day[day].append(exercise_to_dict(ex))
        
        return success_response({
            'program_id': program_id,
            'program_name': program.name,
            'exercises_by_day': exercises_by_day,
            'total_exercises': len(exercises)
        })
        
    except Exception as e:
        return error_response(f'Error fetching exercises: {str(e)}', 500)


@api_programs.route('/<int:program_id>/exercises', methods=['POST'])
@login_required
def add_exercise_to_program(program_id):
    """
    Add an exercise to a program.
    
    Request Body (JSON):
        - name (required): Exercise name
        - day_number: Day number in program
        - order_in_day: Order within the day
        - exercise_library_id: Optional ID from exercise library
        - description: Exercise description
        - exercise_type: Type (strength, cardio, flexibility, balance)
        - muscle_group: Target muscle group
        - equipment: Required equipment
        - sets: Number of sets
        - reps: Reps (can be range like "8-12")
        - duration_minutes: Duration in minutes
        - rest_seconds: Rest period in seconds
        - weight: Weight specification
        - instructions: Exercise instructions
        - video_url: Video URL
        - image_url: Image URL
        
    Returns:
        JSON response with created exercise details
    """
    try:
        program = Program.query.get(program_id)
        
        if not program:
            return error_response('Program not found', 404)
        
        # Check permission
        if program.trainer_id != current_user.id:
            return error_response('You do not have permission to modify this program', 403)
        
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        if not data.get('name'):
            return error_response('Exercise name is required', 400)
        
        # If exercise_library_id provided, copy data from library
        if data.get('exercise_library_id'):
            lib_exercise = ExerciseLibrary.query.get(data['exercise_library_id'])
            if lib_exercise:
                data.setdefault('description', lib_exercise.description)
                data.setdefault('exercise_type', lib_exercise.category)
                data.setdefault('muscle_group', ', '.join(lib_exercise.get_primary_muscles()))
                data.setdefault('equipment', ', '.join(lib_exercise.get_equipment()))
                data.setdefault('instructions', lib_exercise.setup_instructions)
                data.setdefault('image_url', lib_exercise.image_url)
                data.setdefault('video_url', lib_exercise.video_url)
        
        # Create exercise
        exercise = Exercise(
            program_id=program_id,
            name=data['name'],
            description=data.get('description'),
            exercise_type=data.get('exercise_type'),
            muscle_group=data.get('muscle_group'),
            equipment=data.get('equipment'),
            sets=data.get('sets'),
            reps=data.get('reps'),
            duration_minutes=data.get('duration_minutes'),
            rest_seconds=data.get('rest_seconds'),
            weight=data.get('weight'),
            day_number=data.get('day_number', 1),
            order_in_day=data.get('order_in_day', 1),
            instructions=data.get('instructions'),
            video_url=data.get('video_url'),
            image_url=data.get('image_url')
        )
        
        db.session.add(exercise)
        db.session.commit()
        
        return success_response(
            exercise_to_dict(exercise),
            'Exercise added to program successfully',
            201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error adding exercise: {str(e)}', 500)


@api_programs.route('/<int:program_id>/exercises/<int:exercise_id>', methods=['PUT', 'PATCH'])
@login_required
def update_program_exercise(program_id, exercise_id):
    """
    Update an exercise in a program.
    
    Request Body (JSON):
        Any exercise fields to update
        
    Returns:
        JSON response with updated exercise details
    """
    try:
        exercise = Exercise.query.get(exercise_id)
        
        if not exercise:
            return error_response('Exercise not found', 404)
        
        if exercise.program_id != program_id:
            return error_response('Exercise does not belong to this program', 400)
        
        # Check permission
        program = Program.query.get(program_id)
        if program.trainer_id != current_user.id:
            return error_response('You do not have permission to modify this program', 403)
        
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        # Update fields
        updatable_fields = [
            'name', 'description', 'exercise_type', 'muscle_group', 'equipment',
            'sets', 'reps', 'duration_minutes', 'rest_seconds', 'weight',
            'day_number', 'order_in_day', 'instructions', 'video_url', 'image_url'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(exercise, field, data[field])
        
        exercise.updated_at = datetime.utcnow()
        db.session.commit()
        
        return success_response(
            exercise_to_dict(exercise),
            'Exercise updated successfully'
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating exercise: {str(e)}', 500)


@api_programs.route('/<int:program_id>/exercises/<int:exercise_id>', methods=['DELETE'])
@login_required
def delete_program_exercise(program_id, exercise_id):
    """
    Delete an exercise from a program.
    
    Returns:
        JSON response confirming deletion
    """
    try:
        exercise = Exercise.query.get(exercise_id)
        
        if not exercise:
            return error_response('Exercise not found', 404)
        
        if exercise.program_id != program_id:
            return error_response('Exercise does not belong to this program', 400)
        
        # Check permission
        program = Program.query.get(program_id)
        if program.trainer_id != current_user.id:
            return error_response('You do not have permission to modify this program', 403)
        
        db.session.delete(exercise)
        db.session.commit()
        
        return success_response(message='Exercise deleted successfully')
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error deleting exercise: {str(e)}', 500)
