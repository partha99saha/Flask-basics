import pytest
import sys
import os
from unittest.mock import patch
import jwt

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_dir)

from app import app, db
from models.Book import Book


@pytest.fixture
def client():
    app.config["TESTING"] = True
    client = app.test_client()

    # setup
    with app.app_context():
        db.create_all()
        yield client
        db.session.remove()
        db.drop_all()


def test_add_books(client):
    data = {"title": "Test Book"}

    with patch("jwt.encode") as mock_encode:
        mock_encode.return_value = "dummy_token"
        response = client.post(
            "/add-books", json=data, headers={"Authorization": "Bearer dummy_token"}
        )
        assert response.status_code == 201


def test_get_books(client):
    with patch("jwt.encode") as mock_encode:
        mock_encode.return_value = "dummy_token"

        response = client.get(
            "/get-books", headers={"Authorization": "Bearer dummy_token"}
        )
        assert response.status_code == 200


def test_get_book(client):
    with patch("jwt.encode") as mock_encode:
        mock_encode.return_value = "dummy_token"

        response = client.get(
            f"/get-book/{1}", headers={"Authorization": "Bearer dummy_token"}
        )
        assert response.status_code == 200


def test_update_book(client):
    with patch("jwt.encode") as mock_encode:
        mock_encode.return_value = "dummy_token"
        data = {"title": "Updated Title", "available": False}
        response = client.put(
            f"/update-book/{1}",
            json=data,
            headers={"Authorization": "Bearer dummy_token"},
        )
        assert response.status_code == 200

        updated_book = Book.query.get(1)
        assert updated_book.title == "Updated Title"
        assert updated_book.available == False


def test_delete_book(client):
    with patch("jwt.encode") as mock_encode:
        mock_encode.return_value = "dummy_token"

        response = client.delete(
            f"/delete-book/{1}", headers={"Authorization": "Bearer dummy_token"}
        )
        assert response.status_code == 200

        deleted_book = Book.query.get(1)
        assert deleted_book is None
