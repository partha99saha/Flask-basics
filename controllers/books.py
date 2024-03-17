from flask import Flask, request, jsonify
from app import app, db
from models.Book import Book
from services.jwt import auth_required
from utils.utils import success_response, error_response


@app.route("/add-books", methods=["POST"])
@auth_required
def addBooks():
    try:
        title = request.json.get("title")
        if not title:
            return jsonify(error_response("Title is required")), 400

        existing_book = Book.query.filter_by(title=title).first()
        if existing_book:
            return (
                jsonify(
                    error_response(
                        f'Book with title "{title}" already exists in the library.'
                    )
                ),
                409,
            )

        new_book = Book(title=title, available=True)
        db.session.add(new_book)
        db.session.commit()

        return (jsonify(success_response(new_book.serialize())), 201)

    except Exception as e:
        print("Error occurred during add-books:", str(e))
        db.session.rollback()
        return (
            jsonify(error_response("An error occurred while adding the book.")),
            500,
        )


@app.route("/get-books", methods=["GET"])
@auth_required
def getBooks():
    try:
        library = Book.query.all()
        serialized_books = [book.serialize() for book in library]

        if serialized_books:
            return (jsonify(success_response(serialized_books)), 200)
        else:
            return (jsonify(error_response("No books found in the library!")), 404)
    except Exception as e:
        print("Error occurred during get-books:", str(e))
        return (
            jsonify(error_response("An error occurred while retrieving books")),
            500,
        )


@app.route("/get-book/<int:id>", methods=["GET"])
@auth_required
def getbook(id):
    try:
        book_details = Book.query.get(id)
        if not book_details:
            return jsonify(error_response("Book not found")), 404

        serialized_book = book_details.serialize()
        return (jsonify(success_response(serialized_book)), 200)

    except Exception as e:
        print("Error occurred during get-book:", str(e))
        return jsonify(error_response("Internal Server Error")), 500


@app.route("/update-book/<int:id>", methods=["PUT"])
@auth_required
def updateBookTitles(id):
    try:
        data = request.json
        title = data.get("title")
        availability = data.get("available")

        book_details = Book.query.get(id)
        if not book_details:
            return jsonify(error_response("No Book Found with that ID.")), 404

        if title is not None:
            book_details.title = title
        if availability is not None:
            book_details.available = availability

        db.session.commit()

        return (
            jsonify(
                success_response(f'Book titled with "{book_details.title}" updated.')
            ),
            200,
        )

    except Exception as e:
        print("Error occurred during update-title:", str(e))
        db.session.rollback()
        return (
            jsonify(error_response("An error occurred while updating the book.")),
            500,
        )


@app.route("/delete-book/<int:id>", methods=["DELETE"])
@auth_required
def deleteRequest(id):
    try:
        book_detail = Book.query.get(id)
        if book_detail:
            db.session.delete(book_detail)
            db.session.commit()
            return (jsonify(success_response("Book deleted successfully.")), 200)
        else:
            return jsonify(error_response("Book not found.")), 404
    except Exception as e:
        print("Error occurred during delete-book:", str(e))
        db.session.rollback()
        return (
            jsonify(error_response("An error occurred while deleting the book.")),
            500,
        )
