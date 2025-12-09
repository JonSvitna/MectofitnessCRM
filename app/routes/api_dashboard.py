"""RESTful API for trainer dashboard and analytics."""
from datetime import datetime, date, timedelta
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func, and_
from app import db
from app.models.client import Client
from app.models.session import Session
from app.models.program import Program
from app.models.progress import ProgressEntry
from app.models.nutrition import NutritionPlan, FoodLog
from app.models.booking import OnlineBooking
from app.models.payments import Payment, Subscription

api_dashboard = Blueprint('api_dashboard', __name__, url_prefix='/api/v1/dashboard')

def error_response(message, status_code=400):
    return jsonify({'success': False, 'error': message}), status_code

def success_response(data=None, message=None, status_code=200):
    response = {'success': True}
    if message:
        response['message'] = message
    if data is not None:
        response['data'] = data
    return jsonify(response), status_code

@api_dashboard.route('/overview', methods=['GET'])
@login_required
def get_dashboard_overview():
    """Get comprehensive dashboard overview."""
    try:
        days = request.args.get('days', 30, type=int)
        start_date = date.today() - timedelta(days=days)
        
        # Client stats
        total_clients = Client.query.filter_by(trainer_id=current_user.id, status='active').count()
        new_clients = Client.query.filter(
            Client.trainer_id == current_user.id,
            Client.created_at >= start_date
        ).count()
        
        # Session stats
        total_sessions = Session.query.filter_by(trainer_id=current_user.id).count()
        completed_sessions = Session.query.filter_by(
            trainer_id=current_user.id, status='completed'
        ).filter(Session.session_date >= start_date).count()
        
        upcoming_sessions = Session.query.filter(
            Session.trainer_id == current_user.id,
            Session.session_date >= date.today(),
            Session.status == 'scheduled'
        ).count()
        
        # Program stats
        active_programs = Program.query.filter_by(
            trainer_id=current_user.id, status='active'
        ).count()
        
        # Revenue stats
        revenue = db.session.query(func.sum(Payment.amount)).filter(
            Payment.trainer_id == current_user.id,
            Payment.payment_status == 'completed',
            Payment.payment_date >= start_date
        ).scalar() or 0
        
        # Active subscriptions
        active_subscriptions = Subscription.query.filter_by(
            trainer_id=current_user.id, status='active'
        ).count()
        
        # Pending bookings
        pending_bookings = OnlineBooking.query.filter_by(
            trainer_id=current_user.id, status='pending'
        ).count()
        
        return success_response({
            'period_days': days,
            'clients': {
                'total_active': total_clients,
                'new_this_period': new_clients
            },
            'sessions': {
                'total': total_sessions,
                'completed_this_period': completed_sessions,
                'upcoming': upcoming_sessions
            },
            'programs': {
                'active': active_programs
            },
            'revenue': {
                'total_this_period': float(revenue),
                'currency': 'USD',
                'active_subscriptions': active_subscriptions
            },
            'bookings': {
                'pending': pending_bookings
            }
        })
    except Exception as e:
        return error_response(f'Error fetching overview: {str(e)}', 500)

@api_dashboard.route('/activity', methods=['GET'])
@login_required
def get_recent_activity():
    """Get recent activity feed."""
    try:
        limit = request.args.get('limit', 20, type=int)
        
        activities = []
        
        # Recent clients
        recent_clients = Client.query.filter_by(
            trainer_id=current_user.id
        ).order_by(Client.created_at.desc()).limit(5).all()
        
        for client in recent_clients:
            activities.append({
                'type': 'new_client',
                'timestamp': client.created_at.isoformat(),
                'description': f'New client: {client.first_name} {client.last_name}',
                'client_id': client.id
            })
        
        # Recent sessions
        recent_sessions = Session.query.filter_by(
            trainer_id=current_user.id
        ).order_by(Session.session_date.desc()).limit(5).all()
        
        for session in recent_sessions:
            activities.append({
                'type': 'session',
                'timestamp': session.session_date.isoformat(),
                'description': f'Session: {session.session_type} - {session.status}',
                'client_id': session.client_id,
                'status': session.status
            })
        
        # Recent payments
        recent_payments = Payment.query.filter_by(
            trainer_id=current_user.id
        ).order_by(Payment.payment_date.desc()).limit(5).all()
        
        for payment in recent_payments:
            activities.append({
                'type': 'payment',
                'timestamp': payment.payment_date.isoformat(),
                'description': f'Payment received: ${payment.amount}',
                'client_id': payment.client_id,
                'amount': float(payment.amount)
            })
        
        # Sort all activities by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return success_response({'activities': activities[:limit]})
    except Exception as e:
        return error_response(f'Error fetching activity: {str(e)}', 500)

