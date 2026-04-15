# 🚀 Standalone Development Guide — Rating Microservice

> **Last Updated:** 2026-04-15
> **Port:** 8012
> **Team Isolation:** ✅ This service can be developed, tested, and run completely independently.

---

## 🎯 The Golden Rule

> *As long as the API contract (defined in [CONTRACTS.md](../CONTRACTS.md)) does not change, you can develop this service without touching or needing any other microservice.*

---

## 📋 Prerequisites

| Tool | Version | Purpose |
| :--- | :--- | :--- |
| Python | 3.11+ | Runtime |
| pip | Latest | Package management |
| Docker | 20+ | Container mode (optional) |
| Node.js | 18+ | Admin UI (optional) |

---

## 🏗️ Three Execution Modes

```
┌──────────────────────────────────────────────────────────────────┐
│  MODE 1: LOCAL         │  MODE 2: DOCKER        │  MODE 3: STACK │
│  SQLite • No Docker    │  MSSQL • Single MS     │  MSSQL • All MS│
│  Fastest startup       │  Prod-like isolation   │  Full system   │
└──────────────────────────────────────────────────────────────────┘
```

---

### Mode 1: Local Development (SQLite)

```bash
# 1. Clone (if standalone)
git clone https://github.com/nilsbert/tender-finder-2.0-rating.git
cd tender-finder-2.0-rating

# 2. Setup
cp .env.example .env
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 3. Run (auto-seeds keywords on first start)
PYTHONPATH=. python main.py
```

✅ **Result:** `http://localhost:8012`
✅ **Database:** `rating.db` (SQLite, auto-created)
✅ **Gold Standard:** Keywords auto-seeded via `core/initial_data.py`

---

### Mode 2: Docker with MSSQL

```bash
docker compose up --build
# Service at http://localhost:8012, MSSQL on port 1435
```

---

### Mode 3: Full Stack

```bash
# From orchestrator root:
docker compose up --build
```

---

## 📁 Environment Variables

| Variable | Default | Description |
| :--- | :--- | :--- |
| `DATABASE_URL` | `sqlite+aiosqlite:///./rating.db` | Database (SQLite) |
| `MSSQL_CONNECTION_STRING` | *(none)* | ODBC string (overrides SQLite) |
| `PORT` | `8012` | Service port |
| `FRONTEND_URL` | `http://localhost:3000` | CORS origin |

### Database Auto-Detection
The `DatabaseManager` in `core/database.py` automatically selects:
- **No `MSSQL_CONNECTION_STRING`** → SQLite mode
- **`MSSQL_CONNECTION_STRING` set** → MSSQL mode with schema creation

---

## 🔗 Inter-Service Communication

### This Service as Provider
| Consumer | Endpoint | What They Need |
| :--- | :--- | :--- |
| **Enriching MS** | `POST /api/rating/score` | Scoring result |
| **Admin Suite** | `GET/PUT /api/v1/config/*` | Threshold config |

### This Service as Consumer
| Provider | Required? |
| :--- | :--- |
| *(none)* | ✅ **Fully Independent** |

> 💡 **Key Insight:** Rating is a pure scoring engine with zero upstream dependencies. It receives data to score and returns results. Total isolation.

---

## 🧪 Testing

```bash
# BDD tests
PYTHONPATH=. pytest tests/ -v

# Smoke test
curl http://localhost:8012/health
curl http://localhost:8012/api/keywords
```

---
*This guide ensures team independence. Maintained by the Tender Finder Architectural Board.*
