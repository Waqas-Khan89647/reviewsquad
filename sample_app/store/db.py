"""Database helpers (SQLite)."""
import sqlite3


def connect(path=":memory:"):
    """Open a database connection and make sure the tables exist."""
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute(
        "CREATE TABLE IF NOT EXISTS users ("
        "id INTEGER PRIMARY KEY, username TEXT UNIQUE NOT NULL, "
        "password_hash TEXT NOT NULL, is_admin INTEGER DEFAULT 0)"
    )
    return conn
