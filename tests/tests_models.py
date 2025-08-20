import pytest
import json
from unittest.mock import patch, MagicMock
from src.models import Book, Library

# ------------------------
# Fixtures
# ------------------------

@pytest.fixture
def sample_book():
    """Return a sample Book object."""
    return Book("Fantastic Mr. Fox", "Roald Dahl", "9780140328721")

@pytest.fixture
def sample_library(tmp_path):
    """Return a Library object with a temporary JSON file."""
    lib = Library("Test Library")
    lib.filename = tmp_path / lib.filename
    return lib

# ------------------------
# Book Tests
# ------------------------

def test_book_creation(sample_book):
    """Test if Book object is created with correct attributes."""
    b = sample_book
    assert b.title == "Fantastic Mr. Fox"
    assert b.author == "Roald Dahl"
    assert b.isbn == "9780140328721"

def test_book_to_dict(sample_book):
    """Test the to_dict method of Book."""
    b = sample_book
    assert b.to_dict() == {
        "title": "Fantastic Mr. Fox",
        "author": "Roald Dahl",
        "isbn": "9780140328721"
    }

# ------------------------
# Library Tests
# ------------------------

def test_library_creation(sample_library):
    """Test Library object creation and initial state."""
    l = sample_library
    assert l.name == "Test Library"
    assert l._books == []


def test_add_book_with_mock(sample_library):
    """Test add_book method with mocked API responses."""

    isbn = "9780140328721"

    mock_book_data = {
        "title": "Fantastic Mr. Fox",
        "author": [{"key": "/authors/OL34184A"}],
    }
    mock_author_data = {"author": "Roald Dahl"}

    with patch("httpx.get") as mock_get:
        mock_resp1 = MagicMock()
        mock_resp1.json.return_value = mock_book_data
        mock_resp1.raise_for_status.return_value = None

        mock_resp2 = MagicMock()
        mock_resp2.json.return_value = mock_author_data
        mock_resp2.raise_for_status.return_value = None

        mock_get.side_effect = [mock_resp1, mock_resp2]

    sample_library.add_book(isbn)
    
    assert len(sample_library._books) == 1
    book = sample_library._books[0]
    assert isinstance(book, Book)
    assert book.isbn == isbn
    assert book.title == "Fantastic Mr. Fox"
    assert book.author == "Roald Dahl"

def test_remove_book(sample_library, sample_book):
    """Test removing a book from the library."""
    lib = sample_library
    lib.add_book(sample_book.isbn)
    lib.remove_book(sample_book.isbn)
    assert lib._books == []

def test_remove_nonexistent_book(sample_library):
    """Test removing a book that does not exist."""
    lib = sample_library
    lib.remove_book("wrong-isbn")
    assert lib._books == []

def test_find_book(sample_library, sample_book):
    """Test finding a book by ISBN."""
    lib = sample_library
    lib.add_book(sample_book.isbn)
    found = lib.find_book(sample_book.isbn)
    assert found == sample_book

def test_find_nonexistent_book(sample_library):
    """Test finding a book that does not exist returns None."""
    lib = sample_library
    assert lib.find_book("wrong-isbn") is None

# ------------------------
# Load/Save Tests
# ------------------------

def test_save_and_load_books(sample_library, sample_book):
    lib = sample_library
    b2 = Book("Pride and Prejudice", "Jane Austen", "9780141439518")

    lib._books.extend([sample_book, b2])
    lib.save_books()

    with open(lib.filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == [sample_book.to_dict(), b2.to_dict()]

    new_lib = Library("Test Library")
    new_lib.filename = lib.filename
    new_lib.load_books()

    assert len(new_lib._books) == 2
    assert new_lib._books[0].title == "Fantastic Mr. Fox"
    assert new_lib._books[1].title == "Pride and Prejudice"
