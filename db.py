import sqlite3
import random
import datetime
from models import Book


def getNewId():
    return random.getrandbits(28)


books = [
    {
        'available': True,
        'title': 'The Lord of Fire',
        'timestamp': datetime.datetime.now()
    },
    {
        'available': True,
        'title': 'Harry Potter',
        'timestamp': datetime.datetime.now()
    },
    {
        'available': True,
        'title': 'Power of Habbit',
        'timestamp': datetime.datetime.now()
    },
    {
        'available': True,
        'title': 'The Lion King',
        'timestamp': datetime.datetime.now()
    },
    {
        'available': True,
        'title': 'The Da Vinci Code',
        'timestamp': datetime.datetime.now()
    },
]


def connect():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute(
        "CREATE TABLE IF NOT EXISTS books (id INTEGER PRIMARY KEY, available BOOLEAN, title TEXT, timestamp TEXT)")
    conn.commit()
    conn.close()
    # Insert data in DB
    for i in books:
        bk = Book(getNewId(), i['available'], i['title'], i['timestamp'])
        insert(bk)


def insert(book):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO books VALUES (?,?,?,?)", (
        book.id,
        book.available,
        book.title,
        book.timestamp
    ))
    conn.commit()
    conn.close()


def view():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    books = []
    for i in rows:
        book = Book(i[0], True if i[1] == 1 else False, i[2], i[3])
        books.append(book)
    conn.close()
    return books


def update(book):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("UPDATE books SET available=?, title=? WHERE id=?",
                (book.available, book.title, book.id))
    conn.commit()
    conn.close()


def delete(theId):
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (theId,))
    conn.commit()
    conn.close()


def deleteAll():
    conn = sqlite3.connect('books.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM books")
    conn.commit()
    conn.close()
