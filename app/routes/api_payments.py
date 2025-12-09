"""RESTful API for payments and subscriptions."""
from datetime import datetime, date, timedelta
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from sqlalchemy import func
import json
from app import db
from app.models.payments import PaymentPlan, Subscription, Payment
from app.models.client import Client

api_payments = Blueprint('api_payments', __name__, url_prefix='/api/v1/payments')

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

@api_payments.route('/plans', methods=['GET'])
@login_required
def get_payment_plans():
    """Get payment plans."""
    try:
        query = PaymentPlan.query.filter_by(trainer_id=current_user.id, is_active=True)
        plan_type = request.args.get('plan_type')
        if plan_type:
            query = query.filter_by(plan_type=plan_type)
        
        plans = query.order_by(PaymentPlan.price).all()
        
        return success_response({'plans': [{
            'id': p.id, 'name': p.name, 'plan_type': p.plan_type,
            'price': float(p.price), 'currency': p.currency,
            'sessions_included': p.sessions_included,
            'billing_frequency': p.billing_frequency,
            'features': p.get_features(), 'description': p.description
        } for p in plans]})
    except Exception as e:
        return error_response(f'Error fetching plans: {str(e)}', 500)

@api_payments.route('/plans', methods=['POST'])
@login_required
def create_payment_plan():
    """Create a new payment plan."""
    try:
        data = request.get_json()
        if not data or not data.get('name') or not data.get('price'):
            return error_response('name and price are required')
        
        plan = PaymentPlan(
            trainer_id=current_user.id,
            name=data['name'],
            plan_type=data.get('plan_type', 'package'),
            price=data['price'],
            currency=data.get('currency', 'USD'),
            sessions_included=data.get('sessions_included'),
            billing_frequency=data.get('billing_frequency'),
            description=data.get('description'),
            features_data=json.dumps(data.get('features', [])),
            is_active=data.get('is_active', True)
        )
        db.session.add(plan)
        db.session.commit()
        
        return success_response({'id': plan.id, 'name': plan.name}, 'Payment plan created', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating plan: {str(e)}', 500)

@api_payments.route('/plans/<int:plan_id>', methods=['PUT', 'PATCH'])
@login_required
def update_payment_plan(plan_id):
    """Update a payment plan."""
    try:
        plan = PaymentPlan.query.get(plan_id)
        if not plan or plan.trainer_id != current_user.id:
            return error_response('Plan not found', 404)
        
        data = request.get_json()
        fields = ['name', 'price', 'sessions_included', 'billing_frequency', 'description', 'is_active']
        for field in fields:
            if field in data:
                setattr(plan, field, data[field])
        
        if 'features' in data:
            plan.features_data = json.dumps(data['features'])
        
        plan.updated_at = datetime.utcnow()
        db.session.commit()
        return success_response({'id': plan.id}, 'Plan updated')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating plan: {str(e)}', 500)

@api_payments.route('/subscriptions', methods=['GET'])
@login_required
def get_subscriptions():
    """Get client subscriptions."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 100)
        client_id = request.args.get('client_id', type=int)
        status = request.args.get('status')
        
        query = Subscription.query.filter_by(trainer_id=current_user.id)
        if client_id:
            query = query.filter_by(client_id=client_id)
        if status:
            query = query.filter_by(status=status)
        
        query = query.order_by(Subscription.created_at.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        subscriptions = [{
            'id': s.id, 'client_id': s.client_id, 'payment_plan_id': s.payment_plan_id,
            'status': s.status, 'start_date': s.start_date.isoformat(),
            'end_date': s.end_date.isoformat() if s.end_date else None,
            'sessions_used': s.sessions_used, 'sessions_remaining': s.sessions_remaining,
            'next_billing_date': s.next_billing_date.isoformat() if s.next_billing_date else None,
            'created_at': s.created_at.isoformat()
        } for s in pagination.items]
        
        return success_response({'subscriptions': subscriptions, 'pagination': {
            'page': pagination.page, 'per_page': pagination.per_page,
            'total_pages': pagination.pages, 'total_items': pagination.total
        }})
    except Exception as e:
        return error_response(f'Error fetching subscriptions: {str(e)}', 500)

@api_payments.route('/subscriptions', methods=['POST'])
@login_required
def create_subscription():
    """Create a new subscription for a client."""
    try:
        data = request.get_json()
        if not data or not data.get('client_id') or not data.get('payment_plan_id'):
            return error_response('client_id and payment_plan_id are required')
        
        client = Client.query.get(data['client_id'])
        if not client or client.trainer_id != current_user.id:
            return error_response('Invalid client_id', 403)
        
        plan = PaymentPlan.query.get(data['payment_plan_id'])
        if not plan or plan.trainer_id != current_user.id:
            return error_response('Invalid payment_plan_id', 403)
        
        subscription = Subscription(
            client_id=data['client_id'],
            trainer_id=current_user.id,
            payment_plan_id=data['payment_plan_id'],
            status='active',
            start_date=date.fromisoformat(data.get('start_date', str(date.today()))),
            sessions_remaining=plan.sessions_included or 0,
            stripe_customer_id=data.get('stripe_customer_id'),
            stripe_subscription_id=data.get('stripe_subscription_id')
        )
        
        # Calculate next billing date based on plan
        if plan.billing_frequency == 'monthly':
            subscription.next_billing_date = subscription.start_date + timedelta(days=30)
        elif plan.billing_frequency == 'annual':
            subscription.next_billing_date = subscription.start_date + timedelta(days=365)
        
        db.session.add(subscription)
        db.session.commit()
        
        return success_response({'id': subscription.id, 'status': 'active'}, 'Subscription created', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error creating subscription: {str(e)}', 500)

@api_payments.route('/subscriptions/<int:sub_id>/status', methods=['PATCH'])
@login_required
def update_subscription_status(sub_id):
    """Update subscription status (pause/cancel)."""
    try:
        subscription = Subscription.query.get(sub_id)
        if not subscription or subscription.trainer_id != current_user.id:
            return error_response('Subscription not found', 404)
        
        data = request.get_json()
        new_status = data.get('status')
        if new_status not in ['active', 'paused', 'cancelled', 'expired']:
            return error_response('Invalid status')
        
        subscription.status = new_status
        if new_status in ['cancelled', 'expired']:
            subscription.end_date = date.today()
        
        subscription.updated_at = datetime.utcnow()
        db.session.commit()
        return success_response({'id': subscription.id, 'status': new_status}, 'Subscription updated')
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error updating subscription: {str(e)}', 500)

@api_payments.route('/transactions', methods=['GET'])
@login_required
def get_payments():
    """Get payment transactions."""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = min(request.args.get('per_page', 50, type=int), 100)
        client_id = request.args.get('client_id', type=int)
        status = request.args.get('status')
        
        query = Payment.query.filter_by(trainer_id=current_user.id)
        if client_id:
            query = query.filter_by(client_id=client_id)
        if status:
            query = query.filter_by(payment_status=status)
        
        query = query.order_by(Payment.payment_date.desc())
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)
        
        payments = [{
            'id': p.id, 'client_id': p.client_id, 'subscription_id': p.subscription_id,
            'payment_date': p.payment_date.isoformat(), 'amount': float(p.amount),
            'currency': p.currency, 'payment_method': p.payment_method,
            'payment_status': p.payment_status, 'transaction_id': p.transaction_id
        } for p in pagination.items]
        
        return success_response({'payments': payments, 'pagination': {
            'page': pagination.page, 'per_page': pagination.per_page,
            'total_pages': pagination.pages, 'total_items': pagination.total
        }})
    except Exception as e:
        return error_response(f'Error fetching payments: {str(e)}', 500)

@api_payments.route('/transactions', methods=['POST'])
@login_required
def record_payment():
    """Record a payment transaction."""
    try:
        data = request.get_json()
        if not data or not data.get('client_id') or not data.get('amount'):
            return error_response('client_id and amount are required')
        
        client = Client.query.get(data['client_id'])
        if not client or client.trainer_id != current_user.id:
            return error_response('Invalid client_id', 403)
        
        payment = Payment(
            client_id=data['client_id'],
            trainer_id=current_user.id,
            subscription_id=data.get('subscription_id'),
            amount=data['amount'],
            currency=data.get('currency', 'USD'),
            payment_method=data.get('payment_method', 'cash'),
            payment_status=data.get('payment_status', 'completed'),
            payment_date=date.fromisoformat(data.get('payment_date', str(date.today()))),
            transaction_id=data.get('transaction_id'),
            stripe_payment_intent_id=data.get('stripe_payment_intent_id'),
            notes=data.get('notes')
        )
        db.session.add(payment)
        db.session.commit()
        
        return success_response({'id': payment.id, 'payment_status': payment.payment_status},
                              'Payment recorded', 201)
    except Exception as e:
        db.session.rollback()
        return error_response(f'Error recording payment: {str(e)}', 500)

@api_payments.route('/revenue', methods=['GET'])
@login_required
def get_revenue_stats():
    """Get revenue statistics."""
    try:
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date', str(date.today()))
        
        query = Payment.query.filter(
            Payment.trainer_id == current_user.id,
            Payment.payment_status == 'completed'
        )
        
        if start_date:
            query = query.filter(Payment.payment_date >= date.fromisoformat(start_date))
        query = query.filter(Payment.payment_date <= date.fromisoformat(end_date))
        
        payments = query.all()
        total_revenue = sum(p.amount for p in payments)
        
        # Group by month
        monthly = {}
        for p in payments:
            month_key = p.payment_date.strftime('%Y-%m')
            monthly[month_key] = monthly.get(month_key, 0) + float(p.amount)
        
        return success_response({
            'total_revenue': float(total_revenue),
            'total_transactions': len(payments),
            'currency': 'USD',
            'monthly_breakdown': monthly,
            'period_start': start_date or payments[0].payment_date.isoformat() if payments else None,
            'period_end': end_date
        })
    except Exception as e:
        return error_response(f'Error calculating revenue: {str(e)}', 500)
