from app import db
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime


class User(db.Model):
    """
    Represents a user in the system.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        password (str): The password of the user.
        updated_at (datetime): The timestamp when the user was last updated.
    """

    __tablename__ = "User"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, username, password):
        """
        Initializes a User object.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
        """
        self.username = username
        self.password = password

    def __repr__(self):
        """
        Returns a string representation of the User object.

        Returns:
            str: A string representation of the User object.
        """
        return "<User(%s,%s)>" % (self.username, self.password)

    def serialize(self):
        """
        Serializes the User object into a dictionary.

        Returns:
            dict: A dictionary containing the serialized User object.
        """
        return {"username": self.username, "password": self.password}
