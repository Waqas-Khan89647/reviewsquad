from store import db, users


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
