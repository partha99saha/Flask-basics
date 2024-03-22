from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import get_config

app = Flask(__name__)

# Load configuration from environment variables or .env file
app.config.from_object(get_config())

# Explicitly set SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_DATABASE_URI"] = get_config().SQLALCHEMY_DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# ORM setup
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Routes import
from routes.auth_routes import auth_bp
from routes.book_routes import book_bp

# Register Blueprint
app.register_blueprint(auth_bp)
app.register_blueprint(book_bp)


if __name__ == "__main__":
    app.run(debug=True)
