"""Main application routes.

This module serves the React SPA as the primary interface.
The dashboard route now serves the React app with full backend integration.
Legacy Jinja templates are available at /dashboard/legacy if needed.
"""
from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from app.models.client import Client
from app.models.session import Session
from app.models.program import Program
from datetime import datetime, timedelta

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    """Landing page."""
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard'))
    return render_template('index.html')


@bp.route('/app')
@bp.route('/app/<path:path>')
@login_required
def app(path=''):
    """Serve React app for authenticated users."""
    return render_template('app.html')


@bp.route('/dashboard/legacy')
@login_required
def dashboard_legacy():
    """Legacy dashboard - Jinja template version (for backwards compatibility)."""
    # Get statistics
    total_clients = Client.query.filter_by(trainer_id=current_user.id, is_active=True).count()
    total_programs = Program.query.filter_by(trainer_id=current_user.id, status='active').count()
    
    # Get upcoming sessions (next 7 days)
    now = datetime.utcnow()
    week_later = now + timedelta(days=7)
    upcoming_sessions = Session.query.filter(
        Session.trainer_id == current_user.id,
        Session.scheduled_start >= now,
        Session.scheduled_start <= week_later,
        Session.status == 'scheduled'
    ).order_by(Session.scheduled_start).limit(5).all()
    
    # Get today's sessions
    today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    today_sessions = Session.query.filter(
        Session.trainer_id == current_user.id,
        Session.scheduled_start >= today_start,
        Session.scheduled_start < today_end
    ).order_by(Session.scheduled_start).all()
    
    # Get recent clients
    recent_clients = Client.query.filter_by(
        trainer_id=current_user.id,
        is_active=True
    ).order_by(Client.created_at.desc()).limit(5).all()
    
    return render_template('dashboard.html',
                         total_clients=total_clients,
                         total_programs=total_programs,
                         upcoming_sessions=upcoming_sessions,
                         today_sessions=today_sessions,
                         recent_clients=recent_clients)


@bp.route('/dashboard')
@bp.route('/dashboard/<path:path>')
@login_required
def dashboard(path=''):
    """Main dashboard - serves React SPA with full backend integration."""
    # Don't serve React app for /dashboard/legacy
    if path == 'legacy':
        return redirect(url_for('main.dashboard_legacy'))
    # Redirect /dashboard/settings to /settings
    if path and path.startswith('settings'):
        return redirect(url_for('settings.index'))
    return render_template('app.html')


@bp.route('/about')
def about():
    """About page."""
    return render_template('about.html')


@bp.route('/health')
def health():
    """Health check endpoint for Railway/Render monitoring."""
    from app import db
    from flask import jsonify
    
    health_status = {
        'status': 'healthy',
        'database': 'unknown'
    }
    
    try:
        # Test database connection
        db.session.execute(db.text('SELECT 1'))
        health_status['database'] = 'connected'
    except Exception as e:
        health_status['status'] = 'unhealthy'
        health_status['database'] = 'disconnected'
        health_status['error'] = str(e)
        return jsonify(health_status), 503
    
    return jsonify(health_status), 200
