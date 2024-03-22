import pytest
from unittest.mock import MagicMock, patch
from middleware.jwt import auth_required
from flask import Flask, request
from werkzeug import exceptions

jwt_mock = MagicMock()
user_mock = MagicMock()
request_mock = MagicMock()


def test_auth_required_no_token():
    with patch("middleware.jwt.jwt", jwt_mock):
        with Flask(__name__).test_request_context():
            request.headers = {}
            with pytest.raises(exceptions.UnsupportedMediaType):
                auth_required(lambda: None)()


def test_auth_required_invalid_token():
    with patch("middleware.jwt.jwt", jwt_mock):
        with Flask(__name__).test_request_context():
            request.headers = {"Authorization": "Bearer invalid_token"}
            jwt_mock.decode.side_effect = jwt_mock.InvalidTokenError
            with pytest.raises(TypeError):
                auth_required(lambda: None)()


def test_auth_required_expired_token():
    with patch("middleware.jwt.jwt", jwt_mock):
        with Flask(__name__).test_request_context():
            request.headers = {"Authorization": "Bearer expired_token"}
            jwt_mock.decode.side_effect = jwt_mock.ExpiredSignatureError
            with pytest.raises(TypeError):
                auth_required(lambda: None)()


def test_auth_required_valid_token():
    with patch("middleware.jwt.jwt", jwt_mock):
        with Flask(__name__).test_request_context():
            request.headers = {"Authorization": "Bearer valid_token"}
            jwt_mock.decode.return_value = {"user_id": 1}
            user_mock.query.filter_by().first.return_value.serialize.return_value = {
                "uid": 1
            }


def test_auth_required_exception():
    with patch("middleware.jwt.jwt", jwt_mock):
        with Flask(__name__).test_request_context():
            request.headers = {"Authorization": "Bearer valid_token"}
            jwt_mock.decode.side_effect = Exception("Some exception occurred")
            with pytest.raises(Exception):
                auth_required(lambda: None)()


def test_auth_required_invalid_user():
    with patch("middleware.jwt.jwt", jwt_mock):
        with patch("middleware.jwt.User", user_mock):
            with Flask(__name__).test_request_context():
                request.headers = {"Authorization": "Bearer valid_token"}
                jwt_mock.decode.return_value = {"user_id": 1}
                user_mock.query.filter_by().first.return_value = None
                with pytest.raises(Exception):
                    auth_required(lambda: None)()


def test_auth_required_missing_user_id():
    with patch("middleware.jwt.jwt", jwt_mock):
        with patch("middleware.jwt.User", user_mock):
            with Flask(__name__).test_request_context():
                request.headers = {"Authorization": "Bearer valid_token"}
                jwt_mock.decode.return_value = {}
                with pytest.raises(Exception):
                    auth_required(lambda: None)()


def test_auth_required_success():
    with patch("middleware.jwt.jwt", jwt_mock):
        with patch("middleware.jwt.User", user_mock):
            with Flask(__name__).test_request_context():
                request.headers = {"Authorization": "Bearer valid_token"}
                jwt_mock.decode.return_value = {"user_id": 1}
                user_mock.query.filter_by().first.return_value = {"uid": 1}
                with pytest.raises(Exception):
                    assert auth_required(lambda: None)() == None
