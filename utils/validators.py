def validate_email(email):
    import re
    pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def validate_phone_number(phone):
    pattern = r'^\+?[1-9]\d{1,14}$'
    return re.match(pattern, phone) is not None


def validate_username(username):
    pattern = r'^[a-zA-Z0-9_.-]{3,20}$'
    return re.match(pattern, username) is not None