@api_dashboard.route('/calendar', methods=['GET'])
@login_required
def get_calendar_view():
    """Get calendar view of sessions."""
    try:
        start_date = request.args.get('start_date', str(date.today()))
        end_date = request.args.get('end_date', str(date.today() + timedelta(days=7)))
        
        sessions = Session.query.filter(
            Session.trainer_id == current_user.id,
            Session.session_date >= date.fromisoformat(start_date),
            Session.session_date <= date.fromisoformat(end_date)
        ).order_by(Session.session_date, Session.session_time).all()
        
        calendar_events = []
        for s in sessions:
            calendar_events.append({
                'id': s.id,
                'date': s.session_date.isoformat(),
                'time': s.session_time.strftime('%H:%M') if s.session_time else None,
                'duration': s.duration_minutes,
                'client_id': s.client_id,
                'session_type': s.session_type,
                'status': s.status,
                'location': s.location
            })
        
        return success_response({
            'start_date': start_date,
            'end_date': end_date,
            'events': calendar_events
        })
    except Exception as e:
        return error_response(f'Error fetching calendar: {str(e)}', 500)

@api_dashboard.route('/client-progress/<int:client_id>', methods=['GET'])
@login_required
def get_client_progress_summary(client_id):
    """Get quick progress summary for a client."""
    try:
        client = Client.query.get(client_id)
        if not client or client.trainer_id != current_user.id:
            return error_response('Client not found', 404)
        
        # Get latest progress entry
        latest_progress = ProgressEntry.query.filter_by(
            client_id=client_id
        ).order_by(ProgressEntry.entry_date.desc()).first()
        
        # Get session count
        total_sessions = Session.query.filter_by(
            client_id=client_id, status='completed'
        ).count()
        
        # Get active programs
        active_programs = Program.query.filter_by(
            trainer_id=current_user.id, status='active'
        ).join(Program.clients).filter(Client.id == client_id).count()
        
        # Get subscription
        active_subscription = Subscription.query.filter_by(
            client_id=client_id, status='active'
        ).first()
        
        summary = {
            'client_id': client_id,
            'client_name': f'{client.first_name} {client.last_name}',
            'total_sessions': total_sessions,
            'active_programs': active_programs,
            'latest_progress': None,
            'subscription': None
        }
        
        if latest_progress:
            summary['latest_progress'] = {
                'date': latest_progress.entry_date.isoformat(),
                'weight': latest_progress.weight,
                'body_fat': latest_progress.body_fat_percentage
            }
        
        if active_subscription:
            summary['subscription'] = {
                'id': active_subscription.id,
                'status': active_subscription.status,
                'sessions_remaining': active_subscription.sessions_remaining
            }
        
        return success_response(summary)
    except Exception as e:
        return error_response(f'Error fetching client progress: {str(e)}', 500)

@api_dashboard.route('/stats/sessions', methods=['GET'])
@login_required
def get_session_stats():
    """Get detailed session statistics."""
    try:
        days = request.args.get('days', 30, type=int)
        start_date = date.today() - timedelta(days=days)
        
        sessions = Session.query.filter(
            Session.trainer_id == current_user.id,
            Session.session_date >= start_date
        ).all()
        
        # Group by status
        by_status = {}
        for s in sessions:
            by_status[s.status] = by_status.get(s.status, 0) + 1
        
        # Group by type
        by_type = {}
        for s in sessions:
            by_type[s.session_type] = by_type.get(s.session_type, 0) + 1
        
        # Daily count
        daily_counts = {}
        for s in sessions:
            date_key = s.session_date.isoformat()
            daily_counts[date_key] = daily_counts.get(date_key, 0) + 1
        
        return success_response({
            'period_days': days,
            'total_sessions': len(sessions),
            'by_status': by_status,
            'by_type': by_type,
            'daily_counts': daily_counts
        })
    except Exception as e:
        return error_response(f'Error fetching session stats: {str(e)}', 500)

@api_dashboard.route('/stats/revenue', methods=['GET'])
@login_required
def get_revenue_breakdown():
    """Get revenue breakdown and trends."""
    try:
        days = request.args.get('days', 90, type=int)
        start_date = date.today() - timedelta(days=days)
        
        payments = Payment.query.filter(
            Payment.trainer_id == current_user.id,
            Payment.payment_status == 'completed',
            Payment.payment_date >= start_date
        ).all()
        
        total = sum(p.amount for p in payments)
        
        # Monthly breakdown
        monthly = {}
        for p in payments:
            month_key = p.payment_date.strftime('%Y-%m')
            monthly[month_key] = monthly.get(month_key, 0) + float(p.amount)
        
        # By payment method
        by_method = {}
        for p in payments:
            method = p.payment_method or 'unknown'
            by_method[method] = by_method.get(method, 0) + float(p.amount)
        
        # Average per client
        unique_clients = len(set(p.client_id for p in payments))
        avg_per_client = float(total / unique_clients) if unique_clients > 0 else 0
        
        return success_response({
            'period_days': days,
            'total_revenue': float(total),
            'total_transactions': len(payments),
            'unique_clients': unique_clients,
            'average_per_client': avg_per_client,
            'monthly_breakdown': monthly,
            'by_payment_method': by_method,
            'currency': 'USD'
        })
    except Exception as e:
        return error_response(f'Error fetching revenue breakdown: {str(e)}', 500)
