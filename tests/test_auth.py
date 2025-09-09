from db import Database
from auth import Auth

def test_hash_and_verify():
    pw = "SuperSecret123!"
    h = Auth.hash_password(pw)
    assert isinstance(h, str)
    assert Auth.verify_password(pw, h)
    assert not Auth.verify_password("wrongpw", h)

def test_register_and_retrieve_user(tmp_path):
    db_path = tmp_path / "test_app.db"
    db = Database(str(db_path))
    username = "tester"
    password = "pw"
    # store hashed via auth
    hashed = Auth.hash_password(password)
    assert db.add_user(username, hashed)
    row = db.get_user_hash(username)
    assert row is not None
    assert row[0] == hashed