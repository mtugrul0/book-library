import pytest
import json
from src.models import Book, Library

# ------------------------
# Fixtures
# ------------------------

@pytest.fixture
def sample_book():
    """Return a sample Book object."""
    return Book("1984", "George Orwell", "978-6257124614")

@pytest.fixture
def sample_library(tmp_path):
    """Return a Library object with a temporary JSON file."""
    lib = Library("Test Library")
    lib.filename = tmp_path / "library.json"
    return lib

# ------------------------
# Book Tests
# ------------------------

def test_book_creation(sample_book):
    """Test if Book object is created with correct attributes."""
    b = sample_book
    assert b.title == "1984"
    assert b.author == "George Orwell"
    assert b.isbn == "978-6257124614"

def test_book_to_dict(sample_book):
    """Test the to_dict method of Book."""
    b = sample_book
    assert b.to_dict() == {
        "title": "1984",
        "author": "George Orwell",
        "isbn": "978-6257124614"
    }

# ------------------------
# Library Tests
# ------------------------

def test_library_creation(sample_library):
    """Test Library object creation and initial state."""
    l = sample_library
    assert l.name == "Test Library"
    assert l._books == []

def test_add_book(sample_library, sample_book):
    """Test adding a book to the library."""
    lib = sample_library
    lib.add_book(sample_book)
    assert lib._books == [sample_book]

def test_remove_book(sample_library, sample_book):
    """Test removing a book from the library."""
    lib = sample_library
    lib.add_book(sample_book)
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
    lib.add_book(sample_book)
    found = lib.find_book(sample_book.isbn)
    assert found == sample_book

def test_find_nonexistent_book(sample_library):
    """Test finding a book that does not    exist returns None."""
    lib = sample_library
    assert lib.find_book("wrong-isbn") is None

# ------------------------
# Load/Save Tests
# ------------------------

def test_save_and_load_books(tmp_path):
    """Test that Library can save to and load from JSON file correctly."""
    filename = tmp_path / "library.json"
    lib = Library("My Library")
    lib.filename = filename

    b1 = Book("1984", "George Orwell", "978-6257124614")
    b2 = Book("Brave New World", "Aldous Huxley", "978-0060850524")
    lib.add_book(b1)
    lib.add_book(b2)
    
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == [b1.to_dict(), b2.to_dict()]

    new_lib = Library("My Library")
    new_lib.filename = filename
    new_lib.load_books()
    
    assert len(new_lib._books) == 2
    assert new_lib._books[0].title == "1984"
    assert new_lib._books[1].title == "Brave New World"
