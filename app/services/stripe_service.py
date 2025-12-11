"""Stripe Payment Processing Service."""
import os
import stripe
from typing import Optional, Dict, Any, List
import logging
from decimal import Decimal

logger = logging.getLogger(__name__)


class StripeService:
    """Service for managing Stripe payments and subscriptions."""
    
    def __init__(self):
        """Initialize Stripe service with API keys from environment."""
        self.secret_key = os.environ.get('STRIPE_SECRET_KEY')
        self.publishable_key = os.environ.get('STRIPE_PUBLISHABLE_KEY')
        self.webhook_secret = os.environ.get('STRIPE_WEBHOOK_SECRET')
        
        if self.secret_key:
            stripe.api_key = self.secret_key
    
    def is_configured(self) -> bool:
        """Check if Stripe credentials are configured."""
        return bool(self.secret_key and self.publishable_key)
    
    def create_customer(
        self,
        email: str,
        name: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        """
        Create a Stripe customer.
        
        Args:
            email: Customer email address
            name: Customer name (optional)
            metadata: Additional metadata (optional)
            
        Returns:
            Stripe customer ID or None if failed
        """
        if not self.is_configured():
            logger.error("Stripe not configured")
            return None
        
        try:
            customer_data = {'email': email}
            if name:
                customer_data['name'] = name
            if metadata:
                customer_data['metadata'] = metadata
            
            customer = stripe.Customer.create(**customer_data)
            return customer.id
            
        except Exception as e:
            logger.error(f"Failed to create Stripe customer: {str(e)}")
            return None
    
    def create_payment_intent(
        self,
        amount: Decimal,
        currency: str = 'usd',
        customer_id: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a payment intent.
        
        Args:
            amount: Payment amount (will be converted to cents)
            currency: Currency code (default: usd)
            customer_id: Stripe customer ID (optional)
            description: Payment description (optional)
            metadata: Additional metadata (optional)
            
        Returns:
            Dictionary with payment intent details or None if failed
        """
        if not self.is_configured():
            logger.error("Stripe not configured")
            return None
        
        try:
            # Convert amount to cents
            amount_cents = int(amount * 100)
            
            intent_data = {
                'amount': amount_cents,
                'currency': currency,
                'automatic_payment_methods': {'enabled': True}
            }
            
            if customer_id:
                intent_data['customer'] = customer_id
            if description:
                intent_data['description'] = description
            if metadata:
                intent_data['metadata'] = metadata
            
            intent = stripe.PaymentIntent.create(**intent_data)
            
            return {
                'payment_intent_id': intent.id,
                'client_secret': intent.client_secret,
                'amount': amount,
                'currency': currency,
                'status': intent.status
            }
            
        except Exception as e:
            logger.error(f"Failed to create payment intent: {str(e)}")
            return None
    
    def create_subscription(
        self,
        customer_id: str,
        price_id: str,
        metadata: Optional[Dict[str, str]] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create a subscription.
        
        Args:
            customer_id: Stripe customer ID
            price_id: Stripe price ID
            metadata: Additional metadata (optional)
            
        Returns:
            Dictionary with subscription details or None if failed
        """
        if not self.is_configured():
            logger.error("Stripe not configured")
            return None
        
        try:
            subscription_data = {
                'customer': customer_id,
                'items': [{'price': price_id}],
                'payment_behavior': 'default_incomplete',
                'expand': ['latest_invoice.payment_intent']
            }
            
            if metadata:
                subscription_data['metadata'] = metadata
            
            subscription = stripe.Subscription.create(**subscription_data)
            
            return {
                'subscription_id': subscription.id,
                'customer_id': customer_id,
                'status': subscription.status,
                'current_period_end': subscription.current_period_end,
                'client_secret': subscription.latest_invoice.payment_intent.client_secret if subscription.latest_invoice else None
            }
            
        except Exception as e:
            logger.error(f"Failed to create subscription: {str(e)}")
            return None
    
    def cancel_subscription(self, subscription_id: str) -> bool:
        """
        Cancel a subscription.
        
        Args:
            subscription_id: Stripe subscription ID
            
        Returns:
            True if successful, False otherwise
        """
        if not self.is_configured():
            logger.error("Stripe not configured")
            return False
        
        try:
            stripe.Subscription.delete(subscription_id)
            return True
            
        except Exception as e:
            logger.error(f"Failed to cancel subscription: {str(e)}")
            return False
    
    def get_payment_intent(self, payment_intent_id: str) -> Optional[Dict[str, Any]]:
        """
        Get payment intent details.
        
        Args:
            payment_intent_id: Stripe payment intent ID
            
        Returns:
            Dictionary with payment intent details or None if failed
        """
        if not self.is_configured():
            logger.error("Stripe not configured")
            return None
        
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            
            return {
                'payment_intent_id': intent.id,
                'amount': Decimal(intent.amount) / 100,
                'currency': intent.currency,
                'status': intent.status,
                'customer_id': intent.customer,
                'description': intent.description
            }
            
        except Exception as e:
            logger.error(f"Failed to get payment intent: {str(e)}")
            return None
    
    def create_price(
        self,
        product_id: str,
        amount: Decimal,
        currency: str = 'usd',
        interval: Optional[str] = None,
        interval_count: int = 1
    ) -> Optional[str]:
        """
        Create a price for a product.
        
        Args:
            product_id: Stripe product ID
            amount: Price amount (will be converted to cents)
            currency: Currency code (default: usd)
            interval: Billing interval for subscriptions (month, year, etc.)
            interval_count: Number of intervals between billings
            
        Returns:
            Stripe price ID or None if failed
        """
        if not self.is_configured():
            logger.error("Stripe not configured")
            return None
        
        try:
            amount_cents = int(amount * 100)
            
            price_data = {
                'product': product_id,
                'unit_amount': amount_cents,
                'currency': currency
            }
            
            if interval:
                price_data['recurring'] = {
                    'interval': interval,
                    'interval_count': interval_count
                }
            
            price = stripe.Price.create(**price_data)
            return price.id
            
        except Exception as e:
            logger.error(f"Failed to create price: {str(e)}")
            return None
    
    def create_product(
        self,
        name: str,
        description: Optional[str] = None,
        metadata: Optional[Dict[str, str]] = None
    ) -> Optional[str]:
        """
        Create a product.
        
        Args:
            name: Product name
            description: Product description (optional)
            metadata: Additional metadata (optional)
            
        Returns:
            Stripe product ID or None if failed
        """
        if not self.is_configured():
            logger.error("Stripe not configured")
            return None
        
        try:
            product_data = {'name': name}
            if description:
                product_data['description'] = description
            if metadata:
                product_data['metadata'] = metadata
            
            product = stripe.Product.create(**product_data)
            return product.id
            
        except Exception as e:
            logger.error(f"Failed to create product: {str(e)}")
            return None
    
    def verify_webhook_signature(
        self,
        payload: bytes,
        signature: str
    ) -> Optional[Dict[str, Any]]:
        """
        Verify webhook signature and parse event.
        
        Args:
            payload: Raw request body
            signature: Stripe signature from header
            
        Returns:
            Parsed webhook event or None if verification failed
        """
        if not self.webhook_secret:
            logger.error("Webhook secret not configured")
            return None
        
        try:
            event = stripe.Webhook.construct_event(
                payload, signature, self.webhook_secret
            )
            return event
            
        except Exception as e:
            logger.error(f"Failed to verify webhook signature: {str(e)}")
            return None
    
    def get_customer_payment_methods(
        self,
        customer_id: str
    ) -> List[Dict[str, Any]]:
        """
        Get payment methods for a customer.
        
        Args:
            customer_id: Stripe customer ID
            
        Returns:
            List of payment method dictionaries
        """
        if not self.is_configured():
            logger.error("Stripe not configured")
            return []
        
        try:
            payment_methods = stripe.PaymentMethod.list(
                customer=customer_id,
                type='card'
            )
            
            return [
                {
                    'id': pm.id,
                    'type': pm.type,
                    'card_brand': pm.card.brand if pm.card else None,
                    'card_last4': pm.card.last4 if pm.card else None,
                    'exp_month': pm.card.exp_month if pm.card else None,
                    'exp_year': pm.card.exp_year if pm.card else None
                }
                for pm in payment_methods.data
            ]
            
        except Exception as e:
            logger.error(f"Failed to get payment methods: {str(e)}")
            return []


# Singleton instance
stripe_service = StripeService()
