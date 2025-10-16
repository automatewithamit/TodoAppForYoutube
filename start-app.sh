#!/bin/bash

echo "🚀 Starting ToDo Application"
echo "============================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check prerequisites
print_status "Checking prerequisites..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed. Please install Node.js 14 or higher."
    exit 1
fi

if ! command -v npm &> /dev/null; then
    print_error "npm is not installed. Please install npm."
    exit 1
fi

print_success "Prerequisites check passed!"

# Kill any existing processes on common ports
print_status "Clearing ports..."
lsof -ti:3000,5001 | xargs kill -9 2>/dev/null || true
sleep 2

# Use standard ports
BACKEND_PORT=5001
FRONTEND_PORT=3000

print_success "Using ports: Backend=$BACKEND_PORT, Frontend=$FRONTEND_PORT"

# Set up backend
print_status "Setting up backend..."
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    print_status "Creating Python virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
print_status "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
print_status "Installing Python dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    print_status "Creating environment file..."
    cp env.example .env
fi

# Initialize database
print_status "Initializing database..."
python -c "from app import app, db; app.app_context().push(); db.create_all(); print('Database initialized successfully!')"

# Start backend in background
print_status "Starting Flask backend on port $BACKEND_PORT..."
python app.py &
BACKEND_PID=$!

# Wait for backend to start
print_status "Waiting for backend to start..."
sleep 5

# Test backend
if curl -s http://localhost:$BACKEND_PORT/api/health > /dev/null; then
    print_success "Backend is running successfully!"
else
    print_warning "Backend might still be starting up..."
fi

# Go back to root directory
cd ..

# Set up frontend
print_status "Setting up frontend..."
cd frontend

# Install Node.js dependencies
print_status "Installing Node.js dependencies..."
npm install

# Start frontend in background
print_status "Starting React frontend on port $FRONTEND_PORT..."
npm start &
FRONTEND_PID=$!

# Go back to root directory
cd ..

# Wait for frontend to start
print_status "Waiting for frontend to start..."
sleep 10

# Test frontend
if curl -s http://localhost:$FRONTEND_PORT > /dev/null; then
    print_success "Frontend is running successfully!"
else
    print_warning "Frontend might still be starting up..."
fi

echo ""
echo "🎉 ToDo Application is now running!"
echo "=================================="
echo ""
echo "📱 Frontend: http://localhost:$FRONTEND_PORT"
echo "🔧 Backend API: http://localhost:$BACKEND_PORT"
echo "🔍 Health Check: http://localhost:$BACKEND_PORT/api/health"
echo ""
echo "📋 Available API Endpoints:"
echo "   POST /api/auth/register - User registration"
echo "   POST /api/auth/login - User login"
echo "   GET /api/tasks - Get all tasks"
echo "   POST /api/tasks - Create new task"
echo "   PUT /api/tasks/<id> - Update task"
echo "   DELETE /api/tasks/<id> - Delete task"
echo "   GET /api/stats - Get task statistics"
echo ""
echo "Press Ctrl+C to stop both servers"

# Function to cleanup background processes
cleanup() {
    echo ""
    print_status "Stopping servers..."
    kill $BACKEND_PID 2>/dev/null
    kill $FRONTEND_PID 2>/dev/null
    print_success "Servers stopped successfully!"
    exit 0
}

# Set up signal handlers
trap cleanup SIGINT SIGTERM

# Wait for background processes
wait
