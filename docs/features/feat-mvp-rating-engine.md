# FEATURE: FEAT-MVP - Rating Engine & Policy Studio

**Status:** [VALIDATING]
**Owner:** @Jeff (PO)
**Target:** SPRINT 1 (Walking Skeleton)

## 🎯 Feature Story
**As a** Bid Manager (Haruki)  
**I want to** automatically see relevancy scores for every new tender  
**So that** I can instantly ignore non-matching opportunities and focus on high-probability bids.

---

## 🔍 Domain Alignment (DDD)
- **Primary Bounded Context**: Rating & Evaluation
- **Cross-Domain Dependencies**: 
    - **Enriching**: Call the Rating API during the 7-stage pipeline.
    - **Taxonomy**: Source for initial sector/service labels.
- **Ubiquitous Language**:
    - **Scoring Engine**: The stateless component that applies weights to text.
    - **Keyword Policy**: The "Company Brain" — a managed database of weights.
    - **Multiplier**: The factor applied to matches based on location (Title = 5.0x, Description = 3.0x).

---

## 🛠 MVP Walking Skeleton (Iteration 1)

| Feature | In MVP (Iteration 1) | Future Iterations (v2+) |
| :--- | :--- | :--- |
| **Scoring Logic** | Keyword-based weighting (Stateless) | AI-driven semantic score (LLM) |
| **API** | `POST /api/rate` (Single Tender) | Bulk rating endpoints |
| **Admin UI** | Search with **Visual Highlighting** | Management Studio (Bulk Move, Export) |
| **Search Breadth** | Keywords + Categories + Sub-types | Semantic (Vector) Search |
| **Calibration** | Manual weight input | Scoring Slider, UI-driven re-parenting |
| **Seed Data** | 100+ Sector/Service keywords | Custom customer-specific profiles |

---

## ✅ BDD Scenarios (Validation Phase 0.3)

### Background
  Given the Rating Microservice is connected to the "rating" MSSQL schema
  And the following Keyword Policy is active:
    | term | weight | type |
    | "AI" | 2.0 | "Service" |
    | "Cloud" | 1.5 | "Service" |
    | "Catering" | -5.0 | "Exclusion" |

### 1. Happy Path (Success Guaranteed)

**Scenario: Standard Relevancy Score Computation**
  Given a tender with Title "AI Research Project" and Description "Cloud based AI"
  When I request a rating via `POST /api/rate`
  Then the `title_score` should be 10.0 (2.0 * 5.0 multiplier)
  And the `total_score` should account for "AI" in Title and "AI" + "Cloud" in Description.

**Scenario: Exclusion Logic Precedence**
  Given a tender with Title "IT Services" and Description "Includes Catering services"
  When I request a rating via `POST /api/rate`
  Then the `total_score` should be significantly reduced by the -5.0 exclusion weight
  And the `matched_keywords` list must contain "Catering".

**Scenario: Case-Insensitive Matching**
  Given a tender with Title "ai research"
  When I request a rating
  Then it should match the keyword "AI" correctly
  And the score should be identical to uppercase matches.

**Scenario: Re-rating after Policy Update**
  Given I update the weight of "AI" to 5.0
  When I request a rating for "AI Research"
  Then the `title_score` must immediately reflect 25.0 (5.0 * 5.0).

**Scenario: Multi-word Description Match**
  Given a tender where "Cloud" appears 5 times in the description
  When I request a rating
  Then the engine should match only the FIRST occurrence for impact calculation (standard policy)
  And the score should not be artificially inflated by repetition.

### 2. Problem Path (Degraded but Safe)

**Scenario: Minimal Tender Text Handling**
  Given a tender with Title "A" and empty Description
  When I request a rating
  Then the system should still return 200 OK
  And the scores should be 0.0 without crashing.

**Scenario: High Character Count Payload**
  Given a tender with 5MB of "full_text"
  When I request a rating
  Then the engine should process it within the 200ms threshold
  And not throw a memory overflow error.

**Scenario: Special Characters in Metadata**
  Given a tender with title containing "AI & Cloud (2026!)"
  When I request a rating
  Then the tokenizer should successfully isolate "AI" and "Cloud"
  And match them against the policy.

**Scenario: Database Connection Latency**
  Given the MSSQL database responds with a 3-second delay
  When I request a rating
  Then the service should wait (up to 5s timeout) and fulfill the request
  And not prematurely return a 504.

**Scenario: Concurrent Rating Stress**
  Given 50 parallel requests from the Enriching service
  When they hit the `/api/rate` endpoint simultaneously
  Then all requests should finish successfully
  And the connection pool should scale correctly.

### 3. Error Path (Validation Failures)

