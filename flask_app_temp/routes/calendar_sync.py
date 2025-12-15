"""Calendar synchronization routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_required, current_user
from app import db
from app.models.calendar import CalendarIntegration
from datetime import datetime

bp = Blueprint('calendar', __name__, url_prefix='/calendar')


@bp.route('/')
@login_required
def calendar_settings():
    """Calendar integration settings."""
    integrations = CalendarIntegration.query.filter_by(user_id=current_user.id).all()
    return render_template('calendar/settings.html', integrations=integrations)


@bp.route('/connect/google')
@login_required
def connect_google():
    """Connect Google Calendar."""
    # Placeholder for Google OAuth flow
    flash('Google Calendar integration will be available soon. Please configure your Google API credentials.', 'info')
    return redirect(url_for('calendar.calendar_settings'))


@bp.route('/connect/outlook')
@login_required
def connect_outlook():
    """Connect Outlook Calendar."""
    # Placeholder for Outlook OAuth flow
    flash('Outlook Calendar integration will be available soon. Please configure your Microsoft API credentials.', 'info')
    return redirect(url_for('calendar.calendar_settings'))


@bp.route('/disconnect/<int:integration_id>', methods=['POST'])
@login_required
def disconnect_calendar(integration_id):
    """Disconnect calendar integration."""
    integration = CalendarIntegration.query.filter_by(
        id=integration_id,
        user_id=current_user.id
    ).first_or_404()
    
    db.session.delete(integration)
    db.session.commit()
    
    flash(f'{integration.provider.title()} Calendar disconnected successfully!', 'success')
    return redirect(url_for('calendar.calendar_settings'))


@bp.route('/sync/<int:integration_id>', methods=['POST'])
@login_required
def sync_calendar(integration_id):
    """Manually sync calendar."""
    integration = CalendarIntegration.query.filter_by(
        id=integration_id,
        user_id=current_user.id
    ).first_or_404()
    
    # Placeholder for sync logic
    integration.last_sync = datetime.utcnow()
    db.session.commit()
    
    flash(f'{integration.provider.title()} Calendar sync initiated!', 'success')
    return redirect(url_for('calendar.calendar_settings'))
