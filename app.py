from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import get_config

app = Flask(__name__)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config.from_object(get_config())

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
