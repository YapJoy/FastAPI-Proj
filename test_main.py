from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest
from core.database.database import Base
from main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

@pytest.fixture()
def client(session):

    # Dependency override

    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

import pytest
from pytest_postgresql import factories
test_db = factories.postgresql_proc(port=None, dbname="test_db")

fake_db = {
    "author": {"id": 1, "name": "Test Author"},
    "author_update": {"id": 1},
    "author_update_resp": {"id": 1, "name": "Test Author (updated)", "books": []},
    "author_resp": {"id": 1, "name": "Test Author", "books": []},
    "book": {"name": "Test Book", "author_id": 1},
    "book_updated": {"id":1, "name": "Test Book (updated)", "author_id": 1},
    "book_updated_resp": {"name": "Test Book (updated)", "author_id": 1},
    "book_resp": {"id": 1, "name": "Test Book", "author_id": 1},
    "authors_books": {"id": 1, "name": "Test Author (updated)", "books": [{"id": 1, "name": "Test Book", "author_id": 1}]},
}

def test_read_main():
    response = client.get("/authors")
    print(response)
    assert response.status_code == 200
    assert response.json() == []

def test_read_books():
    response = client.get("/books")
    print(response)
    assert response.status_code == 200
    assert response.json() == []

def test_create_author():
    response = client.post("/authors",
                           json=fake_db['author'])
    assert response.status_code == 200
    assert response.json() == fake_db['author_resp']

def test_update_author():
    response = client.patch("/authors/1?name=Test Author (updated)")
    assert response.status_code == 200
    assert response.json() == fake_db['author_update_resp']

def test_create_book():
    response = client.post("/books",
                           json=fake_db['book'])
    assert response.status_code == 200
    assert response.json() == fake_db['book']

def test_update_book():
    response = client.patch("/books/1?name=Test Book (updated)&author_id=1",
                           json=fake_db['book_updated'])
    assert response.status_code == 200
    assert response.json() == fake_db['book_updated_resp']

def test_update_book():
    response = client.patch("/books/1?name=Test Book (updated)&author_id=1",
                           json=fake_db['book_updated'])
    assert response.status_code == 200
    assert response.json() == fake_db['book_updated_resp']

def test_delete_book():
    response = client.delete("/books/1")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == fake_db['book_updated_resp']

def test_delete_author():
    response = client.delete("/authors/1")
    assert response.status_code == 200
    print(response.json())
    assert response.json() == fake_db['author_update_resp']
