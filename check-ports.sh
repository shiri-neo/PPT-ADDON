#!/bin/bash

echo "🔍 Port & Configuration Check"
echo "================================"
echo ""

# Check backend process
echo "1. Backend Process:"
BACKEND_PID=$(lsof -ti:8000 2>/dev/null)
if [ -n "$BACKEND_PID" ]; then
    echo "   ✅ Backend is running (PID: $BACKEND_PID)"
    echo "   Process: $(ps -p $BACKEND_PID -o comm=)"
else
    echo "   ❌ No process listening on port 8000"
fi

echo ""

# Check frontend process
echo "2. Frontend Process:"
FRONTEND_PID=$(lsof -ti:5173 2>/dev/null)
if [ -n "$FRONTEND_PID" ]; then
    echo "   ✅ Frontend is running (PID: $FRONTEND_PID)"
    echo "   Process: $(ps -p $FRONTEND_PID -o comm=)"
else
    echo "   ❌ No process listening on port 5173"
fi

echo ""

# Check backend .env
echo "3. Backend Configuration (backend/.env):"
if [ -f "backend/.env" ]; then
    grep -E "DATABASE_URL|CORS" backend/.env
else
    echo "   ❌ backend/.env not found"
fi

echo ""

# Check frontend .env
echo "4. Frontend Configuration (frontend/.env):"
if [ -f "frontend/.env" ]; then
    cat frontend/.env
else
    echo "   ❌ frontend/.env not found"
fi

echo ""

# Test backend directly
echo "5. Direct Backend Test:"
if curl -s -m 2 http://localhost:8000/health > /dev/null 2>&1; then
    echo "   ✅ Backend responds to http://localhost:8000/health"
    curl -s http://localhost:8000/health
else
    echo "   ❌ Backend does NOT respond to http://localhost:8000/health"
    echo "   Try: cd backend && ./start.sh"
fi

echo ""

# Test CORS
echo "6. CORS Test (simulating frontend request):"
CORS_RESPONSE=$(curl -s -X OPTIONS http://localhost:8000/auth/signup \
  -H "Origin: http://localhost:5173" \
  -H "Access-Control-Request-Method: POST" \
  -H "Access-Control-Request-Headers: content-type" \
  -i 2>/dev/null | grep -i "access-control")

if [ -n "$CORS_RESPONSE" ]; then
    echo "   ✅ CORS headers present:"
    echo "$CORS_RESPONSE" | sed 's/^/      /'
else
    echo "   ⚠️  No CORS headers found (backend might not be running)"
fi

echo ""
echo "================================"
echo ""
echo "Quick Commands:"
echo "  Start backend:  cd backend && ./start.sh"
echo "  Start frontend: cd frontend && npm run dev"
echo "  Test backend:   curl http://localhost:8000/health"
