# tests/test_user.py

import pytest
from httpx import AsyncClient
from app.main import app  # 假设 FastAPI 实例在 app/main.py 中

@pytest.mark.asyncio
async def test_create_user():
    async with AsyncClient(base_url="http://test") as ac:
        response = await ac.post("/creat_user", json={
            "UserId": "testuser123",
            "UserName": "Test User",
            "UserPassword": "123456",
            "UserEmail": "test@example.com"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["UserId"] == "testuser123"

@pytest.mark.asyncio
async def test_get_user():
    async with AsyncClient(base_url="http://test") as ac:
        response = await ac.get("/get_user", params={"user_id": "testuser123"})
        assert response.status_code == 200
        data = response.json()
        assert data["UserId"] == "testuser123"
