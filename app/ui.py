# =========================
# Bestand: ui.py
# =========================
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import threading
import queue
import cv2
from config import AppConfig
from worker import VideoWorker

class HandFaceApp:
    def __init__(self, root, cfg: AppConfig):
        self.root = root
        self.cfg = cfg
        self.root.title("Leeftijd & Emotie Detectie")
        self.video_label = ttk.Label(root)
        self.video_label.pack()
        self.age_label = ttk.Label(root, text="Leeftijd: ?")
        self.age_label.pack()
        self.emotion_label = ttk.Label(root, text="Emotie: ?")
        self.emotion_label.pack()

        self.queue = queue.Queue()
        self.stop_event = threading.Event()
        self.worker = VideoWorker(cfg, self.queue, self.stop_event)
        self.worker.start()

        self.update_loop()

    def update_loop(self):
        try:
            while True:
                frame, age, emotion = self.queue.get_nowait()
                img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
                self.age_label.config(text=f"Leeftijd: {age}")
                self.emotion_label.config(text=f"Emotie: {emotion}")
        except queue.Empty:
            pass
        self.root.after(50, self.update_loop)

    def on_close(self):
        self.stop_event.set()
        self.root.destroy()