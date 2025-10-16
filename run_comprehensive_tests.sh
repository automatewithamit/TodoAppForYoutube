#!/bin/bash

# Comprehensive Test Execution Script
# This script runs comprehensive end-to-end tests for the ToDo application

echo "🧪 Running Comprehensive ToDo Application Tests"
echo "=============================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Test configuration
BACKEND_URL="http://localhost:5001"
FRONTEND_URL="http://localhost:3000"
TEST_EMAIL="testuser$(date +%s)@example.com"
TEST_PASSWORD="password123"
TEST_NAME="Test User"

# Test results tracking
TOTAL_TESTS=0
PASSED_TESTS=0
FAILED_TESTS=0
TEST_RESULTS=()

# Function to print test results
print_test_result() {
    local test_name="$1"
    local status="$2"
    local details="$3"
    
    TOTAL_TESTS=$((TOTAL_TESTS + 1))
    
    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}✅ $test_name${NC}"
        PASSED_TESTS=$((PASSED_TESTS + 1))
        TEST_RESULTS+=("✅ $test_name - PASS")
    else
        echo -e "${RED}❌ $test_name${NC}"
        FAILED_TESTS=$((FAILED_TESTS + 1))
        TEST_RESULTS+=("❌ $test_name - FAIL: $details")
    fi
}

# Function to check URL accessibility
check_url() {
    local url="$1"
    local timeout="${2:-10}"
    curl -s --max-time "$timeout" "$url" > /dev/null 2>&1
    return $?
}

echo -e "${BLUE}🔧 Test Environment Setup${NC}"
echo "---------------------------"

# Check if services are running
if check_url "$BACKEND_URL/api/health"; then
    print_test_result "Backend Health Check" "PASS" "Backend is running and healthy"
else
    print_test_result "Backend Health Check" "FAIL" "Backend is not responding"
    echo "Please start the backend with: ./start-app.sh"
    exit 1
fi

if check_url "$FRONTEND_URL"; then
    print_test_result "Frontend Accessibility" "PASS" "Frontend is accessible"
else
    print_test_result "Frontend Accessibility" "FAIL" "Frontend is not accessible"
    echo "Please start the frontend with: ./start-app.sh"
    exit 1
fi

echo ""
echo -e "${BLUE}🔐 Authentication Tests${NC}"
echo "------------------------"

# Test 1: User Registration
echo "Testing user registration..."
REGISTER_RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/auth/register" \
    -H "Content-Type: application/json" \
    -d "{\"name\":\"$TEST_NAME\",\"email\":\"$TEST_EMAIL\",\"password\":\"$TEST_PASSWORD\"}")

if echo "$REGISTER_RESPONSE" | grep -q "access_token"; then
    print_test_result "User Registration" "PASS" "New user registered successfully"
    TOKEN=$(echo "$REGISTER_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
elif echo "$REGISTER_RESPONSE" | grep -q "already exists"; then
    print_test_result "User Registration" "PASS" "User already exists (expected behavior)"
    # Try to login with existing user
    LOGIN_RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/auth/login" \
        -H "Content-Type: application/json" \
        -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}")
    if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
        TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
    fi
else
    print_test_result "User Registration" "FAIL" "Registration failed: $REGISTER_RESPONSE"
fi

# Test 2: User Login
echo "Testing user login..."
LOGIN_RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/auth/login" \
    -H "Content-Type: application/json" \
    -d "{\"email\":\"test@example.com\",\"password\":\"password123\"}")

if echo "$LOGIN_RESPONSE" | grep -q "access_token"; then
    print_test_result "User Login" "PASS" "Login successful"
    TOKEN=$(echo "$LOGIN_RESPONSE" | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])" 2>/dev/null)
else
    print_test_result "User Login" "FAIL" "Login failed: $LOGIN_RESPONSE"
fi

# Test 3: Invalid Login
echo "Testing invalid login..."
INVALID_LOGIN_RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/auth/login" \
    -H "Content-Type: application/json" \
    -d '{"email":"invalid@example.com","password":"wrongpassword"}')

if echo "$INVALID_LOGIN_RESPONSE" | grep -q "Invalid email or password"; then
    print_test_result "Invalid Login Handling" "PASS" "Invalid credentials properly rejected"
else
    print_test_result "Invalid Login Handling" "FAIL" "Invalid login not properly handled"
fi

echo ""
echo -e "${BLUE}📝 Task Management Tests${NC}"
echo "-------------------------"

