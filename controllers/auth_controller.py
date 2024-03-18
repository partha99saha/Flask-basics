from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from models.user_model import User
from flask import jsonify, request
import jwt
import datetime
from utils.utils import (
    success_response,
    error_response,
    is_valid_email,
    is_validate_password,
)


def signup():
    """
    Controller function for user signup.

    Returns:
        JSON: Response message.
    """
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not (username and password):
            return (
                jsonify(error_response("Please enter username and password")),
                400,
            )
        if not is_valid_email(username):
            return (
                jsonify(error_response("Please enter a valid username")),
                400,
            )
        if not is_validate_password(password):
            return (
                jsonify(error_response("Please enter a valid password")),
                400,
            )

        is_existing_user = User.query.filter_by(username=username).first()
        if is_existing_user:
            return jsonify(error_response("User already exists")), 400

        # Hash the password using bcrypt
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(success_response("User successfully created")), 200

    except Exception as e:
        # print("Error occurred during signup:", str(e))
        db.session.rollback()
        return jsonify(error_response("Failed to create user")), 500


def encode_token(user):
    """
    Encode JWT token.

    Args:
        user: User object.

    Returns:
        str: JWT token.
    """
    payload = {
        "user_id": user.id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24),
    }
    secret_key = app.config["JWT_SECRET"]
    # generate JWT token
    token = jwt.encode(payload, secret_key, algorithm="HS256")
    return token


def login():
    """
    Controller function for user login.

    Returns:
        JSON: Response message.
    """
    try:
        data = request.get_json()
        username = data.get("username")
        password = data.get("password")

        if not (username and password):
            return (
                jsonify(
                    error_response("Please provide username and password")
                ),
                400,
            )

        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            token = encode_token(user)
            return jsonify({"token": token}), 200
        else:
            return (
                jsonify(
                    error_response(
                        "Login failed, Username or password is wrong"
                    )
                ),
                400,
            )

    except Exception as e:
        # print("Error occurred during login:", str(e))
        db.session.rollback()
        return jsonify(error_response("Internal Server Error")), 500
