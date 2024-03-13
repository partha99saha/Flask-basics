from app import app, db
from werkzeug.security import generate_password_hash, check_password_hash
from models.User import User
from flask import jsonify, request
import jwt
import datetime
from utils.utils import success_response, error_response


@app.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        if not (username and password):
            return jsonify(error_response('Please submit a username and a password')), 400

        # Hash the password using bcrypt
        hashed_password = generate_password_hash(password)

        new_user = User(username=username, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify(success_response('User successfully created')), 200

    except Exception as e:
        print("Error occurred during signup:", str(e))
        db.session.rollback()
        return jsonify(error_response('Failed to create user')), 500


@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        # Missing credentials
        if not (username and password):
            return jsonify({'error': 'Please provide username and password'}), 400

        # Query the user from the database
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            # Authentication successful, generate JWT token
            token = jwt.encode({'id': user.id,
                                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)},
                               app.config['JWT_SECRET'], algorithm='HS256')
            return jsonify({'token': token}), 200

    except Exception as e:
        print("Error occurred during login:", str(e))
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error'}), 500
