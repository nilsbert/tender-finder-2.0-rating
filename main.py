from core.database import db
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv

# Load env
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB (Schema/Tables)
    await db.init_db()
    logger.info("Rating Service starting up...")
    yield
    logger.info("Rating Service shutting down...")

app = FastAPI(
    title="Tender Finder Rating Microservice",
    description="Calculates relevancy scores and keyword matching for Tenders.",
    version="1.0.0",
    lifespan=lifespan
)

from api.routes import router as rating_router
app.include_router(rating_router)

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "rating"}

# CORS Setup
allowed_origins = [
    os.getenv("FRONTEND_URL", "http://localhost:3000"),
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, RedirectResponse

# Serve isolated frontend static files for the rating service
ui_dist_path = os.path.join(os.path.dirname(__file__), "ui", "dist")

if os.path.exists(ui_dist_path):
    app.mount("/assets", StaticFiles(directory=os.path.join(ui_dist_path, "assets")), name="assets")
    
    @app.get("/")
    async def root_redirect():
        return RedirectResponse(url="/ms/rating/")
    
    @app.get("/{full_path:path}")
    async def serve_frontend(full_path: str):
        if full_path.startswith("api") or full_path == "health":
            return None
            
        file_path = os.path.join(ui_dist_path, full_path)
        if os.path.isfile(file_path):
            return FileResponse(file_path)
            
        return FileResponse(os.path.join(ui_dist_path, "index.html"))
else:
    @app.get("/")
    async def root():
        return {"message": "Rating Microservice is running. Frontend not found in ui/dist. Please run 'npm run build' in rating/ui."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
