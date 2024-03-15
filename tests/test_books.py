import pytest
import sys
import os
from unittest.mock import patch
import jwt

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
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
    with app.app_context():
        data = {"title": "Test Book"}

        # Mock the function responsible for generating JWT tokens
        with patch("jwt.encode") as mock_encode:
            mock_encode.return_value = "dummy_token"
            response = client.post(
                "/add-books", json=data, headers={"Authorization": "Bearer dummy_token"}
            )
        assert response.status_code == 201


def test_get_books(client):
    with app.app_context():
        response = client.get("/get-books")
        assert response.status_code == 200

        data = response.get_json()
        assert len(data["res"]) > 0


def test_get_book(client):
    with app.app_context():
        book = Book.query.first()
        if book:
            response = client.get(f"/get-book/{book.id}")
            assert response.status_code == 200
        else:
            pytest.skip("No books available in the database.")


def test_update_book(client):
    with app.app_context():
        book = Book.query.first()
        if book:
            data = {"title": "Updated Title", "available": False}
            response = client.put(f"/update-book/{book.id}", json=data)
            assert response.status_code == 200

            updated_book = Book.query.get(book.id)
            assert updated_book.title == "Updated Title"
            assert updated_book.available == False
        else:
            pytest.skip("No books available in the database.")


def test_delete_book(client):
    with app.app_context():
        book = Book.query.first()
        if book:
            response = client.delete(f"/delete-book/{book.id}")
            assert response.status_code == 200

            deleted_book = Book.query.get(book.id)
            assert deleted_book is None
        else:
            pytest.skip("No books available in the database.")
