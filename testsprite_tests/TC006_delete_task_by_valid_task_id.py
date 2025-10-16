import requests

BASE_URL = "http://localhost:5001"
EMAIL = "testuser1@example.com"
PASSWORD = "Testing@123"
LOGIN_URL = f"{BASE_URL}/api/auth/login"
CREATE_TASK_URL = f"{BASE_URL}/api/tasks"
DELETE_TASK_URL_TEMPLATE = f"{BASE_URL}/api/tasks/{{task_id}}"
TIMEOUT = 30

def test_delete_task_by_valid_task_id():
    # Login to get access token
    login_payload = {
        "email": EMAIL,
        "password": PASSWORD
    }
    try:
        login_resp = requests.post(
            LOGIN_URL,
            json=login_payload,
            timeout=TIMEOUT
        )
        login_resp.raise_for_status()
    except requests.RequestException as e:
        assert False, f"Login request failed: {e}"
    login_data = login_resp.json()
    assert "access_token" in login_data, "Access token missing in login response"
    access_token = login_data["access_token"]
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    # Create a task to delete
    create_task_payload = {
        "title": "Test Task for Deletion",
        "description": "Task created for testing deletion endpoint",
        "priority": "Medium",
        "status": "Pending"
    }
    try:
        create_resp = requests.post(
            CREATE_TASK_URL,
            json=create_task_payload,
            headers=headers,
            timeout=TIMEOUT
        )
        create_resp.raise_for_status()
    except requests.RequestException as e:
        assert False, f"Create task request failed: {e}"
    create_data = create_resp.json()
    assert "task" in create_data, "Task data missing in create response"
    task_id = create_data["task"].get("id")
    assert isinstance(task_id, int), "Created task ID is invalid"

    try:
        # Delete the task
        delete_url = DELETE_TASK_URL_TEMPLATE.format(task_id=task_id)
        try:
            delete_resp = requests.delete(
                delete_url,
                headers=headers,
                timeout=TIMEOUT
            )
        except requests.RequestException as e:
            assert False, f"Delete request failed: {e}"

        assert delete_resp.status_code == 200, f"Expected status code 200 on delete but got {delete_resp.status_code}"
        delete_data = delete_resp.json()
        assert "message" in delete_data, "Delete response missing message"

        # Verify the task is actually deleted by trying to delete again or get the task if get endpoint exists
        # Since get task by id endpoint is not specified, we validate delete by expecting 404 on repeat delete
        repeat_delete_resp = requests.delete(
            delete_url,
            headers=headers,
            timeout=TIMEOUT
        )
        assert repeat_delete_resp.status_code == 404, f"Expected status code 404 on deleting already deleted task but got {repeat_delete_resp.status_code}"

    finally:
        # Cleanup: ensure task is deleted in case test failed before delete
        delete_url = DELETE_TASK_URL_TEMPLATE.format(task_id=task_id)
        try:
            requests.delete(
                delete_url,
                headers=headers,
                timeout=TIMEOUT
            )
        except Exception:
            pass  # Ignore cleanup errors

test_delete_task_by_valid_task_id()