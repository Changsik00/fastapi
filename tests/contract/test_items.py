import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from src.app.routers.items import router as items_router, get_item_repository
from src.infrastructure.repositories.in_memory_item_repository import InMemoryItemRepository

@pytest.fixture(name="app_fixture")
def app_fixture():
    # Create a fresh FastAPI app instance for each test
    app = FastAPI()
    app.include_router(items_router)
    
    # Create a single, fresh InMemoryItemRepository instance for this test's app lifecycle
    test_repository_instance = InMemoryItemRepository()
    
    # Override the dependency to *always* return this specific instance for this app
    app.dependency_overrides[get_item_repository] = lambda: test_repository_instance
    
    return app

@pytest.fixture(name="client")
def client_fixture(app_fixture: FastAPI):
    with TestClient(app_fixture) as client:
        yield client
    app_fixture.dependency_overrides.clear() # Clear overrides after test

@pytest.mark.asyncio
async def test_create_item(client: TestClient):
    response = client.post("/items/", json={"name": "Test Item", "description": "This is a test item."})
    
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item."
    assert "id" in data

@pytest.mark.asyncio
async def test_read_items(client: TestClient):
    client.post("/items/", json={"name": "Item 1", "description": "Desc 1"})
    client.post("/items/", json={"name": "Item 2", "description": "Desc 2"})

    response = client.get("/items/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "Item 1"
    assert data[1]["name"] == "Item 2"
    assert "id" in data[0]
    assert "id" in data[1]


@pytest.mark.asyncio
async def test_read_single_item(client: TestClient):
    create_response = client.post("/items/", json={"name": "Single Item", "description": "A unique item"})
    created_item_id = create_response.json()["id"]

    response = client.get(f"/items/{created_item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Single Item"
    assert data["id"] == created_item_id

@pytest.mark.asyncio
async def test_read_non_existent_item(client: TestClient):
    response = client.get("/items/9999")
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_update_item(client: TestClient):
    # Create an item first
    create_response = client.post("/items/", json={"name": "Old Item", "description": "Old description"})
    created_item_id = create_response.json()["id"]

    # Update the item
    update_data = {"name": "Updated Item", "description": "New description"}
    response = client.put(f"/items/{created_item_id}", json=update_data)
    
    # Now expect 200 and verify content
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_data["name"]
    assert data["description"] == update_data["description"]
    assert data["id"] == created_item_id

@pytest.mark.asyncio
async def test_update_non_existent_item(client: TestClient):
    update_data = {"name": "Non Existent", "description": "Should not exist"}
    response = client.put("/items/9999", json=update_data)
    
    # Now expect 404
    assert response.status_code == 404

@pytest.mark.asyncio
async def test_delete_item(client: TestClient):
    # Create an item first
    create_response = client.post("/items/", json={"name": "Item to Delete", "description": "Delete me!"})
    created_item_id = create_response.json()["id"]

    # Delete the item
    response = client.delete(f"/items/{created_item_id}")
    
    # Now expect 200 and verify message
    assert response.status_code == 200
    assert response.json() == {"message": "Item deleted successfully"}
    
    # Verify the item is actually gone
    get_response = client.get(f"/items/{created_item_id}")
    assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_delete_non_existent_item(client: TestClient):
    response = client.delete("/items/9999")
    
    # Now expect 404
    assert response.status_code == 404
