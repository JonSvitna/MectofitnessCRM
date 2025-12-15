"""RESTful API for user profile management."""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app import db
from app.models.user import User

api_user = Blueprint('api_user', __name__, url_prefix='/api/v1/user')


def error_response(message, status_code=400):
    """Return error response."""
    return jsonify({'success': False, 'error': message}), status_code


def success_response(data=None, message=None, status_code=200):
    """Return success response."""
    response = {'success': True}
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code


@api_user.route('/profile', methods=['GET'])
@login_required
def get_profile():
    """Get current user profile."""
    try:
        # Build full name from first_name and last_name
        full_name = None
        if current_user.first_name and current_user.last_name:
            full_name = f"{current_user.first_name} {current_user.last_name}"
        elif current_user.first_name:
            full_name = current_user.first_name
        elif current_user.last_name:
            full_name = current_user.last_name
        
        user_data = {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'full_name': full_name,
            'phone': current_user.phone,
            'role': current_user.role,
            'organization_id': current_user.organization_id,
            'created_at': current_user.created_at.isoformat() if current_user.created_at else None,
            'is_active': current_user.is_active
        }
        return success_response(user_data)
    except Exception as e:
        return error_response(f'Error fetching profile: {str(e)}', 500)


@api_user.route('/profile', methods=['PUT'])
@login_required
def update_profile():
    """Update user profile."""
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided', 400)
        
        # Update allowed fields
        if 'first_name' in data:
            current_user.first_name = data['first_name']
        
        if 'last_name' in data:
            current_user.last_name = data['last_name']
        
        if 'phone' in data:
            current_user.phone = data['phone']
        
        if 'email' in data:
            # Basic email validation
            email = data['email'].strip()
            if not email or '@' not in email or '.' not in email.split('@')[-1]:
                return error_response('Invalid email address format', 400)
            
            # Check if email is already taken by another user
            existing_user = User.query.filter(
                User.email == email,
                User.id != current_user.id
            ).first()
            if existing_user:
                return error_response('Email already in use', 409)
            current_user.email = email
        
        db.session.commit()
        
        user_data = {
            'id': current_user.id,
            'username': current_user.username,
            'email': current_user.email,
            'first_name': current_user.first_name,
            'last_name': current_user.last_name,
            'phone': current_user.phone,
            'role': current_user.role
        }
        
        return success_response(user_data, 'Profile updated successfully')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating profile: {str(e)}', 500)


@api_user.route('/password', methods=['PUT'])
@login_required
def change_password():
    """Change user password."""
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided', 400)
        
        # Validate required fields
        current_password = data.get('current_password')
        new_password = data.get('new_password')
        
        if not current_password or not new_password:
            return error_response('Current password and new password are required', 400)
        
        # Verify current password
        if not check_password_hash(current_user.password_hash, current_password):
            return error_response('Current password is incorrect', 401)
        
        # Validate new password strength
        if len(new_password) < 8:
            return error_response('New password must be at least 8 characters long', 400)
        
        # Update password
        current_user.password_hash = generate_password_hash(new_password)
        db.session.commit()
        
        return success_response(message='Password changed successfully')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error changing password: {str(e)}', 500)
