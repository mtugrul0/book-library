import json
import os

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
    
    def add_book(self, b: Book):
        self._books.append(b)
        self.save_books()
    
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