#!/bin/bash

echo "🚀 Starting PPT AI Frontend..."
echo ""

# Check if node_modules exists
if [ ! -d "node_modules" ]; then
    echo "📦 Installing dependencies..."
    npm install
fi

echo ""
echo "✅ Frontend ready!"
echo "🌐 Starting dev server at http://localhost:5173"
echo ""

# Start the dev server
npm run dev
