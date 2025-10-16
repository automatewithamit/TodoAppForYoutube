# ToDo Application - Playwright Testing Guide

This document provides a comprehensive guide for running and maintaining the Playwright test suite for the ToDo application.

## 🚀 Quick Start

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Node.js and npm** for the frontend application
3. **Both frontend and backend** applications running

### Setup

1. **Activate the test virtual environment:**
   ```bash
   source test-env/bin/activate
   ```

2. **Install test dependencies:**
   ```bash
   pip install -r requirements-test.txt
   ```

3. **Install Playwright browsers:**
   ```bash
   playwright install
   ```

4. **Start the applications:**
   ```bash
   # Terminal 1 - Backend
   cd backend
   python app.py

   # Terminal 2 - Frontend  
   cd frontend
   npm start
   ```

5. **Run all tests:**
   ```bash
   python run_tests.py
   ```

## 📁 Test Structure

```
tests/
├── __init__.py
├── conftest.py                 # Test configuration and fixtures
├── auth/
│   ├── __init__.py
│   └── test_authentication.py  # Authentication tests
├── tasks/
│   ├── __init__.py
│   └── test_task_management.py # Task management tests
├── ui/
│   ├── __init__.py
│   ├── test_ui_ux.py          # UI/UX tests
│   └── test_navigation.py     # Navigation tests
└── utils/
    ├── __init__.py
    └── helpers.py              # Test utilities and helpers
```

## 🧪 Test Categories

### 1. Authentication Tests (`tests/auth/`)
- User registration with validation
- User login with various scenarios
- Authentication flow and redirects
- Password visibility toggles
- Form validation

### 2. Task Management Tests (`tests/tasks/`)
- Task creation with all field types
- Task editing and updates
- Task deletion
- Task status management
- Search and filtering functionality

### 3. UI/UX Tests (`tests/ui/test_ui_ux.py`)
- Theme toggle functionality
- Responsive design across devices
- Loading states and spinners
- Toast notifications
- Empty states
- Accessibility features
- Error handling

### 4. Navigation Tests (`tests/ui/test_navigation.py`)
- Route protection and authentication guards
- Navigation components
- Page navigation
- Browser navigation (back/forward)
- Deep linking
- Navigation state management

## 🎯 Running Tests

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test Categories
```bash
# Authentication tests only
python run_tests.py --type auth

# Task management tests only
python run_tests.py --type tasks

# UI/UX tests only
python run_tests.py --type ui
```

### Run Tests in Different Browsers
```bash
# Chrome/Chromium (default)
python run_tests.py --browser chromium

# Firefox
python run_tests.py --browser firefox

# Safari/WebKit
python run_tests.py --browser webkit
```

### Run Tests in Headed Mode (Show Browser)
```bash
python run_tests.py --headed
```

### Run Tests in Parallel
```bash
python run_tests.py --parallel
```

### Verbose Output
```bash
python run_tests.py --verbose
```

### Skip Environment Checks
```bash
python run_tests.py --skip-checks
```

## 📊 Test Reports

After running tests, you'll find reports in the `reports/` directory:

- **`reports/report.html`** - Detailed HTML report with screenshots
- **`reports/junit.xml`** - JUnit XML format for CI/CD integration
- **`screenshots/`** - Screenshots taken during test failures

## 🔧 Configuration

### Pytest Configuration (`pytest.ini`)
- Test discovery patterns
- HTML and JUnit report generation
- Custom markers for test categorization
- Verbose output settings

### Test Configuration (`tests/conftest.py`)
- Browser and context setup
- Authentication fixtures
- Test data fixtures
- Environment checks

## 🛠️ Test Utilities

### Helper Functions (`tests/utils/helpers.py`)

#### TestHelpers Class
- `wait_for_element()` - Wait for elements to appear
- `login_user()` - Login with credentials
- `register_user()` - Register new user
- `create_task()` - Create tasks with data
- `edit_task()` - Edit existing tasks
- `delete_task()` - Delete tasks
- `search_tasks()` - Search functionality
- `apply_filters()` - Apply task filters
- `toggle_theme()` - Theme switching

