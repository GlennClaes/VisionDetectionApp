import tkinter as tk
from config import AppConfig
from db import Database
from auth import Auth
from ui import HandFaceApp

def init_admin(db: Database):
    if not db.get_user_hash("admin"):
        db.add_user("admin", Auth.hash_password("admin"))

def main():
    cfg = AppConfig()
    db = Database(cfg.db_path)
    init_admin(db)

    root = tk.Tk()
    root.title("Age & Emotion Detection")
    root.attributes("-fullscreen", True)
    root.configure(bg="#2c3e50")

    HandFaceApp(root, cfg, db)
    root.mainloop()

if __name__ == "__main__":
    main()