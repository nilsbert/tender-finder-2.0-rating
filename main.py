import asyncio
import logging
import os
from contextlib import asynccontextmanager
from typing import Annotated

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.config import router as config_router
from api.routes import router as rating_router
from core.database import db, get_db
from core.initial_data import get_initial_keywords
from core.repository import RatingRepository
from models.orm import ConfigRatingORM

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("rating-ms")

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Initialize Database
    logger.info("🚀 Starting Rating Microservice...")
    await db.init()
    
    # Seed Database if empty
    async with db.session_factory() as session:
        # Seed Keywords
        repo = RatingRepository(session)
        existing_keywords = await repo.get_all_keywords()
        if not existing_keywords:
            logger.info("🌱 Seeding initial keywords...")
            initial_data = get_initial_keywords()
            for kw in initial_data:
                try:
                    await repo.create_keyword(kw)
                except Exception as e:
                    logger.error(f"Failed to seed keyword {kw.term}: {e}")
            logger.info(f"Seeded {len(initial_data)} keywords.")

        # Seed Rating Config
        config_stmt = select(ConfigRatingORM).where(ConfigRatingORM.id == 1)
        config_res = await session.execute(config_stmt)
        config_obj = config_res.scalar_one_or_none()
        
        if not config_obj:
            logger.info("🌱 Seeding default rating configuration...")
            default_config = ConfigRatingORM(
                id=1,
                overall_score_threshold=70,
                title_score_threshold=50
            )
            session.add(default_config)
            await session.commit()
            logger.info("✅ Default rating configuration seeded.")
    
    yield
    # Shutdown: Close connections
    logger.info("🛑 Shutting down Rating Microservice...")
    await db.close()

app = FastAPI(
    title="Rating Microservice",
    description="Calculates relevance scores for tenders based on keywords and AI classification",
    version="1.0.0",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(rating_router)
app.include_router(config_router, prefix="/api/v1")

# --- UI Serving Logic ---
ui_path = os.path.join(os.path.dirname(__file__), "ui", "dist")

if os.path.exists(ui_path):
    # Serve assets with and without /ms/rating prefix to support direct and proxied access
    app.mount("/assets", StaticFiles(directory=os.path.join(ui_path, "assets")), name="assets")
    app.mount("/ms/rating/assets", StaticFiles(directory=os.path.join(ui_path, "assets")), name="ms_assets")

    @app.get("/ms/rating")
    @app.get("/ms/rating/")
    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(ui_path, "index.html"))

    @app.get("/{full_path:path}")
    async def catch_all(request: Request, full_path: str):
        # Exclude API routes and health check from catch-all
        # We check both prefix and non-prefix versions
        api_prefixes = ["api/", "ms/rating/api/", "health", "ms/rating/health"]
        if any(full_path.startswith(prefix) for prefix in api_prefixes):
            return None # Let FastAPI handle as 404 or route

        # Try to serve as a static file first
        # Strip /ms/rating/ if present
        clean_path = full_path
        if clean_path.startswith("ms/rating/"):
            clean_path = clean_path[len("ms/rating/"):]
            
        file_path = os.path.join(ui_path, clean_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)

        # Fallback to SPA index.html for UI routes
        # Only if it doesn't look like an asset (has a dot in filename)
        if "." in full_path.split("/")[-1]:
             raise HTTPException(status_code=404, detail="Asset not found")
             
        return FileResponse(os.path.join(ui_path, "index.html"))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "rating"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8012))
    uvicorn.run(app, host="0.0.0.0", port=port)
