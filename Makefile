.PHONY: build up down logs test

# Leer MODE del .env
MODE := $(shell grep MODE .env | cut -d '=' -f2)

build:
	docker compose build

up:
ifeq ($(MODE),batch)
	docker compose up model batch-worker frontend
endif
ifeq ($(MODE),streaming)
	docker compose up model streaming-worker frontend
endif
ifeq ($(MODE),direct)
	docker compose up model frontend
endif

down:
	docker compose down

logs:
	docker compose logs -f

test:
	PYTHONPATH=$(PWD)/src python3 -m unittest discover -s src/tests