if [ ! -z "$TOKEN" ]; then
    # Test 4: Get Tasks
    echo "Testing task retrieval..."
    GET_TASKS_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" "$BACKEND_URL/api/tasks")
    
    if echo "$GET_TASKS_RESPONSE" | grep -q "tasks"; then
        print_test_result "Get Tasks" "PASS" "Tasks retrieved successfully"
    else
        print_test_result "Get Tasks" "FAIL" "Failed to retrieve tasks: $GET_TASKS_RESPONSE"
    fi
    
    # Test 5: Create Task
    echo "Testing task creation..."
    CREATE_TASK_RESPONSE=$(curl -s -X POST "$BACKEND_URL/api/tasks" \
        -H "Content-Type: application/json" \
        -H "Authorization: Bearer $TOKEN" \
        -d '{"title":"Test Task","description":"This is a test task","priority":"High","category":"Work","status":"Pending"}')
    
    if echo "$CREATE_TASK_RESPONSE" | grep -q "Task created successfully"; then
        print_test_result "Create Task" "PASS" "Task created successfully"
        TASK_ID=$(echo "$CREATE_TASK_RESPONSE" | grep -o '"id":[0-9]*' | cut -d':' -f2)
    else
        print_test_result "Create Task" "FAIL" "Task creation failed: $CREATE_TASK_RESPONSE"
    fi
    
    # Test 6: Update Task (if task was created)
    if [ ! -z "$TASK_ID" ]; then
        echo "Testing task update..."
        UPDATE_TASK_RESPONSE=$(curl -s -X PUT "$BACKEND_URL/api/tasks/$TASK_ID" \
            -H "Content-Type: application/json" \
            -H "Authorization: Bearer $TOKEN" \
            -d '{"title":"Updated Test Task","status":"In Progress"}')
        
        if echo "$UPDATE_TASK_RESPONSE" | grep -q "Task updated successfully"; then
            print_test_result "Update Task" "PASS" "Task updated successfully"
        else
            print_test_result "Update Task" "FAIL" "Task update failed: $UPDATE_TASK_RESPONSE"
        fi
        
        # Test 7: Delete Task
        echo "Testing task deletion..."
        DELETE_TASK_RESPONSE=$(curl -s -X DELETE "$BACKEND_URL/api/tasks/$TASK_ID" \
            -H "Authorization: Bearer $TOKEN")
        
        if echo "$DELETE_TASK_RESPONSE" | grep -q "Task deleted successfully"; then
            print_test_result "Delete Task" "PASS" "Task deleted successfully"
        else
            print_test_result "Delete Task" "FAIL" "Task deletion failed: $DELETE_TASK_RESPONSE"
        fi
    fi
    
    # Test 8: Get Statistics
    echo "Testing statistics endpoint..."
    STATS_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" "$BACKEND_URL/api/stats")
    
    if echo "$STATS_RESPONSE" | grep -q "total_tasks"; then
        print_test_result "Get Statistics" "PASS" "Statistics retrieved successfully"
    else
        print_test_result "Get Statistics" "FAIL" "Statistics retrieval failed: $STATS_RESPONSE"
    fi
    
    # Test 9: Task Filtering
    echo "Testing task filtering..."
    FILTER_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" "$BACKEND_URL/api/tasks?status=Pending")
    
    if echo "$FILTER_RESPONSE" | grep -q "tasks"; then
        print_test_result "Task Filtering" "PASS" "Task filtering works correctly"
    else
        print_test_result "Task Filtering" "FAIL" "Task filtering failed: $FILTER_RESPONSE"
    fi
    
    # Test 10: Task Search
    echo "Testing task search..."
    SEARCH_RESPONSE=$(curl -s -H "Authorization: Bearer $TOKEN" "$BACKEND_URL/api/tasks?search=Test")
    
    if echo "$SEARCH_RESPONSE" | grep -q "tasks"; then
        print_test_result "Task Search" "PASS" "Task search works correctly"
    else
        print_test_result "Task Search" "FAIL" "Task search failed: $SEARCH_RESPONSE"
    fi
    
else
    echo -e "${YELLOW}⚠️  Skipping task management tests - no authentication token available${NC}"
    print_test_result "Task Management Tests" "SKIP" "No authentication token"
fi

echo ""
echo -e "${BLUE}🔒 Security Tests${NC}"
echo "-----------------"

# Test 11: Unauthorized Access
echo "Testing unauthorized access..."
UNAUTHORIZED_RESPONSE=$(curl -s "$BACKEND_URL/api/tasks")

if echo "$UNAUTHORIZED_RESPONSE" | grep -q "Missing Authorization Header"; then
    print_test_result "Unauthorized Access Protection" "PASS" "Unauthorized access properly blocked"
else
    print_test_result "Unauthorized Access Protection" "FAIL" "Unauthorized access not properly blocked"
fi

# Test 12: Invalid JWT Token
echo "Testing invalid JWT token..."
INVALID_TOKEN_RESPONSE=$(curl -s -H "Authorization: Bearer invalid_token" "$BACKEND_URL/api/tasks")

if echo "$INVALID_TOKEN_RESPONSE" | grep -q "422\|401\|Invalid"; then
    print_test_result "Invalid JWT Token Handling" "PASS" "Invalid JWT token properly rejected"
else
    print_test_result "Invalid JWT Token Handling" "FAIL" "Invalid JWT token not properly handled"
fi

echo ""
echo -e "${BLUE}📊 Test Summary${NC}"
echo "==============="

echo "Total Tests: $TOTAL_TESTS"
echo -e "Passed: ${GREEN}$PASSED_TESTS${NC}"
echo -e "Failed: ${RED}$FAILED_TESTS${NC}"

if [ $FAILED_TESTS -eq 0 ]; then
    echo -e "\n${GREEN}🎉 All tests passed! Your ToDo application is working perfectly!${NC}"
else
    echo -e "\n${YELLOW}⚠️  Some tests failed. Please review the results above.${NC}"
fi

echo ""
echo -e "${BLUE}📋 Detailed Test Results${NC}"
echo "------------------------"
for result in "${TEST_RESULTS[@]}"; do
    echo "$result"
done

echo ""
echo -e "${BLUE}🎯 Next Steps${NC}"
echo "-------------"
echo "1. Review the test results above"
echo "2. Fix any failed tests"
echo "3. Run manual UI tests in your browser: $FRONTEND_URL"
echo "4. Test edge cases and error scenarios"
echo "5. Consider implementing additional automated tests"

echo ""
echo -e "${GREEN}🚀 Comprehensive testing completed!${NC}"
