import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


@pytest.fixture
def client(db_session):
    from app.api.http.controllers.users_controller import router
    from fastapi import FastAPI
    
    app = FastAPI()
    app.include_router(router)
    
    # Override get_db dependency
    from app.infrastructure.db.dependencies import get_db
    app.dependency_overrides[get_db] = lambda: db_session
    
    return TestClient(app)


def test_create_user_success(client, db_session):
    response = client.post("/users", json={"email": "test@example.com", "name": "Test User"})
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["name"] == "Test User"
    assert "id" in data


def test_create_user_duplicate_email(client, db_session):
    # Create first user
    client.post("/users", json={"email": "duplicate@example.com", "name": "User 1"})
    
    # Try to create duplicate
    response = client.post("/users", json={"email": "duplicate@example.com", "name": "User 2"})
    assert response.status_code == 409
    assert "already in use" in response.json()["detail"].lower()


def test_create_user_invalid_email(client, db_session):
    response = client.post("/users", json={"email": "invalid-email", "name": "Test"})
    assert response.status_code == 422  # Pydantic validation error


def test_get_user_success(client, db_session):
    # Create user
    create_response = client.post("/users", json={"email": "get@example.com", "name": "Get User"})
    user_id = create_response.json()["id"]
    
    # Get user
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "get@example.com"


def test_get_user_not_found(client, db_session):
    response = client.get("/users/nonexistent-id")
    assert response.status_code == 404


def test_list_users_default_pagination(client, db_session):
    # Create multiple users
    for i in range(5):
        client.post("/users", json={"email": f"user{i}@example.com", "name": f"User {i}"})
    
    # List users
    response = client.get("/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) <= 10  # Default limit


def test_list_users_with_limit(client, db_session):
    # Create multiple users
    for i in range(15):
        client.post("/users", json={"email": f"limit{i}@example.com", "name": f"User {i}"})
    
    # List with limit
    response = client.get("/users?limit=5")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 5


def test_list_users_with_offset(client, db_session):
    # Create users
    for i in range(10):
        client.post("/users", json={"email": f"offset{i}@example.com", "name": f"User {i}"})
    
    # Get first page
    response1 = client.get("/users?limit=5&offset=0")
    data1 = response1.json()
    
    # Get second page
    response2 = client.get("/users?limit=5&offset=5")
    data2 = response2.json()
    
    # Verify different results
    assert data1[0]["id"] != data2[0]["id"]


def test_list_users_with_email_filter(client, db_session):
    # Create users
    client.post("/users", json={"email": "alice@example.com", "name": "Alice"})
    client.post("/users", json={"email": "bob@example.com", "name": "Bob"})
    client.post("/users", json={"email": "alice2@example.com", "name": "Alice 2"})
    
    # Filter by email
    response = client.get("/users?email_like=alice")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert all("alice" in user["email"] for user in data)


def test_list_users_limit_validation(client, db_session):
    # Test limit too high
    response = client.get("/users?limit=200")
    assert response.status_code == 422
    
    # Test negative limit
    response = client.get("/users?limit=-1")
    assert response.status_code == 422


def test_update_user_success(client, db_session):
    # Create user
    create_response = client.post("/users", json={"email": "update@example.com", "name": "Old Name"})
    user_id = create_response.json()["id"]
    
    # Update user
    response = client.put(f"/users/{user_id}", json={"email": "newemail@example.com", "name": "New Name"})
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newemail@example.com"
    assert data["name"] == "New Name"


def test_update_user_not_found(client, db_session):
    response = client.put("/users/nonexistent-id", json={"email": "test@example.com", "name": "Test"})
    assert response.status_code == 404


def test_delete_user_success(client, db_session):
    # Create user
    create_response = client.post("/users", json={"email": "delete@example.com", "name": "Delete Me"})
    user_id = create_response.json()["id"]
    
    # Delete user
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 204
    
    # Verify deleted
    get_response = client.get(f"/users/{user_id}")
    assert get_response.status_code == 404


def test_delete_user_not_found(client, db_session):
    response = client.delete("/users/nonexistent-id")
    assert response.status_code == 404


def test_get_user_books_empty(client, db_session):
    # Create user
    create_response = client.post("/users", json={"email": "books@example.com", "name": "Book User"})
    user_id = create_response.json()["id"]
    
    # Get books (should be empty)
    response = client.get(f"/users/{user_id}/books")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0
