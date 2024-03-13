from functools import wraps
from flask import request, jsonify
from models.User import User
import jwt
from app import app
from utils.utils import success_response, error_response


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        # Check if the token is provided in headers or JSON payload
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization', None)
            token = token.replace('Bearer ', '')
        elif 'x-access-token' in request.headers:
            token = request.headers.get('x-access-token', None)
        elif 'token' in request.json:
            token = request.json.get('token', None)

        # If token is not provided
        if not token:
            return jsonify(error_response('Token required')), 401

        try:
            # Decode the token
            decoded = jwt.decode(token, app.config['JWT_SECRET'])
            # Retrieve user based on user ID from token
            user = User.query.filter_by(id=decoded.get('id')).first()
            if not user:
                return jsonify(success_response('Invalid User')), 401

        except jwt.ExpiredSignatureError:
            return jsonify(error_response('Token has expired')), 401
        except jwt.InvalidTokenError:
            return jsonify(error_response('Invalid Token')), 401

        # Pass the user to the route function
        return f(user, *args, **kwargs)

    return decorator
