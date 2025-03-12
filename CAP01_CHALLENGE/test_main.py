import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_register():
    response = client.post("/register?username=testuser&password=testpass")
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_register_existing_user():
    client.post("/register?username=testuser&password=testpass")
    response = client.post("/register?username=testuser&password=testpass")
    assert response.status_code == 400
    assert response.json() == {"detail": "El usuario ya existe"}

def test_login():
    client.post("/register?username=testuser&password=testpass")
    response = client.post("/login?username=testuser&password=testpass")
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_bubble_sort():
    client.post("/register?username=testuser&password=testpass")
    login_response = client.post("/login?username=testuser&password=testpass")
    token = login_response.json()["access_token"]
    response = client.post("/bubble-sort?token=" + token, json={"numbers": [5, 3, 8, 6, 2]})
    assert response.status_code == 200
    assert response.json() == {"numbers": [2, 3, 5, 6, 8]}

def test_filter_even():
    client.post("/register?username=testuser&password=testpass")
    login_response = client.post("/login?username=testuser&password=testpass")
    token = login_response.json()["access_token"]
    response = client.post("/filter-even?token=" + token, json={"numbers": [5, 3, 8, 6, 2]})
    assert response.status_code == 200
    assert response.json() == {"even_numbers": [8, 6, 2]}

def test_sum_elements():
    client.post("/register?username=testuser&password=testpass")
    login_response = client.post("/login?username=testuser&password=testpass")
    token = login_response.json()["access_token"]
    response = client.post("/sum-elements?token=" + token, json={"numbers": [5, 3, 8, 6, 2]})
    assert response.status_code == 200
    assert response.json() == {"sum": 24}

def test_max_value():
    client.post("/register?username=testuser&password=testpass")
    login_response = client.post("/login?username=testuser&password=testpass")
    token = login_response.json()["access_token"]
    response = client.post("/max-value?token=" + token, json={"numbers": [5, 3, 8, 6, 2]})
    assert response.status_code == 200
    assert response.json() == {"max": 8}

def test_binary_search():
    client.post("/register?username=testuser&password=testpass")
    login_response = client.post("/login?username=testuser&password=testpass")
    token = login_response.json()["access_token"]
    response = client.post("/binary-search?token=" + token, json={"numbers": [2, 3, 5, 6, 8], "target": 6})
    assert response.status_code == 200
    assert response.json() == {"found": True, "index": 3}
