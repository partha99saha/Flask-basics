from flask import Flask, request, jsonify
from app import app, db
from models.Book import Book
from services.jwt import auth_required


@app.route("/add-books", methods=['POST'])
@auth_required
def addBooks():
    try:
        title = request.json.get('title')
        if not title:
            return jsonify({
                'error': 'Title is required in the request JSON.',
                'status': 400
            }), 400

        existing_book = Book.query.filter_by(title=title).first()
        if existing_book:
            return jsonify({
                'error': f'Book with title "{title}" already exists in the library.',
                'status': 409
            }), 409

        new_book = Book(title=title, available=True)
        db.session.add(new_book)
        db.session.commit()

        return jsonify({
            'data': new_book.serialize(),
            'status': 201,
            'message': 'Book added successfully.'
        }), 201

    except Exception as e:
        print("Error occurred during add-books:", str(e))
        db.session.rollback()
        return jsonify({
            'error': 'An error occurred while adding the book.',
            'status': 500
        }), 500


@app.route('/get-books', methods=['GET'])
@auth_required
def getBooks():
    try:
        library = Book.query.all()
        serialized_books = [book.serialize() for book in library]

        if serialized_books:
            return jsonify({
                'res': serialized_books,
                'status': 200,
                'msg': 'Successfully retrieved all books!'
            })
        else:
            return jsonify({
                'error': 'No books found in the library!',
                'status': 404
            })
    except Exception as e:
        print("Error occurred during get-books:", str(e))
        return jsonify({
            'error': 'An error occurred while retrieving books',
            'status': 500,
            'details': str(e)
        })


@app.route('/get-book/<int:id>', methods=['GET'])
@auth_required
def getbook(id):
    try:
        book_details = Book.query.get(id)
        if not book_details:
            return jsonify({
                'error': 'Book not found',
                'status': 404
            }), 404

        serialized_book = book_details.serialize()
        return jsonify({
            'book': serialized_book,
            'status': 200,
            'msg': 'Successfully retrieved book'
        }), 200

    except Exception as e:
        print("Error occurred during get-book:", str(e))
        return jsonify({
            'error': 'Internal Server Error',
            'status': 500,
            'msg': str(e)
        }), 500


@app.route("/update-book/<int:id>", methods=['PUT'])
@auth_required
def updateBookTitles(id):
    try:
        data = request.json
        title = data.get('title')
        availability = data.get('available')

        book_details = Book.query.get(id)
        if not book_details:
            return jsonify({
                'error': 'No Book Found with that ID.',
                'status': 404
            }), 404

        if title is not None:
            book_details.title = title
        if availability is not None:
            book_details.available = availability

        db.session.commit()

        return jsonify({
            'res': book_details.serialize(),
            'status': 200,
            'msg': f'Successfully updated the book titled "{book_details.title}".'
        }), 200

    except Exception as e:
        print("Error occurred during update-title:", str(e))
        db.session.rollback()
        return jsonify({
            'error': 'An error occurred while updating the book.',
            'status': 500
        }), 500


@app.route('/delete-book/<int:id>', methods=['DELETE'])
@auth_required
def deleteRequest(id):
    try:
        book_detail = Book.query.get(id)
        if book_detail:
            db.session.delete(book_detail)
            db.session.commit()
            return jsonify({
                'status': 'success',
                'message': 'Book deleted successfully.'
            }), 200
        else:
            return jsonify({
                'error': 'Book not found.',
                'status': 'error'
            }), 404
    except Exception as e:
        print("Error occurred during delete-book:", str(e))
        db.session.rollback()
        return jsonify({
            'error': 'An error occurred while deleting the book.',
            'status': 'error'
        }), 500
