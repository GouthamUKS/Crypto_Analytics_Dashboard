#!/bin/bash

# Quick Start Script for Crypto Analytics Dashboard
# This script sets up and runs the entire application

set -e

echo "🚀 Starting Crypto Analytics Dashboard Setup"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}Error: Docker is not installed${NC}"
    echo "Please install Docker from https://docs.docker.com/get-docker/"
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo -e "${RED}Error: Docker Compose is not installed${NC}"
    echo "Please install Docker Compose from https://docs.docker.com/compose/install/"
    exit 1
fi

echo -e "${GREEN}✓ Docker is installed${NC}"

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file from .env.example...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
    echo -e "${YELLOW}Please edit .env file with your API keys if needed${NC}"
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Build and start all services
echo -e "\n${YELLOW}Building Docker images...${NC}"
docker-compose build

echo -e "\n${YELLOW}Starting services...${NC}"
docker-compose up -d

# Wait for services to be ready
echo -e "\n${YELLOW}Waiting for services to be ready...${NC}"
sleep 10

# Check service health
echo -e "\n${YELLOW}Checking service health...${NC}"

# Check PostgreSQL
if docker-compose ps postgres | grep -q "Up"; then
    echo -e "${GREEN}✓ PostgreSQL is running${NC}"
else
    echo -e "${RED}✗ PostgreSQL is not running${NC}"
fi

# Check Redis
if docker-compose ps redis | grep -q "Up"; then
    echo -e "${GREEN}✓ Redis is running${NC}"
else
    echo -e "${RED}✗ Redis is not running${NC}"
fi

# Check Backend
if docker-compose ps backend | grep -q "Up"; then
    echo -e "${GREEN}✓ Backend API is running${NC}"
else
    echo -e "${RED}✗ Backend API is not running${NC}"
fi

# Check Frontend
if docker-compose ps frontend | grep -q "Up"; then
    echo -e "${GREEN}✓ Frontend is running${NC}"
else
    echo -e "${RED}✗ Frontend is not running${NC}"
fi

# Check Spark
if docker-compose ps spark-master | grep -q "Up"; then
    echo -e "${GREEN}✓ Spark Master is running${NC}"
else
    echo -e "${RED}✗ Spark Master is not running${NC}"
fi

echo -e "\n${GREEN}=============================================="
echo "🎉 Setup Complete!"
echo "==============================================\n${NC}"

echo "Access the application at:"
echo -e "${GREEN}Frontend:${NC} http://localhost:3000"
echo -e "${GREEN}Backend API:${NC} http://localhost:8000"
echo -e "${GREEN}API Docs:${NC} http://localhost:8000/docs"
echo -e "${GREEN}Spark UI:${NC} http://localhost:8080"

echo -e "\n${YELLOW}Useful commands:${NC}"
echo "  View logs:        docker-compose logs -f"
echo "  Stop services:    docker-compose down"
echo "  Restart services: docker-compose restart"
echo "  View status:      docker-compose ps"

echo -e "\n${YELLOW}Note:${NC} It may take a few minutes for all services to fully initialize."
echo "If you encounter issues, check the logs with: docker-compose logs -f"
