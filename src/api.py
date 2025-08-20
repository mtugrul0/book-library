from typing import List
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from src.models import Library, Book

app = FastAPI(
    title="Library API",
    version="0.1.0",
    description="Basit bir kütüphane (library) servisi. /docs üzerinden test edebilirsiniz."
)

library = Library("My Library")

# ---------- Pydantic Models ----------
class ISBNIn(BaseModel):
    isbn: str = Field(..., min_length=10, max_length=32)

class BookOut(BaseModel):
    title: str
    author: str
    isbn: str

    @classmethod
    def from_book(cls, b: Book) -> "BookOut":
        return cls(title=b.title, author=b.author, isbn=b.isbn)

# ---------- Endpoints ----------
@app.get("/books", response_model=List[BookOut])
def list_books():
    return [BookOut.from_book(b) for b in library._books]

@app.post("/books", response_model=BookOut, status_code=status.HTTP_201_CREATED)
def add_book(payload: ISBNIn):
    isbn = payload.isbn.strip()

    if library.find_book(isbn):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Book with ISBN {isbn} already exists."
        )

    library.add_book(isbn)
    created = library.find_book(isbn)
    if not created:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"Could not fetch / create book with ISBN {isbn} from Open Library."
        )
    return BookOut.from_book(created)

@app.delete("/books/{isbn}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(isbn: str):
    b = library.find_book(isbn)
    if not b:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Book with ISBN {isbn} not found."
        )
    library.remove_book(isbn)
    return