"""Settings and configuration routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.settings import TrainerSettings
from datetime import datetime

bp = Blueprint('settings', __name__, url_prefix='/settings')


@bp.route('/')
@login_required
def index():
    """Settings dashboard."""
    # Get or create settings for current user
    settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
    if not settings:
        settings = TrainerSettings(trainer_id=current_user.id)
        db.session.add(settings)
        db.session.commit()
    
    return render_template('settings/index.html', settings=settings)


@bp.route('/general', methods=['GET', 'POST'])
@login_required
def general():
    """General settings."""
    settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
    if not settings:
        settings = TrainerSettings(trainer_id=current_user.id)
        db.session.add(settings)
        db.session.commit()
    
    if request.method == 'POST':
        settings.business_name = request.form.get('business_name')
        settings.business_phone = request.form.get('business_phone')
        settings.business_website = request.form.get('business_website')
        settings.business_address = request.form.get('business_address')
        settings.notification_email = request.form.get('notification_email')
        
        db.session.commit()
        flash('General settings updated!', 'success')
        return redirect(url_for('settings.general'))
    
    return render_template('settings/general.html', settings=settings)


@bp.route('/features', methods=['GET', 'POST'])
@login_required
def features():
    """Feature toggle settings."""
    settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
    if not settings:
        settings = TrainerSettings(trainer_id=current_user.id)
        db.session.add(settings)
        db.session.commit()
    
    if request.method == 'POST':
        settings.enable_ai_programs = 'enable_ai_programs' in request.form
        settings.enable_email_marketing = 'enable_email_marketing' in request.form
        settings.enable_sms_marketing = 'enable_sms_marketing' in request.form
        settings.enable_calendar_sync = 'enable_calendar_sync' in request.form
        settings.enable_workflow_automation = 'enable_workflow_automation' in request.form
        
        db.session.commit()
        flash('Feature settings updated!', 'success')
        return redirect(url_for('settings.features'))
    
    return render_template('settings/features.html', settings=settings)


@bp.route('/api', methods=['GET', 'POST'])
@login_required
def api_settings():
    """API and rate limiting settings."""
    settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
    if not settings:
        settings = TrainerSettings(trainer_id=current_user.id)
        db.session.add(settings)
        db.session.commit()
    
    if request.method == 'POST':
        # Update API call limit
        new_limit = request.form.get('api_calls_per_day', type=int)
        if new_limit and new_limit > 0:
            settings.api_calls_per_day = new_limit
        
        db.session.commit()
        flash('API settings updated!', 'success')
        return redirect(url_for('settings.api_settings'))
    
    return render_template('settings/api.html', settings=settings)


@bp.route('/integrations', methods=['GET', 'POST'])
@login_required
def integrations():
    """Integration settings (Twilio, SendGrid)."""
    settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
    if not settings:
        settings = TrainerSettings(trainer_id=current_user.id)
        db.session.add(settings)
        db.session.commit()
    
    if request.method == 'POST':
        # Twilio settings
        settings.twilio_enabled = 'twilio_enabled' in request.form
        settings.twilio_account_sid = request.form.get('twilio_account_sid')
        settings.twilio_auth_token = request.form.get('twilio_auth_token')
        settings.twilio_phone_number = request.form.get('twilio_phone_number')
        
        # SendGrid settings
        settings.sendgrid_enabled = 'sendgrid_enabled' in request.form
        settings.sendgrid_api_key = request.form.get('sendgrid_api_key')
        settings.sendgrid_from_email = request.form.get('sendgrid_from_email')
        
        db.session.commit()
        flash('Integration settings updated!', 'success')
        return redirect(url_for('settings.integrations'))
    
    return render_template('settings/integrations.html', settings=settings)


@bp.route('/notifications', methods=['GET', 'POST'])
@login_required
def notifications():
    """Notification preferences."""
    settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
    if not settings:
        settings = TrainerSettings(trainer_id=current_user.id)
        db.session.add(settings)
        db.session.commit()
    
    if request.method == 'POST':
        settings.notify_new_client = 'notify_new_client' in request.form
        settings.notify_session_reminder = 'notify_session_reminder' in request.form
        settings.notify_intake_complete = 'notify_intake_complete' in request.form
        
        db.session.commit()
        flash('Notification settings updated!', 'success')
        return redirect(url_for('settings.notifications'))
    
    return render_template('settings/notifications.html', settings=settings)


@bp.route('/branding', methods=['GET', 'POST'])
@login_required
def branding():
    """Branding and appearance settings."""
    settings = TrainerSettings.query.filter_by(trainer_id=current_user.id).first()
    if not settings:
        settings = TrainerSettings(trainer_id=current_user.id)
        db.session.add(settings)
        db.session.commit()
    
    if request.method == 'POST':
        settings.primary_color = request.form.get('primary_color', '#2ECC71')
        settings.secondary_color = request.form.get('secondary_color', '#27AE60')
        settings.business_logo_url = request.form.get('business_logo_url')
        
        db.session.commit()
        flash('Branding settings updated!', 'success')
        return redirect(url_for('settings.branding'))
    
    return render_template('settings/branding.html', settings=settings)
