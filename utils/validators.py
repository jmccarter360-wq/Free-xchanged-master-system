import re

# Email validation function

def is_valid_email(email):
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    return re.match(pattern, email) is not None

# Phone validation function

def is_valid_phone(phone):
    pattern = r'^\+?1?\d{9,15}$'
    return re.match(pattern, phone) is not None

# Amount validation function

def is_valid_amount(amount):
    try:
        amount = float(amount)
        return amount >= 0
    except ValueError:
        return False

# Customer validation function

def is_valid_customer(customer):
    return isinstance(customer, dict) and 'name' in customer and 'email' in customer and is_valid_email(customer['email'])