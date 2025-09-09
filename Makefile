.PHONY: help install test lint build docker

VENV := .venv

help:
	@echo "Make targets: install, test, lint, build, docker"

install:
	python -m venv $(VENV)
	. $(VENV)/bin/activate && python -m pip install --upgrade pip && \
	pip install -r requirements.txt

test:
	. $(VENV)/bin/activate && pytest -q

lint:
	. $(VENV)/bin/activate && pip install ruff && ruff check .

build:
	# example: create a source distribution
	python -m pip install --upgrade build && python -m build

docker:
	docker-compose build

	models:
	mkdir -p models
	curl -L -o models/age_deploy.prototxt https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt
	curl -L -o models/age_net.caffemodel https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face/dnn_age/age_net.caffemodel