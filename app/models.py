# =========================
# Bestand: models.py
# =========================
import cv2
import numpy as np
from collections import deque
from tensorflow.keras.models import load_model
from config import AGE_BUCKETS

AGE_BUFFER_SIZE = 10

class AgeEmotionModel:
    def __init__(self, age_proto, age_model, emotion_model):
        # Leeftijdsmodel (Caffe)
        self.age_net = cv2.dnn.readNetFromCaffe(age_proto, age_model)

        # Emotiemodel (Keras/TensorFlow)
        self.emotion_net = load_model(emotion_model)
        self.emotion_labels = [
            "Boos", "Walging", "Bang", "Blij", "Verdrietig", "Verbaasd", "Neutraal"
        ]

        # Haarcascades
        self.face_cascade = cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )

    # --- Leeftijd voorspellen ---
    def predict_age(self, face_img):
        try:
            blob = cv2.dnn.blobFromImage(
                face_img, 1.0, (227, 227),
                (78.426, 87.77, 114.89), swapRB=False
            )
            self.age_net.setInput(blob)
            preds = self.age_net.forward()
            return AGE_BUCKETS[preds[0].argmax()]
        except Exception:
            return "?"

    # --- Emotie voorspellen ---
    def predict_emotion(self, face_gray):
        try:
            face_resized = cv2.resize(face_gray, (48, 48))
            face_resized = face_resized.astype("float") / 255.0
            face_resized = np.expand_dims(face_resized, axis=-1)  # (48,48,1)
            face_resized = np.expand_dims(face_resized, axis=0)   # (1,48,48,1)

            preds = self.emotion_net.predict(face_resized, verbose=0)[0]
            idx = np.argmax(preds)
            return self.emotion_labels[idx]
        except Exception:
            return "Onbekend"

# --- Leeftijd stabilisatie ---
class AgeStabilizer:
    def __init__(self, buffer_size=AGE_BUFFER_SIZE):
        self.history = deque(maxlen=buffer_size)

    def update(self, age_str):
        self.history.append(age_str)

    def get_stable_age(self):
        if not self.history:
            return "?"
        indices = [AGE_BUCKETS.index(a) for a in self.history if a in AGE_BUCKETS]
        if not indices:
            return "?"
        median_idx = int(np.median(indices))
        return AGE_BUCKETS[median_idx]
