"""RESTful API for trainer settings management."""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.settings import TrainerSettings

api_settings = Blueprint('api_settings', __name__, url_prefix='/api/v1/settings')

# Allowed fields that can be updated via the API
ALLOWED_SETTINGS_FIELDS = [
    'business_name', 'business_logo_url', 'business_website', 'business_phone', 
    'business_address', 'primary_color', 'secondary_color',
    'enable_ai_programs', 'enable_email_marketing', 'enable_sms_marketing',
    'enable_calendar_sync', 'enable_workflow_automation',
    'notify_new_client', 'notify_session_reminder', 'notify_intake_complete',
    'notification_email', 'twilio_enabled', 'sendgrid_enabled', 'sendgrid_from_email'
]


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
        # Business settings
        'business_name': settings.business_name,
        'business_logo_url': settings.business_logo_url,
        'business_website': settings.business_website,
        'business_phone': settings.business_phone,
        'business_address': settings.business_address,
        # Branding
        'primary_color': settings.primary_color,
        'secondary_color': settings.secondary_color,
        # Feature toggles
        'enable_ai_programs': settings.enable_ai_programs,
        'enable_email_marketing': settings.enable_email_marketing,
        'enable_sms_marketing': settings.enable_sms_marketing,
        'enable_calendar_sync': settings.enable_calendar_sync,
        'enable_workflow_automation': settings.enable_workflow_automation,
        # Notification preferences
        'notify_new_client': settings.notify_new_client,
        'notify_session_reminder': settings.notify_session_reminder,
        'notify_intake_complete': settings.notify_intake_complete,
        'notification_email': settings.notification_email,
        # Integration settings
        'twilio_enabled': settings.twilio_enabled,
        'sendgrid_enabled': settings.sendgrid_enabled,
        'sendgrid_from_email': settings.sendgrid_from_email,
        # API settings
        'api_calls_per_day': settings.api_calls_per_day,
        'current_api_calls': settings.current_api_calls,
        # Timestamps
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
        for field in ALLOWED_SETTINGS_FIELDS:
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
        updated_fields = []
        for field in ALLOWED_SETTINGS_FIELDS:
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
