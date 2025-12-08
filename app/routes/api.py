"""API routes for external integrations."""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models.client import Client
from app.models.session import Session
from app.models.program import Program
from datetime import datetime

bp = Blueprint('api', __name__, url_prefix='/api/v1')


@bp.route('/clients', methods=['GET'])
@login_required
def api_get_clients():
    """Get all clients via API."""
    clients = Client.query.filter_by(
        trainer_id=current_user.id,
        is_active=True
    ).all()
    
    return jsonify({
        'clients': [{
            'id': c.id,
            'first_name': c.first_name,
            'last_name': c.last_name,
            'email': c.email,
            'phone': c.phone,
            'fitness_goal': c.fitness_goal
        } for c in clients]
    })


@bp.route('/sessions', methods=['GET'])
@login_required
def api_get_sessions():
    """Get sessions via API."""
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    query = Session.query.filter_by(trainer_id=current_user.id)
    
    if start_date:
        query = query.filter(Session.scheduled_start >= datetime.fromisoformat(start_date))
    if end_date:
        query = query.filter(Session.scheduled_end <= datetime.fromisoformat(end_date))
    
    sessions = query.all()
    
    return jsonify({
        'sessions': [{
            'id': s.id,
            'title': s.title,
            'client_id': s.client_id,
            'scheduled_start': s.scheduled_start.isoformat(),
            'scheduled_end': s.scheduled_end.isoformat(),
            'status': s.status,
            'location': s.location
        } for s in sessions]
    })


@bp.route('/programs', methods=['GET'])
@login_required
def api_get_programs():
    """Get programs via API."""
    client_id = request.args.get('client_id', type=int)
    
    query = Program.query.filter_by(trainer_id=current_user.id)
    
    if client_id:
        query = query.filter_by(client_id=client_id)
    
    programs = query.all()
    
    return jsonify({
        'programs': [{
            'id': p.id,
            'name': p.name,
            'client_id': p.client_id,
            'goal': p.goal,
            'duration_weeks': p.duration_weeks,
            'status': p.status,
            'is_ai_generated': p.is_ai_generated
        } for p in programs]
    })


@bp.route('/webhook/gym-platform', methods=['POST'])
def webhook_gym_platform():
    """Webhook endpoint for gym platform integrations."""
    data = request.get_json()
    
    # Placeholder for webhook processing
    # This would handle events from gym management systems
    
    return jsonify({'status': 'received'}), 200
