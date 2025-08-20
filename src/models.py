import json
import os
import httpx

# ------------------------
# Book Class
# ------------------------

class Book:
    def __init__(self, title: str, author: str, isbn: str):
        self.title = title
        self.author = author
        self.isbn = isbn

    def __str__(self):
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"
    
    def __eq__(self, other):
        if not isinstance(other, Book):
            return NotImplemented
        return (
            self.title == other.title
            and self.author == other.author
            and self.isbn == other.isbn
        )
    
    def to_dict(self):
        return {"title": self.title, "author": self.author, "isbn": self.isbn}

# ------------------------
# Library Class
# ------------------------

class Library:
    def __init__(self, name: str):
        self.name = name
        self.filename = f"{name.replace(' ', '-')}-library.json"
        self._books = []
        self.load_books()
    

    def add_book(self, isbn):
        if self.find_book(isbn):
            print(f"{isbn} zaten kütüphanede mevcut.")
            return self.find_book(isbn)

        url = f"https://openlibrary.org/isbn/{isbn}.json"
        try:
            response = httpx.get(url, follow_redirects=True)
            response.raise_for_status()
            data = response.json()

            title = data.get("title", "Bilinmeyen Başlık")

            # --- Yazar(lar) ---
            authors: list[str] = []

            if isinstance(data.get("author"), list) and all(isinstance(a, str) for a in data["author"]):
                authors = data["author"]

            elif isinstance(data.get("authors"), list):
                for a in data["authors"]:
                    key = a.get("key")
                    if not key:
                        continue
                    author_url = f"https://openlibrary.org{key}.json"
                    try:
                        author_resp = httpx.get(author_url, follow_redirects=True)
                        author_resp.raise_for_status()
                        author_data = author_resp.json()
                        name = author_data.get("name") or author_data.get("author") or "Bilinmeyen Yazar"
                        authors.append(name)
                    except Exception:
                        authors.append("Bilinmeyen Yazar")

            author = ", ".join(authors) if authors else "Bilinmeyen Yazar"

            new_book = Book(title, author, isbn)
            self._books.append(new_book)
            self.save_books()
            print(f"Kitap eklendi: {new_book}")
            return new_book

        except httpx.HTTPStatusError as e:
            print(f"Kitap bulunamadı (HTTP {e.response.status_code})")
        except Exception as e:
            print(f"Hata: {e}")

    def remove_book(self, isbn: str):
        for b in self._books:
            if b.isbn == isbn:
                self._books.remove(b)
                self.save_books()
                print(f"{b.title} silindi.")
                return
        print("Kitap bulunamadı")

    def list_books(self):
        if not self._books:
            print("Kütüphane boş.")
        for b in self._books:
            print(b)

    def find_book(self, isbn: str):
        for book in self._books:
            if book.isbn == isbn:
                return book

    def load_books(self):
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self._books = [Book(**item) for item in data]
        else:
            self._books = []

    def save_books(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump([book.to_dict() for book in self._books], f, ensure_ascii=False, indent=4)