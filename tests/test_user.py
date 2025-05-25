import pytest
import httpx

@pytest.mark.asyncio
async def test_create_user():
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000/api/v1") as client:
        response = await client.post("/Signup/creat_user", json={
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
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000/api/v1") as client:
        response = await client.get("/Signup/get_user", params={"user_id": "testuser123"})
    assert response.status_code == 200
    data = response.json()
    assert data["UserId"] == "testuser123"
