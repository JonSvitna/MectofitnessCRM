"""Training session routes."""
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models.session import Session
from app.models.client import Client
from datetime import datetime

bp = Blueprint('sessions', __name__, url_prefix='/sessions')


@bp.route('/')
@login_required
def list_sessions():
    """List all sessions."""
    page = request.args.get('page', 1, type=int)
    sessions = Session.query.filter_by(
        trainer_id=current_user.id
    ).order_by(Session.scheduled_start.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    return render_template('sessions/list.html', sessions=sessions)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_session():
    """Add new session."""
    if request.method == 'POST':
        session = Session(
            trainer_id=current_user.id,
            client_id=request.form.get('client_id'),
            title=request.form.get('title'),
            description=request.form.get('description'),
            session_type=request.form.get('session_type'),
            location=request.form.get('location'),
            scheduled_start=datetime.fromisoformat(request.form.get('scheduled_start')),
            scheduled_end=datetime.fromisoformat(request.form.get('scheduled_end')),
            status='scheduled'
        )
        
        db.session.add(session)
        db.session.commit()
        
        flash('Session scheduled successfully!', 'success')
        return redirect(url_for('sessions.view_session', session_id=session.id))
    
    # Get clients for dropdown
    clients = Client.query.filter_by(
        trainer_id=current_user.id,
        is_active=True
    ).order_by(Client.last_name, Client.first_name).all()
    
    return render_template('sessions/add.html', clients=clients)


@bp.route('/<int:session_id>')
@login_required
def view_session(session_id):
    """View session details."""
    session = Session.query.filter_by(id=session_id, trainer_id=current_user.id).first_or_404()
    return render_template('sessions/view.html', session=session)


@bp.route('/<int:session_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_session(session_id):
    """Edit session details."""
    session = Session.query.filter_by(id=session_id, trainer_id=current_user.id).first_or_404()
    
    if request.method == 'POST':
        session.title = request.form.get('title')
        session.description = request.form.get('description')
        session.session_type = request.form.get('session_type')
        session.location = request.form.get('location')
        session.scheduled_start = datetime.fromisoformat(request.form.get('scheduled_start'))
        session.scheduled_end = datetime.fromisoformat(request.form.get('scheduled_end'))
        session.status = request.form.get('status')
        session.notes = request.form.get('notes')
        session.updated_at = datetime.utcnow()
        
        db.session.commit()
        
        flash('Session updated successfully!', 'success')
        return redirect(url_for('sessions.view_session', session_id=session.id))
    
    return render_template('sessions/edit.html', session=session)


@bp.route('/<int:session_id>/complete', methods=['POST'])
@login_required
def complete_session(session_id):
    """Mark session as completed."""
    session = Session.query.filter_by(id=session_id, trainer_id=current_user.id).first_or_404()
    
    session.status = 'completed'
    session.actual_end = datetime.utcnow()
    session.trainer_notes = request.form.get('trainer_notes')
    session.updated_at = datetime.utcnow()
    
    db.session.commit()
    
    flash('Session marked as completed!', 'success')
    return redirect(url_for('sessions.view_session', session_id=session.id))
