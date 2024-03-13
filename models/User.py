from app import db
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime


class User(db.Model):
    __tablename__ = 'User'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(20), nullable=False, unique=True)
    password = Column(String(200), nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def __repr__(self):
        return "<User(%s,%s)>" % (self.username, self.password)

    def serialize(self):
        return {
            'username': self.username,
            'password': self.password
        }
