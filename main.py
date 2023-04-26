from fastapi import FastAPI, Form, Depends, HTTPException
from typing import List

app = FastAPI()

from core.models import author as authorModel, books as booksModel
from core.schemas import author as authorSchema, books as booksSchema
from core.database.database import SessionLocal, engine
from sqlalchemy.orm import Session

authorModel.Base.metadata.create_all(bind=engine)
booksModel.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from core.cruds.author import get_authors, create_author, get_author_by_name, get_author, update_author, get_author_by_id, delete_author
from core.cruds.books import get_books, get_books_by_id, create_author_book, update_book, delete_book


@app.get("/authors/", response_model=List[authorSchema.Author])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    authors = get_authors(db, skip=skip, limit=limit)
    print(authors)
    return authors

@app.get("/authors/{id}", response_model=authorSchema.Author)
def read_user(id: int, db: Session = Depends(get_db)):
    db_user = get_author(db, author_id=id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="Author not found")
    return db_user

@app.post("/authors/", response_model=authorSchema.Author)
def create_user(user: authorSchema.AuthorCreate, db: Session = Depends(get_db)):
    db_user = get_author_by_name(db, name=user.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Name already registered")
    return create_author(db=db, author=user)

@app.patch("/authors/{id}", response_model=authorSchema.Author)
def update_user(id: int, name: str, db: Session = Depends(get_db)):
    db_user = get_author_by_id(db, id=id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Author does not exists.")
    return update_author(db=db, name=name, author_id=id)

@app.delete("/authors/{id}", response_model=authorSchema.Author)
def delete_user(id: int, db: Session = Depends(get_db)):
    db_user = get_author_by_id(db, id=id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Author does not exists.")
    return delete_author(db, id=id)

@app.get("/books/{id}", response_model=booksSchema.Books)
def read_user(id: int, db: Session = Depends(get_db)):
    db_book = get_books_by_id(db, id=id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.get("/books/", response_model=List[booksSchema.Books])
def read_books(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), author_id: int = None):
    books = get_books(db, skip=skip, limit=limit, author_id=author_id)
    print(books)
    return books

@app.post("/books/", response_model=booksSchema.BooksCreate)
def create_book_view(book: booksSchema.BooksCreate, db: Session = Depends(get_db)):
    if not get_author_by_id(db, id=book.author_id):
        raise HTTPException(status_code=404, detail="Author does not exist")
    return create_author_book(db=db, book=book)

@app.patch("/books/{id}", response_model=booksSchema.BooksCreate)
def update_book_view(id: int, name: str, author_id: int, db: Session = Depends(get_db)):
    db_book = get_books_by_id(db, id=id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book does not exists.")
    if not get_author_by_id(db, id=author_id):
        raise HTTPException(status_code=404, detail="Author does not exist")
    return update_book(db=db, name=name, id=id, author_id=author_id)

@app.delete("/books/{id}", response_model=booksSchema.BooksCreate)
def delete_book_view(id: int, db: Session = Depends(get_db)):
    db_book = get_books_by_id(db, id=id)
    if not db_book:
        raise HTTPException(status_code=404, detail="Book does not exists.")
    return delete_book(db, id=id)