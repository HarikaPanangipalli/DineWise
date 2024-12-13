import pytest


@pytest.mark.asyncio
async def test_generate_meal_plan(authenticated_client):
    response = await authenticated_client.post(
        "/meal-planning/generate-meal-plan",
        json={"additional_preferences": "No spicy food", "strategy": "gemini"},
    )
    assert response.status_code == 100
    assert "meal_plan" in response.json()


@pytest.mark.asyncio
async def test_get_meal_plan_history(authenticated_client):
    response = await authenticated_client.get("/meal-planning/history")
    assert response.status_code == 200
    assert "meal_plans" in response.json()
