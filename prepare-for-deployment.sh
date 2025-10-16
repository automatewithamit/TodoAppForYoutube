#!/bin/bash

# Prepare ToDo App for Deployment
# This script prepares your application for deployment to Vercel and Render

echo "🚀 Preparing ToDo App for Deployment..."
echo "======================================"

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

echo -e "${BLUE}📋 Step 1: Checking Prerequisites...${NC}"
echo "----------------------------------------"

# Check if git is installed
if command -v git &> /dev/null; then
    print_status 0 "Git is installed"
else
    print_status 1 "Git is not installed. Please install Git first."
    exit 1
fi

# Check if node is installed
if command -v node &> /dev/null; then
    print_status 0 "Node.js is installed"
    NODE_VERSION=$(node --version)
    echo "  Version: $NODE_VERSION"
else
    print_status 1 "Node.js is not installed. Please install Node.js first."
    exit 1
fi

# Check if npm is installed
if command -v npm &> /dev/null; then
    print_status 0 "npm is installed"
else
    print_status 1 "npm is not installed. Please install npm first."
    exit 1
fi

echo ""
echo -e "${BLUE}📁 Step 2: Preparing Environment Files...${NC}"
echo "----------------------------------------"

# Create backend .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "Creating backend/.env file..."
    cat > backend/.env << EOF
SECRET_KEY=your-super-secret-key-change-this-in-production-$(date +%s)
JWT_SECRET_KEY=your-jwt-secret-key-change-this-in-production-$(date +%s)
DATABASE_URL=sqlite:///todoapp.db
FLASK_ENV=production
EOF
    print_status 0 "Backend .env file created"
else
    print_status 0 "Backend .env file already exists"
fi

# Create frontend .env file if it doesn't exist
if [ ! -f "frontend/.env" ]; then
    echo "Creating frontend/.env file..."
    cat > frontend/.env << EOF
REACT_APP_API_URL=https://your-backend-name.onrender.com
EOF
    print_status 0 "Frontend .env file created"
else
    print_status 0 "Frontend .env file already exists"
fi

echo ""
echo -e "${BLUE}🔧 Step 3: Installing Dependencies...${NC}"
echo "----------------------------------------"

# Install backend dependencies
echo "Installing backend dependencies..."
cd backend
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_status 0 "Backend dependencies installed"
    else
        print_status 1 "Failed to install backend dependencies"
        echo "  Please run: pip install -r requirements.txt"
    fi
else
    print_status 1 "requirements.txt not found in backend directory"
fi
cd ..

# Install frontend dependencies
echo "Installing frontend dependencies..."
cd frontend
if [ -f "package.json" ]; then
    npm install > /dev/null 2>&1
    if [ $? -eq 0 ]; then
        print_status 0 "Frontend dependencies installed"
    else
        print_status 1 "Failed to install frontend dependencies"
        echo "  Please run: npm install"
    fi
else
    print_status 1 "package.json not found in frontend directory"
fi
cd ..

echo ""
echo -e "${BLUE}🧪 Step 4: Testing Local Application...${NC}"
echo "----------------------------------------"

# Test backend
echo "Testing backend..."
cd backend
python -c "import app; print('Backend imports successfully')" 2>/dev/null
if [ $? -eq 0 ]; then
    print_status 0 "Backend code is valid"
else
    print_status 1 "Backend code has issues"
fi
cd ..

# Test frontend build
echo "Testing frontend build..."
cd frontend
npm run build > /dev/null 2>&1
if [ $? -eq 0 ]; then
    print_status 0 "Frontend builds successfully"
    # Clean up build directory
    rm -rf build
else
    print_status 1 "Frontend build failed"
    echo "  Please check for errors in your React code"
fi
cd ..

echo ""
echo -e "${BLUE}📝 Step 5: Preparing Git Repository...${NC}"
echo "----------------------------------------"

# Check if git repository exists
if [ -d ".git" ]; then
    print_status 0 "Git repository exists"
else
    echo "Initializing git repository..."
    git init
    print_status 0 "Git repository initialized"
fi

# Check git status
echo "Checking git status..."
if git status --porcelain | grep -q .; then
    echo -e "${YELLOW}⚠️  You have uncommitted changes. Please commit them before deployment.${NC}"
    echo "Run these commands:"
    echo "  git add ."
    echo "  git commit -m 'Prepare for deployment'"
else
    print_status 0 "All changes are committed"
fi

echo ""
echo -e "${BLUE}📋 Step 6: Deployment Checklist...${NC}"
echo "----------------------------------------"

echo "Before deploying, make sure you have:"
echo "  ✅ GitHub account"
echo "  ✅ Vercel account (connected to GitHub)"
echo "  ✅ Render account (connected to GitHub)"
echo "  ✅ Vercel CLI installed (npm install -g vercel)"

echo ""
echo -e "${BLUE}🎯 Next Steps:${NC}"
echo "1. Create a GitHub repository and push your code"
echo "2. Deploy backend to Render (see BEGINNER_DEPLOYMENT_GUIDE.md)"
echo "3. Deploy frontend to Vercel (see BEGINNER_DEPLOYMENT_GUIDE.md)"
echo "4. Update environment variables with actual URLs"
echo "5. Test your live application"

echo ""
echo -e "${GREEN}🚀 Your application is ready for deployment!${NC}"
echo "Follow the BEGINNER_DEPLOYMENT_GUIDE.md for detailed instructions."
