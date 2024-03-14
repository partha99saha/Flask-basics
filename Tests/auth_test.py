import pytest
from unittest.mock import MagicMock, patch
from app import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@patch('routes.User')
def test_signup_success(mock_User, client):
    mock_user_instance = MagicMock()
    mock_User.query.filter_by.return_value.first.return_value = None
    mock_User.return_value = mock_user_instance
    mock_user_instance.username = 'testuser'
    mock_user_instance.password = 'hashed_password'
    mock_user_instance.id = 1

    response = client.post(
        '/signup', json={'username': 'testuser', 'password': 'password123'})
    assert response.status_code == 200


@patch('routes.User')
def test_signup_existing_user(mock_User, client):
    mock_user_instance = MagicMock()
    mock_User.query.filter_by.return_value.first.return_value = MagicMock()
    mock_User.return_value = mock_user_instance

    response = client.post(
        '/signup', json={'username': 'existinguser', 'password': 'password123'})
    assert response.status_code == 400


@patch('routes.User')
def test_signup_invalid_email(mock_User, client):
    response = client.post(
        '/signup', json={'username': 'invalidemail', 'password': 'password123'})
    assert response.status_code == 400


@patch('routes.User')
def test_signup_invalid_password(mock_User, client):
    response = client.post(
        '/signup', json={'username': 'testuser', 'password': 'pass'})
    assert response.status_code == 400


@patch('routes.User')
def test_login_success(mock_User, client):
    mock_user_instance = MagicMock()
    mock_User.query.filter_by.return_value.first.return_value = mock_user_instance
    mock_user_instance.username = 'testuser'
    mock_user_instance.password = 'hashed_password'

    response = client.post(
        '/login', json={'username': 'testuser', 'password': 'password123'})
    assert response.status_code == 200


@patch('routes.User')
def test_login_failure(mock_User, client):
    mock_User.query.filter_by.return_value.first.return_value = None

    response = client.post(
        '/login', json={'username': 'invaliduser', 'password': 'password123'})
    assert response.status_code == 400
