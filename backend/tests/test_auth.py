import pytest

<<<<<<< HEAD

@pytest.mark.asyncio
async def test_register_success(async_client):
    response = await async_client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "testpass123",
            "full_name": "Test User",
            "preferences": {
                "cuisine_preferences": ["Italian"],
                "dietary_restrictions": ["Vegetarian"],
                "allergies": [],
                "cooking_skill_level": "intermediate",
            },
        },
    )
    assert response.status_code == 201  # Changed to 201 for creation


@pytest.mark.asyncio
async def test_login_success(async_client):
    response = await async_client.post(
        "/auth/token", data={"username": "test@example.com", "password": "testpass123"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
=======
@pytest.mark.asyncio
async def test_register_success(async_client):
    response = await async_client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "testpass123",
        "full_name": "Test User",
        "preferences": {
            "cuisine_preferences": ["Italian"],
            "dietary_restrictions": ["Vegetarian"],
            "allergies": [],
            "cooking_skill_level": "intermediate"
        }
    })
    assert response.status_code == 201  # Changed to 201 for creation

@pytest.mark.asyncio
async def test_login_success(async_client):
    response = await async_client.post("/auth/token",
        data={
            "username": "test@example.com",
            "password": "testpass123"
        })
    assert response.status_code == 200
    assert "access_token" in response.json()
>>>>>>> main
