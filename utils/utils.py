import re

# Regular expression for basic email validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


# Alphanumeric password with minimum 8 characters
def is_validate_password(password):
    pattern = r"^(?=.*[a-zA-Z])(?=.*\d)[a-zA-Z\d]{8,}$"
    if re.match(pattern, password):
        return True
    else:
        return False


def success_response(message):
    return {'message': message, 'success': True}


def error_response(message):
    return {'message': message, 'success': False}
