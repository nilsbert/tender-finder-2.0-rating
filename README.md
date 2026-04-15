# ⭐ Rating Microservice

> **Domain Type:** Supporting Domain
> **Port:** 8012
> **Owner:** Tender Finder Team

---

## 1. Purpose

The Rating Microservice provides an autonomous, high-performance **Scoring Engine** that applies the "Company Brain" (Keyword Policy) to incoming tenders. It calculates quantitative relevance scores using weighted keyword matching with location-aware multipliers.

## 2. 🤖 Agent Context (CRITICAL)

- **Role**: Scoring Intelligence & Policy Engine.
- **Rules**:
  - Owns the `keywords`, `scoring_results`, and `rating_config_*` tables.
  - Provides stateless scoring calculation via pure functions.
  - Manages the Keyword Policy (CRUD + seeding).
  - Does NOT directly access Crawling or Enriching databases.
- **Boundary**: Scoring logic, keyword management, and threshold configuration.

## 3. Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | FastAPI (Python 3.11+) |
| **ORM** | SQLAlchemy 2.0 (Async) |
| **Database** | SQLite (Local) / Azure MSSQL (Prod) |
| **Frontend** | React + Vite (Rating Admin UI) |
| **Container** | Dockerfile included |
| **Tests** | Pytest (BDD-style) |

## 4. Getting Started

```bash
# 1. Navigate
cd rating

# 2. Create & activate virtual environment
python -m venv .venv && source .venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Seed initial keywords (Gold Standard)
PYTHONPATH=. python scripts/seed_config.py

# 5. Run the service
PYTHONPATH=. python main.py
```
The service will be available at `http://localhost:8012`.

## 5. API Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check |
| `POST` | `/api/rating/score` | Calculate score for a tender |
| `GET` | `/api/rating/keywords` | List all keywords |
| `POST` | `/api/rating/keywords` | Add a keyword |
| `PUT` | `/api/rating/keywords/{id}` | Update a keyword |
| `DELETE` | `/api/rating/keywords/{id}` | Remove a keyword |
| `GET` | `/api/rating/config/*` | Threshold configuration CRUD |
| `PUT` | `/api/rating/config/*` | Update thresholds (with audit trail) |

→ Full details in [API.md](./API.md)

## 6. Project Structure

```
rating/
├── main.py                 # FastAPI entry point + seeding
├── api/
│   ├── routes.py           # REST endpoints
│   └── config.py           # Admin config routes
├── core/
│   ├── database.py         # DB engine & session
│   ├── scoring.py          # Pure scoring functions
│   ├── service.py          # RatingEngine orchestrator
│   ├── repository.py       # Data access layer
│   └── initial_data.py     # Gold Standard keyword seeds
├── models/
│   ├── orm.py              # SQLAlchemy ORM models
│   ├── schemas.py          # Pydantic v2 schemas
│   └── config.py           # Config current/history ORM
├── scripts/
│   └── seed_config.py      # Config seeding
├── tests/
│   ├── test_scoring_bdd.py # Scoring logic BDD tests
│   ├── test_keyword_bdd.py # Keyword CRUD BDD tests
│   └── test_integration_bdd.py
├── docs/                   # Feature & architecture docs
├── ui/                     # React Admin UI
├── Dockerfile
└── requirements.txt
```

## 7. Dependencies

| Direction | Service | Relationship |
| :--- | :--- | :--- |
| **Upstream** | Enriching MS | Receives tender data for scoring |
| **Downstream** | Enriching MS | Returns scoring results |
| **Downstream** | Admin Suite UI | Serves threshold configuration |

→ Consumer contracts in [CONTRACTS.md](./CONTRACTS.md)

---
*Maintained by the Tender Finder Architectural Board*
