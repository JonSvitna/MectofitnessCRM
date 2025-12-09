"""
RESTful API endpoints for session management.

This module provides comprehensive session management including:
- CRUD operations for training sessions
- Scheduling and availability checking
- Status management (scheduled, completed, cancelled, no-show)
- Session filtering by date, client, trainer, status
- Statistics and analytics
"""
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, and_, or_
from app import db
from app.models.session import Session
from app.models.client import Client
from app.models.user import User

api_sessions = Blueprint('api_sessions', __name__, url_prefix='/api/v1/sessions')


# ============================================================================
# Helper Functions
# ============================================================================

def session_to_dict(session, include_client=False, include_trainer=False):
    """
    Convert a Session object to a dictionary.
    
    Args:
        session: Session object to convert
        include_client: Whether to include full client details
        include_trainer: Whether to include full trainer details
        
    Returns:
        Dictionary representation of the session
    """
    data = {
        'id': session.id,
        'title': session.title,
        'description': session.description,
        'session_type': session.session_type,
        'location': session.location,
        'scheduled_start': session.scheduled_start.isoformat() if session.scheduled_start else None,
        'scheduled_end': session.scheduled_end.isoformat() if session.scheduled_end else None,
        'actual_start': session.actual_start.isoformat() if session.actual_start else None,
        'actual_end': session.actual_end.isoformat() if session.actual_end else None,
        'status': session.status,
        'exercises_performed': session.exercises_performed,
        'notes': session.notes,
        'client_feedback': session.client_feedback,
        'trainer_notes': session.trainer_notes,
        'google_event_id': session.google_event_id,
        'outlook_event_id': session.outlook_event_id,
        'created_at': session.created_at.isoformat() if session.created_at else None,
        'updated_at': session.updated_at.isoformat() if session.updated_at else None,
        'trainer_id': session.trainer_id,
        'client_id': session.client_id,
    }
    
    # Include nested client details if requested
    if include_client and session.client:
        data['client'] = {
            'id': session.client.id,
            'name': session.client.name,
            'email': session.client.email,
            'phone': session.client.phone,
            'status': session.client.status
        }
    
    # Include nested trainer details if requested
    if include_trainer and session.trainer:
        data['trainer'] = {
            'id': session.trainer.id,
            'username': session.trainer.username,
            'email': session.trainer.email,
            'full_name': session.trainer.full_name
        }
    
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


def validate_session_data(data, is_update=False):
    """
    Validate session data from request.
    
    Args:
        data: Dictionary of session data
        is_update: Whether this is an update operation (makes some fields optional)
        
    Returns:
        Tuple of (is_valid, errors_dict)
    """
    errors = {}
    
    # Required fields for creation
    if not is_update:
        if not data.get('client_id'):
            errors['client_id'] = 'Client ID is required'
        if not data.get('title'):
            errors['title'] = 'Session title is required'
        if not data.get('scheduled_start'):
            errors['scheduled_start'] = 'Scheduled start time is required'
        if not data.get('scheduled_end'):
            errors['scheduled_end'] = 'Scheduled end time is required'
    
    # Validate client exists
    if 'client_id' in data:
        client = Client.query.get(data['client_id'])
        if not client:
            errors['client_id'] = f"Client with ID {data['client_id']} not found"
        elif client.trainer_id != current_user.id:
            errors['client_id'] = "You don't have permission to schedule sessions for this client"
    
    # Validate datetime fields
    datetime_fields = ['scheduled_start', 'scheduled_end', 'actual_start', 'actual_end']
    for field in datetime_fields:
        if field in data and data[field]:
            try:
                datetime.fromisoformat(data[field].replace('Z', '+00:00'))
            except (ValueError, AttributeError):
                errors[field] = f"Invalid datetime format for {field}. Use ISO format (e.g., 2025-12-10T14:00:00)"
    
    # Validate scheduled times
    if 'scheduled_start' in data and 'scheduled_end' in data:
        try:
            start = datetime.fromisoformat(data['scheduled_start'].replace('Z', '+00:00'))
            end = datetime.fromisoformat(data['scheduled_end'].replace('Z', '+00:00'))
            if end <= start:
                errors['scheduled_end'] = 'Scheduled end time must be after start time'
        except (ValueError, AttributeError):
            pass  # Already caught in datetime validation above
    
    # Validate session type
    valid_types = ['personal', 'group', 'online', 'assessment', 'consultation']
    if 'session_type' in data and data['session_type']:
        if data['session_type'] not in valid_types:
            errors['session_type'] = f"Invalid session type. Must be one of: {', '.join(valid_types)}"
    
    # Validate status
    valid_statuses = ['scheduled', 'completed', 'cancelled', 'no-show']
    if 'status' in data and data['status']:
        if data['status'] not in valid_statuses:
            errors['status'] = f"Invalid status. Must be one of: {', '.join(valid_statuses)}"
    
    return len(errors) == 0, errors


