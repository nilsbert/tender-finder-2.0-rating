import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_standard_relevancy_score(client: AsyncClient):
    """
    Scenario: Standard Relevancy Score Computation
    - Given keywords "AI" (2.0) and "Cloud" (1.5)
    - When I request a rating for "AI Research" and "Cloud based AI"
    - Then total_score should be 2.0*5 + 2.0*3 + 1.5*3 = 10 + 6 + 4.5 = 20.5
    """
    # 1. Setup Keywords
    await client.post("/api/keywords", json={"term": "AI", "weight": 2.0, "type": "Service"})
    await client.post("/api/keywords", json={"term": "Cloud", "weight": 1.5, "type": "Service"})

    # 2. Request Rating
    tender_data = {
        "id": "T-101",
        "title": "AI Research Project",
        "description": "Cloud based AI project in aerospace.",
        "full_text": ""
    }

    response = await client.post("/api/rate", json=tender_data)
    assert response.status_code == 200

    data = response.data if hasattr(response, 'data') else response.json()

    # Calculation:
    # Title: "AI" (2.0) * 5.0 multiplier = 10.0
    # Description: "Cloud" (1.5) * 3.0 = 4.5, "AI" (2.0) * 3.0 = 6.0
    # Total: 10 + 4.5 + 6 = 20.5
    assert data["score"] == 20.5
    assert any(m["term"] == "AI" for m in data["matched_keywords"])
    assert any(m["term"] == "Cloud" for m in data["matched_keywords"])

@pytest.mark.asyncio
async def test_exclusion_logic_precedence(client: AsyncClient):
    """
    Scenario: Exclusion Logic Precedence
    - Given "Catering" (-5.0)
    - When I rate "IT Services" with "Includes Catering"
    - Then score should be negative/reduced
    """
    await client.post("/api/keywords", json={"term": "Catering", "weight": -5.0, "type": "Exclusion"})

    tender_data = {
        "id": "T-102",
        "title": "IT Services",
        "description": "Includes Catering and more.",
    }

    response = await client.post("/api/rate", json=tender_data)
    assert response.status_code == 200
    data = response.json()

    # "Catering" (-5.0) * 3.0 multiplier = -15.0
    assert data["score"] == -15.0
    assert data["matched_keywords"][0]["term"] == "Catering"

@pytest.mark.asyncio
async def test_case_insensitive_matching(client: AsyncClient):
    """Scenario: Case-Insensitive Matching"""
    await client.post("/api/keywords", json={"term": "AI", "weight": 2.0, "type": "Service"})

    response = await client.post("/api/rate", json={
        "id": "T-103", "title": "ai research", "description": ""
    })
    assert response.json()["score"] == 10.0

@pytest.mark.asyncio
async def test_no_double_counting_in_same_location(client: AsyncClient):
    """Scenario: Multiple hits of same keyword in same field only count once"""
    await client.post("/api/keywords", json={"term": "Cloud", "weight": 2.0, "type": "Service"})

    response = await client.post("/api/rate", json={
        "id": "T-104", "title": "Cloud Cloud", "description": "Cloud Cloud Cloud"
    })
    # Title match (1x) + Desc match (1x)
    # 2.0*5 + 2.0*3 = 10 + 6 = 16.0
    assert response.json()["score"] == 16.0
