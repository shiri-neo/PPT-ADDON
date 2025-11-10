#!/bin/bash

echo "🔍 Diagnostic Test for PPT AI Assistant"
echo "========================================="
echo ""

# Test 1: Check if backend is running
echo "1. Testing if backend is running..."
if curl -s http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✅ Backend is responding"
    curl -s http://localhost:8000/health | python3 -m json.tool
else
    echo "   ❌ Backend is NOT responding on http://localhost:8000"
    echo "   Please start the backend with: cd backend && ./start.sh"
    exit 1
fi

echo ""

# Test 2: Check backend root endpoint
echo "2. Testing backend root endpoint..."
curl -s http://localhost:8000/ | python3 -m json.tool

echo ""

# Test 3: Test CORS with signup
echo "3. Testing signup endpoint (with CORS)..."
RANDOM_EMAIL="test$(date +%s)@example.com"
RESPONSE=$(curl -s -w "\nHTTP_CODE:%{http_code}" -X POST http://localhost:8000/auth/signup \
  -H "Content-Type: application/json" \
  -H "Origin: http://localhost:5173" \
  -d "{\"email\":\"$RANDOM_EMAIL\",\"password\":\"password123\"}")

HTTP_CODE=$(echo "$RESPONSE" | grep -o "HTTP_CODE:[0-9]*" | cut -d: -f2)
BODY=$(echo "$RESPONSE" | sed 's/HTTP_CODE:[0-9]*//')

echo "   HTTP Status: $HTTP_CODE"
echo "   Response:"
echo "$BODY" | python3 -m json.tool 2>/dev/null || echo "$BODY"

echo ""

# Test 4: Check what's listening on port 8000
echo "4. Checking what's running on port 8000..."
lsof -i :8000 2>/dev/null || echo "   Nothing found (or lsof not available)"

echo ""

# Test 5: Frontend configuration
echo "5. Checking frontend .env..."
if [ -f "frontend/.env" ]; then
    cat frontend/.env
else
    echo "   ⚠️  frontend/.env not found!"
fi

echo ""
echo "========================================="
echo "Diagnostic complete!"
