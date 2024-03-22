from flask import Blueprint
from middleware.jwt import auth_required
from controllers.book_controller import (
    add_books,
    get_books,
    get_book,
    update_book_titles,
    delete_request,
)

book_bp = Blueprint("book_bp", __name__)


@book_bp.route("/add-books", methods=["POST"])
@auth_required
def add_books_route():
    """
    Add a new book to the library.

    Returns:
        JSON: Serialized book data with success message.
    """
    return add_books()


@book_bp.route("/get-books", methods=["GET"])
@auth_required
def get_books_route():
    """
    Retrieve all books from the library.

    Returns:
        JSON: Serialized list of books with success message.
    """
    return get_books()


@book_bp.route("/get-book/<string:uid>", methods=["GET"])
@auth_required
def get_book_route(uid):
    """
    Retrieve details of a specific book.

    Args:
        uid (String): The ID of the book to retrieve.

    Returns:
        JSON: Serialized book data with success message.
    """
    return get_book(uid)


@book_bp.route("/update-book/<string:uid>", methods=["PUT"])
@auth_required
def update_book_titles_route(uid):
    """
    Update the title of a book.

    Args:
        uid (String): The ID of the book to update.

    Returns:
        JSON: Success message with the updated book title.
    """
    return update_book_titles(uid)


@book_bp.route("/delete-book/<string:uid>", methods=["DELETE"])
@auth_required
def delete_book_route(uid):
    """
    Delete a book from the library.

    Args:
        uid (String): The ID of the book to delete.

    Returns:
        JSON: Success message if book is deleted successfully,
        else error message.
    """
    return delete_request(uid)
