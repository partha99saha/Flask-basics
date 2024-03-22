from flask import Blueprint
from controllers.auth_controller import (
    signup,
    login,
    forgot_password,
    reset_password,
)

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/signup", methods=["POST"])
def signup_route():
    """
    Route for user signup.

    Returns:
        JSON: Response message.
    """
    return signup()


@auth_bp.route("/login", methods=["POST"])
def login_route():
    """
    Route for user login.

    Returns:
        JSON: Response message.
    """
    return login()


@auth_bp.route("/reset_password", methods=["POST"])
def reset_password_route():
    """
    Route for resetting user password.

    Returns:
        JSON: Response message.
    """
    return reset_password()


@auth_bp.route("/forgot_password", methods=["POST"])
def forgot_password_route():
    """
    Route for sending password reset instructions.

    Returns:
        JSON: Response message.
    """
    return forgot_password()
