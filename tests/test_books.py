import pytest
from unittest.mock import MagicMock, patch
import sys
import os

project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, project_dir)

from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


@patch("routes.Book")
def test_add_books_success(mock_Book, client):
    mock_book_instance = MagicMock()
    mock_Book.query.filter_by.return_value.first.return_value = None
    mock_Book.return_value = mock_book_instance
    mock_book_instance.serialize.return_value = {
        "title": "Test Book",
        "available": True,
    }

    response = client.post("/add-books", json={"title": "Test Book"})
    assert response.status_code == 201
    assert response.json == {
        "data": {"title": "Test Book", "available": True},
        "status": 201,
        "message": "Book added successfully.",
    }


@patch("routes.Book")
def test_add_books_existing(mock_Book, client):
    mock_Book.query.filter_by.return_value.first.return_value = MagicMock()

    response = client.post("/add-books", json={"title": "Existing Book"})
    assert response.status_code == 409
    assert response.json == {
        "error": 'Book with title "Existing Book" already exists in the library.',
        "status": 409,
    }


@patch("routes.Book")
def test_get_books_success(mock_Book, client):
    mock_book_instance = MagicMock()
    mock_book_instance.serialize.return_value = [
        {"title": "Book 1", "available": True},
        {"title": "Book 2", "available": False},
    ]
    mock_Book.query.all.return_value = [mock_book_instance]

    response = client.get("/get-books")
    assert response.status_code == 200
    assert response.json == {
        "res": [
            {"title": "Book 1", "available": True},
            {"title": "Book 2", "available": False},
        ],
        "status": 200,
        "msg": "Successfully retrieved all books!",
    }


@patch("routes.Book")
def test_get_books_empty(mock_Book, client):
    mock_Book.query.all.return_value = []

    response = client.get("/get-books")
    assert response.status_code == 404
    assert response.json == {
        "error": "No books found in the library!", "status": 404}


@patch("routes.Book")
def test_get_book_success(mock_Book, client):
    mock_book_instance = MagicMock()
    mock_book_instance.serialize.return_value = {
        "title": "Test Book",
        "available": True,
    }
    mock_Book.query.get.return_value = mock_book_instance

    response = client.get("/get-book/1")
    assert response.status_code == 200
    assert response.json == {
        "book": {"title": "Test Book", "available": True},
        "status": 200,
        "msg": "Successfully retrieved book",
    }


@patch("routes.Book")
def test_get_book_not_found(mock_Book, client):
    mock_Book.query.get.return_value = None

    response = client.get("/get-book/1")
    assert response.status_code == 404
    assert response.json == {"error": "Book not found", "status": 404}


@patch("routes.Book")
def test_update_book_success(mock_Book, client):
    mock_book_instance = MagicMock()
    mock_Book.query.get.return_value = mock_book_instance

    response = client.put(
        "/update-book/1", json={"title": "Updated Title", "available": False}
    )
    assert response.status_code == 200
    assert response.json == {
        "res": {"title": "Updated Title", "available": False},
        "status": 200,
        "msg": 'Successfully updated the book titled "Updated Title".',
    }


@patch("routes.Book")
def test_update_book_not_found(mock_Book, client):
    mock_Book.query.get.return_value = None

    response = client.put("/update-book/1", json={"title": "Updated Title"})
    assert response.status_code == 404
    assert response.json == {
        "error": "No Book Found with that ID.", "status": 404}


@patch("routes.Book")
def test_delete_book_success(mock_Book, client):
    mock_book_instance = MagicMock()
    mock_Book.query.get.return_value = mock_book_instance

    response = client.delete("/delete-book/1")
    assert response.status_code == 200
    assert response.json == {"status": 200,
                             "message": "Book deleted successfully."}


@patch("routes.Book")
def test_delete_book_not_found(mock_Book, client):
    mock_Book.query.get.return_value = None

    response = client.delete("/delete-book/1")
    assert response.status_code == 404
    assert response.json == {"error": "Book not found.", "status": 404}
