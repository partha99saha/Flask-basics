from app import db
from datetime import datetime
from sqlalchemy import Column, String, Integer, DateTime


class Book(db.Model):
    __tablename__ = "Book"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, unique=True)
    available = Column(String(200))
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __init__(self, title, available):
        self.title = title
        self.available = available

    def __repr__(self):
        return "<Book(title='%s', available='%s')>" % (
            self.title,
            self.available,
        )

    def serialize(self):
        return {"title": self.title, "available": self.available}
