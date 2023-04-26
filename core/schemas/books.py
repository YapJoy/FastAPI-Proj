from pydantic import BaseModel


class BooksBase(BaseModel):
    name: str

class Books(BooksBase):
    id: int
    author_id: int

    class Config:
        orm_mode = True

class BooksCreate(BooksBase):
    author_id: int

    class Config:
        orm_mode = True
