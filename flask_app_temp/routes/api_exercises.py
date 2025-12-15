"""
RESTful API endpoints for exercise library management.

This module provides comprehensive exercise library management including:
- Browse and search exercises from WGER database
- Filter by muscle group, equipment, category, difficulty
- CRUD operations for custom trainer exercises
- Exercise statistics and popular exercises
"""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, or_
import json
from app import db
from app.models.exercise_library import ExerciseLibrary

api_exercises = Blueprint('api_exercises', __name__, url_prefix='/api/v1/exercises')


# ============================================================================
# Helper Functions
# ============================================================================

def exercise_to_dict(exercise, include_usage=False):
    """
    Convert an ExerciseLibrary object to a dictionary.
    
    Args:
        exercise: ExerciseLibrary object to convert
        include_usage: Whether to include usage statistics
        
    Returns:
        Dictionary representation of the exercise
    """
    data = {
        'id': exercise.id,
        'name': exercise.name,
        'description': exercise.description,
        'category': exercise.category,
        'primary_muscle_groups': exercise.get_primary_muscles(),
        'secondary_muscle_groups': json.loads(exercise.secondary_muscle_groups) if exercise.secondary_muscle_groups else [],
        'difficulty_level': exercise.difficulty_level,
        'equipment_required': exercise.get_equipment(),
        'exercise_type': exercise.exercise_type,
        'setup_instructions': exercise.setup_instructions,
        'execution_steps': exercise.get_execution_steps(),
        'common_mistakes': json.loads(exercise.common_mistakes) if exercise.common_mistakes else [],
        'tips_and_cues': json.loads(exercise.tips_and_cues) if exercise.tips_and_cues else [],
        'image_url': exercise.image_url,
        'video_url': exercise.video_url,
        'animation_url': exercise.animation_url,
        'easier_variations': json.loads(exercise.easier_variations) if exercise.easier_variations else [],
        'harder_variations': json.loads(exercise.harder_variations) if exercise.harder_variations else [],
        'alternative_exercises': json.loads(exercise.alternative_exercises) if exercise.alternative_exercises else [],
        'contraindications': json.loads(exercise.contraindications) if exercise.contraindications else [],
        'injury_considerations': exercise.injury_considerations,
        'typical_sets': exercise.typical_sets,
        'typical_reps': exercise.typical_reps,
        'typical_rest_seconds': exercise.typical_rest_seconds,
        'tags': exercise.get_tags(),
        'is_custom': exercise.is_custom,
        'is_public': exercise.is_public,
        'is_active': exercise.is_active,
        'created_at': exercise.created_at.isoformat() if exercise.created_at else None,
        'updated_at': exercise.updated_at.isoformat() if exercise.updated_at else None,
    }
    
    # Include creator info for custom exercises
    if exercise.is_custom and exercise.created_by_trainer_id:
        data['created_by_trainer_id'] = exercise.created_by_trainer_id
    
    # Include usage stats if requested
    if include_usage:
        data['usage_count'] = exercise.usage_count
        data['average_rating'] = exercise.average_rating
    
    return data


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


def validate_exercise_data(data, is_update=False):
    """
    Validate exercise data from request.
    
    Args:
        data: Dictionary of exercise data
        is_update: Whether this is an update operation
        
    Returns:
        Tuple of (is_valid, errors_dict)
    """
    errors = {}
    
    # Required fields for creation
    if not is_update:
        if not data.get('name'):
            errors['name'] = 'Exercise name is required'
        if not data.get('category'):
            errors['category'] = 'Category is required'
    
    # Validate category
    valid_categories = ['strength', 'cardio', 'flexibility', 'balance', 'mobility']
    if 'category' in data and data['category']:
        if data['category'] not in valid_categories:
            errors['category'] = f"Invalid category. Must be one of: {', '.join(valid_categories)}"
    
    # Validate difficulty
    valid_difficulties = ['beginner', 'intermediate', 'advanced']
    if 'difficulty_level' in data and data['difficulty_level']:
        if data['difficulty_level'] not in valid_difficulties:
            errors['difficulty_level'] = f"Invalid difficulty. Must be one of: {', '.join(valid_difficulties)}"
    
    # Validate exercise type
    valid_types = ['compound', 'isolation', 'bodyweight', 'cardio', 'plyometric']
    if 'exercise_type' in data and data['exercise_type']:
        if data['exercise_type'] not in valid_types:
            errors['exercise_type'] = f"Invalid exercise type. Must be one of: {', '.join(valid_types)}"
    
    return len(errors) == 0, errors


# ============================================================================
# API Endpoints
# ============================================================================

