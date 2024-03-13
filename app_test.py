import unittest
from flask_testing import TestCase
import json
import db
from app import app
from unittest.mock import MagicMock


class TestFlaskApp(TestCase):

    def create_app(self):
        return app

    def setUp(self):
        self.app = app.test_client()
        self.mock_db = MagicMock()
        self.app.application.config['DB'] = self.mock_db

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Flask App is Running on PORT: 5000", response.data)

    def test_add_book(self):
        # Define a mock request data
        mock_request_data = {
            'title': 'Test Book'
        }
        # Mock the view function of db module
        self.mock_db.view.return_value = []
        response = self.app.post('/add-books', json=mock_request_data)
        self.assertEqual(response.status_code, 200)

    def test_add_books(self):
        data = json.dumps({'title': 'Test Book'})
        response = self.app.post(
            '/add-books', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 409)
        self.assertIn(
            b"Book with title Test Book is already in library!", response.data)

    def test_get_books(self):
        response = self.app.get('/get-books')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Successfully all books retrived!", response.data)

    def test_get_book(self):
        response = self.app.get('/get-book/57752045')
        self.assertEqual(response.status_code, 404)
        self.assertIn(f"Book with id '{id}' was not found!", response.data)

    def test_update_book_titles(self):
        data = json.dumps({'title': 'Updated Title', 'available': False})
        response = self.app.put(
            '/update-book/57752045', data=data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            b"Successfully the book titled Updated Title updated", response.data)

    def test_delete_request(self):
        response = self.app.delete('/delete-book/57752045')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"No Book Found!", response.data)

    # def tearDown(self):
    #     db.session.remove()
    #     db.drop_all()


if __name__ == '__main__':
    unittest.main()
