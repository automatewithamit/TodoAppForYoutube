import requests
from datetime import datetime

BASE_URL = "http://localhost:5001"
EMAIL = "testuser1@example.com"
PASSWORD = "Testing@123"
TIMEOUT = 30

def parse_datetime(dt_str):
    # Try parsing the date-time string in known ISO formats
    for fmt in ("%Y-%m-%dT%H:%M:%SZ", "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S%z", "%Y-%m-%dT%H:%M:%S.%f%z"):
        try:
            return datetime.strptime(dt_str, fmt)
        except (ValueError, TypeError):
            continue
    # If all fail, raise error
    raise ValueError(f"Unknown datetime format: {dt_str}")

def test_update_existing_task_with_valid_data():
    # Login to get access token
    login_url = f"{BASE_URL}/api/auth/login"
    login_payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    try:
        login_resp = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
        assert login_resp.status_code == 200, f"Login failed with status {login_resp.status_code}"
        login_data = login_resp.json()
        access_token = login_data.get("access_token")
        assert access_token, "No access token returned on login"

        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        # Create a new task to update later
        create_task_url = f"{BASE_URL}/api/tasks"
        create_payload = {
            "title": "Initial Title for Update Test",
            "description": "Initial description",
            "due_date": "2025-12-31T23:59:59Z",
            "priority": "Medium",
            "status": "Pending",
            "category": "Testing",
            "tags": ["update", "test"]
        }
        create_resp = requests.post(create_task_url, json=create_payload, headers=headers, timeout=TIMEOUT)
        assert create_resp.status_code == 201, f"Task creation failed with status {create_resp.status_code}"
        create_data = create_resp.json()
        task = create_data.get("task")
        assert task, "No task object in create response"
        task_id = task.get("id")
        assert task_id is not None, "No task ID returned"

        # Prepare update payload with valid data
        update_payload = {
            "title": "Updated Title for Task",
            "description": "Updated description of the task",
            "due_date": "2026-01-15T12:00:00Z",
            "priority": "High",
            "status": "In Progress",
            "category": "Updated Testing",
            "tags": ["updated", "important"]
        }

        update_task_url = f"{BASE_URL}/api/tasks/{task_id}"
        update_resp = requests.put(update_task_url, json=update_payload, headers=headers, timeout=TIMEOUT)
        assert update_resp.status_code == 200, f"Task update failed with status {update_resp.status_code}"
        update_data = update_resp.json()

        # Validate response contains updated task details
        updated_task = update_data.get("task")
        assert updated_task, "No task object in update response"
        assert updated_task.get("id") == task_id, "Updated task ID mismatch"
        assert updated_task.get("title") == update_payload["title"], "Title not updated correctly"
        assert updated_task.get("description") == update_payload["description"], "Description not updated correctly"

        # Compare due_date via datetime equality
        expected_due_date = parse_datetime(update_payload["due_date"])
        actual_due_date = parse_datetime(updated_task.get("due_date"))
        assert expected_due_date == actual_due_date, "Due date not updated correctly"

        assert updated_task.get("priority") == update_payload["priority"], "Priority not updated correctly"
        assert updated_task.get("status") == update_payload["status"], "Status not updated correctly"
        assert updated_task.get("category") == update_payload["category"], "Category not updated correctly"
        assert updated_task.get("tags") == update_payload["tags"], "Tags not updated correctly"

    finally:
        # Cleanup - delete the created task if it exists
        if 'task_id' in locals() and task_id is not None:
            delete_url = f"{BASE_URL}/api/tasks/{task_id}"
            try:
                delete_resp = requests.delete(delete_url, headers={"Authorization": f"Bearer {access_token}"}, timeout=TIMEOUT)
                # It's okay if delete fails, just attempt cleanup
            except Exception:
                pass


test_update_existing_task_with_valid_data()
