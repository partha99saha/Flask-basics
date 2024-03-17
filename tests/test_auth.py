import json
from werkzeug.security import generate_password_hash
import pytest
import sys
import os

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_dir)

from app import app, db
from models.User import User


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()

    # Setup
    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()


def test_signup_success(client):
    data = {"username": "testuser@example.com", "password": "TestPassword123"}
    response = client.post("/signup", json=data)
    assert response.status_code == 200


def test_signup_missing_data(client):
    data = {}
    response = client.post("/signup", json=data)
    assert response.status_code == 400


def test_signup_invalid_email(client):
    data = {"username": "invalidemail", "password": "TestPassword123"}
    response = client.post("/signup", json=data)
    assert response.status_code == 400


def test_signup_existing_user(client):
    # Create a user
    hashed_password = generate_password_hash("TestPassword123")
    existing_user = User(username="existinguser@example.com", password=hashed_password)
    db.session.add(existing_user)
    db.session.commit()

    # Try to signup with the same username
    data = {"username": "existinguser@example.com", "password": "TestPassword123"}
    response = client.post("/signup", json=data)
    assert response.status_code == 400


def test_login_success(client):
    # Create a user
    hashed_password = generate_password_hash("TestPassword123")
    new_user = User(username="testuser@example.com", password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    data = {"username": "testuser@example.com", "password": "TestPassword123"}
    response = client.post("/login", json=data)
    assert response.status_code == 200
    assert "token" in json.loads(response.data)


def test_login_missing_data(client):
    data = {}
    response = client.post("/login", json=data)
    assert response.status_code == 400


def test_login_invalid_credentials(client):
    # Create a user
    hashed_password = generate_password_hash("TestPassword123")
    new_user = User(username="testuser@example.com", password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    data = {"username": "testuser@example.com", "password": "InvalidPassword"}
    response = client.post("/login", json=data)
    assert response.status_code == 400


def test_login_nonexistent_user(client):
    data = {
        "username": "nonexistentuser@example.com",
        "password": "NonExistentPassword",
    }
    response = client.post("/login", json=data)
    assert response.status_code == 400
