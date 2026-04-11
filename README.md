# ⭐ Rating Microservice

The **Rating** microservice calculates quantitative scores for tenders. It provides both automated scoring (via AI) and manual scoring fields for human evaluation.

## 🎯 Responsibility
- Calculate `Overall Score` and `Title Score`.
- Provide scoring metrics for the Matching Engine in **Distribution**.
- Handle complex scoring rules based on Tender metadata.

## 🛠️ Tech Stack
- **Language**: Python 3.11+
- **Framework**: FastAPI

## 🏁 Getting Started

### 👤 Human Path
1. **Navigate**: `cd rating`
2. **Setup Venv**: `python -m venv .venv && source .venv/bin/activate`
3. **Install**: `pip install -r requirements.txt`
4. **Run Standalone**:
   ```bash
   python main.py
   ```
   The service will be available at `http://localhost:8012`.

### 🤖 Agent Path
1. **Entry Point**: `rating/main.py`.
2. **Scoring Logic**: Check `rating/core/scoring.py`.
3. **Metrics**: Check `rating/models/` for score schemas.

## 📡 API Reference
- **OpenAPI Docs**: `http://localhost:8012/docs`
- **Health Check**: `GET /health`

## 🔗 Dependencies
- **Tender Core**: To read tender data and store scores.
