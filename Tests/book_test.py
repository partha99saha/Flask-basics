from unittest.mock import MagicMock
from app import app, db
from models import Book
import pytest
import json


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.session.remove()
            db.drop_all()


def test_add_books(client):
    book_data = {'title': 'Test Book'}
    response = client.post('/add-books', json=book_data)
    assert response.status_code == 201
    assert response.json['data']['title'] == 'Test Book'
    assert response.json['status'] == 201
    assert response.json['message'] == 'Book added successfully.'


def test_add_books_existing(client):
    book = Book(title='Existing Book', available=True)
    db.session.add(book)
    db.session.commit()
    response = client.post('/add-books', json={'title': 'Existing Book'})
    assert response.status_code == 409
    assert response.json['error'] == 'Book with title "Existing Book" already exists in the library.'
    assert response.json['status'] == 409


def test_get_books(client):
    Book(title='Test Book', available=True).save()
    response = client.get('/get-books')
    assert response.status_code == 200
    assert len(response.json['res']) == 1


def test_get_books_empty(client):
    response = client.get('/get-books')
    assert response.status_code == 404
    assert response.json['error'] == 'No books found in the library!'
    assert response.json['status'] == 404


def test_get_book(client):
    book = Book(title='Test Book', available=True)
    book.save()
    response = client.get(f'/get-book/{book.id}')
    assert response.status_code == 200
    assert response.json['book']['title'] == 'Test Book'


def test_get_book_not_found(client):
    response = client.get('/get-book/999')
    assert response.status_code == 404
    assert response.json['error'] == 'Book not found'
    assert response.json['status'] == 404


def test_update_book(client):
    book = Book(title='Old Title', available=True)
    book.save()
    update_data = {'title': 'New Title', 'available': False}
    response = client.put(f'/update-book/{book.id}', json=update_data)
    assert response.status_code == 200
    assert response.json['res']['title'] == 'New Title'
    assert response.json['res']['available'] == False


def test_update_book_not_found(client):
    update_data = {'title': 'New Title', 'available': False}
    response = client.put('/update-book/999', json=update_data)
    assert response.status_code == 404
    assert response.json['error'] == 'No Book Found with that ID.'
    assert response.json['status'] == 404


def test_delete_book(client):
    book = Book(title='Test Book', available=True)
    book.save()
    response = client.delete(f'/delete-book/{book.id}')
    assert response.status_code == 200
    assert response.json['status'] == 'success'
    assert response.json['message'] == 'Book deleted successfully.'


def test_delete_book_not_found(client):
    response = client.delete('/delete-book/999')
    assert response.status_code == 404
    assert response.json['error'] == 'Book not found.'
    assert response.json['status'] == 'error'
