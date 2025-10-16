import requests

BASE_URL = "http://localhost:5001"
AUTH_EMAIL = "testuser1@example.com"
AUTH_PASSWORD = "Testing@123"
TIMEOUT = 30

def test_get_user_task_statistics_with_valid_token():
    login_url = f"{BASE_URL}/api/auth/login"
    stats_url = f"{BASE_URL}/api/stats"

    # Step 1: Authenticate user to get access token
    login_payload = {
        "email": AUTH_EMAIL,
        "password": AUTH_PASSWORD
    }

    try:
        login_response = requests.post(login_url, json=login_payload, timeout=TIMEOUT)
        assert login_response.status_code == 200, f"Login failed with status code {login_response.status_code}"
        login_data = login_response.json()
        assert "access_token" in login_data and login_data["access_token"], "Access token not found in login response"
        token = login_data["access_token"]

        # Step 2: Request task statistics with valid token
        headers = {
            "Authorization": f"Bearer {token}"
        }
        stats_response = requests.get(stats_url, headers=headers, timeout=TIMEOUT)
        assert stats_response.status_code == 200, f"Statistics request failed with status code {stats_response.status_code}"
        stats = stats_response.json()

        # Validate response fields exist and are of correct type
        required_fields = {
            "total_tasks": int,
            "completed_tasks": int,
            "pending_tasks": int,
            "in_progress_tasks": int,
            "overdue_tasks": int,
            "completion_rate": (float, int)  # can be float or integer number type
        }

        for field, field_type in required_fields.items():
            assert field in stats, f"Missing field '{field}' in statistics response"
            assert isinstance(stats[field], field_type), f"Field '{field}' should be type {field_type} but got {type(stats[field])}"

        # Additional logical checks:
        total = stats["total_tasks"]
        completed = stats["completed_tasks"]
        pending = stats["pending_tasks"]
        in_progress = stats["in_progress_tasks"]
        overdue = stats["overdue_tasks"]

        assert total >= 0, "Total tasks should be non-negative"
        assert completed >= 0, "Completed tasks should be non-negative"
        assert pending >= 0, "Pending tasks should be non-negative"
        assert in_progress >= 0, "In-progress tasks should be non-negative"
        assert overdue >= 0, "Overdue tasks should be non-negative"

        # completion_rate should be between 0 and 100 if percentage, or 0 to 1 if ratio
        completion_rate = stats["completion_rate"]
        assert 0 <= completion_rate <= 100 or 0 <= completion_rate <= 1, "Completion rate should be between 0 and 1 or 0 and 100"

    except requests.RequestException as e:
        assert False, f"Request failed: {e}"


test_get_user_task_statistics_with_valid_token()
