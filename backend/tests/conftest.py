import pytest
from fastapi.testclient import TestClient
from app.main import app
from httpx import AsyncClient
import asyncio

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client


@pytest.fixture
async def authenticated_client(async_client):
    response = await async_client.post(
        "/auth/token", data={"username": "test@example.com", "password": "testpass123"}
    )
    token = response.json()["access_token"]
    async_client.headers["Authorization"] = f"Bearer {token}"
    return async_client
