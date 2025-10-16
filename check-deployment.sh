#!/bin/bash

# Check Deployment Status
# This script checks the status of your deployed application

echo "🔍 Checking Deployment Status..."
echo "==============================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print status
print_status() {
    if [ $1 -eq 0 ]; then
        echo -e "${GREEN}✅ $2${NC}"
    else
        echo -e "${RED}❌ $2${NC}"
    fi
}

# Function to check URL
check_url() {
    local url=$1
    local name=$2
    
    echo "Checking $name..."
    if curl -s --max-time 10 "$url" > /dev/null 2>&1; then
        print_status 0 "$name is accessible"
        return 0
    else
        print_status 1 "$name is not accessible"
        return 1
    fi
}

echo -e "${BLUE}📊 Local Development Status${NC}"
echo "----------------------------"

# Check local backend
if curl -s http://localhost:5001/api/health > /dev/null 2>&1; then
    print_status 0 "Local backend is running (port 5001)"
else
    print_status 1 "Local backend is not running"
fi

# Check local frontend
if curl -s -I http://localhost:3000 | grep -q "200 OK" 2>/dev/null; then
    print_status 0 "Local frontend is running (port 3000)"
else
    print_status 1 "Local frontend is not running"
fi

echo ""
echo -e "${BLUE}🌐 Production Deployment Status${NC}"
echo "--------------------------------"

# Check if environment files exist
if [ -f "frontend/.env" ]; then
    API_URL=$(grep "REACT_APP_API_URL" frontend/.env | cut -d'=' -f2)
    if [ ! -z "$API_URL" ] && [ "$API_URL" != "https://your-backend-name.onrender.com" ]; then
        echo "Backend URL found: $API_URL"
        check_url "$API_URL/api/health" "Production Backend"
    else
        echo -e "${YELLOW}⚠️  Backend URL not configured in frontend/.env${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  Frontend .env file not found${NC}"
fi

echo ""
echo -e "${BLUE}📋 Deployment Checklist${NC}"
echo "----------------------"

# Check if files exist
if [ -f "BEGINNER_DEPLOYMENT_GUIDE.md" ]; then
    print_status 0 "Deployment guide exists"
else
    print_status 1 "Deployment guide missing"
fi

if [ -f "DEPLOYMENT_CHECKLIST.md" ]; then
    print_status 0 "Deployment checklist exists"
else
    print_status 1 "Deployment checklist missing"
fi

if [ -f "backend/.env" ]; then
    print_status 0 "Backend environment file exists"
else
    print_status 1 "Backend environment file missing"
fi

if [ -f "frontend/.env" ]; then
    print_status 0 "Frontend environment file exists"
else
    print_status 1 "Frontend environment file missing"
fi

# Check git status
if [ -d ".git" ]; then
    if git status --porcelain | grep -q .; then
        echo -e "${YELLOW}⚠️  You have uncommitted changes${NC}"
    else
        print_status 0 "All changes are committed"
    fi
    
    if git remote get-url origin > /dev/null 2>&1; then
        print_status 0 "GitHub remote is configured"
    else
        print_status 1 "GitHub remote not configured"
    fi
else
    print_status 1 "Git repository not initialized"
fi

echo ""
echo -e "${BLUE}🎯 Quick Actions${NC}"
echo "----------------"

echo "To prepare for deployment:"
echo "  ./prepare-for-deployment.sh"

echo ""
echo "To push to GitHub:"
echo "  ./deploy-to-github.sh"

echo ""
echo "To test your application:"
echo "  ./test_application.sh"

echo ""
echo "To check local status:"
echo "  ./status.sh"

echo ""
echo -e "${BLUE}📖 Documentation${NC}"
echo "----------------"

echo "📋 Deployment Guide: BEGINNER_DEPLOYMENT_GUIDE.md"
echo "✅ Checklist: DEPLOYMENT_CHECKLIST.md"
echo "🧪 Test Report: testsprite_tests/comprehensive_test_report.md"

echo ""
echo -e "${GREEN}🚀 Ready to deploy your ToDo application!${NC}"
