from sqlalchemy.orm import Session
from core.models.author import Author
from core.schemas.author import AuthorCreate


def get_authors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Author).offset(skip).limit(limit).all()

def get_author_by_id(db: Session, id: str):
    return db.query(Author).filter(Author.id == id).first()

def get_author_by_name(db: Session, name: str):
    return db.query(Author).filter(Author.name == name).first()

def update_author(db: Session, name: str, author_id: int):
    author = db.query(Author).filter(Author.id == author_id).first()
    author.name = name
    db.add(author)
    db.commit()
    db.refresh(author)
    return author

def create_author(db: Session, author: AuthorCreate):
    db_user = Author(name=author.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def delete_author(db: Session, id: id):
    author = db.query(Author).filter(Author.id == id).first()
    db.delete(author)
    db.commit()
    # db.refresh(author)
    return author

def get_author(db: Session, author_id: int):
    return db.query(Author).filter(Author.id == author_id).first()
