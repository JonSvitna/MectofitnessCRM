"""RESTful API for online booking system."""
from datetime import datetime, date, time, timedelta
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import and_, or_
import json
from app import db
from app.models.booking import BookingAvailability, BookingException, OnlineBooking
from app.models.client import Client
from app.models.user import User

api_booking = Blueprint('api_booking', __name__, url_prefix='/api/v1/booking')

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

@api_booking.route('/availability', methods=['GET'])
@login_required
def get_availability():
    """Get trainer's weekly availability schedule."""
    try:
        slots = BookingAvailability.query.filter_by(
            trainer_id=current_user.id,
            is_active=True
        ).order_by(BookingAvailability.day_of_week, BookingAvailability.start_time).all()
        
        return success_response({'availability': [{
            'id': s.id, 'day_of_week': s.day_of_week, 'day_name': s.day_name,
            'start_time': s.start_time.strftime('%H:%M'), 'end_time': s.end_time.strftime('%H:%M'),
            'session_type': s.session_type, 'max_bookings': s.max_bookings
        } for s in slots]})
    except Exception as e:
        return error_response(f'Error fetching availability: {str(e)}', 500)

@api_booking.route('/availability', methods=['POST'])
@login_required
def create_availability():
    """Create availability slot."""
    try:
        data = request.get_json()
        if not data or data.get('day_of_week') is None:
            return error_response('day_of_week, start_time, end_time are required')
        
        slot = BookingAvailability(
            trainer_id=current_user.id,
            day_of_week=data['day_of_week'],
            start_time=datetime.strptime(data['start_time'], '%H:%M').time(),
            end_time=datetime.strptime(data['end_time'], '%H:%M').time(),
            session_type=data.get('session_type'),
            max_bookings=data.get('max_bookings', 1),
            is_active=data.get('is_active', True)
        )
        db.session.add(slot)
        db.session.commit()
        
        return success_response({'id': slot.id}, 'Availability created', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating availability: {str(e)}', 500)

@api_booking.route('/availability/<int:slot_id>', methods=['PUT', 'PATCH'])
@login_required
def update_availability(slot_id):
    """Update availability slot."""
    try:
        slot = BookingAvailability.query.get(slot_id)
        if not slot or slot.trainer_id != current_user.id:
            return error_response('Availability slot not found', 404)
        
        data = request.get_json()
        if 'start_time' in data:
            slot.start_time = datetime.strptime(data['start_time'], '%H:%M').time()
        if 'end_time' in data:
            slot.end_time = datetime.strptime(data['end_time'], '%H:%M').time()
        if 'session_type' in data:
            slot.session_type = data['session_type']
        if 'max_bookings' in data:
            slot.max_bookings = data['max_bookings']
        if 'is_active' in data:
            slot.is_active = data['is_active']
        
        slot.updated_at = datetime.utcnow()
        db.session.commit()
        return success_response({'id': slot.id}, 'Availability updated')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating availability: {str(e)}', 500)

@api_booking.route('/availability/<int:slot_id>', methods=['DELETE'])
@login_required
def delete_availability(slot_id):
    """Delete availability slot."""
    try:
        slot = BookingAvailability.query.get(slot_id)
        if not slot or slot.trainer_id != current_user.id:
            return error_response('Availability slot not found', 404)
        
        db.session.delete(slot)
        db.session.commit()
        return success_response(message='Availability deleted')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error deleting availability: {str(e)}', 500)

@api_booking.route('/exceptions', methods=['GET'])
@login_required
def get_exceptions():
    """Get booking exceptions (holidays, vacations)."""
    try:
        exceptions = BookingException.query.filter_by(
            trainer_id=current_user.id
        ).order_by(BookingException.start_date.desc()).limit(100).all()
        
        return success_response({'exceptions': [{
            'id': e.id, 'start_date': e.start_date.isoformat(), 'end_date': e.end_date.isoformat(),
            'exception_type': e.exception_type, 'reason': e.reason,
            'special_start_time': e.special_start_time.strftime('%H:%M') if e.special_start_time else None,
            'special_end_time': e.special_end_time.strftime('%H:%M') if e.special_end_time else None
        } for e in exceptions]})
    except Exception as e:
        return error_response(f'Error fetching exceptions: {str(e)}', 500)

@api_booking.route('/exceptions', methods=['POST'])
@login_required
def create_exception():
    """Create booking exception."""
    try:
        data = request.get_json()
        if not data or not data.get('start_date'):
            return error_response('start_date and end_date are required')
        
        exception = BookingException(
            trainer_id=current_user.id,
            start_date=date.fromisoformat(data['start_date']),
            end_date=date.fromisoformat(data.get('end_date', data['start_date'])),
            exception_type=data.get('exception_type', 'unavailable'),
            reason=data.get('reason'),
            special_start_time=datetime.strptime(data['special_start_time'], '%H:%M').time() if data.get('special_start_time') else None,
            special_end_time=datetime.strptime(data['special_end_time'], '%H:%M').time() if data.get('special_end_time') else None
        )
        db.session.add(exception)
        db.session.commit()
        
        return success_response({'id': exception.id}, 'Exception created', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating exception: {str(e)}', 500)

@api_booking.route('/bookings', methods=['GET'])
@login_required
def get_bookings():
    """Get online bookings."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 100)
        status = request.args.get('status')
        
        query = OnlineBooking.query.filter_by(trainer_id=current_user.id)
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(OnlineBooking.requested_date.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        bookings = [{
            'id': b.id, 'client_id': b.client_id, 'status': b.status,
            'requested_date': b.requested_date.isoformat(),
            'requested_time': b.requested_time.strftime('%H:%M'),
            'session_type': b.session_type, 'guest_name': b.guest_name,
            'guest_email': b.guest_email, 'notes': b.notes,
            'created_at': b.created_at.isoformat()
        } for b in pagination.items]
        
        return success_response({'bookings': bookings, 'pagination': {
            'page': pagination.page, 'per_page': pagination.per_page,
            'total_pages': pagination.pages, 'total_items': pagination.total
        }})
    except Exception as e:
        return error_response(f'Error fetching bookings: {str(e)}', 500)

@api_booking.route('/bookings', methods=['POST'])
@login_required
def create_booking():
    """Create online booking (by client or guest)."""
    try:
        data = request.get_json()
        if not data or not data.get('requested_date') or not data.get('requested_time'):
            return error_response('requested_date and requested_time are required')
        
        # For guests, require contact info
        if not data.get('client_id') and (not data.get('guest_name') or not data.get('guest_email')):
            return error_response('guest_name and guest_email required for non-client bookings')
        
        booking = OnlineBooking(
            trainer_id=current_user.id,
            client_id=data.get('client_id'),
            requested_date=date.fromisoformat(data['requested_date']),
            requested_time=datetime.strptime(data['requested_time'], '%H:%M').time(),
            session_type=data.get('session_type'),
            status='pending',
            guest_name=data.get('guest_name'),
            guest_email=data.get('guest_email'),
            guest_phone=data.get('guest_phone'),
            notes=data.get('notes')
        )
        db.session.add(booking)
        db.session.commit()
        
        return success_response({'id': booking.id, 'status': 'pending'}, 'Booking request created', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating booking: {str(e)}', 500)

@api_booking.route('/bookings/<int:booking_id>/status', methods=['PATCH'])
@login_required
def update_booking_status(booking_id):
    """Update booking status (confirm/decline/cancel)."""
    try:
        booking = OnlineBooking.query.get(booking_id)
        if not booking or booking.trainer_id != current_user.id:
            return error_response('Booking not found', 404)
        
        data = request.get_json()
        new_status = data.get('status')
        if new_status not in ['confirmed', 'declined', 'cancelled']:
            return error_response('Invalid status')
        
        booking.status = new_status
        if new_status == 'confirmed':
            booking.confirmed_at = datetime.utcnow()
        
        booking.updated_at = datetime.utcnow()
        db.session.commit()
        return success_response({'id': booking.id, 'status': new_status}, f'Booking {new_status}')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating booking: {str(e)}', 500)

@api_booking.route('/check-availability/<string:check_date>', methods=['GET'])
@login_required
def check_date_availability(check_date):
    """Check if specific date/time is available for booking."""
    try:
        target_date = date.fromisoformat(check_date)
        day_of_week = target_date.weekday()
        
        # Check exceptions first
        exception = BookingException.query.filter(
            BookingException.trainer_id == current_user.id,
            BookingException.start_date <= target_date,
            BookingException.end_date >= target_date
        ).first()
        
        if exception and exception.exception_type == 'unavailable':
            return success_response({'available': False, 'reason': 'Trainer unavailable'})
        
        # Get regular availability for this day
        slots = BookingAvailability.query.filter_by(
            trainer_id=current_user.id,
            day_of_week=day_of_week,
            is_active=True
        ).all()
        
        # Count existing bookings
        existing = OnlineBooking.query.filter(
            OnlineBooking.trainer_id == current_user.id,
            OnlineBooking.requested_date == target_date,
            OnlineBooking.status.in_(['pending', 'confirmed'])
        ).count()
        
        available_slots = []
        for slot in slots:
            if slot.max_bookings > existing:
                available_slots.append({
                    'start_time': slot.start_time.strftime('%H:%M'),
                    'end_time': slot.end_time.strftime('%H:%M'),
                    'session_type': slot.session_type,
                    'slots_remaining': slot.max_bookings - existing
                })
        
        return success_response({
            'date': check_date,
            'available': len(available_slots) > 0,
            'available_slots': available_slots
        })
    except Exception as e:
        return error_response(f'Error checking availability: {str(e)}', 500)
