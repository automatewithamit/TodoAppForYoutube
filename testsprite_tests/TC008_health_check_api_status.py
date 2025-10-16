import requests
from requests.auth import HTTPBasicAuth

BASE_URL = "http://localhost:5001"
USERNAME = "TestUser1"
PASSWORD = "Testing@123"

def test_health_check_api_status():
    url = f"{BASE_URL}/api/health"
    try:
        response = requests.get(url, auth=HTTPBasicAuth(USERNAME, PASSWORD), timeout=30)
        response.raise_for_status()
        data = response.json()
        assert response.status_code == 200, f"Expected status code 200, got {response.status_code}"
        assert "status" in data, "Response JSON missing 'status' field"
        assert "message" in data, "Response JSON missing 'message' field"
        assert data["status"].lower() == "healthy" or data["status"].lower() == "ok" or data["status"].lower() == "healthy", f"Unexpected status message: {data['status']}"
    except requests.exceptions.RequestException as e:
        assert False, f"Request to health check API failed: {e}"

test_health_check_api_status()