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
from utils.send_email import send_reset_password_email


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
        if not user:
            return jsonify(error_response("User does not exists")), 400

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


def reset_password():
    """
    Reset user password.

    Args:
        user_id (str): The ID of the user.
        new_password (str): The new password for the user.

    Returns:
        JSON: Response message.
    """
    try:
        data = request.get_json()
        user_id = data.get("user_id")
        new_password = data.get("new_password")

        if not (user_id and new_password):
            return (
                jsonify(
                    error_response("User ID and new password are required")
                ),
                400,
            )
        if not is_validate_password(new_password):
            return (
                jsonify(error_response("Please enter a valid password")),
                400,
            )
        user = User.query.filter_by(id=user_id).first()
        if not user:
            return jsonify(error_response("User not found")), 404

        user.password = generate_password_hash(new_password)
        db.session.commit()

        return jsonify(success_response("Password reset successfully")), 200

    except Exception as e:
        # print("Error occurred during password reset:", str(e))
        db.session.rollback()
        return jsonify(error_response("Failed to reset password")), 500


def forgot_password():
    """
    Send reset password mail sent to the user's email.

    Args:
        username (str): The email address of the user.

    Returns:
        JSON: Response message.
    """
    try:
        data = request.get_json()
        email = data.get("username")

        if not email:
            return (
                jsonify(error_response("username address is required")),
                400,
            )
        if not is_valid_email(email):
            return (
                jsonify(error_response("Please enter a valid username")),
                400,
            )
        user = User.query.filter_by(username=email).first()
        if not user:
            return jsonify(error_response("username not found")), 404

        # Generate a token for password reset link and Send email
        # reset_token = encode_token(user)
        # send_reset_password_email(email, reset_token)
        return (
            jsonify(success_response("Password reset mail sent")),
            200,
        )

    except Exception as e:
        # print("Error occurred during forgot password:", str(e))
        db.session.rollback()
        return (
            jsonify(error_response("Failed to send reset mail")),
            500,
        )
