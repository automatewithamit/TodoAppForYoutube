#!/bin/bash

# Deploy ToDo App to GitHub
# This script helps you push your code to GitHub for deployment

echo "🚀 Deploying ToDo App to GitHub..."
echo "================================="

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

# Check if git is configured
echo -e "${BLUE}🔧 Checking Git Configuration...${NC}"
echo "----------------------------------------"

if git config --get user.name > /dev/null 2>&1; then
    USER_NAME=$(git config --get user.name)
    print_status 0 "Git user name: $USER_NAME"
else
    echo -e "${YELLOW}⚠️  Git user name not set. Please run:${NC}"
    echo "  git config --global user.name 'Your Name'"
    echo "  git config --global user.email 'your.email@example.com'"
    exit 1
fi

if git config --get user.email > /dev/null 2>&1; then
    USER_EMAIL=$(git config --get user.email)
    print_status 0 "Git user email: $USER_EMAIL"
else
    echo -e "${YELLOW}⚠️  Git user email not set. Please run:${NC}"
    echo "  git config --global user.email 'your.email@example.com'"
    exit 1
fi

echo ""
echo -e "${BLUE}📁 Checking Repository Status...${NC}"
echo "----------------------------------------"

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "Initializing git repository..."
    git init
    print_status 0 "Git repository initialized"
fi

# Check for uncommitted changes
if git status --porcelain | grep -q .; then
    echo "Adding all files to git..."
    git add .
    
    echo "Committing changes..."
    git commit -m "Prepare for deployment - $(date '+%Y-%m-%d %H:%M:%S')"
    print_status 0 "Changes committed"
else
    print_status 0 "No uncommitted changes"
fi

echo ""
echo -e "${BLUE}🌐 GitHub Repository Setup...${NC}"
echo "----------------------------------------"

# Check if remote origin exists
if git remote get-url origin > /dev/null 2>&1; then
    REMOTE_URL=$(git remote get-url origin)
    print_status 0 "Remote origin exists: $REMOTE_URL"
else
    echo -e "${YELLOW}⚠️  No remote origin found.${NC}"
    echo ""
    echo "Please create a GitHub repository first:"
    echo "1. Go to https://github.com"
    echo "2. Click 'New repository'"
    echo "3. Name it 'todo-app-deployment' (or any name you prefer)"
    echo "4. Make it PUBLIC (required for free hosting)"
    echo "5. Don't initialize with README, .gitignore, or license"
    echo ""
    echo "Then run this command (replace YOUR_USERNAME with your GitHub username):"
    echo "  git remote add origin https://github.com/YOUR_USERNAME/todo-app-deployment.git"
    echo ""
    echo "After adding the remote, run this script again."
    exit 1
fi

echo ""
echo -e "${BLUE}📤 Pushing to GitHub...${NC}"
echo "----------------------------------------"

# Push to GitHub
echo "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    print_status 0 "Code pushed to GitHub successfully"
else
    print_status 1 "Failed to push to GitHub"
    echo ""
    echo "Common solutions:"
    echo "1. Check your GitHub username and repository name"
    echo "2. Make sure you have push access to the repository"
    echo "3. Try: git push -u origin main --force (if you're sure)"
    exit 1
fi

echo ""
echo -e "${BLUE}🎯 Next Steps for Deployment...${NC}"
echo "======================================"

echo "Your code is now on GitHub! Next steps:"
echo ""
echo "1. 🌐 Deploy Backend to Render:"
echo "   - Go to https://render.com"
echo "   - Create new Web Service"
echo "   - Connect your GitHub repository"
echo "   - Set build command: pip install -r requirements.txt"
echo "   - Set start command: gunicorn app:app --bind 0.0.0.0:\$PORT"
echo ""
echo "2. 🎨 Deploy Frontend to Vercel:"
echo "   - Go to https://vercel.com"
echo "   - Import your GitHub repository"
echo "   - Set root directory to 'frontend'"
echo "   - Set build command: npm run build"
echo ""
echo "3. 🔗 Connect Frontend to Backend:"
echo "   - Update REACT_APP_API_URL in Vercel with your Render backend URL"
echo ""
echo "📖 For detailed instructions, see: BEGINNER_DEPLOYMENT_GUIDE.md"
echo "📋 For checklist, see: DEPLOYMENT_CHECKLIST.md"

echo ""
echo -e "${GREEN}🎉 Your code is ready for deployment!${NC}"
