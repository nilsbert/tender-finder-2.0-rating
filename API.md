# 🛠️ Public Interface: Rating API

> **Base Path:** `/api/rating`
> **Port:** 8012
> **OpenAPI Docs:** `http://localhost:8012/docs`

The Rating MS serves as the **Scoring Intelligence Engine**, providing keyword-based relevance scoring and threshold management.

---

## 📡 Endpoints

### 1. GET /health
Health check endpoint.

#### Response (200)
```json
{ "status": "healthy" }
```

### 2. POST /api/rating/score
Calculate a relevance score for a tender.
- **Consumers**: Enriching MS

#### Request Body
```json
{
  "tender_id": "string",
  "title": "Infrastructure modernization project",
  "description": "Full project description text..."
}
```

#### Response (200)
```json
{
  "tender_id": "string",
  "total_score": 85.5,
  "title_score": 42.0,
  "matches": [
    {
      "keyword": "infrastructure",
      "weight": 10.0,
      "location": "HEADLINE",
      "multiplier": 3.0,
      "contribution": 30.0
    }
  ]
}
```

### 3. GET /api/rating/keywords
List all registered keywords.

#### Response (200)
```json
{
  "keywords": [
    {
      "id": 1,
      "term": "infrastructure",
      "weight": 10.0,
      "category": "core",
      "is_active": true
    }
  ]
}
```

### 4. POST /api/rating/keywords
Add a new keyword.

### 5. PUT /api/rating/keywords/{id}
Update an existing keyword.

### 6. DELETE /api/rating/keywords/{id}
Remove a keyword.

### 7. GET /api/rating/config/thresholds
Fetch current scoring thresholds.

### 8. PUT /api/rating/config/thresholds
Update scoring thresholds with mandatory audit trail.

#### Request Body
```json
{
  "overall_score_threshold": 50.0,
  "title_score_threshold": 20.0,
  "change_summary": "Lowered thresholds for broader lead capture"
}
```

---
*Maintained by the Tender Finder Architectural Board*
