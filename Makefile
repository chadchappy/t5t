.PHONY: help build start stop restart logs clean setup test

help:
	@echo "Top 5 Things Email Generator - Available Commands"
	@echo "=================================================="
	@echo ""
	@echo "  make setup      - Initial setup (copy .env.example)"
	@echo "  make build      - Build the Docker container"
	@echo "  make start      - Start the application"
	@echo "  make stop       - Stop the application"
	@echo "  make restart    - Restart the application"
	@echo "  make logs       - View application logs"
	@echo "  make clean      - Stop and remove containers"
	@echo "  make test       - Run basic connectivity tests"
	@echo ""

setup:
	@echo "Setting up environment..."
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "✅ Created .env file"; \
		echo "⚠️  Please edit .env and add your Azure AD credentials"; \
		echo "   See SETUP.md for instructions"; \
	else \
		echo "⚠️  .env already exists, skipping..."; \
	fi

build:
	@echo "Building Docker container..."
	docker-compose build

start:
	@echo "Starting application..."
	docker-compose up -d
	@echo ""
	@echo "✅ Application started!"
	@echo "📱 Open http://localhost:5000 in your browser"
	@echo ""
	@echo "View logs: make logs"

stop:
	@echo "Stopping application..."
	docker-compose down

restart: stop start

logs:
	docker-compose logs -f

clean:
	@echo "Cleaning up..."
	docker-compose down -v
	@echo "✅ Containers and volumes removed"

test:
	@echo "Testing Docker connectivity..."
	@docker info > /dev/null 2>&1 && echo "✅ Docker is running" || echo "❌ Docker is not running"
	@echo ""
	@echo "Checking .env file..."
	@test -f .env && echo "✅ .env file exists" || echo "❌ .env file not found"
	@echo ""
	@echo "Testing application endpoint..."
	@curl -s http://localhost:5000 > /dev/null && echo "✅ Application is responding" || echo "⚠️  Application not running (run 'make start' first)"