@api_exercises.route('', methods=['GET'])
@login_required
def get_exercises():
    """
    Get a paginated list of exercises with filtering and search.
    
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 20, max: 100)
        - search: Search in name and description
        - category: Filter by category (strength, cardio, flexibility, balance, mobility)
        - muscle: Filter by muscle group (partial match)
        - equipment: Filter by equipment (partial match)
        - difficulty: Filter by difficulty (beginner, intermediate, advanced)
        - exercise_type: Filter by type (compound, isolation, bodyweight, cardio)
        - custom_only: Show only custom exercises (true/false)
        - include_usage: Include usage statistics (true/false)
        - sort_by: Sort field (default: name)
        - sort_order: Sort order (asc/desc, default: asc)
        
    Returns:
        JSON response with paginated exercise list
    """
    try:
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # Base query - only active exercises
        query = ExerciseLibrary.query.filter_by(is_active=True)
        
        # Filter: custom only or include all
        custom_only = request.args.get('custom_only', 'false').lower() == 'true'
        if custom_only:
            query = query.filter_by(is_custom=True, created_by_trainer_id=current_user.id)
        else:
            # Show public exercises + user's custom exercises
            query = query.filter(
                or_(
                    ExerciseLibrary.is_public == True,
                    ExerciseLibrary.created_by_trainer_id == current_user.id
                )
            )
        
        # Search
        search_term = request.args.get('search')
        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.filter(
                or_(
                    ExerciseLibrary.name.ilike(search_pattern),
                    ExerciseLibrary.description.ilike(search_pattern)
                )
            )
        
        # Filters
        category = request.args.get('category')
        if category:
            query = query.filter_by(category=category)
        
        muscle = request.args.get('muscle')
        if muscle:
            muscle_pattern = f"%{muscle}%"
            query = query.filter(
                or_(
                    ExerciseLibrary.primary_muscle_groups.ilike(muscle_pattern),
                    ExerciseLibrary.secondary_muscle_groups.ilike(muscle_pattern)
                )
            )
        
        equipment = request.args.get('equipment')
        if equipment:
            equipment_pattern = f"%{equipment}%"
            query = query.filter(ExerciseLibrary.equipment_required.ilike(equipment_pattern))
        
        difficulty = request.args.get('difficulty')
        if difficulty:
            query = query.filter_by(difficulty_level=difficulty)
        
        exercise_type = request.args.get('exercise_type')
        if exercise_type:
            query = query.filter_by(exercise_type=exercise_type)
        
        # Sorting
        sort_by = request.args.get('sort_by', 'name')
        sort_order = request.args.get('sort_order', 'asc').lower()
        
        valid_sort_fields = ['name', 'category', 'difficulty_level', 'usage_count', 'created_at']
        if sort_by not in valid_sort_fields:
            return error_response(f'Invalid sort_by field. Must be one of: {", ".join(valid_sort_fields)}')
        
        sort_column = getattr(ExerciseLibrary, sort_by)
        if sort_order == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Execute query with pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Convert to dict
        include_usage = request.args.get('include_usage', 'false').lower() == 'true'
        
        exercises = [
            exercise_to_dict(exercise, include_usage=include_usage)
            for exercise in pagination.items
        ]
        
        return success_response({
            'exercises': exercises,
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
        return error_response(f'Error fetching exercises: {str(e)}', 500)


@api_exercises.route('/<int:exercise_id>', methods=['GET'])
@login_required
def get_exercise(exercise_id):
    """
    Get a single exercise by ID.
    
    Query Parameters:
        - include_usage: Include usage statistics (true/false)
        
    Returns:
        JSON response with exercise details
    """
    try:
        exercise = ExerciseLibrary.query.get(exercise_id)
        
        if not exercise:
            return error_response('Exercise not found', 404)
        
        # Check permission for private custom exercises
        if exercise.is_custom and not exercise.is_public:
            if exercise.created_by_trainer_id != current_user.id:
                return error_response('You do not have permission to view this exercise', 403)
        
        include_usage = request.args.get('include_usage', 'false').lower() == 'true'
        
        return success_response(exercise_to_dict(exercise, include_usage=include_usage))
        
    except Exception as e:
        return error_response(f'Error fetching exercise: {str(e)}', 500)


@api_exercises.route('', methods=['POST'])
@login_required
def create_exercise():
    """
    Create a new custom exercise.
    
    Request Body (JSON):
        - name (required): Exercise name
        - category (required): Category (strength, cardio, flexibility, balance, mobility)
        - description: Exercise description
        - primary_muscle_groups: Array of primary muscles
        - secondary_muscle_groups: Array of secondary muscles
        - equipment_required: Array of equipment needed
        - difficulty_level: Difficulty (beginner, intermediate, advanced)
        - exercise_type: Type (compound, isolation, bodyweight, cardio)
        - setup_instructions: Setup text
        - execution_steps: Array of step-by-step instructions
        - common_mistakes: Array of common mistakes
        - tips_and_cues: Array of coaching tips
        - image_url: Image URL
        - video_url: Video URL
        - contraindications: Array of contraindications
        - injury_considerations: Injury considerations text
        - typical_sets: Typical sets (e.g., "3-4")
        - typical_reps: Typical reps (e.g., "8-12")
        - typical_rest_seconds: Rest period in seconds
        - tags: Array of searchable tags
        - is_public: Whether exercise is public (default: false for custom)
        
    Returns:
        JSON response with created exercise details
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        # Validate data
        is_valid, errors = validate_exercise_data(data)
        if not is_valid:
            return error_response('Validation failed', 400, errors)
        
        # Check for duplicate name (for this trainer)
        existing = ExerciseLibrary.query.filter_by(
            name=data['name'],
            created_by_trainer_id=current_user.id,
            is_custom=True
        ).first()
        
        if existing:
            return error_response(f'You already have a custom exercise named "{data["name"]}"', 409)
        
        # Create exercise
        exercise = ExerciseLibrary(
            name=data['name'],
            description=data.get('description'),
            category=data['category'],
            primary_muscle_groups=json.dumps(data.get('primary_muscle_groups', [])),
            secondary_muscle_groups=json.dumps(data.get('secondary_muscle_groups', [])),
            difficulty_level=data.get('difficulty_level', 'intermediate'),
            equipment_required=json.dumps(data.get('equipment_required', [])),
            exercise_type=data.get('exercise_type', 'compound'),
            setup_instructions=data.get('setup_instructions'),
            execution_steps=json.dumps(data.get('execution_steps', [])),
            common_mistakes=json.dumps(data.get('common_mistakes', [])),
            tips_and_cues=json.dumps(data.get('tips_and_cues', [])),
            image_url=data.get('image_url'),
            video_url=data.get('video_url'),
            animation_url=data.get('animation_url'),
            contraindications=json.dumps(data.get('contraindications', [])),
            injury_considerations=data.get('injury_considerations'),
            typical_sets=data.get('typical_sets'),
            typical_reps=data.get('typical_reps'),
            typical_rest_seconds=data.get('typical_rest_seconds'),
            tags=json.dumps(data.get('tags', [])),
            is_custom=True,
            created_by_trainer_id=current_user.id,
            is_public=data.get('is_public', False),
            is_active=True
        )
        
        db.session.add(exercise)
        db.session.commit()
        
        return success_response(
            exercise_to_dict(exercise),
            'Custom exercise created successfully',
            201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating exercise: {str(e)}', 500)


@api_exercises.route('/<int:exercise_id>', methods=['PUT', 'PATCH'])
@login_required
def update_exercise(exercise_id):
    """
    Update an existing custom exercise.
    Only the creator can update custom exercises.
    
    Request Body (JSON):
        Any exercise fields to update (partial updates supported with PATCH)
        
    Returns:
        JSON response with updated exercise details
    """
    try:
        exercise = ExerciseLibrary.query.get(exercise_id)
        
        if not exercise:
            return error_response('Exercise not found', 404)
        
        # Only allow updating custom exercises
        if not exercise.is_custom:
            return error_response('Cannot modify standard exercises from the library', 403)
        
        # Check permission
        if exercise.created_by_trainer_id != current_user.id:
            return error_response('You do not have permission to update this exercise', 403)
        
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        # Validate data
        is_valid, errors = validate_exercise_data(data, is_update=True)
        if not is_valid:
            return error_response('Validation failed', 400, errors)
        
        # Update simple fields
        simple_fields = [
            'name', 'description', 'category', 'difficulty_level',
            'exercise_type', 'setup_instructions', 'injury_considerations',
            'image_url', 'video_url', 'animation_url',
            'typical_sets', 'typical_reps', 'typical_rest_seconds',
            'is_public', 'is_active'
        ]
        
        for field in simple_fields:
            if field in data:
                setattr(exercise, field, data[field])
        
        # Update JSON fields
        json_fields = [
            'primary_muscle_groups', 'secondary_muscle_groups', 'equipment_required',
            'execution_steps', 'common_mistakes', 'tips_and_cues',
            'contraindications', 'tags'
        ]
        
        for field in json_fields:
            if field in data:
                setattr(exercise, field, json.dumps(data[field]))
        
        db.session.commit()
        
        return success_response(
            exercise_to_dict(exercise),
            'Exercise updated successfully'
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating exercise: {str(e)}', 500)


@api_exercises.route('/<int:exercise_id>', methods=['DELETE'])
@login_required
def delete_exercise(exercise_id):
    """
    Delete a custom exercise.
    Only the creator can delete custom exercises.
    
    Query Parameters:
        - permanent: If true, permanently delete. Otherwise just deactivate.
        
    Returns:
        JSON response confirming deletion
    """
    try:
        exercise = ExerciseLibrary.query.get(exercise_id)
        
        if not exercise:
            return error_response('Exercise not found', 404)
        
        # Only allow deleting custom exercises
        if not exercise.is_custom:
            return error_response('Cannot delete standard exercises from the library', 403)
        
        # Check permission
        if exercise.created_by_trainer_id != current_user.id:
            return error_response('You do not have permission to delete this exercise', 403)
        
        permanent = request.args.get('permanent', 'false').lower() == 'true'
        
        if permanent:
            db.session.delete(exercise)
            db.session.commit()
            return success_response(message='Exercise permanently deleted')
        else:
            # Soft delete - just deactivate
            exercise.is_active = False
            db.session.commit()
            return success_response(
                exercise_to_dict(exercise),
                'Exercise deactivated successfully'
            )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error deleting exercise: {str(e)}', 500)


@api_exercises.route('/stats', methods=['GET'])
@login_required
def get_exercise_stats():
    """
    Get exercise library statistics.
    
    Returns:
        JSON response with exercise statistics
    """
    try:
        # Total counts
        total_exercises = ExerciseLibrary.query.filter_by(is_active=True).count()
        standard_exercises = ExerciseLibrary.query.filter_by(is_custom=False, is_active=True).count()
        custom_exercises = ExerciseLibrary.query.filter_by(
            is_custom=True,
            created_by_trainer_id=current_user.id,
            is_active=True
        ).count()
        
        # Category breakdown
        category_breakdown = db.session.query(
            ExerciseLibrary.category,
            func.count(ExerciseLibrary.id)
        ).filter_by(is_active=True).group_by(ExerciseLibrary.category).all()
        
        # Difficulty breakdown
        difficulty_breakdown = db.session.query(
            ExerciseLibrary.difficulty_level,
            func.count(ExerciseLibrary.id)
        ).filter_by(is_active=True).group_by(ExerciseLibrary.difficulty_level).all()
        
        # Most popular exercises (by usage)
        popular_exercises = ExerciseLibrary.query.filter_by(
            is_active=True
        ).order_by(
            ExerciseLibrary.usage_count.desc()
        ).limit(10).all()
        
        stats = {
            'total_exercises': total_exercises,
            'standard_exercises': standard_exercises,
            'custom_exercises': custom_exercises,
            'by_category': {cat: count for cat, count in category_breakdown if cat},
            'by_difficulty': {diff: count for diff, count in difficulty_breakdown if diff},
            'most_popular': [
                {
                    'id': ex.id,
                    'name': ex.name,
                    'usage_count': ex.usage_count,
                    'category': ex.category
                }
                for ex in popular_exercises
            ]
        }
        
        return success_response(stats)
        
    except Exception as e:
        return error_response(f'Error calculating stats: {str(e)}', 500)


@api_exercises.route('/categories', methods=['GET'])
@login_required
def get_categories():
    """
    Get available exercise categories with counts.
    
    Returns:
        JSON response with category list
    """
    try:
        categories = db.session.query(
            ExerciseLibrary.category,
            func.count(ExerciseLibrary.id).label('count')
        ).filter_by(is_active=True).group_by(ExerciseLibrary.category).all()
        
        category_list = [
            {
                'name': cat,
                'count': count
            }
            for cat, count in categories if cat
        ]
        
        return success_response(category_list)
        
    except Exception as e:
        return error_response(f'Error fetching categories: {str(e)}', 500)


@api_exercises.route('/muscles', methods=['GET'])
@login_required
def get_muscle_groups():
    """
    Get all unique muscle groups from exercises.
    
    Returns:
        JSON response with muscle group list
    """
    try:
        # Get all exercises
        exercises = ExerciseLibrary.query.filter_by(is_active=True).all()
        
        # Collect all unique muscles
        muscles = set()
        for exercise in exercises:
            muscles.update(exercise.get_primary_muscles())
            if exercise.secondary_muscle_groups:
                muscles.update(json.loads(exercise.secondary_muscle_groups))
        
        muscle_list = sorted([m for m in muscles if m])
        
        return success_response(muscle_list)
        
    except Exception as e:
        return error_response(f'Error fetching muscle groups: {str(e)}', 500)


@api_exercises.route('/equipment', methods=['GET'])
@login_required
def get_equipment():
    """
    Get all unique equipment types from exercises.
    
    Returns:
        JSON response with equipment list
    """
    try:
        # Get all exercises
        exercises = ExerciseLibrary.query.filter_by(is_active=True).all()
        
        # Collect all unique equipment
        equipment = set()
        for exercise in exercises:
            equipment.update(exercise.get_equipment())
        
        equipment_list = sorted([e for e in equipment if e])
        
        return success_response(equipment_list)
        
    except Exception as e:
        return error_response(f'Error fetching equipment: {str(e)}', 500)
