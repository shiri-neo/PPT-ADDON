#!/bin/bash

echo "🚀 Starting PPT AI Assistant"
echo "============================="
echo ""
echo "Choose an option:"
echo "  1) Start Backend only"
echo "  2) Start Frontend only"
echo "  3) Start Both (in separate terminals - requires tmux or screen)"
echo ""
read -p "Enter choice [1-3]: " choice

case $choice in
    1)
        echo "Starting Backend..."
        cd backend && ./start.sh
        ;;
    2)
        echo "Starting Frontend..."
        cd frontend && ./start.sh
        ;;
    3)
        echo "Starting both services..."
        echo ""
        echo "Backend will start in background..."
        cd backend
        source venv/bin/activate 2>/dev/null || true
        uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
        BACKEND_PID=$!
        cd ..

        echo "Backend started with PID: $BACKEND_PID"
        echo "Waiting 3 seconds for backend to initialize..."
        sleep 3

        echo ""
        echo "Starting Frontend..."
        cd frontend
        npm run dev

        # Cleanup on exit
        trap "kill $BACKEND_PID 2>/dev/null" EXIT
        ;;
    *)
        echo "Invalid choice. Exiting."
        exit 1
        ;;
esac
