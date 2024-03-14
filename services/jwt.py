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

        # Check if the token is provided in headers or not
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')
            if token.startswith('Bearer '):
                token = token.split('Bearer ')[1]
        elif 'x-access-token' in request.headers:
            token = request.headers.get('x-access-token')
        elif 'token' in request.json:
            token = request.json.get('token')

        # If token is not provided
        if not token:
            return jsonify(error_response('Token required')), 401

        try:
            # Decode the token
            JWT_SECRET = app.config['JWT_SECRET']
            decoded = jwt.decode(
                token, JWT_SECRET, algorithms=['HS256'])
            user_id = decoded.get('user_id')
            user = User.query.filter_by(id=user_id).first()
            user = user.serialize()
            if not user:
                return jsonify(success_response('Invalid User')), 401

        except jwt.ExpiredSignatureError:
            return jsonify(error_response('Token has expired')), 401
        except jwt.InvalidTokenError:
            return jsonify(error_response('Invalid Token')), 401

        return f(*args, **kwargs)

    return decorator
