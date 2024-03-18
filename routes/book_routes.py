from app import app
from middleware.jwt import auth_required
from controllers.book_controller import (
    add_books,
    get_books,
    get_book,
    update_book_titles,
    delete_request
)


@app.route("/add-books", methods=["POST"])
@auth_required
def add_books_route():
    """
    Add a new book to the library.

    Returns:
        JSON: Serialized book data with success message.
    """
    return add_books()


@app.route("/get-books", methods=["GET"])
@auth_required
def get_books_route():
    """
    Retrieve all books from the library.

    Returns:
        JSON: Serialized list of books with success message.
    """
    return get_books()


@app.route("/get-book/<int:id>", methods=["GET"])
@auth_required
def get_book_route(id):
    """
    Retrieve details of a specific book.

    Args:
        id (int): The ID of the book to retrieve.

    Returns:
        JSON: Serialized book data with success message.
    """
    return get_book(id)


@app.route("/update-book/<int:id>", methods=["PUT"])
@auth_required
def update_book_titles_route(id):
    """
    Update the title of a book.

    Args:
        id (int): The ID of the book to update.

    Returns:
        JSON: Success message with the updated book title.
    """
    return update_book_titles(id)


@app.route("/delete-book/<int:id>", methods=["DELETE"])
@auth_required
def delete_book_route(id):
    """
    Delete a book from the library.

    Args:
        id (int): The ID of the book to delete.

    Returns:
        JSON: Success message if book is deleted successfully, else error message.
    """
    return delete_request(id)
