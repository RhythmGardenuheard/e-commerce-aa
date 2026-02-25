import pytest
from fastapi.testclient import TestClient
from app.models import ProductCreate

def test_create_product(client: TestClient):
    # First login to get token
    user_data = {"username": "testuser", "password": "password123"}
    login_response = client.post("/auth/token", data=user_data)
    token = login_response.json()["access_token"]
    
    product_data = ProductCreate(name="Test Product", description="A test product", price=10.99, stock=100)
    response = client.post("/api/products", json=product_data.dict(), headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Product"

def test_get_products(client: TestClient):
    # Login
    user_data = {"username": "testuser", "password": "password123"}
    login_response = client.post("/auth/token", data=user_data)
    token = login_response.json()["access_token"]
    
    response = client.get("/api/products", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_product(client: TestClient):
    # Login
    user_data = {"username": "testuser", "password": "password123"}
    login_response = client.post("/auth/token", data=user_data)
    token = login_response.json()["access_token"]
    
    # Create product first
    product_data = ProductCreate(name="Test Product", description="A test product", price=10.99, stock=100)
    create_response = client.post("/api/products", json=product_data.dict(), headers={"Authorization": f"Bearer {token}"})
    product_id = create_response.json()["id"]
    
    response = client.get(f"/api/products/{product_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id

def test_update_product(client: TestClient):
    # Login
    user_data = {"username": "testuser", "password": "password123"}
    login_response = client.post("/auth/token", data=user_data)
    token = login_response.json()["access_token"]
    
    # Create product
    product_data = ProductCreate(name="Test Product", description="A test product", price=10.99, stock=100)
    create_response = client.post("/api/products", json=product_data.dict(), headers={"Authorization": f"Bearer {token}"})
    product_id = create_response.json()["id"]
    
    # Update
    update_data = ProductCreate(name="Updated Product", description="Updated", price=15.99, stock=50)
    response = client.put(f"/api/products/{product_id}", json=update_data.dict(), headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Product"

def test_delete_product(client: TestClient):
    # Login
    user_data = {"username": "testuser", "password": "password123"}
    login_response = client.post("/auth/token", data=user_data)
    token = login_response.json()["access_token"]
    
    # Create product
    product_data = ProductCreate(name="Test Product", description="A test product", price=10.99, stock=100)
    create_response = client.post("/api/products", json=product_data.dict(), headers={"Authorization": f"Bearer {token}"})
    product_id = create_response.json()["id"]
    
    # Delete
    response = client.delete(f"/api/products/{product_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    
    # Check if deleted
    get_response = client.get(f"/api/products/{product_id}", headers={"Authorization": f"Bearer {token}"})
    assert get_response.status_code == 404