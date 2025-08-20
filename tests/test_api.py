from pathlib import Path
from unittest.mock import patch, MagicMock

from fastapi.testclient import TestClient
from src.api import app, library

client = TestClient(app)

def setup_function(_fn):
    # Her test öncesi kütüphane dosyasını izole et
    tmpfile = Path("test-My-Library-library.json")
    library.filename = tmpfile
    library._books = []
    if tmpfile.exists():
        tmpfile.unlink()

def test_get_books_empty():
    resp = client.get("/books")
    assert resp.status_code == 200
    assert resp.json() == []

def test_post_books_and_list_and_delete():
    isbn = "9780140328721"  # Fantastic Mr. Fox

    # Open Library mock yanıtları
    mock_book_data = {
        "title": "Fantastic Mr. Fox",
        "authors": [{"key": "/authors/OL34184A"}],
    }
    mock_author_data = {"name": "Roald Dahl"}

    with patch("httpx.get") as mock_get:
        mock_resp1 = MagicMock()
        mock_resp1.json.return_value = mock_book_data
        mock_resp1.raise_for_status.return_value = None

        mock_resp2 = MagicMock()
        mock_resp2.json.return_value = mock_author_data
        mock_resp2.raise_for_status.return_value = None

        # add_book içinde (1) kitap ayrıntısı, (2) yazar ayrıntısı çağrıları
        mock_get.side_effect = [mock_resp1, mock_resp2]

        # --- POST /books
        resp = client.post("/books", json={"isbn": isbn})
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Fantastic Mr. Fox"
        assert data["author"] == "Roald Dahl"
        assert data["isbn"] == isbn

    # --- GET /books (liste 1 öğe)
    resp = client.get("/books")
    assert resp.status_code == 200
    books = resp.json()
    assert len(books) == 1

    # --- Duplicate POST -> 409
    resp = client.post("/books", json={"isbn": isbn})
    assert resp.status_code == 409

    # --- DELETE /books/{isbn} -> 204
    resp = client.delete(f"/books/{isbn}")
    assert resp.status_code == 204

    # --- DELETE non-existent -> 404
    resp = client.delete(f"/books/{isbn}")
    assert resp.status_code == 404