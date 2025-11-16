#!/bin/bash

echo "🚀 Starting PPT AI Backend..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -q -r requirements.txt

# Check if database is initialized
echo "🗄️  Checking database..."
python init_db.py

echo ""
echo "✅ Backend ready!"
echo "🌐 Starting server at http://localhost:8000"
echo "📚 API docs at http://localhost:8000/docs"
echo ""

# Start the server (only watch app directory, not venv)
uvicorn app.main:app --reload --reload-dir app --host 0.0.0.0 --port 8000
