# ⭐ Rating Microservice

> **Domain Type:** Supporting Domain (Scoring Engine)
> **Port:** 8012
> **Owner:** Tender Finder Team

---

## 1. Purpose

The **Rating Microservice** is the prioritization engine of the ecosystem. It provides an autonomous, high-performance scoring system that applies the "Company Brain" (authoritative keyword weights) to enriched tender data.

### Key Capabilities

* **Weighted Keyword Matching**: Calculates relevance scores based on the presence and frequency of authoritative terms.
* **Location-Aware Multipliers**: Adjusts scores based on the tender's proximity to regional offices or strategic markets.
* **Transparents Scoring**: Provides detailed breakdowns of how each point was calculated, ensuring auditability for the match results.
* **Premium UI**: Features a cohesive, dark-mode glassmorphism interface for managing scoring policies.

## 📚 Project Foundation

This microservice is part of the Tender Finder 2.0 ecosystem. To ensure architectural sovereignty and consistency, please refer to the central documentation in the orchestrator repository.

## 2. 🤖 Agent Context (CRITICAL)

- **Role**: Scoring Intelligence & Policy Engine.
- **Rules**:
  - Owns the `keywords`, `scoring_results`, and `rating_config` tables.
  - Consumes authoritative keyword weights from the Distribution Authority MS.
  - Provides a stateless scoring API for high-throughput evaluation.
  - **Auditability**: Every score must be accompanied by a "points breakdown" explainability payload.
- **Boundary**: Scoring mathematics, keyword evaluation, and priority thresholds.

## 3. Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | FastAPI (Python 3.11+) |
| **ORM** | SQLAlchemy 2.0 (Async) |
| **Database** | Azure SQL (Staging/Prod) / SQLite (Local) |
| **Frontend** | React + Vite (Premium PDS-based UI) |
| **Styling** | Glassmorphism / Dark Mode Optimization |

## 4. Getting Started

```bash
cd rating
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
PYTHONPATH=. python main.py
```

The service will be available at `http://localhost:8012`.

## 5. API Summary

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/health` | Health check |
| `POST` | `/api/rating/score` | High-performance scoring for a tender payload |
| `GET` | `/api/rating/explain/{tender_id}` | Detailed points breakdown for a result |
| `PUT` | `/api/rating/config/thresholds` | Update priority cut-off values |

## 6. Project Structure

```text
rating/
├── main.py                 # FastAPI entry point
├── api/v1/
│   ├── scoring.py          # Calculation & Explainability REST
│   └── config.py           # Threshold management
├── core/
│   ├── engine.py           # Weighted matching algorithm
│   └── explainers/         # Points breakdown generators
├── models/
│   ├── orm.py              # Scoring results & thresholds
│   └── schemas.py          # Pydantic v2 schemas
└── ui/                     # Glassmorphism Rating Dashboard
```

## 7. Dependencies

| Direction | Service | Relationship |
| :--- | :--- | :--- |
| **Upstream** | Distribution MS | Pulls authoritative keyword weights |
| **Upstream** | Enriching MS | Receives enriched notices for evaluation |
| **Downstream** | Enriching MS | Returns final scores and breakdowns |

---

Maintained by the Tender Finder Architectural Board