#### AssertHelpers Class
- `assert_task_visible()` - Assert task visibility
- `assert_url_contains()` - Assert URL patterns
- `assert_element_visible()` - Assert element visibility
- `assert_text_visible()` - Assert text presence

## 🎨 Test Data

### Sample Test Data
Tests use consistent test data defined in fixtures:

```python
test_user_data = {
    "name": "Test User",
    "email": "test@example.com", 
    "password": "password123"
}

sample_task_data = {
    "title": "Test Task",
    "description": "This is a test task description",
    "priority": "High",
    "category": "Work",
    "tags": ["test", "automation"]
}
```

## 🐛 Debugging Tests

### Running Individual Tests
```bash
# Run specific test file
python -m pytest tests/auth/test_authentication.py

# Run specific test method
python -m pytest tests/auth/test_authentication.py::TestUserRegistration::test_successful_registration

# Run with verbose output
python -m pytest tests/auth/test_authentication.py -v
```

### Debug Mode
```bash
# Run in headed mode to see browser
python run_tests.py --headed

# Run with slow motion
# Edit conftest.py and set slow_mo=2000 in browser fixture
```

### Screenshots and Videos
- Screenshots are automatically taken on test failures
- Check the `screenshots/` directory
- Videos can be enabled by adding `video="retain-on-failure"` to browser context

## 🔄 Continuous Integration

### GitHub Actions Example
```yaml
name: Playwright Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r requirements-test.txt
        playwright install
    - name: Run tests
      run: python run_tests.py --browser chromium
```

## 📝 Writing New Tests

### Test Structure
```python
import pytest
from playwright.sync_api import Page, expect
from tests.utils.helpers import TestHelpers, AssertHelpers

class TestNewFeature:
    """Test new feature functionality."""
    
    def test_feature_behavior(self, authenticated_page: Page):
        """Test specific feature behavior."""
        page = authenticated_page
        
        # Test steps
        page.click("button")
        page.fill("input", "value")
        
        # Assertions
        expect(page.locator("text=Expected Result")).to_be_visible()
```

### Best Practices
1. **Use descriptive test names** that explain what is being tested
2. **Group related tests** in classes
3. **Use fixtures** for common setup
4. **Add proper assertions** with meaningful error messages
5. **Clean up test data** when necessary
6. **Use page object pattern** for complex interactions

## 🚨 Troubleshooting

### Common Issues

1. **"Application not running" error**
   - Ensure both frontend (port 3000) and backend (port 5001) are running
   - Check firewall settings

2. **"Browser not found" error**
   - Run `playwright install` to install browsers
   - Check browser installation: `playwright install --dry-run`

3. **Tests timing out**
   - Increase timeout values in test helpers
   - Check application performance
   - Verify network connectivity

4. **Flaky tests**
   - Add proper waits for elements
   - Use `wait_for_selector()` instead of `click()`
   - Check for race conditions

### Environment Issues
- **Python version**: Ensure Python 3.8+ is used
- **Virtual environment**: Always use the test-env virtual environment
- **Dependencies**: Keep requirements-test.txt updated

## 📈 Performance Testing

### Load Testing
```python
# Example of testing with multiple users
@pytest.mark.parametrize("user_count", [1, 5, 10])
def test_concurrent_users(authenticated_page: Page, user_count):
    # Test with multiple concurrent users
    pass
```

### Performance Monitoring
- Monitor test execution times
- Track memory usage during tests
- Check for memory leaks in long-running tests

## 🔐 Security Testing

### Authentication Security
- Test for SQL injection in forms
- Verify JWT token handling
- Test session management
- Check for XSS vulnerabilities

### Data Validation
- Test input sanitization
- Verify server-side validation
- Test file upload security (if applicable)

## 📚 Additional Resources

- [Playwright Documentation](https://playwright.dev/python/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Playwright Best Practices](https://playwright.dev/python/docs/best-practices)

## 🤝 Contributing

When adding new tests:

1. Follow the existing test structure
2. Add appropriate test markers
3. Update this documentation
4. Ensure tests are reliable and fast
5. Add proper error handling

## 📞 Support

For issues with the test suite:
1. Check this documentation
2. Review test logs and reports
3. Check application logs
4. Verify environment setup
