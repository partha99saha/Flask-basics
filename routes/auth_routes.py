from app import app
from controllers.auth_controller import signup, login


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
