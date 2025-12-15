"""API routes for client management - RESTful endpoints."""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app import db
from app.models.client import Client
from app.models.session import Session
from app.models.program import Program
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError

api_clients = Blueprint('api_clients', __name__, url_prefix='/api/v1/clients')


# Helper function for error responses
def error_response(message, status_code=400):
    """Return standardized error response."""
    return jsonify({'error': message, 'success': False}), status_code


def success_response(data, message='Success', status_code=200):
    """Return standardized success response."""
    return jsonify({'data': data, 'message': message, 'success': True}), status_code


def client_to_dict(client, include_details=False):
    """Convert client model to dictionary."""
    client_dict = {
        'id': client.id,
        'first_name': client.first_name,
        'last_name': client.last_name,
        'full_name': client.full_name,
        'email': client.email,
        'phone': client.phone,
        'is_active': client.is_active,
        'created_at': client.created_at.isoformat() if client.created_at else None,
        'updated_at': client.updated_at.isoformat() if client.updated_at else None,
    }
    
    if include_details:
        client_dict.update({
            'date_of_birth': client.date_of_birth.isoformat() if client.date_of_birth else None,
            'gender': client.gender,
            'address': client.address,
            'emergency_contact': client.emergency_contact,
            'emergency_phone': client.emergency_phone,
            'fitness_goal': client.fitness_goal,
            'medical_conditions': client.medical_conditions,
            'fitness_level': client.fitness_level,
            'weight': client.weight,
            'height': client.height,
            'membership_type': client.membership_type,
            'membership_start': client.membership_start.isoformat() if client.membership_start else None,
            'membership_end': client.membership_end.isoformat() if client.membership_end else None,
            'notes': client.notes,
        })
    
    return client_dict


@api_clients.route('', methods=['GET'])
@login_required
def get_clients():
    """
    GET /api/v1/clients
    Get all clients for the current trainer.
    
    Query Parameters:
        - page (int): Page number for pagination (default: 1)
        - per_page (int): Results per page (default: 20, max: 100)
        - search (str): Search by name or email
        - status (str): Filter by 'active' or 'inactive'
        - fitness_level (str): Filter by fitness level
        - sort_by (str): Sort field (default: 'last_name')
        - sort_order (str): 'asc' or 'desc' (default: 'asc')
    
    Returns:
        JSON with clients list, pagination info, and metadata
    """
    try:
        # Pagination parameters
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 20, type=int), 100)
        
        # Filter parameters
        search = request.args.get('search', '').strip()
        status = request.args.get('status', 'active')
        fitness_level = request.args.get('fitness_level', '')
        
        # Sort parameters
        sort_by = request.args.get('sort_by', 'last_name')
        sort_order = request.args.get('sort_order', 'asc')
        
        # Base query
        query = Client.query.filter_by(trainer_id=current_user.id)
        
        # Apply filters
        if status == 'active':
            query = query.filter_by(is_active=True)
        elif status == 'inactive':
            query = query.filter_by(is_active=False)
        
        if search:
            search_filter = f'%{search}%'
            query = query.filter(
                db.or_(
                    Client.first_name.ilike(search_filter),
                    Client.last_name.ilike(search_filter),
                    Client.email.ilike(search_filter)
                )
            )
        
        if fitness_level:
            query = query.filter_by(fitness_level=fitness_level)
        
        # Apply sorting
        sort_column = getattr(Client, sort_by, Client.last_name)
        if sort_order == 'desc':
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())
        
        # Execute query with pagination
        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        # Format response
        clients_data = [client_to_dict(client) for client in pagination.items]
        
        return success_response({
            'clients': clients_data,
            'pagination': {
                'page': pagination.page,
                'per_page': pagination.per_page,
                'total_pages': pagination.pages,
                'total_items': pagination.total,
                'has_next': pagination.has_next,
                'has_prev': pagination.has_prev
            },
            'filters': {
                'search': search,
                'status': status,
                'fitness_level': fitness_level,
                'sort_by': sort_by,
                'sort_order': sort_order
            }
        })
        
    except Exception as e:
        return error_response(f'Error fetching clients: {str(e)}', 500)


