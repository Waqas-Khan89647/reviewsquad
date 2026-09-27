import pytest

from store import db, users


# ---------------------------------------------------------------------------
# Existing tests (unchanged)
# ---------------------------------------------------------------------------

def test_create_and_verify_user():
    conn = db.connect()
    users.create_user(conn, "alice", "s3cret!")
    assert users.verify_password(conn, "alice", "s3cret!")
    assert not users.verify_password(conn, "alice", "wrong")


def test_unknown_user_cannot_log_in():
    conn = db.connect()
    assert not users.verify_password(conn, "nobody", "x")


def test_get_user():
    conn = db.connect()
    uid = users.create_user(conn, "bob", "pw", is_admin=True)
    row = users.get_user(conn, uid)
    assert row["username"] == "bob" and row["is_admin"] == 1


def test_passwords_are_not_stored_in_plain_text():
    conn = db.connect()
    users.create_user(conn, "carol", "hunter2")
    stored = conn.execute("SELECT password_hash FROM users").fetchone()[0]
    assert "hunter2" not in stored


# ---------------------------------------------------------------------------
# find_users_by_name
# ---------------------------------------------------------------------------

def test_find_users_by_name_normal():
    conn = db.connect()
    users.create_user(conn, "david", "pw")
    results = users.find_users_by_name(conn, "dav")
    assert any(row["username"] == "david" for row in results)


def test_find_users_by_name_no_match():
    conn = db.connect()
    results = users.find_users_by_name(conn, "zzznomatch")
    assert results == []


def test_find_users_by_name_sql_injection_is_safe():
    """A name containing SQL metacharacters must not cause an error or data leak."""
    conn = db.connect()
    users.create_user(conn, "eve", "pw")
    # If parameterisation is broken this would return all rows or raise.
    results = users.find_users_by_name(conn, "' OR '1'='1")
    assert results == []


# ---------------------------------------------------------------------------
# login
# ---------------------------------------------------------------------------

def test_login_correct_credentials():
    conn = db.connect()
    users.create_user(conn, "frank", "correct")
    assert users.login(conn, "frank", "correct") is True


def test_login_wrong_password():
    conn = db.connect()
    users.create_user(conn, "grace", "correct")
    assert users.login(conn, "grace", "wrong") is False


def test_login_unknown_user():
    conn = db.connect()
    assert users.login(conn, "nobody", "anything") is False


def test_login_has_no_master_password_backdoor():
    """The old ADMIN_PASSWORD backdoor must not grant access."""
    conn = db.connect()
    users.create_user(conn, "henry", "realpassword")
    assert users.login(conn, "henry", "changeme123") is False