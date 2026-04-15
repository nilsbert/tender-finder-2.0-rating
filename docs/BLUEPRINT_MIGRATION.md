# Blueprint: Rating Service Migration (v2.0)

> [!IMPORTANT]
> This blueprint covers the migration of the Rating/Scoring domain from `tender-finder` to `tender-finder-2.0-orchestrator/rating`.

## 1. Strategic Alignment (Roman's View)
- **Goal:** Enable autonomous scoring of tenders to eliminate "manual fatigue."
- **Focus:** Decoupled execution, allowing the rating engine to run independently of the sourcing/enrichment pipeline if needed.
- **Value:** Improve decision speed and consistency via semantic keyword matching.

## 2. Domain Glossary & Language (Martin's View)
*Consistent with `docs/DOMAIN_GLOSSARY.md`*
- **Scoring Engine:** The component responsible for calculating relevance.
- **Keyword:** A weighted term (Aggregate Root for configuration).
- **Match Location:** Semantic context (Headline, Description, Full Text).
- **Consensus Score:** The final verdict after engine execution.

## 3. Structural Blueprint (Arc42)
The Rating service remains a sovereign submodule with its own database (`rating.db`) and UI.

### Component Map:
- **`rating/models/`**: SQLAlchemy 2.0 ORM models for Keywords and Scoring Results.
- **`rating/core/`**:
    - `scoring.py`: The logic engine (Pure functions where possible).
    - `service.py`: Orchestration of scoring workflow.
    - `database.py`: Async SQLite management.
- **`rating/api/`**: FastAPI routes.
- **`rating/ui/`**: React/Vite frontend (Ported from v1.0).

## 4. Migration Strategy
1. **Model Porting:** Move `orm.py` and `schemas.py`. Update to Pydantic v2 and ensure async compatibility.
2. **Logic Refactoring:**
- [x] Port `core/scoring.py` (Refactor to use new schemas)
- [x] Port `core/database.py` keyword CRUD methods
- [x] Port `core/initial_data.py` (Gold Standard)
- [x] Implement `core/service.py` (RatingEngine orchestrator)
- [x] Refactor `api/routes.py` (API Parity with monolith)
- [x] Update `main.py` (Lifespan for seeding, UI mounting)
3. **Data Migration:** Ensure `initial_data.py` (Gold Standard keywords) are correctly seeded in the new `rating.db`.
4. **UI Adaptation:** Port the React components. Update API paths to match the new gateway structure (`/ms/rating/api/`).

## 5. Known Gotchas & Risks
- **Asset Paths:** UI build assets must be correctly mapped for the Nginx proxy (BASE_URL handling).
- **Model Synchronization:** If keywords are shared with other services, we must ensure the source of truth is the Rating service.

---
**Sign-off requested from Martin (Architecture) and Roman (Product).**
