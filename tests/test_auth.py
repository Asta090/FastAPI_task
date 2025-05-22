from fastapi.testclient import TestClient
from sqlmodel import Session
from ..models import User
from ..hashing import Hash

def test_create_user(client: TestClient):
    response = client.post(
        "/users/register",
        json={
            "name": "testuser",
            "email": "test@example.com",
            "password": "testpass123"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert data["email"] == "test@example.com"
    assert "password" not in data

def test_login(client: TestClient, test_user: tuple[User, str]):
    user, plain_password = test_user
    response = client.post(
        "/login",
        data={
            "username": user.email,
            "password": plain_password
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"