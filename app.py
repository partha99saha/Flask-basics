from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['ENV'] = 'development'

# Configuration
if app.config['ENV'] == 'testing':
    app.config.from_object('config.TestingConfig')
else:
    app.config.from_object("config.DevelopmentConfig")

# ORM setup
db = SQLAlchemy(app)

# migration code
# migrate = Migrate(app, db)

# Routes setup
import Routes.auth
import Routes.books
from models.Book import Book
from models.User import User


if __name__ == "__main__":
    app.run(debug=True)
