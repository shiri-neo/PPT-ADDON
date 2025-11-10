#!/bin/bash

echo "🎨 PPT AI Assistant - Setup Script"
echo "===================================="
echo ""

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python version
echo "Checking Python version..."
PYTHON_CMD=""

# Try different Python commands
for cmd in python3.12 python3.11 python3.10 python3.9 python3; do
    if command -v $cmd &> /dev/null; then
        VERSION=$($cmd -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
        MAJOR=$(echo $VERSION | cut -d. -f1)
        MINOR=$(echo $VERSION | cut -d. -f2)

        if [ "$MAJOR" -eq 3 ] && [ "$MINOR" -ge 9 ] && [ "$MINOR" -le 12 ]; then
            PYTHON_CMD=$cmd
            echo -e "${GREEN}✓ Found compatible Python: $cmd (version $VERSION)${NC}"
            break
        fi
    fi
done

if [ -z "$PYTHON_CMD" ]; then
    echo -e "${RED}❌ Error: Python 3.9-3.12 is required${NC}"
    echo -e "${YELLOW}You have Python 3.13 which is too new for some dependencies.${NC}"
    echo -e "${YELLOW}Please install Python 3.12 or 3.11:${NC}"
    echo ""
    echo "  macOS:   brew install python@3.12"
    echo "  Ubuntu:  sudo apt install python3.12"
    echo "  Windows: Download from python.org"
    echo ""
    exit 1
fi

# Backend setup
echo ""
echo -e "${BLUE}📦 Setting up Backend...${NC}"
cd backend

# Create/update .env file with SQLite configuration
echo "Creating .env configuration..."
cat > .env << 'EOF'
APP_NAME=ppt-ai-backend
DEBUG=True
DATABASE_URL=sqlite:///./pptai.db
JWT_SECRET_KEY=dev-secret-key-change-in-production-12345678
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=60
CORS_ALLOWED_ORIGINS=["http://localhost:5173","https://localhost:5173"]
EOF

if [ ! -d "venv" ]; then
    echo "Creating Python virtual environment with $PYTHON_CMD..."
    $PYTHON_CMD -m venv venv
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

echo "Testing backend setup..."
python test_setup.py

if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Backend setup test failed${NC}"
    echo -e "${YELLOW}Please check the errors above${NC}"
    exit 1
fi

cd ..
echo -e "${GREEN}✅ Backend setup complete!${NC}"
echo ""

# Frontend setup
echo -e "${BLUE}📦 Setting up Frontend...${NC}"
cd frontend

# Create/update .env file with API URL
echo "Creating .env configuration..."
cat > .env << 'EOF'
VITE_API_BASE_URL=http://localhost:8000
EOF

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
