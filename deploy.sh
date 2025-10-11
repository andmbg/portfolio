#!/bin/bash

# Deployment script for production server
set -e

echo "🚀 Starting deployment..."

# Configuration
DEPLOY_DIR="/opt/portfolio"
REPO_URL="https://github.com/andmbg/portfolio.git"
COMPOSE_FILE="docker-compose.prod.yml"

# Create deployment directory if it doesn't exist
sudo mkdir -p $DEPLOY_DIR
cd $DEPLOY_DIR

# Clone or update repository
if [ -d ".git" ]; then
    echo "📥 Pulling latest changes..."
    git pull origin main
else
    echo "📥 Cloning repository..."
    git clone $REPO_URL .
fi

# Check .env file exists
if [ ! -f ".env" ]; then
    echo "⚙️  Creating .env file from example..."
    cp .env.example .env
    echo "❗ Please update .env with production values!"
    echo "📝 Edit the file: nano /opt/portfolio/.env"
    exit 1
fi

# Verify .env has been customized (check for example values)
if grep -q "CHANGE_THIS" .env; then
    echo "❗ .env file contains example values. Please update with production secrets!"
    echo "📝 Edit the file: nano /opt/portfolio/.env"
    exit 1
fi

# Pull latest images
echo "📦 Pulling latest Docker images..."
docker-compose -f $COMPOSE_FILE pull

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker-compose -f $COMPOSE_FILE down

# Start updated containers
echo "🔄 Starting updated containers..."
docker-compose -f $COMPOSE_FILE up -d

# Clean up old images
echo "🧹 Cleaning up old images..."
docker image prune -f

# Show running containers
echo "✅ Deployment complete! Running containers:"
docker ps

echo "🌐 Application should be available at your domain"
