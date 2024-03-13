import datetime
import re

# Regular expression for basic email validation
def is_valid_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def success_response(message):
    return {'message': message, 'success': True}


def error_response(message):
    return {'message': message, 'success': False}
