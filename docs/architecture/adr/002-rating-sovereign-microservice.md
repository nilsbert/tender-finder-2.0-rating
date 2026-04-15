# ADR 002: Rating Sovereign Microservice Migration

## Status
Accepted (Validated 2026-04-12)

## Context
The Rating engine was previously a submodule of the `tender-finder` monolith. To improve scalability, reduce AI/IDE context complexity, and enable independent deployment, we required a "hard-sovereign" microservice architecture for the 2.0 Orchestrator.

## Decision
We migrated the Rating service logic to a standalone project within the `rating/` directory of the orchestrator monorepo.

Key implementation details:
- **Language/Framework:** FastAPI (Python)
- **Persistence:** Isolated SQLite (with MSSQL support) via SQLAlchemy 2.0.
- **Data Path:** Unified `RatingRepository` for all domain CRUD, removing direct DB access from logic.
- **Stateless Engine:** The `RatingEngine` is fully stateless, taking input and policy as arguments.
- **Frontend:** Self-contained React/Vite UI served by the FastAPI service.

## Consequences
- **Positive:** Full operational independence. Service can be tested and deployed without the monolith.
- **Positive:** 100% logic verification via BDD suite.
- **Negative:** Minor increase in infrastructure overhead (separate DB/process).
- **Negative:** Frontend builds must be managed within the service lifecycle.

## Verification
The decision is validated by 10/10 passing BDD scenarios covering:
1. Scoring Parity (Locality-aware matching).
2. Keyword CRUD & Duplicate Protection.
3. Import/Export Integration.
