import requests
import json

BASE_URL = "http://localhost:8000"

def test_register():
    """Test user registration"""
    url = f"{BASE_URL}/auth/register"
    data = {
        "email": "test@example.com",
        "username": "testuser",
        "password": "password123"
    }
    
    response = requests.post(url, json=data)
    print("\nRegistration Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

def test_login():
    """Test user login"""
    url = f"{BASE_URL}/auth/login"
    data = {
        "username": "test@example.com",
        "password": "password123"
    }
    
    response = requests.post(url, data=data)
    print("\nLogin Response:")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.json()

if __name__ == "__main__":
    print("Testing Authentication Endpoints...")
    
    # Test registration
    register_response = test_register()
    
    # Test login
    login_response = test_login() 