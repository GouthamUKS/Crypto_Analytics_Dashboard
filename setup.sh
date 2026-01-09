#!/bin/bash

# Manual Setup Script for Development
# Use this if you want to run services locally without Docker

set -e

echo "🛠️  Manual Setup for Crypto Analytics Dashboard"
echo "=============================================="

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "Error: Node.js is not installed"
    exit 1
fi

# Check PostgreSQL
if ! command -v psql &> /dev/null; then
    echo "Warning: PostgreSQL client not found. Make sure PostgreSQL is installed."
fi

echo -e "${GREEN}✓ Prerequisites check passed${NC}\n"

# 1. Setup Database
echo -e "${YELLOW}Step 1: Database Setup${NC}"
echo "Creating database..."
createdb crypto_analytics || echo "Database may already exist"

echo "Running migrations..."
psql -d crypto_analytics -f database/init.sql

echo -e "${GREEN}✓ Database setup complete\n${NC}"

# 2. Setup Backend
echo -e "${YELLOW}Step 2: Backend Setup${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo -e "${GREEN}✓ Backend setup complete\n${NC}"
cd ..

# 3. Setup Spark
echo -e "${YELLOW}Step 3: Spark Setup${NC}"
cd spark

echo "Installing Spark dependencies..."
pip install -r requirements.txt

echo -e "${GREEN}✓ Spark setup complete\n${NC}"
cd ..

# 4. Setup Frontend
echo -e "${YELLOW}Step 4: Frontend Setup${NC}"
cd frontend

echo "Installing Node.js dependencies..."
npm install

echo -e "${GREEN}✓ Frontend setup complete\n${NC}"
cd ..

# 5. Create .env file
if [ ! -f .env ]; then
    echo -e "${YELLOW}Creating .env file...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ .env file created${NC}"
fi

echo -e "\n${GREEN}=============================================="
echo "✅ Manual Setup Complete!"
echo "==============================================\n${NC}"

echo "To start the application, run these commands in separate terminals:"
echo ""
echo -e "${YELLOW}Terminal 1 - Backend:${NC}"
echo "  cd backend"
echo "  source venv/bin/activate"
echo "  uvicorn app.main:app --reload --port 8000"
echo ""
echo -e "${YELLOW}Terminal 2 - Spark Streaming:${NC}"
echo "  cd spark"
echo "  spark-submit streaming_processor.py"
echo ""
echo -e "${YELLOW}Terminal 3 - Frontend:${NC}"
echo "  cd frontend"
echo "  npm start"
echo ""
echo -e "${YELLOW}Terminal 4 - Redis (if not running):${NC}"
echo "  redis-server"
