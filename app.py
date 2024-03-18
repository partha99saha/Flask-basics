from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import get_config

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.from_object(get_config())

# ORM setup
db = SQLAlchemy(app)

# Models import
import models.user_model
import models.book_model

# Routes import
import routes.auth_routes
import routes.book_routes


if __name__ == "__main__":
    app.run(debug=True)
