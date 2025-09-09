import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from db import Database
from auth import Auth


class LoginRegisterDialog:
    def __init__(self, root, db: Database):
        self.db = db
        self.username = None
        self.top = tk.Toplevel(root)
        self.top.title("Login / Register")
        self.top.attributes("-fullscreen", True)

        self.frame = ttk.Frame(self.top)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(self.frame, text="Username:").grid(row=0, column=0)
        self.entry_user = ttk.Entry(self.frame)
        self.entry_user.grid(row=0, column=1)

        ttk.Label(self.frame, text="Password:").grid(row=1, column=0)
        self.entry_pass = ttk.Entry(self.frame, show="*")
        self.entry_pass.grid(row=1, column=1)

        ttk.Button(
            self.frame,
            text="Login",
            command=self.login
        ).grid(row=2, column=0)

        ttk.Button(
            self.frame,
            text="Register",
            command=self.register,
        ).grid(row=2, column=1)

    def login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        row = self.db.get_user_hash(username)
        if row and Auth.verify_password(password, row[0]):
            self.username = username
            self.top.destroy()
        else:
            messagebox.showerror(
                "Login failed",
                "Invalid username or password"
            )

    def register(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        if self.db.add_user(username, Auth.hash_password(password)):
            messagebox.showinfo(
                "Success",
                "User registered successfully!"
            )
        else:
            messagebox.showerror(
                "Error",
                "Username already exists"
            )
