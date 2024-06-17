.PHONY: build up down collectstatic, migrate

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

collectstatic:
	@echo "Collecting static files..."
	docker-compose exec app python manage.py collectstatic --noinput
	@echo "Static files collected successfully."

migrate:
	@echo "Applying migrations..."
	docker-compose exec app python manage.py migrate
	@echo "Migrations applied successfully."
