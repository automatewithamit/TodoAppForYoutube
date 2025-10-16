#!/usr/bin/env python3
"""
Test runner script for the ToDo application Playwright tests.
"""
import os
import sys
import subprocess
import argparse
from pathlib import Path


def check_environment():
    """Check if the test environment is properly set up."""
    print("🔍 Checking test environment...")
    
    # Check if virtual environment is activated
    if not hasattr(sys, 'real_prefix') and not (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("⚠️  Warning: Virtual environment not detected. Consider using the test-env virtual environment.")
    
    # Check if required packages are installed
    try:
        import playwright
        import pytest
        print("✅ Required packages are installed")
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install requirements: pip install -r requirements-test.txt")
        return False
    
    # Check if browsers are installed
    try:
        result = subprocess.run(["playwright", "install", "--dry-run"], 
                              capture_output=True, text=True, check=True)
        if "chromium" in result.stdout:
            print("✅ Playwright browsers are installed")
        else:
            print("⚠️  Some browsers may not be installed. Run: playwright install")
    except subprocess.CalledProcessError:
        print("⚠️  Could not verify browser installation")
    
    return True


def check_application_status():
    """Check if the application is running."""
    print("🔍 Checking application status...")
    
    import requests
    
    # Check frontend
    try:
        response = requests.get("http://localhost:3000", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend is running on http://localhost:3000")
        else:
            print(f"⚠️  Frontend returned status code: {response.status_code}")
    except requests.exceptions.RequestException:
        print("❌ Frontend is not running on http://localhost:3000")
        print("Please start the frontend: cd frontend && npm start")
        return False
    
    # Check backend
    try:
        response = requests.get("http://localhost:5001/api/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is running on http://localhost:5001")
        else:
            print(f"⚠️  Backend returned status code: {response.status_code}")
    except requests.exceptions.RequestException:
        print("❌ Backend is not running on http://localhost:5001")
        print("Please start the backend: cd backend && python app.py")
        return False
    
    return True


def run_tests(test_type=None, browser=None, headless=True, parallel=False, verbose=False):
    """Run the Playwright tests."""
    print("🚀 Starting test execution...")
    
    # Create reports directory
    os.makedirs("reports", exist_ok=True)
    os.makedirs("screenshots", exist_ok=True)
    
    # Build pytest command
    cmd = ["python", "-m", "pytest"]
    
    # Add test path
    if test_type:
        cmd.append(f"tests/{test_type}/")
    else:
        cmd.append("tests/")
    
    # Add browser option
    if browser:
        cmd.extend(["--browser", browser])
    
    # Add headless option
    if headless:
        cmd.append("--headed=false")
    else:
        cmd.append("--headed=true")
    
    # Add parallel execution
    if parallel:
        cmd.extend(["-n", "auto"])
    
    # Add verbose output
    if verbose:
        cmd.append("-v")
    
    # Add HTML report
    cmd.extend([
        "--html=reports/report.html",
        "--self-contained-html",
        "--junitxml=reports/junit.xml"
    ])
    
    print(f"Running command: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("✅ All tests passed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Tests failed with exit code: {e.returncode}")
        return False


def main():
    """Main function to run the test suite."""
    parser = argparse.ArgumentParser(description="Run Playwright tests for ToDo application")
    parser.add_argument("--type", choices=["auth", "tasks", "ui"], 
                       help="Run specific test type")
    parser.add_argument("--browser", choices=["chromium", "firefox", "webkit"], 
                       help="Run tests in specific browser")
    parser.add_argument("--headed", action="store_true", 
                       help="Run tests in headed mode (show browser)")
    parser.add_argument("--parallel", action="store_true", 
                       help="Run tests in parallel")
    parser.add_argument("--verbose", "-v", action="store_true", 
                       help="Verbose output")
    parser.add_argument("--skip-checks", action="store_true", 
                       help="Skip environment and application checks")
    
    args = parser.parse_args()
    
    print("🧪 ToDo Application Test Runner")
    print("=" * 50)
    
    # Check environment and application status
    if not args.skip_checks:
        if not check_environment():
            sys.exit(1)
        
        if not check_application_status():
            sys.exit(1)
    
    print("\n" + "=" * 50)
    
    # Run tests
    success = run_tests(
        test_type=args.type,
        browser=args.browser,
        headless=not args.headed,
        parallel=args.parallel,
        verbose=args.verbose
    )
    
    if success:
        print("\n🎉 Test execution completed successfully!")
        print("📊 Check reports/report.html for detailed results")
    else:
        print("\n💥 Test execution failed!")
        print("📊 Check reports/report.html for detailed results")
        sys.exit(1)


if __name__ == "__main__":
    main()





