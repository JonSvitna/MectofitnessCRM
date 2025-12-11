"""RESTful API for trainer settings management."""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.settings import TrainerSettings

api_settings = Blueprint('api_settings', __name__, url_prefix='/api/v1/settings')


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


def serialize_settings(settings):
    """Serialize TrainerSettings object to dictionary."""
    return {
        'id': settings.id,
        'trainer_id': settings.trainer_id,
        'business_name': settings.business_name,
        'business_email': settings.business_email,
        'business_phone': settings.business_phone,
        'business_address': settings.business_address,
        'timezone': settings.timezone,
        'currency': settings.currency,
        'language': settings.language,
        'session_reminder_hours': settings.session_reminder_hours,
        'booking_buffer_minutes': settings.booking_buffer_minutes,
        'default_session_duration': settings.default_session_duration,
        'allow_online_booking': settings.allow_online_booking,
        'require_booking_approval': settings.require_booking_approval,
        'ai_program_generation_enabled': settings.ai_program_generation_enabled,
        'payment_processing_enabled': settings.payment_processing_enabled,
        'notifications_enabled': settings.notifications_enabled,
        'email_notifications': settings.email_notifications,
        'sms_notifications': settings.sms_notifications,
        'calendar_sync_enabled': settings.calendar_sync_enabled,
        'created_at': settings.created_at.isoformat() if settings.created_at else None,
        'updated_at': settings.updated_at.isoformat() if settings.updated_at else None
    }


@api_settings.route('/', methods=['GET'])
@login_required
def get_settings():
    """Get all settings for current trainer."""
    try:
        settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
        
        # Create default settings if none exist
        if not settings:
            settings = TrainerSettings(trainer_id=current_user.id)
            db.session.add(settings)
            db.session.commit()
        
        return success_response(serialize_settings(settings))
    except Exception as e:
        return error_response(f'Error fetching settings: {str(e)}', 500)


@api_settings.route('/', methods=['PUT'])
@login_required
def update_settings():
    """Update all settings for current trainer."""
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided', 400)
        
        settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
        
        # Create settings if they don't exist
        if not settings:
            settings = TrainerSettings(trainer_id=current_user.id)
            db.session.add(settings)
        
        # Update all provided fields
        allowed_fields = [
            'business_name', 'business_email', 'business_phone', 'business_address',
            'timezone', 'currency', 'language',
            'session_reminder_hours', 'booking_buffer_minutes', 'default_session_duration',
            'allow_online_booking', 'require_booking_approval',
            'ai_program_generation_enabled', 'payment_processing_enabled',
            'notifications_enabled', 'email_notifications', 'sms_notifications',
            'calendar_sync_enabled'
        ]
        
        for field in allowed_fields:
            if field in data:
                setattr(settings, field, data[field])
        
        db.session.commit()
        
        return success_response(serialize_settings(settings), 'Settings updated successfully')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating settings: {str(e)}', 500)


@api_settings.route('/', methods=['PATCH'])
@login_required
def patch_settings():
    """Partially update settings for current trainer."""
    try:
        data = request.get_json()
        
        if not data:
            return error_response('No data provided', 400)
        
        settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
        
        # Create settings if they don't exist
        if not settings:
            settings = TrainerSettings(trainer_id=current_user.id)
            db.session.add(settings)
        
        # Update only provided fields
        allowed_fields = [
            'business_name', 'business_email', 'business_phone', 'business_address',
            'timezone', 'currency', 'language',
            'session_reminder_hours', 'booking_buffer_minutes', 'default_session_duration',
            'allow_online_booking', 'require_booking_approval',
            'ai_program_generation_enabled', 'payment_processing_enabled',
            'notifications_enabled', 'email_notifications', 'sms_notifications',
            'calendar_sync_enabled'
        ]
        
        updated_fields = []
        for field in allowed_fields:
            if field in data:
                setattr(settings, field, data[field])
                updated_fields.append(field)
        
        if not updated_fields:
            return error_response('No valid fields provided for update', 400)
        
        db.session.commit()
        
        return success_response(
            serialize_settings(settings),
            f'Settings updated successfully: {", ".join(updated_fields)}'
        )
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating settings: {str(e)}', 500)
