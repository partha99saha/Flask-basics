import pytest
import sys
import os
from unittest.mock import patch

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


def create_dummy_book():
    # Create a dummy book for testing
    book = Book(title="Test Book", available=True)
    db.session.add(book)
    db.session.commit()
    return book.id


def create_access_token_mock(user_id):
    # Mock function to create access tokens
    return "dummy_token"


def test_add_books(client):
    data = {"title": "Test Book"}

    with patch("jwt.encode", side_effect=create_access_token_mock):
        response = client.post(
            "/add-books",
            json=data,
            headers={"Authorization": "Bearer dummy_token"},
        )
        assert response.status_code == 201


def test_get_books(client):
    create_dummy_book()
    with patch("jwt.encode", side_effect=create_access_token_mock):
        response = client.get(
            "/get-books", headers={"Authorization": "Bearer dummy_token"}
        )
        assert response.status_code == 200


def test_get_book(client):
    book_id = create_dummy_book()

    with patch("jwt.encode", side_effect=create_access_token_mock):
        response = client.get(
            f"/get-book/{book_id}",
            headers={"Authorization": "Bearer dummy_token"},
        )
        assert response.status_code == 200


def test_update_book(client):
    book_id = create_dummy_book()
    data = {"title": "Updated Title", "available": False}

    with patch("jwt.encode", side_effect=create_access_token_mock):
        response = client.put(
            f"/update-book/{book_id}",
            json=data,
            headers={"Authorization": "Bearer dummy_token"},
        )
        assert response.status_code == 200


def test_delete_book(client):
    book_id = create_dummy_book()

    with patch("jwt.encode", side_effect=create_access_token_mock):
        response = client.delete(
            f"/delete-book/{book_id}",
            headers={"Authorization": "Bearer dummy_token"},
        )
        assert response.status_code == 200
