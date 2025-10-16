#!/bin/bash

echo "📊 ToDo Application Status"
echo "========================="

# Check backend
echo "🔧 Backend Status:"
if curl -s http://localhost:5001/api/health > /dev/null; then
    echo "  ✅ Backend is running on http://localhost:5001"
    echo "  ✅ API is responding correctly"
else
    echo "  ❌ Backend is not responding"
fi

# Check frontend
echo ""
echo "📱 Frontend Status:"
if curl -s -I http://localhost:3000 | grep -q "200 OK"; then
    echo "  ✅ Frontend is running on http://localhost:3000"
else
    echo "  ❌ Frontend is not responding"
fi

# Check processes
echo ""
echo "🔄 Process Status:"
if pgrep -f "python app.py" > /dev/null; then
    echo "  ✅ Flask backend process is running"
else
    echo "  ❌ Flask backend process not found"
fi

if pgrep -f "npm start" > /dev/null; then
    echo "  ✅ React frontend process is running"
else
    echo "  ❌ React frontend process not found"
fi

echo ""
echo "🌐 Access URLs:"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:5001"
echo "  Health Check: http://localhost:5001/api/health"

