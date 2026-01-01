import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_404_error(client: AsyncClient):
    response = await client.get("/non-existent-route")
    assert response.status_code == 404
    assert response.json() == {
        "code": "NOT_FOUND",
        "message": "The requested resource was not found",
        "path": "/non-existent-route"
    }
