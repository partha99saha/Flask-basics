from app import app
from controllers.auth_controller import (
    signup,
    login,
    forgot_password,
    reset_password,
)


@app.route("/signup", methods=["POST"])
def signup_route():
    """
    Route for user signup.

    Returns:
        JSON: Response message.
    """
    return signup()


@app.route("/login", methods=["POST"])
def login_route():
    """
    Route for user login.

    Returns:
        JSON: Response message.
    """
    return login()


@app.route("/reset_password", methods=["POST"])
def reset_password_route():
    """
    Route for resetting user password.

    Returns:
        JSON: Response message.
    """
    return reset_password()


@app.route("/forgot_password", methods=["POST"])
def forgot_password_route():
    """
    Route for sending password reset instructions.

    Returns:
        JSON: Response message.
    """
    return forgot_password()
