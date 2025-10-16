#!/bin/bash

echo "🛑 Stopping ToDo Application"
echo "============================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

# Kill all related processes
print_status "Stopping Flask backend..."
pkill -f "python app.py" 2>/dev/null || true

print_status "Stopping React frontend..."
pkill -f "npm start" 2>/dev/null || true
pkill -f "react-scripts start" 2>/dev/null || true

print_status "Freeing up ports..."
lsof -ti:3000,5001 | xargs kill -9 2>/dev/null || true

print_success "All processes stopped successfully!"
echo ""
echo "To start the application again, run:"
echo "  ./start-app.sh"
