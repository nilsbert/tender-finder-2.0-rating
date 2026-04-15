from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List, Dict, Any
from core.database import db
from models.orm import ConfigRatingORM, ConfigRatingHistoryORM
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/config", tags=["Configuration"])

class ConfigResponse(BaseModel):
    overall_score_threshold: int
    title_score_threshold: int
    version: int
    updated_at: datetime

    class Config:
        from_attributes = True

class ConfigUpdate(BaseModel):
    overall_score_threshold: int
    title_score_threshold: int
    change_summary: str
    created_by: str = "Admin"

def orm_to_dict(obj) -> Dict[str, Any]:
    """Extract data fields from ORM."""
    data = {}
    for column in obj.__table__.columns:
        if column.name not in ["id", "version", "updated_at", "change_summary", "created_at", "created_by"]:
            data[column.name] = getattr(obj, column.name)
    return data

@router.get("/", response_model=ConfigResponse)
async def get_rating_config(session: AsyncSession = Depends(db.get_session)):
    """Retrieve the current rating threshold configuration."""
    result = await session.execute(select(ConfigRatingORM).where(ConfigRatingORM.id == 1))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Rating config not initialized")
    return obj

@router.post("/", response_model=ConfigResponse)
async def update_rating_config(payload: ConfigUpdate, session: AsyncSession = Depends(db.get_session)):
    """Update the rating threshold configuration and create a history snapshot."""
    result = await session.execute(select(ConfigRatingORM).where(ConfigRatingORM.id == 1))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Rating config not initialized")
    
    # Historize
    history = ConfigRatingHistoryORM(
        version=obj.version,
        change_summary=payload.change_summary,
        created_by=payload.created_by,
        **orm_to_dict(obj)
    )
    session.add(history)
    
    # Update
    for key, value in payload.model_dump().items():
        if key not in ["change_summary", "created_by"] and hasattr(obj, key):
            setattr(obj, key, value)
            
    obj.version += 1
    await session.commit()
    await session.refresh(obj)
    return obj

@router.get("/history")
async def get_rating_history(session: AsyncSession = Depends(db.get_session)):
    """Retrieve the version history of the rating threshold configuration."""
    result = await session.execute(select(ConfigRatingHistoryORM).order_by(ConfigRatingHistoryORM.version.desc()).limit(10))
    return result.scalars().all()
