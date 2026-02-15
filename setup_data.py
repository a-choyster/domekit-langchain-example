"""Create the sample books database for the LangChain + DomeKit demo."""

import os
import sqlite3

DB_PATH = os.path.join(os.path.dirname(__file__), "data", "books.db")

BOOKS = [
    ("The Left Hand of Darkness", "Ursula K. Le Guin", 1969, "Science Fiction"),
    ("Neuromancer", "William Gibson", 1984, "Science Fiction"),
    ("Dune", "Frank Herbert", 1965, "Science Fiction"),
    ("Pride and Prejudice", "Jane Austen", 1813, "Fiction"),
    ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "Fiction"),
    ("One Hundred Years of Solitude", "Gabriel Garcia Marquez", 1967, "Magical Realism"),
    ("Sapiens", "Yuval Noah Harari", 2011, "Non-Fiction"),
    ("The Pragmatic Programmer", "David Thomas & Andrew Hunt", 1999, "Technology"),
    ("Parable of the Sower", "Octavia Butler", 1993, "Science Fiction"),
    ("The Name of the Wind", "Patrick Rothfuss", 2007, "Fantasy"),
]


def main():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            year INTEGER NOT NULL,
            genre TEXT NOT NULL
        )
    """)

    cur.executemany(
        "INSERT INTO books (title, author, year, genre) VALUES (?, ?, ?, ?)",
        BOOKS,
    )

    conn.commit()
    conn.close()

    print(f"Created {DB_PATH} with {len(BOOKS)} books.")


if __name__ == "__main__":
    main()
