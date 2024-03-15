import pytest
from unittest.mock import MagicMock
from services.jwt import auth_required

# Mocking dependencies
jwt_mock = MagicMock()
user_mock = MagicMock()
request_mock = MagicMock()


# Patching dependencies
@pytest.fixture(autouse=True)
def patch_dependencies(monkeypatch):
    monkeypatch.setattr("services.jwt", jwt_mock)
    monkeypatch.setattr("services.User", user_mock)
    monkeypatch.setattr("services.request", request_mock)


# Test cases for auth_required decorator
def test_auth_required_no_token():
    request_mock.headers = {}
    assert auth_required(lambda: None)() == ({"message": "Token required"}, 401)


def test_auth_required_invalid_token():
    request_mock.headers = {"Authorization": "Bearer invalid_token"}
    jwt_mock.decode.side_effect = jwt.InvalidTokenError
    assert auth_required(lambda: None)() == ({"message": "Invalid Token"}, 401)


def test_auth_required_expired_token():
    request_mock.headers = {"Authorization": "Bearer expired_token"}
    jwt_mock.decode.side_effect = jwt.ExpiredSignatureError
    assert auth_required(lambda: None)() == ({"message": "Token has expired"}, 401)


def test_auth_required_valid_token():
    request_mock.headers = {"Authorization": "Bearer valid_token"}
    jwt_mock.decode.return_value = {"user_id": 123}
    user_mock.query.filter_by().first.return_value.serialize.return_value = {
        "id": 123,
        "username": "test_user",
    }
    assert auth_required(lambda: None)() == None
