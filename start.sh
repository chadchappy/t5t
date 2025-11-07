#!/bin/bash

# Top 5 Things Email Generator - Quick Start Script

echo "🚀 Top 5 Things Email Generator - Quick Start"
echo "=============================================="
echo ""

# Check if .env exists
if [ ! -f .env ]; then
    echo "⚠️  .env file not found!"
    echo ""
    echo "Please follow these steps:"
    echo "1. Copy .env.example to .env:"
    echo "   cp .env.example .env"
    echo ""
    echo "2. Edit .env and fill in your Azure AD credentials"
    echo "   (See SETUP.md for detailed instructions)"
    echo ""
    exit 1
fi

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "⚠️  Docker is not running!"
    echo ""
    echo "Please start Docker Desktop or Colima:"
    echo "  - Docker Desktop: Start from Applications"
    echo "  - Colima: Run 'colima start'"
    echo ""
    exit 1
fi

echo "✅ Environment file found"
echo "✅ Docker is running"
echo ""

# Check if we should rebuild
if [ "$1" == "--rebuild" ]; then
    echo "🔨 Building container (this may take a few minutes)..."
    docker-compose up --build -d
else
    echo "🚀 Starting container..."
    docker-compose up -d
fi

# Wait for container to be ready
echo ""
echo "⏳ Waiting for application to start..."
sleep 5

# Check if container is running
if docker-compose ps | grep -q "Up"; then
    echo ""
    echo "✅ Application is running!"
    echo ""
    echo "📱 Open your browser to: http://localhost:5000"
    echo ""
    echo "To view logs: docker-compose logs -f"
    echo "To stop: docker-compose down"
    echo ""
else
    echo ""
    echo "❌ Failed to start application"
    echo ""
    echo "Check logs with: docker-compose logs"
    echo ""
    exit 1
fi