# ============================================================================
# API Endpoints
# ============================================================================

@api_sessions.route('', methods=['GET'])
@login_required
def get_sessions():
    """
    Get a paginated list of sessions with filtering and sorting.
    
    Query Parameters:
        - page: Page number (default: 1)
        - per_page: Items per page (default: 20, max: 100)
        - client_id: Filter by client ID
        - status: Filter by status (scheduled, completed, cancelled, no-show)
        - session_type: Filter by type (personal, group, online, assessment)
        - start_date: Filter sessions starting from this date (ISO format)
        - end_date: Filter sessions up to this date (ISO format)
        - include_client: Include client details (true/false)
        - include_trainer: Include trainer details (true/false)
        - sort_by: Sort field (default: scheduled_start)
        - sort_order: Sort order (asc/desc, default: desc)
        
    Returns:
        JSON response with paginated session list
    """
    try:
        # Pagination
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # Base query - only sessions for current trainer
        query = Session.query.filter_by(trainer_id=current_user.id)
        
        # Filters
        client_id = request.args.get('client_id', type=int)
        if client_id:
            query = query.filter_by(client_id=client_id)
        
        status = request.args.get('status')
        if status:
            query = query.filter_by(status=status)
        
        session_type = request.args.get('session_type')
        if session_type:
            query = query.filter_by(session_type=session_type)
        
        # Date range filtering
        start_date = request.args.get('start_date')
        if start_date:
            try:
                start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
                query = query.filter(Session.scheduled_start >= start_dt)
            except ValueError:
                return error_response('Invalid start_date format. Use ISO format.')
        
        end_date = request.args.get('end_date')
        if end_date:
            try:
                end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
                query = query.filter(Session.scheduled_start <= end_dt)
            except ValueError:
                return error_response('Invalid end_date format. Use ISO format.')
        
        # Sorting
        sort_by = request.args.get('sort_by', 'scheduled_start')
        sort_order = request.args.get('sort_order', 'desc').lower()
        
        valid_sort_fields = ['scheduled_start', 'scheduled_end', 'created_at', 'updated_at', 'status', 'title']
        if sort_by not in valid_sort_fields:
            return error_response(f'Invalid sort_by field. Must be one of: {", ".join(valid_sort_fields)}')
        
        sort_column = getattr(Session, sort_by)
        if sort_order == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Execute query with pagination
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        # Convert to dict
        include_client = request.args.get('include_client', 'false').lower() == 'true'
        include_trainer = request.args.get('include_trainer', 'false').lower() == 'true'
        
        sessions = [
            session_to_dict(session, include_client=include_client, include_trainer=include_trainer)
            for session in pagination.items
        ]
        
        return success_response({
            'sessions': sessions,
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
        return error_response(f'Error fetching sessions: {str(e)}', 500)


@api_sessions.route('/<int:session_id>', methods=['GET'])
@login_required
def get_session(session_id):
    """
    Get a single session by ID.
    
    Query Parameters:
        - include_client: Include client details (true/false)
        - include_trainer: Include trainer details (true/false)
        
    Returns:
        JSON response with session details
    """
    try:
        session = Session.query.get(session_id)
        
        if not session:
            return error_response('Session not found', 404)
        
        # Check permission
        if session.trainer_id != current_user.id:
            return error_response('You do not have permission to view this session', 403)
        
        include_client = request.args.get('include_client', 'false').lower() == 'true'
        include_trainer = request.args.get('include_trainer', 'false').lower() == 'true'
        
        return success_response(
            session_to_dict(session, include_client=include_client, include_trainer=include_trainer)
        )
        
    except Exception as e:
        return error_response(f'Error fetching session: {str(e)}', 500)


@api_sessions.route('', methods=['POST'])
@login_required
def create_session():
    """
    Create a new training session.
    
    Request Body (JSON):
        - client_id (required): ID of the client
        - title (required): Session title
        - scheduled_start (required): Start datetime (ISO format)
        - scheduled_end (required): End datetime (ISO format)
        - description: Session description
        - session_type: Type (personal, group, online, assessment)
        - location: Session location
        - notes: Session notes
        
    Returns:
        JSON response with created session details
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        # Validate data
        is_valid, errors = validate_session_data(data)
        if not is_valid:
            return error_response('Validation failed', 400, errors)
        
        # Check for scheduling conflicts
        scheduled_start = datetime.fromisoformat(data['scheduled_start'].replace('Z', '+00:00'))
        scheduled_end = datetime.fromisoformat(data['scheduled_end'].replace('Z', '+00:00'))
        
        conflict = Session.query.filter(
            Session.trainer_id == current_user.id,
            Session.status.in_(['scheduled', 'completed']),
            or_(
                and_(
                    Session.scheduled_start <= scheduled_start,
                    Session.scheduled_end > scheduled_start
                ),
                and_(
                    Session.scheduled_start < scheduled_end,
                    Session.scheduled_end >= scheduled_end
                ),
                and_(
                    Session.scheduled_start >= scheduled_start,
                    Session.scheduled_end <= scheduled_end
                )
            )
        ).first()
        
        if conflict:
            return error_response(
                f'Scheduling conflict detected with session "{conflict.title}" at {conflict.scheduled_start.isoformat()}',
                409
            )
        
        # Create session
        session = Session(
            trainer_id=current_user.id,
            client_id=data['client_id'],
            title=data['title'],
            description=data.get('description'),
            session_type=data.get('session_type', 'personal'),
            location=data.get('location'),
            scheduled_start=scheduled_start,
            scheduled_end=scheduled_end,
            status='scheduled',
            notes=data.get('notes'),
            trainer_notes=data.get('trainer_notes')
        )
        
        db.session.add(session)
        db.session.commit()
        
        return success_response(
            session_to_dict(session, include_client=True),
            'Session created successfully',
            201
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating session: {str(e)}', 500)


@api_sessions.route('/<int:session_id>', methods=['PUT', 'PATCH'])
@login_required
def update_session(session_id):
    """
    Update an existing session.
    
    Request Body (JSON):
        Any session fields to update (partial updates supported with PATCH)
        
    Returns:
        JSON response with updated session details
    """
    try:
        session = Session.query.get(session_id)
        
        if not session:
            return error_response('Session not found', 404)
        
        # Check permission
        if session.trainer_id != current_user.id:
            return error_response('You do not have permission to update this session', 403)
        
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        # Validate data
        is_valid, errors = validate_session_data(data, is_update=True)
        if not is_valid:
            return error_response('Validation failed', 400, errors)
        
        # Check for scheduling conflicts if times are being changed
        if 'scheduled_start' in data or 'scheduled_end' in data:
            scheduled_start = datetime.fromisoformat(data.get('scheduled_start', session.scheduled_start.isoformat()).replace('Z', '+00:00'))
            scheduled_end = datetime.fromisoformat(data.get('scheduled_end', session.scheduled_end.isoformat()).replace('Z', '+00:00'))
            
            conflict = Session.query.filter(
                Session.id != session_id,
                Session.trainer_id == current_user.id,
                Session.status.in_(['scheduled', 'completed']),
                or_(
                    and_(
                        Session.scheduled_start <= scheduled_start,
                        Session.scheduled_end > scheduled_start
                    ),
                    and_(
                        Session.scheduled_start < scheduled_end,
                        Session.scheduled_end >= scheduled_end
                    ),
                    and_(
                        Session.scheduled_start >= scheduled_start,
                        Session.scheduled_end <= scheduled_end
                    )
                )
            ).first()
            
            if conflict:
                return error_response(
                    f'Scheduling conflict detected with session "{conflict.title}" at {conflict.scheduled_start.isoformat()}',
                    409
                )
        
        # Update fields
        updatable_fields = [
            'title', 'description', 'session_type', 'location',
            'status', 'exercises_performed', 'notes',
            'client_feedback', 'trainer_notes'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(session, field, data[field])
        
        # Handle datetime fields separately
        datetime_fields = ['scheduled_start', 'scheduled_end', 'actual_start', 'actual_end']
        for field in datetime_fields:
            if field in data and data[field]:
                setattr(session, field, datetime.fromisoformat(data[field].replace('Z', '+00:00')))
        
        # Allow client reassignment
        if 'client_id' in data:
            session.client_id = data['client_id']
        
        session.updated_at = datetime.utcnow()
        db.session.commit()
        
        return success_response(
            session_to_dict(session, include_client=True),
            'Session updated successfully'
        )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating session: {str(e)}', 500)


@api_sessions.route('/<int:session_id>', methods=['DELETE'])
@login_required
def delete_session(session_id):
    """
    Delete a session.
    
    Query Parameters:
        - permanent: If true, permanently delete. Otherwise just cancel.
        
    Returns:
        JSON response confirming deletion
    """
    try:
        session = Session.query.get(session_id)
        
        if not session:
            return error_response('Session not found', 404)
        
        # Check permission
        if session.trainer_id != current_user.id:
            return error_response('You do not have permission to delete this session', 403)
        
        permanent = request.args.get('permanent', 'false').lower() == 'true'
        
        if permanent:
            db.session.delete(session)
            db.session.commit()
            return success_response(message='Session permanently deleted')
        else:
            # Soft delete - just mark as cancelled
            session.status = 'cancelled'
            session.updated_at = datetime.utcnow()
            db.session.commit()
            return success_response(
                session_to_dict(session),
                'Session cancelled successfully'
            )
        
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error deleting session: {str(e)}', 500)


@api_sessions.route('/stats', methods=['GET'])
@login_required
def get_session_stats():
    """
    Get session statistics for the current trainer.
    
    Query Parameters:
        - start_date: Start date for stats (ISO format)
        - end_date: End date for stats (ISO format)
        - client_id: Filter stats by client
        
    Returns:
        JSON response with session statistics
    """
    try:
        # Base query
        query = Session.query.filter_by(trainer_id=current_user.id)
        
        # Date range filtering
        start_date = request.args.get('start_date')
        if start_date:
            start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00'))
            query = query.filter(Session.scheduled_start >= start_dt)
        
        end_date = request.args.get('end_date')
        if end_date:
            end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00'))
            query = query.filter(Session.scheduled_start <= end_dt)
        
        # Client filtering
        client_id = request.args.get('client_id', type=int)
        if client_id:
            query = query.filter_by(client_id=client_id)
        
        # Calculate stats
        total_sessions = query.count()
        
        status_breakdown = db.session.query(
            Session.status,
            func.count(Session.id)
        ).filter(
            Session.trainer_id == current_user.id
        )
        
        if start_date:
            status_breakdown = status_breakdown.filter(Session.scheduled_start >= start_dt)
        if end_date:
            status_breakdown = status_breakdown.filter(Session.scheduled_start <= end_dt)
        if client_id:
            status_breakdown = status_breakdown.filter(Session.client_id == client_id)
        
        status_breakdown = status_breakdown.group_by(Session.status).all()
        
        type_breakdown = db.session.query(
            Session.session_type,
            func.count(Session.id)
        ).filter(
            Session.trainer_id == current_user.id
        )
        
        if start_date:
            type_breakdown = type_breakdown.filter(Session.scheduled_start >= start_dt)
        if end_date:
            type_breakdown = type_breakdown.filter(Session.scheduled_start <= end_dt)
        if client_id:
            type_breakdown = type_breakdown.filter(Session.client_id == client_id)
        
        type_breakdown = type_breakdown.group_by(Session.session_type).all()
        
        # Upcoming sessions (next 7 days)
        upcoming_query = query.filter(
            Session.scheduled_start >= datetime.utcnow(),
            Session.scheduled_start <= datetime.utcnow() + timedelta(days=7),
            Session.status == 'scheduled'
        )
        upcoming_count = upcoming_query.count()
        
        stats = {
            'total_sessions': total_sessions,
            'by_status': {status: count for status, count in status_breakdown},
            'by_type': {session_type: count for session_type, count in type_breakdown},
            'upcoming_sessions': upcoming_count
        }
        
        return success_response(stats)
        
    except Exception as e:
        return error_response(f'Error calculating stats: {str(e)}', 500)


@api_sessions.route('/availability', methods=['GET'])
@login_required
def check_availability():
    """
    Check trainer availability for scheduling.
    
    Query Parameters:
        - date: Date to check (ISO format, default: today)
        - duration: Session duration in minutes (default: 60)
        
    Returns:
        JSON response with available time slots
    """
    try:
        # Parse date
        date_str = request.args.get('date')
        if date_str:
            check_date = datetime.fromisoformat(date_str.replace('Z', '+00:00')).date()
        else:
            check_date = datetime.utcnow().date()
        
        duration = request.args.get('duration', 60, type=int)
        
        # Get all sessions for this date
        start_of_day = datetime.combine(check_date, datetime.min.time())
        end_of_day = datetime.combine(check_date, datetime.max.time())
        
        booked_sessions = Session.query.filter(
            Session.trainer_id == current_user.id,
            Session.status.in_(['scheduled', 'completed']),
            Session.scheduled_start >= start_of_day,
            Session.scheduled_start <= end_of_day
        ).order_by(Session.scheduled_start).all()
        
        # Define working hours (8 AM to 8 PM)
        work_start = datetime.combine(check_date, datetime.min.time().replace(hour=8))
        work_end = datetime.combine(check_date, datetime.min.time().replace(hour=20))
        
        # Find available slots
        available_slots = []
        current_time = work_start
        
        for session in booked_sessions:
            # Check if there's a gap before this session
            if current_time < session.scheduled_start:
                gap_minutes = (session.scheduled_start - current_time).total_seconds() / 60
                if gap_minutes >= duration:
                    available_slots.append({
                        'start': current_time.isoformat(),
                        'end': session.scheduled_start.isoformat(),
                        'duration_minutes': int(gap_minutes)
                    })
            current_time = max(current_time, session.scheduled_end)
        
        # Check remaining time after last session
        if current_time < work_end:
            gap_minutes = (work_end - current_time).total_seconds() / 60
            if gap_minutes >= duration:
                available_slots.append({
                    'start': current_time.isoformat(),
                    'end': work_end.isoformat(),
                    'duration_minutes': int(gap_minutes)
                })
        
        return success_response({
            'date': check_date.isoformat(),
            'requested_duration': duration,
            'available_slots': available_slots,
            'booked_sessions': [
                {
                    'start': s.scheduled_start.isoformat(),
                    'end': s.scheduled_end.isoformat(),
                    'title': s.title
                }
                for s in booked_sessions
            ]
        })
        
    except Exception as e:
        return error_response(f'Error checking availability: {str(e)}', 500)
