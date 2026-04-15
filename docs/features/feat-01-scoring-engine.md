# FEATURE: FEAT-01 - Stateless Scoring Engine
**Status:** [READY FOR DEV]
**Owner:** @Martin (Architecture), @Jeff (Product)

## 🎯 Value Proposition
Provide a high-performance, autonomous calculation service that computes tender relevancy without owning tender data. This allows for massive horizontal scaling and clear domain separation.

## 📝 User Stories

### US-01: Automated Relevancy Scoring
**As a** Downstream Service (e.g., Enriching)  
**I want to** send tender text to the Rating Engine  
**So that** I receive a standardized relevancy score and match breakdown for persistence.

#### Acceptance Criteria (Gherkin)

**Scenario: Successful Scoring Handshake (Happy Path)**
- **Given** the Rating Engine has a pre-defined Keyword Policy
- **And** the following keywords exist: "AI" (2.0), "Aerospace" (1.5)
- **When** I call the POST `/api/rate` endpoint with:
  | ID | Title | Description |
  | T-101 | "AI in Aerospace" | "Deep learning for planes" |
- **Then** I should receive a 200 OK response
- **And** the "total_score" should be calculated as (2.0 * 5.0) + (1.5 * 5.0) = 17.5
- **And** the "matched_keywords" should list both "AI" and "Aerospace".

**Scenario: Empty Text Handling**
- **Given** a request has an empty "description" and "full_text"
- **When** I call the POST `/api/rate` endpoint
- **Then** the engine should still process the "title"
- **And** return a score based on title keywords only.

## 🛠 Technical Details (Martin's Notes)
- **Endpoint**: `POST /api/rate`
- **Logic**: Implemented in `core/logic.py` via `ScoringPolicy`.
- **Database**: Strictly stateless for calculation; read-only access to `keywords` table.
