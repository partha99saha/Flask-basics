from flask import request, jsonify
from werkzeug.utils import secure_filename
import os
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
        title = request.form.get("title")
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

        # Check if a file is provided
        if "file" not in request.files:
            return jsonify(error_response("No file provided")), 400

        file = request.files["file"]
        if file.filename == "":
            return (
                jsonify(error_response("No file selected for uploading")),
                400,
            )

        # Save the file to the specified directory
        UPLOAD_FOLDER = "./assets/"
        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)
        filename = secure_filename(file.filename)
        file_path = os.path.join(UPLOAD_FOLDER, filename)
        file.save(file_path)

        # Create a new book object
        new_book = Book(title=title, available=True, file_path=file_path)
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


def get_book(uid):
    """
    Retrieve details of a specific book.

    Args:
        uid (int): The ID of the book to retrieve.

    Returns:
        JSON: Serialized book data with success message.
    """
    try:
        book_details = db.session.get(Book, uid)
        if not book_details:
            return jsonify(error_response("Book not found")), 404

        serialized_book = book_details.serialize()
        return jsonify(success_response(serialized_book)), 200

    except Exception as e:
        # print("Error occurred during get-book:", str(e))
        return jsonify(error_response("Internal Server Error")), 500


def update_book_titles(uid):
    """
    Update the title of a book.

    Args:
        uid (int): The ID of the book to update.

    Returns:
        JSON: Success message with the updated book title.
    """
    try:
        data = request.form
        title = data.get("title")
        availability = data.get("available")
        new_file = request.files.get("file")

        book_details = db.session.get(Book, uid)
        if not book_details:
            return jsonify(error_response("No Book Found with that ID.")), 404

        if title is not None:
            book_details.title = title

        if availability is not None:
            book_details.available = availability

        # Handle file update
        if new_file:
            UPLOAD_FOLDER = "./assets/"
            if not os.path.exists(UPLOAD_FOLDER):
                os.makedirs(UPLOAD_FOLDER)

            if book_details.file_path:
                # Remove old file if exists
                os.remove(book_details.file_path)

            filename = secure_filename(new_file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            new_file.save(file_path)
            book_details.file_path = file_path

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


def delete_request(uid):
    """
    Delete a book from the library.

    Args:
        uid (int): The ID of the book to delete.

    Returns:
        JSON: Success message if book is deleted successfully,
        else error message.
    """
    try:
        book_detail = db.session.get(Book, uid)
        if book_detail:
            if book_detail.file_path:
                # Check if the file exists before attempting to delete it
                if os.path.exists(book_detail.file_path):
                    os.remove(book_detail.file_path)
                else:
                    return (
                        jsonify(
                            error_response(
                                "File associated with the book does not exist."
                            )
                        ),
                        404,
                    )

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
