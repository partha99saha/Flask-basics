from flask import request, jsonify
from app import db
from models.book_model import Book
from utils.utils import success_response, error_response


def add_books():
    """
    Add a new book to the library.

    Returns:
        JSON: Serialized book data with success message.
    """
    try:
        title = request.json.get("title")
        if not title:
            return jsonify(error_response("Title is required")), 400

        existing_book = db.session.query(Book).filter_by(title=title).first()
        if existing_book:
            return (
                jsonify(
                    error_response(
                        f"""Book with title "{title}"
                        already exists in the library"""
                    )
                ),
                409,
            )

        new_book = Book(title=title, available=True)
        db.session.add(new_book)
        db.session.commit()

        return jsonify(success_response(new_book.serialize())), 201

    except Exception as e:
        # print("Error occurred during add-books:", str(e))
        db.session.rollback()
        return (
            jsonify(
                error_response("An error occurred while adding the book.")
            ),
            500,
        )


def get_books():
    """
    Retrieve all books from the library.

    Returns:
        JSON: Serialized list of books with success message.
    """
    try:
        library = db.session.query(Book).all()
        serialized_books = [book.serialize() for book in library]

        if serialized_books:
            return jsonify(success_response(serialized_books)), 200
        else:
            return (
                jsonify(error_response("No books found in the library!")),
                404,
            )
    except Exception as e:
        # print("Error occurred during get-books:", str(e))
        return (
            jsonify(
                error_response("An error occurred while retrieving books")
            ),
            500,
        )


def get_book(id):
    """
    Retrieve details of a specific book.

    Args:
        id (int): The ID of the book to retrieve.

    Returns:
        JSON: Serialized book data with success message.
    """
    try:
        book_details = db.session.get(Book, id)
        if not book_details:
            return jsonify(error_response("Book not found")), 404

        serialized_book = book_details.serialize()
        return jsonify(success_response(serialized_book)), 200

    except Exception as e:
        # print("Error occurred during get-book:", str(e))
        return jsonify(error_response("Internal Server Error")), 500


def update_book_titles(id):
    """
    Update the title of a book.

    Args:
        id (int): The ID of the book to update.

    Returns:
        JSON: Success message with the updated book title.
    """
    try:
        data = request.json
        title = data.get("title")
        availability = data.get("available")

        book_details = db.session.get(Book, id)
        if not book_details:
            return jsonify(error_response("No Book Found with that ID.")), 404

        if title is not None:
            book_details.title = title
        if availability is not None:
            book_details.available = availability

        db.session.commit()

        return (
            jsonify(
                success_response(
                    f'Book titled with "{book_details.title}" updated.'
                )
            ),
            200,
        )

    except Exception as e:
        # print("Error occurred during update-title:", str(e))
        db.session.rollback()
        return (
            jsonify(
                error_response("An error occurred while updating the book.")
            ),
            500,
        )


def delete_request(id):
    """
    Delete a book from the library.

    Args:
        id (int): The ID of the book to delete.

    Returns:
        JSON: Success message if book is deleted successfully,
        else error message.
    """
    try:
        book_detail = db.session.get(Book, id)
        if book_detail:
            db.session.delete(book_detail)
            db.session.commit()
            return (
                jsonify(success_response("Book deleted successfully.")),
                200,
            )
        else:
            return jsonify(error_response("Book not found.")), 404
    except Exception as e:
        # print("Error occurred during delete-book:", str(e))
        db.session.rollback()
        return (
            jsonify(
                error_response("An error occurred while deleting the book.")
            ),
            500,
        )