@api_clients.route('/<int:client_id>', methods=['GET'])
@login_required
def get_client(client_id):
    """
    GET /api/v1/clients/<id>
    Get detailed information about a specific client.
    
    Query Parameters:
        - include_sessions (bool): Include recent sessions (default: false)
        - include_programs (bool): Include assigned programs (default: false)
    
    Returns:
        JSON with client details and optional related data
    """
    try:
        client = Client.query.filter_by(
            id=client_id,
            trainer_id=current_user.id
        ).first()
        
        if not client:
            return error_response('Client not found', 404)
        
        # Get client data with full details
        client_data = client_to_dict(client, include_details=True)
        
        # Optional: Include sessions
        if request.args.get('include_sessions', '').lower() == 'true':
            sessions = Session.query.filter_by(client_id=client_id).order_by(
                Session.scheduled_start.desc()
            ).limit(10).all()
            
            client_data['recent_sessions'] = [{
                'id': s.id,
                'scheduled_start': s.scheduled_start.isoformat() if s.scheduled_start else None,
                'scheduled_end': s.scheduled_end.isoformat() if s.scheduled_end else None,
                'status': s.status,
                'session_type': s.session_type
            } for s in sessions]
        
        # Optional: Include programs
        if request.args.get('include_programs', '').lower() == 'true':
            programs = Program.query.filter_by(client_id=client_id).order_by(
                Program.created_at.desc()
            ).all()
            
            client_data['programs'] = [{
                'id': p.id,
                'name': p.name,
                'status': p.status,
                'start_date': p.start_date.isoformat() if p.start_date else None,
                'end_date': p.end_date.isoformat() if p.end_date else None
            } for p in programs]
        
        return success_response(client_data)
        
    except Exception as e:
        return error_response(f'Error fetching client: {str(e)}', 500)


@api_clients.route('', methods=['POST'])
@login_required
def create_client():
    """
    POST /api/v1/clients
    Create a new client.
    
    Request Body (JSON):
        Required:
            - first_name (str)
            - last_name (str)
            - email (str)
        Optional:
            - phone, date_of_birth, gender, address
            - emergency_contact, emergency_phone
            - fitness_goal, medical_conditions, fitness_level
            - weight, height
            - membership_type, membership_start, membership_end
            - notes
    
    Returns:
        JSON with created client data
    """
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided')
        
        # Validate required fields
        required_fields = ['first_name', 'last_name', 'email']
        for field in required_fields:
            if not data.get(field):
                return error_response(f'Missing required field: {field}')
        
        # Check for duplicate email
        existing_client = Client.query.filter_by(
            email=data['email'],
            trainer_id=current_user.id,
            is_active=True
        ).first()
        
        if existing_client:
            return error_response('Client with this email already exists', 409)
        
        # Create new client
        client = Client(
            trainer_id=current_user.id,
            first_name=data['first_name'],
            last_name=data['last_name'],
            email=data['email'],
            phone=data.get('phone'),
            date_of_birth=datetime.fromisoformat(data['date_of_birth']) if data.get('date_of_birth') else None,
            gender=data.get('gender'),
            address=data.get('address'),
            emergency_contact=data.get('emergency_contact'),
            emergency_phone=data.get('emergency_phone'),
            fitness_goal=data.get('fitness_goal'),
            medical_conditions=data.get('medical_conditions'),
            fitness_level=data.get('fitness_level'),
            weight=data.get('weight'),
            height=data.get('height'),
            membership_type=data.get('membership_type'),
            membership_start=datetime.fromisoformat(data['membership_start']) if data.get('membership_start') else None,
            membership_end=datetime.fromisoformat(data['membership_end']) if data.get('membership_end') else None,
            notes=data.get('notes')
        )
        
        db.session.add(client)
        db.session.commit()
        
        return success_response(
            client_to_dict(client, include_details=True),
            message='Client created successfully',
            status_code=201
        )
        
    except ValueError as e:
        db.session.rollback()
        return error_response(f'Invalid data format: {str(e)}')
    except SQLAlchemyError as e:
        db.session.rollback()
        return error_response(f'Database error: {str(e)}', 500)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating client: {str(e)}', 500)


