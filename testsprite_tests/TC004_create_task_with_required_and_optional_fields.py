import requests
from requests.auth import HTTPBasicAuth
from datetime import datetime, timedelta

BASE_URL = "http://localhost:5001"

USERNAME = "testuser1@example.com"
PASSWORD = "Testing@123"

def test_create_task_with_required_and_optional_fields():
    login_url = f"{BASE_URL}/api/auth/login"
    tasks_url = f"{BASE_URL}/api/tasks"
    timeout = 30

    # Step 1: Authenticate to get access token
    try:
        login_payload = {
            "email": USERNAME,
            "password": PASSWORD
        }
        login_resp = requests.post(login_url, json=login_payload, timeout=timeout)
        assert login_resp.status_code == 200, f"Login failed with status code {login_resp.status_code}"
        login_data = login_resp.json()
        access_token = login_data.get("access_token")
        assert access_token, "No access token returned on login"
    except (requests.RequestException, AssertionError) as e:
        raise AssertionError(f"Authentication failed: {e}")

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Prepare task data with mandatory and optional fields
    due_date_iso = (datetime.utcnow() + timedelta(days=7)).replace(microsecond=0).isoformat() + "Z"

    task_payload = {
        "title": "Test Task with optional fields",
        "description": "This is a test task including optional fields",
        "due_date": due_date_iso,
        "priority": "High",
        "status": "Pending",
        "category": "Testing",
        "tags": ["unit-test", "automation"]
    }

    task_id = None
    try:
        # Step 2: Create task request
        create_resp = requests.post(tasks_url, headers=headers, json=task_payload, timeout=timeout)
        assert create_resp.status_code == 201, f"Create task failed with status code {create_resp.status_code}"
        create_data = create_resp.json()

        # Step 3: Validate response content
        assert "message" in create_data and isinstance(create_data["message"], str), "Response missing message field"
        task = create_data.get("task")
        assert task and isinstance(task, dict), "Response missing task data"

        # Validate mandatory title
        assert task.get("title") == task_payload["title"], "Task title does not match payload"

        # Validate optional fields
        assert task.get("description") == task_payload["description"], "Task description mismatch"
        # Due date - allow slight formatting differences, parse and compare
        returned_due_date = task.get("due_date")
        assert returned_due_date is not None, "Task due_date missing"
        # We'll just check that returned_due_date starts with the same date as sent (date+time)
        assert returned_due_date.startswith(due_date_iso[:19]), "Task due_date mismatch"

        assert task.get("priority") == task_payload["priority"], "Task priority mismatch"
        assert task.get("status") == task_payload["status"], "Task status mismatch"
        assert task.get("category") == task_payload["category"], "Task category mismatch"
        assert task.get("tags") == task_payload["tags"], "Task tags mismatch"

        # Validate presence of created_at and updated_at fields
        assert "created_at" in task and isinstance(task["created_at"], str), "Missing created_at"
        assert "updated_at" in task and isinstance(task["updated_at"], str), "Missing updated_at"

        task_id = task.get("id")
        assert isinstance(task_id, int), "Task ID missing or invalid"

    except (requests.RequestException, AssertionError) as e:
        raise AssertionError(f"Create task test failed: {e}")

    finally:
        # Cleanup - delete the created task
        if task_id is not None:
            try:
                delete_resp = requests.delete(f"{tasks_url}/{task_id}", headers=headers, timeout=timeout)
                assert delete_resp.status_code == 200, f"Cleanup delete task failed with status code {delete_resp.status_code}"
            except requests.RequestException:
                pass  # Ignore cleanup errors


test_create_task_with_required_and_optional_fields()
