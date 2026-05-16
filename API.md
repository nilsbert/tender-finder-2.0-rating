# 🛠️ Public Interface: Rating API

> **Base Path:** `/api/v1/rating`
> **Port:** 8012
> **Owner:** Tender Finder Team

The **Rating MS** is the prioritization engine, applying the "Company Brain" to enriched tender data.

---

## 📡 Scoring Endpoints

### 1. POST /api/v1/rating/score

Calculate the authoritative relevance score for a tender.

- **Logic**: Applies weighted keyword matching with location-aware multipliers.
- **Authoritative Data**: Consumes keyword weights from the Distribution Authority.

#### Request Body

```json
{
  "tender_id": "uuid",
  "text_content": "Full tender text...",
  "context": {
    "location": "DE",
    "industry": "Public Sector"
  }
}
```

#### Response: Score Result (200)

```json
{
  "tender_id": "uuid",
  "total_score": 85.5,
  "explanation_id": "uuid"
}
```

### 2. GET /api/v1/rating/explain/{tender_id}

Fetch a detailed points breakdown for a specific scoring result. Used by the UI to justify match results.

#### Response: Explanation Detail (200)

```json
{
  "breakdown": [
    { "factor": "Keyword: Cloud", "points": 30.0, "reason": "Headline match (3.0x)" },
    { "factor": "Location: Munich", "points": 15.0, "reason": "Regional office proximity" }
  ]
}
```

---

## 📡 Policy Management

### 3. GET /api/v1/rating/config/thresholds

Fetch current priority cut-off values (e.g., what constitutes a "High Priority" match).

### 4. PUT /api/v1/rating/config/thresholds

Update threshold values. Requires a `change_summary` for the audit trail.

---

Maintained by the Tender Finder Architectural Board
