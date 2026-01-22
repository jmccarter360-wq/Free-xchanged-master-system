# Stripe ACH Integration

import stripe

# Set your secret key. Remember to switch to your live secret key in production!
stripe.api_key = 'your_secret_key'

# Function to create a source for ACH payment

def create_ach_source(customer_id, account_holder_name, account_number, routing_number):
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

# Example usage
# customer_id = 'cus_123'
# source = create_ach_source(customer_id, 'John Doe', '000123456', '110000000')
# print(source)