"""Tests for resume endpoints."""
import pytest
from httpx import AsyncClient


async def get_auth_token(client: AsyncClient) -> str:
    """Helper to register and get auth token."""
    await client.post(
        "/api/v1/auth/register",
        json={
            "email": "resumetest@example.com",
            "password": "testpassword123",
        },
    )
    response = await client.post(
        "/api/v1/auth/login/json",
        json={
            "email": "resumetest@example.com",
            "password": "testpassword123",
        },
    )
    return response.json()["access_token"]


@pytest.mark.asyncio
async def test_generate_resume(client: AsyncClient):
    """Test resume generation endpoint."""
    token = await get_auth_token(client)

    response = await client.post(
        "/api/v1/resumes/generate",
        json={
            "target_role": "Senior Python Developer",
            "target_company": "Tech Corp",
            "user_experience": "5 years of Python development experience at various startups",
            "user_skills": "Python, FastAPI, Django, PostgreSQL, Docker",
            "user_education": "BS in Computer Science",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert "content" in data
    assert "Senior Python Developer" in data["title"]


@pytest.mark.asyncio
async def test_get_resumes(client: AsyncClient):
    """Test getting resumes list."""
    token = await get_auth_token(client)

    # First generate a resume
    await client.post(
        "/api/v1/resumes/generate",
        json={
            "target_role": "Developer",
            "user_experience": "Experience",
            "user_skills": "Skills",
        },
        headers={"Authorization": f"Bearer {token}"},
    )

    # Get resumes
    response = await client.get(
        "/api/v1/resumes",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0


@pytest.mark.asyncio
async def test_update_resume(client: AsyncClient):
    """Test updating resume content."""
    token = await get_auth_token(client)

    # Generate a resume
    gen_response = await client.post(
        "/api/v1/resumes/generate",
        json={
            "target_role": "Developer",
            "user_experience": "Experience",
            "user_skills": "Skills",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    resume_id = gen_response.json()["id"]

    # Update resume
    response = await client.put(
        f"/api/v1/resumes/{resume_id}",
        json={
            "title": "Updated Resume Title",
            "content": "Updated content",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Resume Title"
