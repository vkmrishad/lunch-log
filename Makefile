.PHONY: build up down

build:
	@echo "Building docker compose..."
	docker-compose build
	@echo "Docker compose built successfully."

up:
	@echo "Starting docker compose..."
	docker-compose up -d
	@echo "Docker compose started successfully."

down:
	@echo "Stopping docker compose..."
	docker-compose down
	@echo "Docker compose stopped successfully."
