import pytest
import sys
import os
from unittest.mock import patch
from flask import jsonify, request

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, project_dir)

from app import app, db
from models.book_model import Book
from controllers.book_controller import (
    add_books,
    get_books,
    get_book,
    update_book_titles,
    delete_request,
)


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
    return book.uid


def create_access_token_mock(user_id):
    # Mock function to create access tokens
    return "dummy_token"


def test_add_books(client):
    # Test adding a book with no file
    data = {"title": "Test Book"}
    with patch("jwt.encode", side_effect=create_access_token_mock):
        response = client.post(
            "/add-books",
            json=data,
            headers={"Authorization": "Bearer dummy_token"},
        )
        assert response.status_code == 400

    # Test adding a book with missing title
    data = {}
    with patch("jwt.encode", side_effect=create_access_token_mock):
        response = client.post(
            "/add-books",
            json=data,
            headers={"Authorization": "Bearer dummy_token"},
        )
        assert response.status_code == 400

    # Test adding a book with existing title
    existing_title = "Test Book"
    create_dummy_book()  # Add a book with existing title
    data = {"title": existing_title}
    with patch("jwt.encode", side_effect=create_access_token_mock):
        response = client.post(
            "/add-books",
            json=data,
            headers={"Authorization": "Bearer dummy_token"},
        )
        assert response.status_code == 400

    # Test adding a book with empty file
    data = {"title": "Book With Empty File"}
    with patch("jwt.encode", side_effect=create_access_token_mock):
        response = client.post(
            "/add-books",
            data={"file": ""},
            query_string=data,
            headers={"Authorization": "Bearer dummy_token"},
        )
        assert response.status_code == 400


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


def test_add_books_exception():
    with pytest.raises(Exception):
        # Simulate a failure in database session
        def mock_session_rollback():
            raise Exception("Database session failed")

        db.session.rollback = mock_session_rollback
        response = add_books()
        assert response.status_code == 400
        assert response.json == jsonify({"message": "Title is required"}).json


def test_get_books_exception():
    with pytest.raises(Exception):
        # Simulate a failure in database session
        def mock_session_rollback():
            raise Exception("Database session failed")

        db.session.rollback = mock_session_rollback
        response = get_books()
        assert response.status_code == 500
        assert (
            response.json
            == jsonify(
                {"message": "An error occurred while retrieving books"}
            ).json
        )


def test_get_book_exception():
    with pytest.raises(Exception):
        # Simulate a failure in database session
        def mock_session_rollback():
            raise Exception("Database session failed")

        db.session.rollback = mock_session_rollback
        response = get_book(1)
        assert response.status_code == 500
        assert (
            response.json == jsonify({"message": "Internal Server Error"}).json
        )


def test_update_book_titles_exception():
    with pytest.raises(Exception):
        # Simulate a failure in database session
        def mock_session_rollback():
            raise Exception("Database session failed")

        db.session.rollback = mock_session_rollback
        response = update_book_titles(1)
        assert response.status_code == 404
        assert (
            response.json
            == jsonify({"message": "No Book Found with that ID."}).json
        )


def test_delete_request_exception():
    with pytest.raises(Exception):
        # Simulate a failure in database session
        def mock_session_rollback():
            raise Exception("Database session failed")

        db.session.rollback = mock_session_rollback
        response = delete_request(1)
        assert response.status_code == 500
        assert (
            response.json
            == jsonify(
                {"message": "An error occurred while deleting the book."}
            ).json
        )
