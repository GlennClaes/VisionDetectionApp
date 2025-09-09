import os
import sqlite3
from datetime import datetime

class Database:
    def __init__(self, path: str):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        self.conn = sqlite3.connect(path, check_same_thread=False)
        self._init_tables()

    def _init_tables(self):
        c = self.conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users (
                        username TEXT PRIMARY KEY, 
                        password_hash TEXT NOT NULL
                     )''')
        c.execute('''CREATE TABLE IF NOT EXISTS logs (
                        id INTEGER PRIMARY KEY AUTOINCREMENT, 
                        username TEXT, 
                        age TEXT, 
                        emotion TEXT, 
                        timestamp TEXT, 
                        FOREIGN KEY(username) REFERENCES users(username)
                     )''')
        self.conn.commit()

    def add_user(self, username: str, password_hash: str) -> bool:
        try:
            self.conn.execute(
                "INSERT INTO users (username, password_hash) VALUES (?, ?)",
                (username, password_hash)
            )
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def get_user_hash(self, username: str):
        c = self.conn.cursor()
        c.execute("SELECT password_hash FROM users WHERE username=?", (username,))
        return c.fetchone()

    def log_entry(self, username: str, age: str, emotion: str) -> None:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.conn.execute(
            "INSERT INTO logs (username, age, emotion, timestamp) VALUES (?, ?, ?, ?)",
            (username, age, emotion, ts)
        )
        self.conn.commit()