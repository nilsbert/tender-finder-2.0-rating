import pytest
from httpx import AsyncClient
import yaml
import json

@pytest.mark.asyncio
async def test_keyword_export_import_flow(client: AsyncClient):
    """Scenario: Import/Export Lifecycle and Dry Run"""
    
    # 1. Export initial (should have seeded keywords)
    resp = await client.get("/api/keywords/export")
    assert resp.status_code == 200
    assert "application/x-yaml" in resp.headers["content-type"]
    
    # 2. Add a new keyword via direct post
    await client.post("/api/keywords", json={"term": "ImportTest", "weight": 9.9, "type": "Service"})
    
    # 3. Export again and verify new keyword
    resp = await client.get("/api/keywords/export")
    data = yaml.safe_load(resp.text)
    terms = [k["term"] for k in data["keywords"]]
    assert "ImportTest" in terms

    # 4. Prepare Import Data (YAML)
    import_data = {
        "keywords": [
            {"term": "ImportTest", "weight": 5.5, "type": "Service"}, # Update
            {"term": "NewViaImport", "weight": 1.0, "type": "Service"} # Create
        ]
    }
    yaml_bytes = yaml.dump(import_data).encode("utf-8")
    
    # 5. Dry Run Import
    resp = await client.post(
        "/api/keywords/import?dry_run=True", 
        files={"file": ("test.yaml", yaml_bytes, "application/x-yaml")}
    )
    assert resp.status_code == 200
    res_json = resp.json()
    assert res_json["dry_run"] is True
    assert len(res_json["summary"]["updated"]) == 1
    assert len(res_json["summary"]["created"]) == 1

    # 6. Real Import (Sync)
    resp = await client.post(
        "/api/keywords/import?dry_run=False", 
        files={"file": ("test.yaml", yaml_bytes, "application/x-yaml")}
    )
    assert resp.status_code == 200
    
    # 7. Verify Changes
    resp = await client.get("/api/keywords")
    keywords = resp.json()
    import_test_kw = next(k for k in keywords if k["term"] == "ImportTest")
    assert import_test_kw["weight"] == 5.5
    assert any(k["term"] == "NewViaImport" for k in keywords)

@pytest.mark.asyncio
async def test_rate_batch_endpoint(client: AsyncClient):
    """Scenario: Batch rating of multiple tenders"""
    await client.post("/api/keywords", json={"term": "AI", "weight": 2.0, "type": "Service"})
    
    batch_data = {
        "tenders": [
            {"id": "B1", "title": "AI Project", "description": "Desc"},
            {"id": "B2", "title": "Non Related", "description": "Cloud"}
        ]
    }
    
    resp = await client.post("/api/rate-batch", json=batch_data)
    assert resp.status_code == 200
    data = resp.json()
    assert len(data["results"]) == 2
    assert data["results"][0]["tender_id"] == "B1"
    assert data["results"][0]["score"] > 0
    assert data["results"][1]["score"] == 0

@pytest.mark.asyncio
async def test_error_paths(client: AsyncClient):
    """Scenario: Error handling for missing resources and bad data"""
    # 1. Update non-existent keyword
    resp = await client.put("/api/keywords/non-existent-id", json={"term": "X", "weight": 1.0, "type": "Service"})
    assert resp.status_code == 404
    
    # 2. Malformed Import (Invalid JSON/YAML)
    bad_bytes = b"not a yaml: ["
    resp = await client.post(
        "/api/keywords/import?dry_run=False", 
        files={"file": ("bad.yaml", bad_bytes, "application/x-yaml")}
    )
    assert resp.status_code == 400 or resp.status_code == 422 # Depends on how it fails
    assert "Import failed" in resp.json()["detail"] or "validation" in resp.json()["detail"].lower()

@pytest.mark.asyncio
async def test_keyword_tree_and_categories(client: AsyncClient):
    """Scenario: Metadata exploration"""
    await client.post("/api/keywords", json={"term": "X", "weight": 1.0, "type": "Service", "sub_type": "SubX"})
    
    resp = await client.get("/api/keywords/categories")
    assert resp.status_code == 200
    assert "SubX" in resp.json()
    
    resp = await client.get("/api/keywords/tree")
    assert resp.status_code == 200
    tree = resp.json()
    assert "Service" in tree
    assert "SubX" in tree["Service"]
