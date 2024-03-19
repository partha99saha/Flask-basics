# import uuid
from app import db
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime


class Book(db.Model):
    """
    Represents a book in the library.

    Attributes:
        # uid (str): The unique identifier for the book (UUID).
        id (int): The unique identifier for the book.
        title (str): The title of the book.
        available (str): The availability status of the book.
        updated_at (datetime): The timestamp when the book was last updated.
    """

    __tablename__ = "Book"

    # uid = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, unique=True)
    available = Column(String(200))
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, title, available):
        """
        Initializes a Book object.

        Args:
            title (str): The title of the book.
            available (str): The availability status of the book.
        """
        self.title = title
        self.available = available

    def __repr__(self):
        """
        Returns a string representation of the Book object.

        Returns:
            str: A string representation of the Book object.
        """
        return "<Book(title='%s', available='%s')>" % (
            self.title,
            self.available,
        )

    def serialize(self):
        """
        Serializes the Book object into a dictionary.

        Returns:
            dict: A dictionary containing the serialized Book object.
        """
        return {"title": self.title, "available": self.available}
