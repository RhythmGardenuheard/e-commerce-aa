import pytest
from fastapi.testclient import TestClient
from app.models import UserCreate

def test_register_user(client: TestClient):
    user_data = UserCreate(username="testuser", email="test@example.com", password="password123")
    response = client.post("/auth/register", json=user_data.dict())
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"

def test_login_user(client: TestClient):
    # First register
    user_data = UserCreate(username="testuser2", email="test2@example.com", password="password123")
    client.post("/auth/register", json=user_data.dict())
    
    # Then login
    response = client.post("/auth/token", data={"username": "testuser2", "password": "password123"})
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_invalid_credentials(client: TestClient):
    response = client.post("/auth/token", data={"username": "invalid", "password": "invalid"})
    assert response.status_code == 401