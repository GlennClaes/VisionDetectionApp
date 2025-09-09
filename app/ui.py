import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import threading, queue, cv2
from worker import VideoWorker
from models import AgeStabilizer, EmotionStabilizer
from auth import Auth

class HandFaceApp:
    def __init__(self, root, cfg, db):
        self.root = root
        self.cfg = cfg
        self.db = db
        self.username = None
        self.latest_frame = None

        # --- Queue & threading ---
        self.queue = queue.Queue()
        self.stop_event = threading.Event()
        self.worker = None

        # --- Top frame voor close button ---
        self.top_frame = tk.Frame(root, bg="#34495e")
        self.top_frame.pack(side="top", fill="x")

        # --- Top-right close button ---
        self.btn_close = tk.Button(
            self.top_frame,
            text="✖",
            command=self.on_close,
            font=("Helvetica", 16, "bold"),
            bg="#e74c3c",
            fg="white",
            bd=0,
            relief="flat",
            activebackground="#c0392b",
            activeforeground="white"
        )
        self.btn_close.pack(side="right", padx=10, pady=5)

        # --- Login Frame ---
        self.login_frame = tk.Frame(root, bg="#34495e")
        self.login_frame.pack(expand=True, fill="both")

        tk.Label(self.login_frame, text="Login", font=("Helvetica", 36, "bold"),
                 fg="#ecf0f1", bg="#34495e").pack(pady=40)

        self.entry_user = ttk.Entry(self.login_frame, font=("Helvetica", 18))
        self.entry_user.pack(pady=10)
        self.entry_user.insert(0, "")  # Start empty

        self.entry_pass = ttk.Entry(self.login_frame, show="*", font=("Helvetica", 18))
        self.entry_pass.pack(pady=10)
        self.entry_pass.insert(0, "")  # Start empty

        ttk.Button(self.login_frame, text="Login", command=self.login).pack(pady=20)
        ttk.Button(self.login_frame, text="Register", command=self.register).pack()

        # --- Detection Frame ---
        self.detect_frame = tk.Frame(root, bg="#2c3e50")

        self.video_label = tk.Label(self.detect_frame, bg="#2c3e50")
        self.video_label.pack(pady=20)

        self.info_frame = tk.Frame(self.detect_frame, bg="#2c3e50")
        self.info_frame.pack(pady=10)

        self.age_label = tk.Label(self.info_frame, text="Age: ?", font=("Helvetica", 28, "bold"),
                                  fg="cyan", bg="#2c3e50")
        self.age_label.pack(side="left", padx=30)

        self.emotion_label = tk.Label(self.info_frame, text="Emotion: ?", font=("Helvetica", 28, "bold"),
                                      fg="magenta", bg="#2c3e50")
        self.emotion_label.pack(side="left", padx=30)

        self.btn_frame = tk.Frame(self.detect_frame, bg="#2c3e50")
        self.btn_frame.pack(pady=15)
        self.snapshot_btn = ttk.Button(self.btn_frame, text="Snapshot", command=self.take_snapshot)
        self.snapshot_btn.pack(side="left", padx=15)
        self.stop_btn = ttk.Button(self.btn_frame, text="Stop", command=self.on_close)
        self.stop_btn.pack(side="left", padx=15)

    # --- Login logic ---
    def login(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()

        # Default admin
        if username == "" and password == "":
            username = "admin"
            password = "admin"

        row = self.db.get_user_hash(username)
        if row and Auth.verify_password(password, row[0]):
            self.username = username
            self.start_detection()
        else:
            messagebox.showerror("Login failed", "Invalid username or password")

    def register(self):
        username = self.entry_user.get().strip()
        password = self.entry_pass.get().strip()
        if self.db.add_user(username, Auth.hash_password(password)):
            messagebox.showinfo("Success", "User registered successfully!")
        else:
            messagebox.showerror("Error", "Username already exists")

    # --- Switch frames & start worker ---
    def start_detection(self):
        self.login_frame.pack_forget()
        self.detect_frame.pack(expand=True, fill="both")

        self.worker = VideoWorker(self.cfg, self.queue, self.stop_event)
        self.worker.start()
        self.update_loop()

    # --- Update GUI with frames from worker ---
    def update_loop(self):
        try:
            while True:
                frame, stable_age, stable_emotion = self.queue.get_nowait()
                self.latest_frame = frame.copy()

                for (x, y, w, h) in getattr(self.worker, "last_faces", []):
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.putText(frame, f"{stable_age}, {stable_emotion}", (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)

                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)

                self.age_label.config(text=f"Age: {stable_age}")
                self.emotion_label.config(text=f"Emotion: {stable_emotion}")
        except queue.Empty:
            pass
        self.root.after(50, self.update_loop)

    def take_snapshot(self):
        if self.latest_frame is None:
            return
        import os
        from datetime import datetime
        os.makedirs("data/photos", exist_ok=True)
        filename = f"data/photos/{self.username}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        cv2.imwrite(filename, self.latest_frame)
        print(f"Snapshot saved: {filename}")

    def on_close(self):
        self.stop_event.set()
        self.root.destroy()