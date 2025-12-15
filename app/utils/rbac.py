"""Authorization decorators for RBAC."""
from functools import wraps
from flask import jsonify
from flask_login import current_user


def role_required(*roles):
    """
    Decorator to check if user has required role.
    
    Usage:
        @role_required('owner')
        @role_required('owner', 'admin')
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                return jsonify({'success': False, 'error': 'Authentication required'}), 401
            
            if current_user.role not in roles:
                return jsonify({
                    'success': False,
                    'error': f'Access denied. Required role: {" or ".join(roles)}'
                }), 403
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def owner_required(f):
    """Decorator to require organization owner role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        
        if not current_user.is_owner():
            return jsonify({'success': False, 'error': 'Owner access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    """Decorator to require admin or owner role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        
        if not current_user.is_admin():
            return jsonify({'success': False, 'error': 'Admin access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


def trainer_required(f):
    """Decorator to require trainer, admin, or owner role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        
        if not current_user.is_trainer():
            return jsonify({'success': False, 'error': 'Trainer access required'}), 403
        
        return f(*args, **kwargs)
    return decorated_function


def same_organization_required(f):
    """Decorator to check if user is in same organization as resource."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            return jsonify({'success': False, 'error': 'Authentication required'}), 401
        
        if not current_user.organization_id:
            return jsonify({'success': False, 'error': 'No organization assigned'}), 403
        
        return f(*args, **kwargs)
    return decorated_function