@api_clients.route('/<int:client_id>', methods=['PUT', 'PATCH'])
@login_required
def update_client(client_id):
    """
    PUT/PATCH /api/v1/clients/<id>
    Update an existing client.
    
    Request Body (JSON):
        Any client fields to update (same as create, all optional)
    
    Returns:
        JSON with updated client data
    """
    try:
        client = Client.query.filter_by(
            id=client_id,
            trainer_id=current_user.id
        ).first()
        
        if not client:
            return error_response('Client not found', 404)
        
        data = request.get_json()
        if not data:
            return error_response('No data provided')
        
        # Update allowed fields
        allowed_fields = [
            'first_name', 'last_name', 'email', 'phone', 'gender', 'address',
            'emergency_contact', 'emergency_phone', 'fitness_goal',
            'medical_conditions', 'fitness_level', 'weight', 'height',
            'membership_type', 'notes', 'is_active'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(client, field, data[field])
        
        # Handle date fields separately
        if 'date_of_birth' in data and data['date_of_birth']:
            client.date_of_birth = datetime.fromisoformat(data['date_of_birth'])
        
        if 'membership_start' in data and data['membership_start']:
            client.membership_start = datetime.fromisoformat(data['membership_start'])
        
        if 'membership_end' in data and data['membership_end']:
            client.membership_end = datetime.fromisoformat(data['membership_end'])
        
        client.updated_at = datetime.utcnow()
        db.session.commit()
        
        return success_response(
            client_to_dict(client, include_details=True),
            message='Client updated successfully'
        )
        
    except ValueError as e:
        db.session.rollback()
        return error_response(f'Invalid data format: {str(e)}')
    except SQLAlchemyError as e:
        db.session.rollback()
        return error_response(f'Database error: {str(e)}', 500)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating client: {str(e)}', 500)


@api_clients.route('/<int:client_id>', methods=['DELETE'])
@login_required
def delete_client(client_id):
    """
    DELETE /api/v1/clients/<id>
    Soft delete a client (marks as inactive).
    
    Query Parameters:
        - permanent (bool): If true, permanently delete (default: false)
    
    Returns:
        JSON with success message
    """
    try:
        client = Client.query.filter_by(
            id=client_id,
            trainer_id=current_user.id
        ).first()
        
        if not client:
            return error_response('Client not found', 404)
        
        permanent = request.args.get('permanent', '').lower() == 'true'
        
        if permanent:
            # Hard delete (use with caution)
            db.session.delete(client)
            message = 'Client permanently deleted'
        else:
            # Soft delete (recommended)
            client.is_active = False
            client.updated_at = datetime.utcnow()
            message = 'Client deactivated successfully'
        
        db.session.commit()
        
        return success_response(
            {'client_id': client_id},
            message=message
        )
        
    except SQLAlchemyError as e:
        db.session.rollback()
        return error_response(f'Database error: {str(e)}', 500)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error deleting client: {str(e)}', 500)


@api_clients.route('/stats', methods=['GET'])
@login_required
def get_client_stats():
    """
    GET /api/v1/clients/stats
    Get statistics about clients.
    
    Returns:
        JSON with client statistics
    """
    try:
        total_clients = Client.query.filter_by(
            trainer_id=current_user.id
        ).count()
        
        active_clients = Client.query.filter_by(
            trainer_id=current_user.id,
            is_active=True
        ).count()
        
        inactive_clients = total_clients - active_clients
        
        # Clients by fitness level
        fitness_levels = db.session.query(
            Client.fitness_level,
            db.func.count(Client.id)
        ).filter_by(
            trainer_id=current_user.id,
            is_active=True
        ).group_by(Client.fitness_level).all()
        
        # Recent clients (last 30 days)
        thirty_days_ago = datetime.utcnow().date()
        from datetime import timedelta
        thirty_days_ago = thirty_days_ago - timedelta(days=30)
        
        recent_clients = Client.query.filter(
            Client.trainer_id == current_user.id,
            Client.created_at >= thirty_days_ago
        ).count()
        
        return success_response({
            'total_clients': total_clients,
            'active_clients': active_clients,
            'inactive_clients': inactive_clients,
            'recent_clients_30_days': recent_clients,
            'by_fitness_level': {
                level or 'Not Set': count 
                for level, count in fitness_levels
            }
        })
        
    except Exception as e:
        return error_response(f'Error fetching statistics: {str(e)}', 500)
