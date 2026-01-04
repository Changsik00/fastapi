import pytest
from httpx import AsyncClient
from app.domain.models.user import UserRole

@pytest.mark.asyncio
async def test_signup_flow(client: AsyncClient):
    # 1. Signup
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "newuser@example.com", "password": "newpassword", "role": "user"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "newuser@example.com"
    assert data["role"] == "user"
    assert "id" in data

    # 2. Signup (Duplicate)
    response = await client.post(
        "/api/v1/auth/signup",
        json={"email": "newuser@example.com", "password": "newpassword", "role": "user"}
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_login_flow(client: AsyncClient):
    # 0. Setup User
    await client.post(
        "/api/v1/auth/signup",
        json={"email": "loginuser@example.com", "password": "loginpassword"}
    )

    # 1. Login (Success)
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "loginuser@example.com", "password": "loginpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

    # 2. Login (Wrong Password)
    response = await client.post(
        "/api/v1/auth/login",
        data={"username": "loginuser@example.com", "password": "wrongpassword"}
    )
    assert response.status_code == 401
