import pytest
from unittest.mock import MagicMock
from app import app, db
from models.User import User


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        db.drop_all()


def test_signup(client):
    # Mock the request data
    client.post = MagicMock()
    client.post.json = MagicMock(
        return_value={'username': 'test_user', 'password': 'password'})

    # Make a request to the signup route
    response = client.post('/signup')

    # Assert the response
    assert response.status_code == 200
    assert b'User successfully created' in response.data


def test_login(client):
    # Create a test user
    test_user = User(username='test_user', password='password')
    db.session.add(test_user)
    db.session.commit()

    # Mock the request data
    client.post = MagicMock()
    client.post.json = MagicMock(
        return_value={'username': 'test_user', 'password': 'password'})

    # Make a request to the login route
    response = client.post('/login')

    # Assert the response
    assert response.status_code == 200
    assert b'token' in response.data
