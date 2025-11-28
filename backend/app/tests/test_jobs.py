"""Tests for job endpoints."""
import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient) -> str:
    """Helper to register and get auth token."""
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "jobtest@example.com",
            "password": "testpassword123",
            "skills": "Python,JavaScript,React",
            "keywords": "remote,startup",
        },
    )
    response = await client.post(
        "/api/v1/auth/login/json",
        json={
            "email": "jobtest@example.com",
            "password": "testpassword123",
        },
    )
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_search_jobs(client: AsyncClient):
    """Test job search endpoint."""
    token = await get_auth_token(client)

    response = await client.post(
        "/api/v1/jobs/search",
        json={
            "query": "Python Developer",
            "location": "Remote",
            "sources": ["mock"],
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert "title" in data[0]
    assert "match_score" in data[0]


@pytest.mark.asyncio
async def test_get_jobs(client: AsyncClient):
    """Test getting jobs list."""
    token = await get_auth_token(client)

    # First search for jobs
    await client.post(
        "/api/v1/jobs/search",
        json={"query": "Developer"},
        headers={"Authorization": f"Bearer {token}"},
    )

    # Get jobs
    response = await client.get(
        "/api/v1/jobs",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


@pytest.mark.asyncio
async def test_update_job_status(client: AsyncClient):
    """Test updating job status."""
    token = await get_auth_token(client)

    # Search for jobs
    search_response = await client.post(
        "/api/v1/jobs/search",
        json={"query": "Developer"},
        headers={"Authorization": f"Bearer {token}"},
    )
    job_id = search_response.json()[0]["id"]

    # Update status
    response = await client.patch(
        f"/api/v1/jobs/{job_id}",
        json={"status": "applied"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["status"] == "applied"


@pytest.mark.asyncio
async def test_unauthorized_access(client: AsyncClient):
    """Test accessing jobs without authentication."""
    response = await client.get("/api/v1/jobs")
    assert response.status_code == 401
