# =========================
# Bestand: main.py
# =========================
import tkinter as tk
from config import AppConfig
from db import Database
from login import LoginDialog
from ui import HandFaceApp

from auth import Auth

# Zorg dat er minimaal 1 admin bestaat
def init_admin(db: Database):
    if not db.get_user_hash("admin"):
        db.add_user("admin", Auth.hash_password("admin"))


def main():
    cfg = AppConfig()
    db = Database(cfg.db_path)
    init_admin(db)

    root = tk.Tk()
    dlg = LoginDialog(root, db)
    if not dlg.username:
        root.destroy()
        return

    app = HandFaceApp(root, cfg)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()

if __name__ == "__main__":
    main()