**Scenario: Missing Required Title**
  Given a rating request with null "title"
  When I request a rating
  Then the system should return 422 Unprocessable Entity
  And the error should highlight "title" as a mandatory field.

**Scenario: Invalid Keyword Weight (Boundary)**
  Given I attempt to add a keyword with weight "INF"
  When I POST to `/api/keywords`
  Then the system should return 400 Bad Request
  And reject the non-numeric weight.

**Scenario: Unauthorized Admin Access**
  Given a request to DELETE a keyword without a valid Bearer token
  When the request hits the API
  Then it should return 401 Unauthorized
  And the keyword should remain in the database.

**Scenario: Database Down Recovery**
  Given the MSSQL server is unreachable
  When a rating request arrives
  Then the service should return 503 Service Unavailable
  And provide a clear error message indicating a connection problem.

**Scenario: Duplicate Keyword Term Conflict**
  Given the keyword "AI" already exists
  When I attempt to POST a new keyword with term "AI"
  Then the system should return 409 Conflict
  And suggest using the PATCH endpoint for updates.

### 4. Edge Case (Boundary Stress)

**Scenario: Zero-Weight Keyword Behavior**
  Given a keyword "Test" with weight 0.0
  When a tender matches "Test"
  Then it should appear in `matched_keywords`
  But contribute exactly 0.0 to the `total_score`.

**Scenario: Seeding Idempotency**
  Given the `keywords` table is already populated
  When the service Bootstraps and triggers Seeding
  Then it should NOT create duplicate records
  And log "Database already seeded".

**Scenario: Maximum Multi-match Overlap**
  Given a tender where one word matches THREE different keyword terms (e.g., "SAP", "SAP-HANA", "HANA")
  When a rating is computed
  Then all three matches should be recorded with their respective impacts.

**Scenario: Very Long Keyword Term**
  Given a keyword term with 255 characters
  When a tender text contains this exact string
  Then the matching logic should successfully identify it without truncation.

**Scenario: RTL (Right-to-Left) Text Integrity**
  Given a tender with Arabic text (if supported/present)
  When a rating is requested
  Then the service should handle the encoding without corrupting the response JSON.

---

## 🏗 E2E Test Scenarios (Draft)

1. **Journey: Full Policy Lifecycle**
   - Admin logs in -> Adds "Quantum" (10.0) -> Verifies via List.
   - External system POSTs "Quantum Tender" -> Receives high score.
   - Admin deletes "Quantum" -> Verifies next rating is 0.0.

2. **Journey: Mass Rerating Event**
   - 100 tenders exist in system -> Admin changes weight of "Public Sector".
   - Admin triggers "Rerate All" (Future feature) -> Checks metrics.

3. **Journey: Seeding to Scoring**
   - Fresh install -> Check health -> Verify 100 keywords exist -> Post first tender.

---

## ⛈ Sad Path Deep Analysis

| Sad Path | Trigger Condition | System Behavior | Recovery Path |
| :--- | :--- | :--- | :--- |
| **Database Downtime** | MSSQL connection fail at boot | Lifespan hook logs error; health check fails (503) | Service must be restarted after DB is healthy; Seeding is idempotent. |
| **Malformed Payload** | Enrichment sends invalid JSON | Pydantic exception caught by FastAPI | Returns 422 with specific field error; state is unaffected (stateless). |
| **Timeout (AI)** | Azure OpenAI latency > 30s | `httpx.Timeout` exception | Service returns 504; Client (Enrichment) should retry per 8-stage pipeline logic. |
| **Deadlock (Keywords)** | High concurrency UPDATE/DELETE | SQL Alchemy `DBAPIError` (Deadlock) | Transaction roll-back; system returns 500; retry recommended. |

## 🧪 Quality Assurance (Lisa's Desk)

### Quality Scenarios
- **Source**: External Service (Enriching) → **Stimulus**: Scoring Request → **Environment**: Peak Load → **Response**: Processed → **Measure**: Latency < 100ms.
- **Source**: Admin (Jony) → **Stimulus**: Keyword Delete → **Environment**: Normal → **Response**: Policy Synced → **Measure**: Immediate impact on next score.

### Exploratory Test Charter
- **Charter**: "Explore the scoring engine's handling of non-Latin characters and very long strings."
- **Focus**: Tokenization accuracy and memory usage.
- **Oracle**: Scores should match manual calculations based on identified substrings.

### Test Strategy
- **Mocks**: Use `pytest-mock` to simulate MSSQL downtime.
- **Data**: Seed with 5,000 "junk" keywords to simulate extreme policy scale-up.
- **E2E**: Use `testclient` (FastAPI) to verify the `/rate` endpoint lifecycle.
