# 🛠️ Scripts Reference Guide

This document provides a comprehensive overview of all available scripts in the ToDo application project.

## 📋 Available Scripts

### 🚀 **Development Scripts**

#### `start-app.sh` - Main Development Script
**Purpose**: Starts the complete ToDo application (backend + frontend)
**Usage**: `./start-app.sh`
**What it does**:
- Checks prerequisites (Python, Node.js, npm)
- Clears ports 3000 and 5001
- Sets up backend (virtual environment, dependencies, database)
- Starts Flask backend on port 5001
- Sets up frontend (dependencies)
- Starts React frontend on port 3000
- Provides status updates and URLs

**Features**:
- Automatic dependency installation
- Database initialization
- Health checks for both services
- Graceful shutdown with Ctrl+C

#### `stop.sh` - Stop Application
**Purpose**: Stops all running application processes
**Usage**: `./stop.sh`
**What it does**:
- Stops Flask backend processes
- Stops React frontend processes
- Frees up ports 3000 and 5001
- Provides confirmation of shutdown

#### `status.sh` - Check Application Status
**Purpose**: Check if the application is running
**Usage**: `./status.sh`
**What it does**:
- Checks backend health endpoint
- Checks frontend accessibility
- Shows running processes
- Displays access URLs

### 🧪 **Testing Scripts**

#### `test_application.sh` - Comprehensive Testing
**Purpose**: Run comprehensive tests on the application
**Usage**: `./test_application.sh`
**What it does**:
- Tests backend health check
- Tests frontend accessibility
- Tests user registration and login
- Tests task CRUD operations
- Tests API endpoints
- Tests error handling
- Provides detailed test results

### 🚀 **Deployment Scripts**

#### `prepare-for-deployment.sh` - Deployment Preparation
**Purpose**: Prepares the application for deployment
**Usage**: `./prepare-for-deployment.sh`
**What it does**:
- Checks prerequisites
- Creates environment files
- Installs dependencies
- Tests local build
- Prepares git repository
- Provides deployment checklist

#### `deploy-to-github.sh` - GitHub Deployment
**Purpose**: Pushes code to GitHub for deployment
**Usage**: `./deploy-to-github.sh`
**What it does**:
- Checks git configuration
- Commits all changes
- Pushes to GitHub repository
- Provides next steps for deployment

#### `check-deployment.sh` - Deployment Status
**Purpose**: Checks deployment status and configuration
**Usage**: `./check-deployment.sh`
**What it does**:
- Checks local development status
- Checks production deployment status
- Verifies environment files
- Provides deployment checklist
- Shows quick actions and documentation links

## 🎯 **Quick Start Commands**

### For Development:
```bash
# Start the application
./start-app.sh

# Check status
./status.sh

# Stop the application
./stop.sh

# Test the application
./test_application.sh
```

### For Deployment:
```bash
# Prepare for deployment
./prepare-for-deployment.sh

# Push to GitHub
./deploy-to-github.sh

# Check deployment status
./check-deployment.sh
```

## 📁 **Script Organization**

### ✅ **Kept Scripts (Essential)**
- `start-app.sh` - Main development script
- `stop.sh` - Stop application
- `status.sh` - Status checking
- `test_application.sh` - Comprehensive testing
- `prepare-for-deployment.sh` - Deployment preparation
- `deploy-to-github.sh` - GitHub deployment
- `check-deployment.sh` - Deployment status

### ❌ **Removed Scripts (Redundant)**
- `start.sh` - Basic version, superseded by `start-app.sh`
- `quick-start.sh` - Unnecessary wrapper
- `test-api.sh` - Superseded by `test_application.sh`
- `test-frontend.html` - Manual testing file
- `stop-app.sh` - Simple script, integrated into main workflow

## 🔧 **Script Features**

### **Color-coded Output**
All scripts use consistent color coding:
- 🔵 **Blue**: Information messages
- 🟢 **Green**: Success messages
- 🟡 **Yellow**: Warning messages
- 🔴 **Red**: Error messages

### **Error Handling**
- Prerequisites checking
- Port availability checking
- Process cleanup on exit
- Graceful error messages

### **Cross-platform Compatibility**
- Works on macOS, Linux, and Windows (with WSL)
- Uses standard shell commands
- Handles different package managers

## 🚨 **Troubleshooting**

### Common Issues:

1. **Permission Denied**
   ```bash
   chmod +x script-name.sh
   ```

2. **Port Already in Use**
   ```bash
   ./stop.sh  # Stop existing processes
   ./start-app.sh  # Start fresh
   ```

3. **Dependencies Missing**
   ```bash
   ./prepare-for-deployment.sh  # Install dependencies
   ```

4. **Git Not Configured**
   ```bash
   git config --global user.name "Your Name"
   git config --global user.email "your.email@example.com"
   ```

## 📖 **Related Documentation**

- **`BEGINNER_DEPLOYMENT_GUIDE.md`** - Complete deployment guide
- **`DEPLOYMENT_CHECKLIST.md`** - Deployment checklist
- **`DEPLOYMENT_SUMMARY.md`** - Deployment overview
- **`testsprite_tests/comprehensive_test_report.md`** - Test results

## 🎉 **Benefits of Refactored Scripts**

1. **Simplified**: Removed redundant and complex scripts
2. **Focused**: Each script has a clear, single purpose
3. **Reliable**: Better error handling and cleanup
4. **Maintainable**: Cleaner code and consistent structure
5. **User-friendly**: Clear output and helpful messages

---

**All scripts are now optimized for ease of use and maintenance! 🚀**







