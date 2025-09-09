import tempfile
import os
from db import Database
from auth import Auth

def test_log_entry_and_retrieve(tmp_path):
    db_path = tmp_path / "test_app.db"
    db = Database(str(db_path))
    username = "tester2"
    password = "pw2"
    hashed = Auth.hash_password(password)
    assert db.add_user(username, hashed)
    # write some logs
    db.log_entry(username, "(25-32)", "Blij")
    db.log_entry(username, "(25-32)", "Neutraal")
    # check rows exist
    cur = db.conn.cursor()
    cur.execute("SELECT COUNT(*) FROM logs WHERE username=?", (username,))
    count = cur.fetchone()[0]
    assert count == 2