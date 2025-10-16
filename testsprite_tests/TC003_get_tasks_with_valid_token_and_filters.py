import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost:5001"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
TASKS_URL = f"{BASE_URL}/api/tasks"
TIMEOUT = 30

def test_get_tasks_with_valid_token_and_filters():
    # Step 1: Login to get access token
    login_payload = {
        "email": "testuser1@example.com",    # Corrected to a valid email format
        "password": "Testing@123"
    }
    try:
        login_response = requests.post(
            LOGIN_URL,
            json=login_payload,
            timeout=TIMEOUT
        )
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"
        login_data = login_response.json()
        access_token = login_data.get("access_token")
        assert access_token, "No access token returned on login"
    except Exception as e:
        assert False, f"Exception during login: {e}"

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Define a set of filters to test
    filters_list = [
        {"status": "Pending"},
        {"category": "Work"},
        {"priority": "High"},
        {"search": "report"},
        {"status": "Completed", "category": "Home"},
        {"priority": "Low", "search": "shopping"},
        {"status": "In Progress", "category": "Work", "priority": "Medium", "search": "project"},
    ]

    for filters in filters_list:
        try:
            response = requests.get(
                TASKS_URL,
                headers=headers,
                params=filters,
                timeout=TIMEOUT
            )
            assert response.status_code == 200, f"Failed to get tasks with filters {filters}: {response.status_code} - {response.text}"

            data = response.json()
            tasks = data.get("tasks")
            assert isinstance(tasks, list), f"Tasks is not a list with filters {filters}"

            # If tasks returned, validate that each task meets filter criteria if possible
            for task in tasks:
                # Validate type and essential fields presence
                assert "id" in task and isinstance(task["id"], int)
                assert "title" in task and isinstance(task["title"], str)
                assert "status" in task and isinstance(task["status"], str)
                assert "category" in task and isinstance(task["category"], str)
                assert "priority" in task and isinstance(task["priority"], str)
                assert "description" in task and isinstance(task["description"], str)
                assert "tags" in task and isinstance(task["tags"], list)

                # Check filters match if filter is set and value present
                if "status" in filters:
                    assert filters["status"].lower() == task["status"].lower(), f"Status filter mismatch: expected {filters['status']} got {task['status']}"
                if "category" in filters:
                    assert filters["category"].lower() == task["category"].lower(), f"Category filter mismatch: expected {filters['category']} got {task['category']}"
                if "priority" in filters:
                    assert filters["priority"].lower() == task["priority"].lower(), f"Priority filter mismatch: expected {filters['priority']} got {task['priority']}"
                if "search" in filters:
                    # Search should match either title or description (case insensitive)
                    search_term = filters["search"].lower()
                    title = task["title"].lower()
                    description = task["description"].lower()
                    assert search_term in title or search_term in description, f"Search term '{filters['search']}' not found in title or description"
        except Exception as e:
            assert False, f"Exception fetching tasks with filters {filters}: {e}"

test_get_tasks_with_valid_token_and_filters()
