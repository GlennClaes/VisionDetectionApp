import threading
import cv2
import time
from models import AgeEmotionModel, AgeStabilizer, EmotionStabilizer

class VideoWorker(threading.Thread):
    def __init__(self, cfg, queue, stop_event):
        super().__init__(daemon=True)
        self.cfg = cfg
        self.queue = queue
        self.stop_event = stop_event

        # Load models
        self.model = AgeEmotionModel(
            cfg.age_proto_path,
            cfg.age_model_path,
            cfg.emotion_model_path  # This uses emotion_model.hdf5
        )
        self.age_stabilizer = AgeStabilizer()
        self.emotion_stabilizer = EmotionStabilizer()

        # Last faces for GUI drawing
        self.last_faces = []

    def run(self):
        cap = cv2.VideoCapture(self.cfg.camera_index)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, self.cfg.frame_width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, self.cfg.frame_height)

        while not self.stop_event.is_set():
            ret, frame = cap.read()
            if not ret:
                time.sleep(0.01)
                continue

            frame = cv2.flip(frame, 1)
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            faces = self.model.face_cascade.detectMultiScale(
                gray,
                scaleFactor=self.cfg.face_scaleFactor,
                minNeighbors=self.cfg.face_minNeighbors,
                minSize=self.cfg.face_minSize
            )

            self.last_faces = faces  # store for GUI

            for (x, y, w, h) in faces[:1]:  # process first/largest face
                face_color = frame[y:y+h, x:x+w]
                face_gray = gray[y:y+h, x:x+w]

                # Predict age & emotion
                age = self.model.predict_age(face_color)
                emotion = self.model.predict_emotion(face_gray)

                # Stabilize predictions
                self.age_stabilizer.update(age)
                self.emotion_stabilizer.update(emotion)
                stable_age = self.age_stabilizer.get_stable_age()
                stable_emotion = self.emotion_stabilizer.get_stable_emotion()

                # Push to GUI
                self.queue.put((frame, stable_age, stable_emotion))
                break

            time.sleep(0.01)

        cap.release()