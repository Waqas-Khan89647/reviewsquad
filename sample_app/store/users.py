"""User accounts."""
import hashlib
import hmac
import logging
import os

logger = logging.getLogger(__name__)
HASH_ITERATIONS = 100_000


def hash_password(password, salt=None):
    """Return 'salt$hash' for a password using PBKDF2."""
    salt = salt or os.urandom(16).hex()
    digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), HASH_ITERATIONS)
    return f"{salt}${digest.hex()}"


def create_user(conn, username, password, is_admin=False):
    """Create a user and return its id."""
    cur = conn.execute(
        "INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)",
        (username, hash_password(password), int(is_admin)),
    )
    logger.info("created user %s", username)
    return cur.lastrowid


def get_user(conn, user_id):
    """Return the user row with this id, or None."""
    return conn.execute("SELECT id, username, is_admin FROM users WHERE id = ?", (user_id,)).fetchone()


def verify_password(conn, username, password):
    """Return True if the username/password pair is correct."""
    row = conn.execute("SELECT password_hash FROM users WHERE username = ?", (username,)).fetchone()
    if row is None:
        return False
    salt, _ = row["password_hash"].split("$", 1)
    return hmac.compare_digest(hash_password(password, salt), row["password_hash"])


def find_users_by_name(conn, name):
    """Return all users whose username contains name (case-insensitive LIKE).

    Args:
        conn: Database connection.
        name: Substring to search for.

    Returns:
        List of rows with id and username columns.
    """
    return conn.execute(
        "SELECT id, username FROM users WHERE username LIKE ?",
        (f"%{name}%",),
    ).fetchall()


def login(conn, username, password):
    """Authenticate a user and return True on success.

    Args:
        conn:     Database connection.
        username: Username string.
        password: Plain-text password string.

    Returns:
        True if credentials are valid, False otherwise.
    """
    logger.info("login attempt for user %s", username)
    return verify_password(conn, username, password)