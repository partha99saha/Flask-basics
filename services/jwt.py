from functools import wraps
from flask import request, jsonify
from models.User import User
import jwt
from app import app
from utils.utils import success_response, error_response


def decode_jwt(token):
    JWT_SECRET = app.config["JWT_SECRET"]
    decoded = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
    return decoded.get("user_id")


def auth_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        # Check if the token is provided in headers or not
        token = None
        if "Authorization" in request.headers:
            auth_header = request.headers["Authorization"]
            if auth_header.startswith("Bearer "):
                token = auth_header.split("Bearer ")[1]
        elif "x-access-token" in request.headers:
            token = request.headers["x-access-token"]
        elif "token" in request.json:
            token = request.json["token"]

        if not token:
            return jsonify(error_response("Token required")), 401

        try:
            user_id = decode_jwt(token)
            user = User.query.filter_by(id=user_id).first()
            user = user.serialize()
            if not user:
                return jsonify(success_response("Invalid User")), 401

        except jwt.ExpiredSignatureError:
            return jsonify(error_response("Token has expired")), 401
        except jwt.InvalidTokenError:
            return jsonify(error_response("Invalid Token")), 401

        # return f(user, *args, **kwargs)
        return f(*args, **kwargs)

    return decorator
