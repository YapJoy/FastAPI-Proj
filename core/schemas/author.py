from typing import List
from pydantic import BaseModel
from core.schemas.books import Books


class AuthorBase(BaseModel):
    name: str

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List[Books] = []

    class Config:
        orm_mode = True