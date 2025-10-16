import requests

def test_user_login_with_valid_credentials():
    base_url = "http://localhost:5001"
    login_endpoint = f"{base_url}/api/auth/login"
    
    payload = {
        "email": "testuser1@example.com",
        "password": "Testing@123"
    }
    headers = {
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(login_endpoint, json=payload, headers=headers, timeout=30)
    except requests.RequestException as e:
        assert False, f"Request failed: {e}"

    assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"

    try:
        data = response.json()
    except ValueError:
        assert False, "Response is not in JSON format"

    assert "access_token" in data, "Response JSON does not contain access_token"
    assert isinstance(data["access_token"], str) and data["access_token"], "access_token is empty or not a string"

    user = data.get("user")
    assert user is not None, "Response JSON does not contain user object"
    assert isinstance(user, dict), "user field is not an object"
    assert "id" in user and isinstance(user["id"], int), "User id missing or not int"
    assert "name" in user and isinstance(user["name"], str), "User name missing or not string"
    assert "email" in user and isinstance(user["email"], str), "User email missing or not string"
    assert user["email"].lower() == payload["email"].lower(), "User email in response does not match login email"

    assert "message" in data and isinstance(data["message"], str) and data["message"], "Response message is missing or empty"

test_user_login_with_valid_credentials()