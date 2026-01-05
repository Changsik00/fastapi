import pytest
from httpx import AsyncClient




@pytest.mark.asyncio
async def test_change_password_success(client: AsyncClient):
    # 1. Signup
    email = "changepw@example.com"
    password = "oldpassword"
    response = await client.post("/api/v1/auth/signup", json={"email": email, "password": password})
    assert response.status_code == 200
    
    # 2. Login to get token
    login_data = {"username": email, "password": password}
    response = await client.post("/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 3. Change Password
    new_password = "newpassword"
    response = await client.post(
        "/api/v1/auth/password/change",
        headers=headers,
        json={"current_password": password, "new_password": new_password}
    )
    assert response.status_code == 200
    
    # 4. Login with OLD password (should fail)
    response = await client.post("/api/v1/auth/login", data={"username": email, "password": password})
    assert response.status_code == 401
    
    # 5. Login with NEW password (should success)
    response = await client.post("/api/v1/auth/login", data={"username": email, "password": new_password})
    assert response.status_code == 200

@pytest.mark.asyncio
async def test_change_password_wrong_current(client: AsyncClient):
    # 1. Signup & Login
    email = "wrongpw@example.com"
    password = "password"
    await client.post("/api/v1/auth/signup", json={"email": email, "password": password})
    
    login_res = await client.post("/api/v1/auth/login", data={"username": email, "password": password})
    token = login_res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. Change Password with WRONG current
    response = await client.post(
        "/api/v1/auth/password/change",
        headers=headers,
        json={"current_password": "wrong", "new_password": "new"}
    )
    assert response.status_code == 400

@pytest.mark.asyncio
async def test_password_recovery_flow(client: AsyncClient):
    # 1. Signup
    email = "reset@example.com"
    password = "oldpassword"
    await client.post("/api/v1/auth/signup", json={"email": email, "password": password})
    
    # 2. Request Recovery
    response = await client.post("/api/v1/auth/password/recover", json={"email": email})
    assert response.status_code == 200
    
    # DEV ONLY: Extract token from response (Mock Email Workflow)
    fake_token = response.json()["reset_token"]
    
    # 3. Reset Password
    new_password = "newresetpassword"
    response = await client.post(
        "/api/v1/auth/password/reset",
        json={"token": fake_token, "new_password": new_password}
    )
    assert response.status_code == 200
    
    # 4. Login with NEW password
    response = await client.post("/api/v1/auth/login", data={"username": email, "password": new_password})
    assert response.status_code == 200
