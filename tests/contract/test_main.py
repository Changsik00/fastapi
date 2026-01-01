from fastapi.testclient import TestClient
import sys
import os
import pytest
from httpx import AsyncClient

# Add the src directory to the sys.path to allow for absolute imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# This import will fail initially, which is expected in TDD
from app.main import app

# The client fixture will be provided by pytest-asyncio and httpx
# We no longer need a global client = TestClient(app)

@pytest.mark.asyncio
async def test_read_main(client: AsyncClient):
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the Clean Architecture example!"}
