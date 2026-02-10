#!/bin/bash

# 🚀 RaceTracker - Quick Start Script
# This script starts the entire RaceTracker application

echo "🎉 RaceTracker Application - Starting..."
echo "=========================================="
echo ""

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Stop any running containers
echo "🛑 Stopping any running RaceTracker containers..."
docker-compose down 2>/dev/null || true
sleep 2

# Start the application
echo "🚀 Starting RaceTracker containers..."
docker-compose up -d

# Wait for services to be ready
echo "⏳ Waiting for services to start..."
sleep 5

# Check backend health
echo "🔍 Checking backend health..."
if curl -s http://localhost:8000/health | grep -q "healthy"; then
    echo "✅ Backend is healthy"
else
    echo "⚠️  Backend might not be fully ready yet"
fi

echo ""
echo "=========================================="
echo "✅ RaceTracker is now running!"
echo ""
echo "📍 Access Points:"
echo "   🌐 Frontend:    http://localhost"
echo "   🔌 API:         http://localhost:8000"
echo "   📖 API Docs:    http://localhost:8000/docs"
echo "   ❤️  Health:      http://localhost:8000/health"
echo ""
echo "📚 Documentation:"
echo "   📄 GETTING_STARTED.md  - User guide"
echo "   🐳 DOCKER_SETUP.md     - Docker guide"
echo "   📊 PROJECT_STATUS.md   - Project status"
echo ""
echo "🛑 To stop: docker-compose down"
echo "📋 To view logs: docker-compose logs -f"
echo "=========================================="
