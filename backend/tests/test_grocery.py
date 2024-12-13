import pytest


@pytest.mark.asyncio
async def test_gmail_auth(authenticated_client):
    response = await authenticated_client.post("/gmail-auth")
    assert response.status_code == 200
    assert "message" in response.json()


@pytest.mark.asyncio
async def test_fetch_emails(authenticated_client):
    response = await authenticated_client.get("/grocery/fetch-emails")
    assert response.status_code == 200
    assert "emails_data" in response.json()
