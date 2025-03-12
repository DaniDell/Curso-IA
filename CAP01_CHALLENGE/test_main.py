import pytest
from fastapi.testclient import TestClient
from main import app, fake_db, get_password_hash

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_and_teardown():
    # Setup: clear the fake_db before each test
    fake_db["users"].clear()
    yield
    # Teardown: clear the fake_db after each test
    fake_db["users"].clear()

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI application!"}

def test_register():
    response = client.post("/register", params={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert response.json() == {"message": "User registered successfully"}

def test_register_existing_user():
    fake_db["users"]["testuser"] = get_password_hash("testpass")
    response = client.post("/register", params={"username": "testuser", "password": "testpass"})
    assert response.status_code == 400
    assert response.json() == {"detail": "El usuario ya existe"}

def test_login():
    fake_db["users"]["testuser"] = get_password_hash("testpass")
    response = client.post("/login", params={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_login_invalid_credentials():
    response = client.post("/login", params={"username": "testuser", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Credenciales inválidas"}

def test_bubble_sort():
    fake_db["users"]["testuser"] = get_password_hash("testpass")
    login_response = client.post("/login", params={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    response = client.post("/bubble-sort", json={"numbers": [5, 3, 8, 4, 2]}, params={"token": token})
    assert response.status_code == 200
    assert response.json() == {"numbers": [2, 3, 4, 5, 8]}

def test_filter_even():
    fake_db["users"]["testuser"] = get_password_hash("testpass")
    login_response = client.post("/login", params={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    response = client.post("/filter-even", json={"numbers": [1, 2, 3, 4, 5, 6]}, params={"token": token})
    assert response.status_code == 200
    assert response.json() == {"even_numbers": [2, 4, 6]}

def test_sum_elements():
    fake_db["users"]["testuser"] = get_password_hash("testpass")
    login_response = client.post("/login", params={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    response = client.post("/sum-elements", json={"numbers": [1, 2, 3, 4, 5]}, params={"token": token})
    assert response.status_code == 200
    assert response.json() == {"sum": 15}

def test_max_value():
    fake_db["users"]["testuser"] = get_password_hash("testpass")
    login_response = client.post("/login", params={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    response = client.post("/max-value", json={"numbers": [1, 2, 3, 4, 5]}, params={"token": token})
    assert response.status_code == 200
    assert response.json() == {"max": 5}

def test_binary_search():
    fake_db["users"]["testuser"] = get_password_hash("testpass")
    login_response = client.post("/login", params={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    response = client.post("/binary-search", json={"numbers": [1, 2, 3, 4, 5], "target": 3}, params={"token": token})
    assert response.status_code == 200
    assert response.json() == {"found": True, "index": 2}

def test_binary_search_not_found():
    fake_db["users"]["testuser"] = get_password_hash("testpass")
    login_response = client.post("/login", params={"username": "testuser", "password": "testpass"})
    token = login_response.json()["access_token"]
    response = client.post("/binary-search", json={"numbers": [1, 2, 3, 4, 5], "target": 6}, params={"token": token})
    assert response.status_code == 200
    assert response.json() == {"found": False, "index": -1}
