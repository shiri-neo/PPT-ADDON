#!/bin/bash

echo "🎨 PPT AI Assistant - Setup Script"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Backend setup
echo -e "${BLUE}📦 Setting up Backend...${NC}"
cd backend

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Upgrading pip..."
pip install --upgrade pip setuptools wheel

echo "Installing Python dependencies..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Failed to install Python dependencies"
    exit 1
fi

echo "Setting up database..."
python init_db.py

if [ $? -ne 0 ]; then
    echo "❌ Failed to set up database"
    exit 1
fi

cd ..
echo -e "${GREEN}✅ Backend setup complete!${NC}"
echo ""

# Frontend setup
echo -e "${BLUE}📦 Setting up Frontend...${NC}"
cd frontend

echo "Installing Node dependencies..."
npm install

cd ..
echo -e "${GREEN}✅ Frontend setup complete!${NC}"
echo ""

echo -e "${GREEN}🎉 Setup completed successfully!${NC}"
echo ""
echo "To start the application:"
echo "  Backend:  cd backend && ./start.sh"
echo "  Frontend: cd frontend && ./start.sh"
echo ""
echo "Or use: ./run.sh"
