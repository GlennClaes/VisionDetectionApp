# =========================
# Bestand: docker/Dockerfile
# =========================
FROM python:3.11-slim

# Install system deps for OpenCV and Tk
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    pkg-config \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    libgtk2.0-0 \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# copy requirements and install
COPY requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

# copy app
COPY . /app

# default entrypoint for headless worker (adjust if GUI needed)
CMD ["python", "-u", "app/main.py"]