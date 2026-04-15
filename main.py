from core.database import db
import os
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
from core.initial_data import get_initial_keywords
from core.repository import RatingRepository
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Load env
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB (Schema/Tables)
    await db.init_db()
    
    # Seeding Logic via Repository
    async with db.session_factory() as session:
        async with session.begin():
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

# API Routes
from api.routes import router as rating_router
app.include_router(rating_router)

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
    @app.get("/")
    async def root_redirect():
        return FileResponse(os.path.join(ui_dist_path, "index.html"))
    
    app.mount("/", StaticFiles(directory=ui_dist_path, html=True), name="ui")
else:
    @app.get("/")
    async def root():
        return {"message": "Rating Microservice is running. Frontend not found in ui/dist. Please run 'npm run build' in rating/ui."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8012)
