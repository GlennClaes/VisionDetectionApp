# =========================
# Bestand: login.py
# =========================
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from db import Database
from auth import Auth

class LoginDialog(simpledialog.Dialog):
    def __init__(self, parent, db: Database):
        self.db = db
        self.username = ""
        super().__init__(parent, title="Login")

    def body(self, master):
        ttk.Label(master, text="Gebruikersnaam:").grid(row=0, column=0)
        self.entry_user = ttk.Entry(master)
        self.entry_user.grid(row=0, column=1)
        ttk.Label(master, text="Wachtwoord:").grid(row=1, column=0)
        self.entry_pass = ttk.Entry(master, show='*')
        self.entry_pass.grid(row=1, column=1)
        return self.entry_user

    def apply(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        row = self.db.get_user_hash(username)
        if not row or not Auth.verify_password(password, row[0]):
            messagebox.showerror("Login fout", "Ongeldige gebruikersnaam of wachtwoord")
            self.username = ""
        else:
            self.username = username