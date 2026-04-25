import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_keyword_crud_lifecycle(client: AsyncClient):
    """Scenario: Full Keyword CRUD Lifecycle"""

    # 1. Create
    new_kw = {"term": "Blockchain", "weight": 4.0, "type": "Service"}
    resp = await client.post("/api/keywords", json=new_kw)
    assert resp.status_code == 201
    created = resp.json()
    assert created["term"] == "Blockchain"
    kw_id = created["id"]

    # 2. Update
    update_kw = {"term": "Blockchain", "weight": 5.0, "type": "Service"}
    resp = await client.put(f"/api/keywords/{kw_id}", json=update_kw)
    assert resp.status_code == 200
    assert resp.json()["weight"] == 5.0

    # 3. List
    resp = await client.get("/api/keywords")
    assert resp.status_code == 200
    assert any(k["id"] == kw_id for k in resp.json())

    # 4. Delete
    resp = await client.delete(f"/api/keywords/{kw_id}")
    assert resp.status_code == 204

    # 5. Verify gone
    resp = await client.get("/api/keywords")
    assert not any(k["id"] == kw_id for k in resp.json())

@pytest.mark.asyncio
async def test_duplicate_keyword_behavior(client: AsyncClient):
    """Scenario: Duplicate Keyword Conflict"""
    await client.post("/api/keywords", json={"term": "SAP", "weight": 1.0, "type": "Service"})

    resp = await client.post("/api/keywords", json={"term": "SAP", "weight": 2.0, "type": "Service"})
    assert resp.status_code == 409
    assert "already exists" in resp.json()["detail"].lower()
