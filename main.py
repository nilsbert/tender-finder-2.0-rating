import logging
import os
from contextlib import asynccontextmanager

from api.config import router as config_router
from api.routes import router as rating_router
from core.database import db
from core.initial_data import get_initial_keywords
from core.repository import RatingRepository
from dotenv import load_dotenv
from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

# Load env
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rating-ms")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB (Schema/Tables)
    await db.init_db()

    # Seeding Logic via Repository
    async with db.session_factory() as session, session.begin():
        repo = RatingRepository(session)
        keywords = await repo.get_all_keywords()
        if not keywords:
            logger.info("Database empty. Seeding initial keywords...")
            initial_data = get_initial_keywords()
            for kw in initial_data:
                try:
                    # Safely pass only available attributes
                    kw_dict = kw.model_dump()
                    await repo.add_keyword(**kw_dict)
                except Exception as e:
                    logger.error(f"Failed to seed keyword {kw.term}: {e}")
            logger.info(f"Seeded {len(initial_data)} keywords.")

    logger.info("Rating Service starting up...")
    yield
    logger.info("Rating Service shutting down...")

app = FastAPI(
    title="Tender Finder Rating Microservice",
    description="Calculates relevancy scores and keyword matching for Tenders.",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

@app.middleware("http")
async def log_requests(request, call_next):
    logger.info(f"🔍 Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"🔄 Response: {response.status_code}")
    return response

app.include_router(rating_router)
app.include_router(config_router, prefix="/api/v1")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "rating"}

# CORS Setup
allowed_origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "http://localhost:3000",
    "http://localhost:8012",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve isolated frontend static files
ui_dist_path = os.path.join(os.path.dirname(__file__), "ui", "dist")

if os.path.exists(ui_dist_path):
    @app.get("/ms/rating/", include_in_schema=False)
    @app.get("/")
    async def ui_root():
        return FileResponse(os.path.join(ui_dist_path, "index.html"))

    app.mount("/assets", StaticFiles(directory=os.path.join(ui_dist_path, "assets")), name="assets")
    app.mount("/ms/rating/assets", StaticFiles(directory=os.path.join(ui_dist_path, "assets")), name="ms_assets")

    # Catch-all for React SPA routes
    @app.get("/{full_path:path}", include_in_schema=False)
    async def spa_catchall(request: Request, full_path: str):
        # Ignore API routes
        if full_path.startswith("api/") or full_path == "health":
            return None # Let FastAPI handle it

        # Strip the /ms/rating prefix if present in the request path
        search_path = full_path
        if search_path.startswith("ms/rating/"):
            search_path = search_path[len("ms/rating/") :]

        # Check if file exists in dist
        file_path = os.path.join(ui_dist_path, search_path.lstrip("/"))
        if os.path.isfile(file_path):
            return FileResponse(file_path)

        # Do NOT serve index.html for missing assets
        if "." in search_path.split("/")[-1] and not search_path.endswith(".html"):
             raise HTTPException(status_code=404, detail="Asset not found")

        return FileResponse(os.path.join(ui_dist_path, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "Rating Microservice is running. Frontend not found in ui/dist. Please run 'npm run build' in rating/ui."}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8012))
    uvicorn.run(app, host="0.0.0.0", port=port)
