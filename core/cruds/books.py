from sqlalchemy.orm import Session
from core.models.books import Books


def get_books(db: Session, skip: int = 0, limit: int = 100, author_id: int=None):
    books = db.query(Books)
    if author_id:
        print(author_id)
        print(type(author_id))
        print('inside author')
        books = books.filter(Books.author_id == author_id)
        print(books)
    return books.offset(skip).limit(limit).all()

def get_books_by_id(db: Session, id: str):
    return db.query(Books).filter(Books.id == id).first()

def update_book(db: Session, name: str, author_id: int, id: int):
    book = db.query(Books).filter(Books.id == id).first()
    book.name = name
    book.author_id = author_id
    db.add(book)
    db.commit()
    db.refresh(book)
    return book

def delete_book(db: Session, id: id):
    book = db.query(Books).filter(Books.id == id).first()
    db.delete(book)
    db.commit()
    return book

def create_author_book(db: Session, book: Books):
    db_book = Books(**book.dict())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book