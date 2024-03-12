from flask import Flask, request, jsonify
import os
import re
import datetime
import db
from models import Book


app = Flask(__name__)

if not os.path.isfile('books.db'):
    db.connect()


@app.route("/")
def index():
    return "Flask App is Running on PORT: 5000"


# def isValidEmail(email):
#     regex = re.compile(
#         r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
#     if re.fullmatch(regex, email):
#         return True
#     else:
#         return False
#
# {
#     'available': True,
#     'title': 'Don Quixote',
#     'timestamp': datetime.datetime.now()
# }

@app.route("/add-books", methods=['POST'])
def addBooks():
    req_data = request.get_json()
    # print(req_data)
    # email = req_data['email']
    # if not isValid(email):
    #     return jsonify({
    #         'status': '422',
    #         'res': 'failure',
    #         'error': 'Invalid email format. Please enter a valid email address'
    #     })
    title = req_data['title']
    library = [books.serialize() for books in db.view()]
    for books in library:
        if books['title'] == title:
            return jsonify({
                'res': f'Book with title {title} is already in library!',
                'status': '404'
            })

    books_details = Book(db.getNewId(), True, title, datetime.datetime.now())
    db.insert(books_details)

    return jsonify({
        'res': books_details.serialize(),
        'status': '200',
        'msg': 'Successfully a new book created!'
    })


@app.route('/get-books', methods=['GET'])
def getBooks():
    library = [books.serialize() for books in db.view()]
    if len(library) != 0:
        return jsonify({
            'res': library,
            'status': '200',
            'msg': 'Successfully all books retrived!'
        })
    else:
        return jsonify({
            'res': '',
            'status': '404',
            'msg': 'No books Found in library!',
        })


@app.route('/get-book/<id>', methods=['GET'])
def getbook(id):
    book_id = request.view_args
    if (book_id['id']):
        library = [books.serialize() for books in db.view()]
        for books in library:
            if books['id'] == int(book_id['id']):
                return jsonify({
                    'res': books,
                    'status': '200',
                    'msg': 'Successfully getting book'
                })
        return jsonify({
            'error': f"Book with id '{book_id['id']}' was not found!",
            'res': '',
            'status': '404'
        })
    else:
        return jsonify({
            'status': '400',
            'error': 'Book ID is missing'
        })


@app.route("/update-book/<id>", methods=['PUT'])
def updateBookTitles(id):
    book_id = request.view_args
    req_data = request.get_json()
    availability = req_data['available']
    title = req_data['title']
    uid = int(book_id['id'])

    library = [books.serialize() for books in db.view()]
    for books in library:
        if books['id'] == uid:
            books_details = Book(
                uid,
                availability,
                title,
                datetime.datetime.now()
            )
            db.update(books_details)

            return jsonify({
                'res': books_details.serialize(),
                'status': '200',
                'msg': f'Successfully the book titled {title} updated'
            })
    return jsonify({
        'res': f'Failed to update Book title: {title}!',
        'status': '404'
    })


@app.route('/delete-book/<id>', methods=['DELETE'])
def deleteRequest(id):
    book_id = request.view_args
    library = [books.serialize() for books in db.view()]
    if book_id:
        for books in library:
            if books['id'] == int(book_id['id']):
                db.delete(books['id'])
                updated_library = [books.serialize() for books in db.view()]
                return jsonify({
                    'res': updated_library,
                    'status': '200',
                    'msg': 'Successfully book deleted',
                    'no_of_books': len(updated_library)
                })
    else:
        return jsonify({
            'error': "No Book Found!",
            'status': '404'
        })


if __name__ == '__main__':
    app.run()
