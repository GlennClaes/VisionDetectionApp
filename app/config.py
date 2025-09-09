# =========================
# Bestand: config.py
# =========================
from dataclasses import dataclass
from typing import Tuple

AGE_BUCKETS = [
    "(0-2)", "(4-6)", "(8-12)", "(15-20)",
    "(25-32)", "(38-43)", "(48-53)", "(60-100)"
]

@dataclass
class AppConfig:
    camera_index: int = 0
    frame_width: int = 1280
    frame_height: int = 720
    show_fps: bool = True
    draw_debug: bool = True

    # Haarcascade parameters
    face_scaleFactor: float = 1.1
    face_minNeighbors: int = 6
    face_minSize: Tuple[int, int] = (100, 100)

    # Leeftijdsstabilisatie
    age_history_size: int = 15

    # Modelbestanden
    age_proto_path: str = "models/age_deploy.prototxt"
    age_model_path: str = "models/age_net.caffemodel"
    emotion_model_path: str = "models/emotion_model.hdf5"

    # Data opslag
    db_path: str = "data/app.db"
    photos_dir: str = "data/photos"
    csv_path: str = "data/hand_face_data.csv"
