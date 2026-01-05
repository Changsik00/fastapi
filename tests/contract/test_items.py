import pytest
from httpx import AsyncClient
from app.main import app
from app.api.deps import get_current_user
from app.domain.models.user import User, UserRole

# Fixtures removed, using conftest.py fixtures

# Fixtures removed, using conftest.py fixtures

@pytest.fixture(autouse=True)
def override_auth():
    mock_user = User(
        id=1,
        email="test@example.com", 
        hashed_password="hashed_pw",
        role=UserRole.USER,
        is_active=True
    )
    app.dependency_overrides[get_current_user] = lambda: mock_user
    yield
    # Overrides are cleared by conftest.py's client fixture, 
    # but strictly we could pop it here. 
    # Let's rely on conftest for clean slate to avoid race conditions in parallel tests if any.

@pytest.mark.asyncio
async def test_create_item(client: AsyncClient): # Changed type hint to AsyncClient
    response = await client.post("/api/v1/items/", json={"name": "Test Item", "description": "This is a test item."}) # Added await
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item."
    assert "id" in data

@pytest.mark.asyncio
async def test_read_items(client: AsyncClient): # Changed type hint to AsyncClient
    await client.post("/api/v1/items/", json={"name": "Item 1", "description": "Desc 1"}) # Added await
    await client.post("/api/v1/items/", json={"name": "Item 2", "description": "Desc 2"}) # Added await

    response = await client.get("/api/v1/items/") # Added await
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Item 1"
    assert data[1]["name"] == "Item 2"
    assert "id" in data[0]
    assert "id" in data[1]


@pytest.mark.asyncio
async def test_read_single_item(client: AsyncClient):
    create_response = await client.post("/api/v1/items/", json={"name": "Single Item", "description": "A unique item"})
    created_item_id = create_response.json()["id"]

    response = await client.get(f"/api/v1/items/{created_item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Single Item"
    assert data["id"] == created_item_id

@pytest.mark.asyncio
async def test_read_non_existent_item(client: AsyncClient):
    response = await client.get("/api/v1/items/9999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_item(client: AsyncClient):
    # Create an item first
    create_response = await client.post("/api/v1/items/", json={"name": "Old Item", "description": "Old description"})
    created_item_id = create_response.json()["id"]

    # Update the item
    update_data = {"name": "Updated Item", "description": "New description"}
    response = await client.put(f"/api/v1/items/{created_item_id}", json=update_data)
    
    # Now expect 200 and verify content
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["id"] == created_item_id

@pytest.mark.asyncio
async def test_update_non_existent_item(client: AsyncClient):
    update_data = {"name": "Non Existent", "description": "Should not exist"}
    response = await client.put("/api/v1/items/9999", json=update_data)
    
    # Now expect 404
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient):
    # Create an item first
    create_response = await client.post("/api/v1/items/", json={"name": "Item to Delete", "description": "Delete me!"})
    created_item_id = create_response.json()["id"]

    # Delete the item
    response = await client.delete(f"/api/v1/items/{created_item_id}")
    
    # Now expect 200 and verify message
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}
    
    # Verify the item is actually gone
    get_response = await client.get(f"/api/v1/items/{created_item_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_non_existent_item(client: AsyncClient):
    response = await client.delete("/api/v1/items/9999")
    
    # Now expect 404
    assert response.status_code == 404
