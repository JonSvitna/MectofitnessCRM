from flask import Blueprint, jsonify, request
import requests
bp = Blueprint('api', __name__, url_prefix='/api/v1')

# ...existing code...

@bp.route('/exercises/search', methods=['GET'])
def api_search_exercises():
    """Proxy search to WGER API for exercises."""
    query = request.args.get('q', '')
    language = request.args.get('language', '2')  # 2 = English
    page = request.args.get('page', 1)
    per_page = request.args.get('limit', 20)

    # WGER API endpoint
    wger_url = f"https://wger.de/api/v2/exercise/"
    params = {
        'language': language,
        'status': '2',  # only public
        'limit': per_page,
        'page': page,
    }
    if query:
        params['name'] = query

    try:
        resp = requests.get(wger_url, params=params, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        # Optionally filter results by query in name/description
        if query:
            filtered = [ex for ex in data.get('results', []) if query.lower() in ex['name'].lower() or query.lower() in (ex['description'] or '').lower()]
        else:
            filtered = data.get('results', [])
        return jsonify({'exercises': filtered, 'count': len(filtered)})
    except Exception as e:
        return jsonify({'error': str(e), 'exercises': [], 'count': 0}), 500
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


@bp.route('/health', methods=['GET'])
def health_check():
    """
    Health check endpoint to verify application and database status.
    Returns 200 OK if database is accessible, 503 Service Unavailable otherwise.
    Uses pool_pre_ping behavior to detect stale connections.
    """
    from app import db
    from app.models.user import User
    import time
    
    start_time = time.time()
    
    try:
        # Try to execute a simple query to check database connectivity
        # This will use pool_pre_ping if configured, automatically detecting stale connections
        with db.engine.connect() as connection:
            result = connection.execute(db.text("SELECT 1"))
            result.fetchone()
        
        # Try to query a table to ensure tables exist
        user_count = User.query.count()
        
        response_time = round((time.time() - start_time) * 1000, 2)  # ms
        
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'response_time_ms': response_time,
            'user_count': user_count,
            'timestamp': datetime.utcnow().isoformat()
        }), 200
        
    except Exception as e:
        # Dispose of connection pool to avoid stale connections
        try:
            db.engine.dispose()
        except Exception:
            pass
        
        response_time = round((time.time() - start_time) * 1000, 2)  # ms
        
        return jsonify({
            'status': 'unhealthy',
            'database': 'disconnected',
            'error': 'Database connection failed',
            'response_time_ms': response_time,
            'timestamp': datetime.utcnow().isoformat()
        }), 503
