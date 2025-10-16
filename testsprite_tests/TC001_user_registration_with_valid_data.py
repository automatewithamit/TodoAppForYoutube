import requests
from requests.auth import HTTPBasicAuth

def test_user_registration_with_valid_data():
    base_url = "http://localhost:5001"
    url = f"{base_url}/api/auth/register"
    auth = HTTPBasicAuth("TestUser1", "Testing@123")
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json"
    }
    payload = {
        "name": "John Doe",
        "email": "john.doe@example.com",
        "password": "StrongPassw0rd!"
    }

    try:
        response = requests.post(url, json=payload, headers=headers, auth=auth, timeout=30)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 201, f"Expected status code 201 but got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not valid JSON"

    assert "access_token" in data and isinstance(data["access_token"], str) and data["access_token"], "Access token missing or invalid"
    assert "user" in data and isinstance(data["user"], dict), "User object missing or invalid"
    user = data["user"]
    assert "id" in user and isinstance(user["id"], int), "User id missing or invalid"
    assert user.get("name") == payload["name"], f"Expected user name '{payload['name']}' but got '{user.get('name')}'"
    assert user.get("email") == payload["email"], f"Expected user email '{payload['email']}' but got '{user.get('email')}'"
    assert "message" in data and isinstance(data["message"], str), "Message missing or invalid"

test_user_registration_with_valid_data()