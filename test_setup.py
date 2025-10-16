#!/usr/bin/env python3
"""
Simple test to verify the Playwright setup is working correctly.
"""
import sys
import os

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import playwright
        print("✅ Playwright imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Playwright: {e}")
        return False
    
    try:
        import pytest
        print("✅ Pytest imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import pytest: {e}")
        return False
    
    try:
        from playwright.sync_api import sync_playwright
        print("✅ Playwright sync_api imported successfully")
    except ImportError as e:
        print(f"❌ Failed to import Playwright sync_api: {e}")
        return False
    
    return True

def test_browser_installation():
    """Test that browsers are installed."""
    print("\nTesting browser installation...")
    
    try:
        from playwright.sync_api import sync_playwright
        
        with sync_playwright() as p:
            # Try to launch Chromium
            browser = p.chromium.launch(headless=True)
            browser.close()
            print("✅ Chromium browser is available")
            
            # Try to launch Firefox
            browser = p.firefox.launch(headless=True)
            browser.close()
            print("✅ Firefox browser is available")
            
            # Try to launch WebKit
            browser = p.webkit.launch(headless=True)
            browser.close()
            print("✅ WebKit browser is available")
            
    except Exception as e:
        print(f"❌ Browser test failed: {e}")
        return False
    
    return True

def test_test_structure():
    """Test that test files exist and can be imported."""
    print("\nTesting test structure...")
    
    test_files = [
        "tests/__init__.py",
        "tests/conftest.py",
        "tests/auth/test_authentication.py",
        "tests/tasks/test_task_management.py",
        "tests/ui/test_ui_ux.py",
        "tests/ui/test_navigation.py",
        "tests/utils/helpers.py"
    ]
    
    for test_file in test_files:
        if os.path.exists(test_file):
            print(f"✅ {test_file} exists")
        else:
            print(f"❌ {test_file} missing")
            return False
    
    return True

def test_configuration():
    """Test that configuration files exist."""
    print("\nTesting configuration...")
    
    config_files = [
        "pytest.ini",
        "requirements-test.txt",
        "run_tests.py"
    ]
    
    for config_file in config_files:
        if os.path.exists(config_file):
            print(f"✅ {config_file} exists")
        else:
            print(f"❌ {config_file} missing")
            return False
    
    return True

def main():
    """Run all setup tests."""
    print("🧪 Playwright Test Setup Verification")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_browser_installation,
        test_test_structure,
        test_configuration
    ]
    
    all_passed = True
    
    for test in tests:
        if not test():
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 All setup tests passed! Your Playwright test environment is ready.")
        print("\nNext steps:")
        print("1. Start your applications (frontend and backend)")
        print("2. Run: python run_tests.py")
    else:
        print("💥 Some setup tests failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()





