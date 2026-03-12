.PHONY: build up down logs test

build:
	docker compose build

up:
	docker compose up

down:
	docker compose down

logs:
	docker compose logs -f

test:
	PYTHONPATH=$(PWD)/src python3 -m unittest discover -s src/tests