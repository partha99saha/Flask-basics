from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ENV"] = "development"

# Configuration
if app.config["ENV"] == "testing":
    app.config.from_object("config.TestingConfig")
else:
    app.config.from_object("config.DevelopmentConfig")

# ORM setup
db = SQLAlchemy(app)

# Models import
from models.User import User
from models.Book import Book

# Routes import
import Routes.auth
import Routes.books


if __name__ == "__main__":
    app.run(debug=True)
