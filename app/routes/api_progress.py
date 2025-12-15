"""RESTful API for progress tracking - measurements, photos, metrics."""
from datetime import datetime, date, timedelta
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
import json
from app import db
from app.models.progress import ProgressEntry, ProgressPhoto, CustomMetric
from app.models.client import Client

api_progress = Blueprint('api_progress', __name__, url_prefix='/api/v1/progress')

def error_response(message, status_code=400, errors=None):
    response = {'success': False, 'error': message}
    if errors:
        response['errors'] = errors
    return jsonify(response), status_code

def success_response(data=None, message=None, status_code=200):
    response = {'success': True}
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

@api_progress.route('/entries', methods=['GET'])
@login_required
def get_progress_entries():
    """Get progress entries with filtering."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 100)
        client_id = request.args.get('client_id', type=int)
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')
        
        query = ProgressEntry.query.filter_by(trainer_id=current_user.id)
        
        if client_id:
            query = query.filter_by(client_id=client_id)
        if start_date:
            query = query.filter(ProgressEntry.entry_date >= date.fromisoformat(start_date))
        if end_date:
            query = query.filter(ProgressEntry.entry_date <= date.fromisoformat(end_date))
        
        query = query.order_by(ProgressEntry.entry_date.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        entries = [{
            'id': e.id, 'client_id': e.client_id, 'entry_date': e.entry_date.isoformat(),
            'weight': e.weight, 'body_fat_percentage': e.body_fat_percentage,
            'muscle_mass': e.muscle_mass, 'chest': e.chest, 'waist': e.waist,
            'hips': e.hips, 'thigh': e.thigh, 'arm': e.arm,
            'custom_metrics': e.get_custom_metrics(), 'notes': e.notes,
            'mood_rating': e.mood_rating, 'energy_level': e.energy_level,
            'created_at': e.created_at.isoformat()
        } for e in pagination.items]
        
        return success_response({'entries': entries, 'pagination': {
            'page': pagination.page, 'per_page': pagination.per_page,
            'total_pages': pagination.pages, 'total_items': pagination.total
        }})
    except Exception as e:
        return error_response(f'Error fetching entries: {str(e)}', 500)

@api_progress.route('/entries', methods=['POST'])
@login_required
def create_progress_entry():
    """Create a new progress entry."""
    try:
        data = request.get_json()
        if not data or not data.get('client_id'):
            return error_response('client_id is required')
        
        client = Client.query.get(data['client_id'])
        if not client or client.trainer_id != current_user.id:
            return error_response('Invalid client_id', 403)
        
        entry = ProgressEntry(
            client_id=data['client_id'], trainer_id=current_user.id,
            entry_date=date.fromisoformat(data.get('entry_date', str(date.today()))),
            weight=data.get('weight'), body_fat_percentage=data.get('body_fat_percentage'),
            muscle_mass=data.get('muscle_mass'), chest=data.get('chest'),
            waist=data.get('waist'), hips=data.get('hips'), thigh=data.get('thigh'),
            arm=data.get('arm'), notes=data.get('notes'),
            mood_rating=data.get('mood_rating'), energy_level=data.get('energy_level'),
            custom_metrics_data=json.dumps(data.get('custom_metrics', {}))
        )
        db.session.add(entry)
        db.session.commit()
        
        return success_response({'id': entry.id, 'entry_date': entry.entry_date.isoformat()},
                              'Progress entry created', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating entry: {str(e)}', 500)

@api_progress.route('/entries/<int:entry_id>', methods=['PUT', 'PATCH'])
@login_required
def update_progress_entry(entry_id):
    """Update a progress entry."""
    try:
        entry = ProgressEntry.query.get(entry_id)
        if not entry or entry.trainer_id != current_user.id:
            return error_response('Entry not found', 404)
        
        data = request.get_json()
        fields = ['weight', 'body_fat_percentage', 'muscle_mass', 'chest', 'waist',
                 'hips', 'thigh', 'arm', 'notes', 'mood_rating', 'energy_level']
        for field in fields:
            if field in data:
                setattr(entry, field, data[field])
        
        if 'custom_metrics' in data:
            entry.custom_metrics_data = json.dumps(data['custom_metrics'])
        
        entry.updated_at = datetime.utcnow()
        db.session.commit()
        return success_response({'id': entry.id}, 'Entry updated')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating entry: {str(e)}', 500)

@api_progress.route('/entries/<int:entry_id>', methods=['DELETE'])
@login_required
def delete_progress_entry(entry_id):
    """Delete a progress entry."""
    try:
        entry = ProgressEntry.query.get(entry_id)
        if not entry or entry.trainer_id != current_user.id:
            return error_response('Entry not found', 404)
        
        db.session.delete(entry)
        db.session.commit()
        return success_response(message='Entry deleted')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error deleting entry: {str(e)}', 500)

@api_progress.route('/photos', methods=['GET'])
@login_required
def get_progress_photos():
    """Get progress photos."""
    try:
        client_id = request.args.get('client_id', type=int)
        query = ProgressPhoto.query.filter_by(trainer_id=current_user.id)
        if client_id:
            query = query.filter_by(client_id=client_id)
        
        photos = query.order_by(ProgressPhoto.taken_at.desc()).limit(100).all()
        return success_response({'photos': [{
            'id': p.id, 'client_id': p.client_id, 'photo_url': p.photo_url,
            'photo_type': p.photo_type, 'caption': p.caption,
            'weight_at_time': p.weight_at_time, 'taken_at': p.taken_at.isoformat()
        } for p in photos]})
    except Exception as e:
        return error_response(f'Error fetching photos: {str(e)}', 500)

@api_progress.route('/stats/<int:client_id>', methods=['GET'])
@login_required
def get_progress_stats(client_id):
    """Get progress statistics for a client."""
    try:
        client = Client.query.get(client_id)
        if not client or client.trainer_id != current_user.id:
            return error_response('Client not found', 404)
        
        days = request.args.get('days', 90, type=int)
        start_date = date.today() - timedelta(days=days)
        
        entries = ProgressEntry.query.filter(
            ProgressEntry.client_id == client_id,
            ProgressEntry.entry_date >= start_date
        ).order_by(ProgressEntry.entry_date).all()
        
        if not entries:
            return success_response({'total_entries': 0, 'date_range_days': days})
        
        first_entry = entries[0]
        latest_entry = entries[-1]
        
        stats = {
            'total_entries': len(entries),
            'date_range_days': days,
            'first_entry_date': first_entry.entry_date.isoformat(),
            'latest_entry_date': latest_entry.entry_date.isoformat(),
            'weight_change': (latest_entry.weight - first_entry.weight) if (latest_entry.weight and first_entry.weight) else None,
            'body_fat_change': (latest_entry.body_fat_percentage - first_entry.body_fat_percentage) if (latest_entry.body_fat_percentage and first_entry.body_fat_percentage) else None,
            'latest_measurements': {
                'weight': latest_entry.weight,
                'body_fat': latest_entry.body_fat_percentage,
                'chest': latest_entry.chest,
                'waist': latest_entry.waist,
                'hips': latest_entry.hips
            }
        }
        
        return success_response(stats)
    except Exception as e:
        return error_response(f'Error calculating stats: {str(e)}', 500)
