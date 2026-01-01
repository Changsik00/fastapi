import pytest
from httpx import AsyncClient

# Fixtures removed, using conftest.py fixtures

@pytest.mark.asyncio
async def test_create_item(client: AsyncClient): # Changed type hint to AsyncClient
    response = await client.post("/items/", json={"name": "Test Item", "description": "This is a test item."}) # Added await
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item."
    assert "id" in data

@pytest.mark.asyncio
async def test_read_items(client: AsyncClient): # Changed type hint to AsyncClient
    await client.post("/items/", json={"name": "Item 1", "description": "Desc 1"}) # Added await
    await client.post("/items/", json={"name": "Item 2", "description": "Desc 2"}) # Added await

    response = await client.get("/items/") # Added await
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Item 1"
    assert data[1]["name"] == "Item 2"
    assert "id" in data[0]
    assert "id" in data[1]


@pytest.mark.asyncio
async def test_read_single_item(client: AsyncClient):
    create_response = await client.post("/items/", json={"name": "Single Item", "description": "A unique item"})
    created_item_id = create_response.json()["id"]

    response = await client.get(f"/items/{created_item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Single Item"
    assert data["id"] == created_item_id

@pytest.mark.asyncio
async def test_read_non_existent_item(client: AsyncClient):
    response = await client.get("/items/9999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_item(client: AsyncClient):
    # Create an item first
    create_response = await client.post("/items/", json={"name": "Old Item", "description": "Old description"})
    created_item_id = create_response.json()["id"]

    # Update the item
    update_data = {"name": "Updated Item", "description": "New description"}
    response = await client.put(f"/items/{created_item_id}", json=update_data)
    
    # Now expect 200 and verify content
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["id"] == created_item_id

@pytest.mark.asyncio
async def test_update_non_existent_item(client: AsyncClient):
    update_data = {"name": "Non Existent", "description": "Should not exist"}
    response = await client.put("/items/9999", json=update_data)
    
    # Now expect 404
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_item(client: AsyncClient):
    # Create an item first
    create_response = await client.post("/items/", json={"name": "Item to Delete", "description": "Delete me!"})
    created_item_id = create_response.json()["id"]

    # Delete the item
    response = await client.delete(f"/items/{created_item_id}")
    
    # Now expect 200 and verify message
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}
    
    # Verify the item is actually gone
    get_response = await client.get(f"/items/{created_item_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_non_existent_item(client: AsyncClient):
    response = await client.delete("/items/9999")
    
    # Now expect 404
    assert response.status_code == 404
