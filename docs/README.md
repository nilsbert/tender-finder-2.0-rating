# Rating Microservice Documentation

Welcome to the **Rating & Evaluation** domain documentation.

## 🚀 Product Vision
Provide an autonomous, high-performance scoring engine that applies the "Company Brain" (Keyword Policy) to incoming tenders.

## 🗺️ Product Roadmap
- **[MVP: FEAT-MVP - Rating Engine & Policy Studio](./features/feat-mvp-rating-engine.md)** — Iteration 1 (Walking Skeleton).
- **[FEAT-01: Scoring Intelligence Engine](./features/feat-01-scoring-engine.md)** — Stateless calculation details.
- **[FEAT-02: Keyword Policy Studio](./features/feat-02-keyword-policy.md)** — Advanced management features.
- **[FEAT-03: Policy Seeding](./features/feat-03-policy-seeding.md)** — System initialization.

## 🏗️ Architecture
- **Language**: Python 3.11 (FastAPI)
- **Database**: MSSQL (Schema: `rating`)
- **Isolation**: Sovereign microservice with NO direct dependencies on Enriching or Sourcing.

---
*Owner: @Jeff (Product Owner)*
