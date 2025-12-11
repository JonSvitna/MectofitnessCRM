"""API routes for Stripe payment integration."""
from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.integrations import Integration
from app.models.payments import Payment
from app.models.client import Client
from app.services.stripe_service import stripe_service
from datetime import datetime
from decimal import Decimal
import logging

bp = Blueprint('api_stripe', __name__, url_prefix='/api/v1/stripe')
logger = logging.getLogger(__name__)


@bp.route('/status', methods=['GET'])
@login_required
def get_status():
    """Check if Stripe integration is configured and connected."""
    try:
        # Check if integration exists for user
        integration = Integration.query.filter_by(
            trainer_id=current_user.id,
            integration_type='stripe'
        ).first()
        
        return jsonify({
            'success': True,
            'configured': stripe_service.is_configured(),
            'connected': integration.is_connected if integration else False,
            'integration_id': integration.id if integration else None,
            'publishable_key': stripe_service.publishable_key if stripe_service.is_configured() else None
        })
    except Exception as e:
        logger.error(f"Error checking Stripe status: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to check status'}), 500


@bp.route('/connect', methods=['POST'])
@login_required
def connect():
    """Connect Stripe integration for the current user."""
    try:
        # Check if Stripe service is configured
        if not stripe_service.is_configured():
            return jsonify({
                'success': False,
                'error': 'Stripe credentials not configured in server'
            }), 400
        
        # Check if integration already exists
        integration = Integration.query.filter_by(
            trainer_id=current_user.id,
            integration_type='stripe'
        ).first()
        
        if not integration:
            integration = Integration(
                trainer_id=current_user.id,
                integration_type='stripe',
                integration_name='Stripe Payment Processing'
            )
            db.session.add(integration)
        
        # Mark as connected
        integration.is_connected = True
        integration.is_active = True
        integration.last_sync_at = datetime.utcnow()
        
        db.session.commit()
        
        logger.info(f"Stripe integration connected for user {current_user.id}")
        
        return jsonify({
            'success': True,
            'message': 'Stripe integration connected successfully',
            'integration_id': integration.id
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error connecting Stripe: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to connect Stripe'}), 500


@bp.route('/disconnect', methods=['POST'])
@login_required
def disconnect():
    """Disconnect Stripe integration."""
    try:
        integration = Integration.query.filter_by(
            trainer_id=current_user.id,
            integration_type='stripe'
        ).first()
        
        if integration:
            integration.is_connected = False
            integration.is_active = False
            db.session.commit()
            
            logger.info(f"Stripe integration disconnected for user {current_user.id}")
        
        return jsonify({
            'success': True,
            'message': 'Stripe integration disconnected'
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error disconnecting Stripe: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to disconnect Stripe'}), 500


@bp.route('/customers', methods=['POST'])
@login_required
def create_customer():
    """Create a Stripe customer for a client."""
    try:
        data = request.get_json()
        client_id = data.get('client_id')
        
        if not client_id:
            return jsonify({'success': False, 'error': 'Client ID required'}), 400
        
        # Get the client
        client = Client.query.get(client_id)
        if not client or client.trainer_id != current_user.id:
            return jsonify({'success': False, 'error': 'Client not found'}), 404
        
        # Check if customer already exists
        if client.stripe_customer_id:
            return jsonify({
                'success': False,
                'error': 'Stripe customer already exists for this client'
            }), 400
        
        # Create customer in Stripe
        customer_id = stripe_service.create_customer(
            email=client.email,
            name=f"{client.first_name} {client.last_name}",
            metadata={'client_id': str(client_id)}
        )
        
        if not customer_id:
            return jsonify({
                'success': False,
                'error': 'Failed to create Stripe customer'
            }), 500
        
        # Save to database
        client.stripe_customer_id = customer_id
        db.session.commit()
        
        logger.info(f"Stripe customer created for client {client_id}")
        
        return jsonify({
            'success': True,
            'customer_id': customer_id
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating Stripe customer: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to create customer'}), 500


@bp.route('/payment-intents', methods=['POST'])
@login_required
def create_payment_intent():
    """Create a payment intent for a payment."""
    try:
        data = request.get_json()
        amount = data.get('amount')
        client_id = data.get('client_id')
        description = data.get('description')
        
        if not amount or not client_id:
            return jsonify({
                'success': False,
                'error': 'Amount and client_id required'
            }), 400
        
        # Get the client
        client = Client.query.get(client_id)
        if not client or client.trainer_id != current_user.id:
            return jsonify({'success': False, 'error': 'Client not found'}), 404
        
        # Create customer if doesn't exist
        customer_id = client.stripe_customer_id
        if not customer_id:
            customer_id = stripe_service.create_customer(
                email=client.email,
                name=f"{client.first_name} {client.last_name}",
                metadata={'client_id': str(client_id)}
            )
            if customer_id:
                client.stripe_customer_id = customer_id
                db.session.commit()
        
        # Create payment intent
        intent_data = stripe_service.create_payment_intent(
            amount=Decimal(str(amount)),
            customer_id=customer_id,
            description=description,
            metadata={
                'client_id': str(client_id),
                'trainer_id': str(current_user.id)
            }
        )
        
        if not intent_data:
            return jsonify({
                'success': False,
                'error': 'Failed to create payment intent'
            }), 500
        
        # Create payment record
        payment = Payment(
            trainer_id=current_user.id,
            client_id=client_id,
            amount=Decimal(str(amount)),
            status='pending',
            payment_method='stripe',
            stripe_payment_intent_id=intent_data['payment_intent_id'],
            description=description
        )
        
        db.session.add(payment)
        db.session.commit()
        
        logger.info(f"Payment intent created for client {client_id}")
        
        return jsonify({
            'success': True,
            'client_secret': intent_data['client_secret'],
            'payment_id': payment.id,
            'payment_intent_id': intent_data['payment_intent_id']
        })
        
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating payment intent: {str(e)}")
        return jsonify({'success': False, 'error': 'Failed to create payment intent'}), 500


@bp.route('/webhook', methods=['POST'])
def webhook():
    """Handle Stripe webhooks."""
    try:
        payload = request.get_data()
        sig_header = request.headers.get('Stripe-Signature')
        
        # Verify webhook signature
        event = stripe_service.verify_webhook_signature(payload, sig_header)
        
        if not event:
            return jsonify({'success': False, 'error': 'Invalid signature'}), 400
        
        event_type = event['type']
        data = event['data']['object']
        
        logger.info(f"Received Stripe webhook: {event_type}")
        
        # Handle different event types
        if event_type == 'payment_intent.succeeded':
            payment_intent_id = data['id']
            
            # Update payment status
            payment = Payment.query.filter_by(
                stripe_payment_intent_id=payment_intent_id
            ).first()
            
            if payment:
                payment.status = 'completed'
                payment.paid_at = datetime.utcnow()
                db.session.commit()
                logger.info(f"Payment {payment.id} marked as completed")
        
        elif event_type == 'payment_intent.payment_failed':
            payment_intent_id = data['id']
            
            # Update payment status
            payment = Payment.query.filter_by(
                stripe_payment_intent_id=payment_intent_id
            ).first()
            
            if payment:
                payment.status = 'failed'
                db.session.commit()
                logger.info(f"Payment {payment.id} marked as failed")
        
        elif event_type == 'customer.subscription.created':
            subscription_id = data['id']
            customer_id = data['customer']
            
            # Find client by stripe customer ID
            client = Client.query.filter_by(stripe_customer_id=customer_id).first()
            
            if client:
                client.stripe_subscription_id = subscription_id
                db.session.commit()
                logger.info(f"Subscription created for client {client.id}")
        
        elif event_type == 'customer.subscription.deleted':
            subscription_id = data['id']
            
            # Find client by subscription ID
            client = Client.query.filter_by(stripe_subscription_id=subscription_id).first()
            
            if client:
                client.stripe_subscription_id = None
                db.session.commit()
                logger.info(f"Subscription cancelled for client {client.id}")
        
        return jsonify({'success': True})
        
    except Exception as e:
        logger.error(f"Error processing Stripe webhook: {str(e)}")
        return jsonify({'success': False}), 500
