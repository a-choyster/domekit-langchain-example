"""Tests for setup_data.py — verifies the books database is created correctly."""

import os
import sqlite3
import subprocess
import sys

import pytest

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "books.db")
SETUP_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "setup_data.py")


@pytest.fixture(autouse=True)
def fresh_db():
    """Re-run setup_data before each test to ensure a clean database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
    subprocess.run([sys.executable, SETUP_SCRIPT], check=True, capture_output=True)
    yield
    # Cleanup after tests
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)


def test_db_file_created():
    assert os.path.exists(DB_PATH)


def test_books_table_exists():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name='books'"
    )
    tables = cursor.fetchall()
    conn.close()
    assert len(tables) == 1


def test_books_table_has_correct_columns():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("PRAGMA table_info(books)")
    columns = [row[1] for row in cursor.fetchall()]
    conn.close()
    assert columns == ["id", "title", "author", "year", "genre"]


def test_books_table_has_10_rows():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]
    conn.close()
    assert count == 10


def test_all_books_have_non_empty_fields():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT title, author, year, genre FROM books")
    for row in cursor.fetchall():
        assert row[0], "title should not be empty"
        assert row[1], "author should not be empty"
        assert row[2] > 0, "year should be positive"
        assert row[3], "genre should not be empty"
    conn.close()


def test_setup_is_idempotent():
    """Running setup twice should not cause errors or duplicate data."""
    subprocess.run([sys.executable, SETUP_SCRIPT], check=True, capture_output=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT COUNT(*) FROM books")
    count = cursor.fetchone()[0]
    conn.close()
    assert count == 10
