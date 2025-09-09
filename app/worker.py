# =========================
# Bestand: worker.py
# =========================
import threading
import cv2
import time
from models import AgeEmotionModel, AgeStabilizer

class VideoWorker(threading.Thread):
    def __init__(self, cfg, queue, stop_event):
        super().__init__(daemon=True)
        self.cfg = cfg
        self.queue = queue
        self.stop_event = stop_event
        self.model = AgeEmotionModel(
            cfg.age_proto_path, cfg.age_model_path, cfg.emotion_model_path
        )
        self.stabilizer = AgeStabilizer()

    def run(self):
        cap = cv2.VideoCapture(self.cfg.camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cfg.frame_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cfg.frame_height)

        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                continue

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.model.face_cascade.detectMultiScale(
                gray,
                scaleFactor=self.cfg.face_scaleFactor,
                minNeighbors=self.cfg.face_minNeighbors,
                minSize=self.cfg.face_minSize
            )

            for (x, y, w, h) in faces:
                face_color = frame[y:y+h, x:x+w]
                face_gray = gray[y:y+h, x:x+w]

                # Leeftijd en emotie voorspellen
                age = self.model.predict_age(face_color)
                emotion = self.model.predict_emotion(face_gray)

                self.stabilizer.update(age)
                stable_age = self.stabilizer.get_stable_age()

                self.queue.put((frame, stable_age, emotion))
                break  # pak alleen grootste/1e gezicht

            time.sleep(0.01)

        cap.release()
