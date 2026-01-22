# Stripe ACH Integration

import stripe
import os
from utils.retry_logic import retry
from utils.error_handlers import ValidationError

# Set your secret key from environment variable
stripe.api_key = os.environ.get('STRIPE_API_KEY', 'your_secret_key')


class StripeService:
    """Service for handling Stripe payment operations"""
    
    @staticmethod
    @retry(max_attempts=3, delay=1, backoff=2)
    def create_customer(email, name):
        """Create a Stripe customer"""
        try:
            customer = stripe.Customer.create(
                email=email,
                name=name
            )
            return customer
        except stripe.error.StripeError as e:
            raise ValidationError(f"Stripe error: {str(e)}")
    
    @staticmethod
    @retry(max_attempts=3, delay=1, backoff=2)
    def create_ach_source(customer_id, account_holder_name, account_number, routing_number):
        """Create a source for ACH payment"""
        try:
            source = stripe.Source.create(
                type='ach_credit_transfer',
                owner={
                    'name': account_holder_name,
                },
                ach_credit_transfer={
                    'account_number': account_number,
                    'routing_number': routing_number,
                },
                customer=customer_id,
            )
            return source
        except stripe.error.StripeError as e:
            raise ValidationError(f"Stripe error: {str(e)}")
    
    @staticmethod
    @retry(max_attempts=3, delay=1, backoff=2)
    def create_payout(amount, destination, currency='usd'):
        """Create a payout to a bank account"""
        try:
            # Amount should be in cents
            amount_cents = int(amount * 100)
            
            payout = stripe.Payout.create(
                amount=amount_cents,
                currency=currency,
                destination=destination
            )
            return payout
        except stripe.error.StripeError as e:
            raise ValidationError(f"Stripe error: {str(e)}")
    
    @staticmethod
    @retry(max_attempts=3, delay=1, backoff=2)
    def charge_customer(customer_id, amount, currency='usd', description=None):
        """Charge a customer"""
        try:
            # Amount should be in cents
            amount_cents = int(amount * 100)
            
            charge = stripe.Charge.create(
                customer=customer_id,
                amount=amount_cents,
                currency=currency,
                description=description
            )
            return charge
        except stripe.error.StripeError as e:
            raise ValidationError(f"Stripe error: {str(e)}")
    
    @staticmethod
    def get_balance():
        """Get Stripe account balance"""
        try:
            balance = stripe.Balance.retrieve()
            return balance
        except stripe.error.StripeError as e:
            raise ValidationError(f"Stripe error: {str(e)}")


# Backward compatibility functions
def create_ach_source(customer_id, account_holder_name, account_number, routing_number):
    """Legacy function for creating ACH source"""
    return StripeService.create_ach_source(
        customer_id, account_holder_name, account_number, routing_number
    )
