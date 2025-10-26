#!/bin/bash

# Script to start both frontend and backend applications for testing

echo "🚀 Starting ToDo Application for Testing"
echo "========================================"

# Function to check if a port is in use
check_port() {
    if lsof -Pi :$1 -sTCP:LISTEN -t >/dev/null ; then
        echo "✅ Port $1 is already in use"
        return 0
    else
        echo "❌ Port $1 is not in use"
        return 1
    fi
}

# Check if applications are already running
echo "🔍 Checking application status..."

if check_port 3000; then
    echo "Frontend appears to be running on port 3000"
else
    echo "Starting frontend on port 3000..."
    cd frontend
    npm start &
    FRONTEND_PID=$!
    cd ..
    echo "Frontend started with PID: $FRONTEND_PID"
fi

if check_port 5001; then
    echo "Backend appears to be running on port 5001"
else
    echo "Starting backend on port 5001..."
    cd backend
    source venv/bin/activate
    python app.py &
    BACKEND_PID=$!
    cd ..
    echo "Backend started with PID: $BACKEND_PID"
fi

echo ""
echo "⏳ Waiting for applications to start..."
sleep 5

# Check if applications are responding
echo "🔍 Verifying applications are responding..."

# Check frontend
if curl -s http://localhost:3000 > /dev/null; then
    echo "✅ Frontend is responding on http://localhost:3000"
else
    echo "❌ Frontend is not responding on http://localhost:3000"
fi

# Check backend
if curl -s http://localhost:5001/api/health > /dev/null; then
    echo "✅ Backend is responding on http://localhost:5001"
else
    echo "❌ Backend is not responding on http://localhost:5001"
fi

echo ""
echo "🎉 Applications are ready for testing!"
echo ""
echo "To run tests:"
echo "  source test-env/bin/activate"
echo "  python run_tests.py"
echo ""
echo "To stop applications:"
echo "  ./stop.sh"







