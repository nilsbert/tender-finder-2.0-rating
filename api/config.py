import yaml
from datetime import datetime
from typing import Any

from core.database import db
from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile, File, Query
from models.orm import ConfigRatingHistoryORM, ConfigRatingORM
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

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

def orm_to_dict(obj) -> dict[str, Any]:
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

# --- Export / Import ---

@router.get("/export", response_class=Response)
async def export_config_yaml(session: AsyncSession = Depends(db.get_session)):
    """Download rating configuration as a YAML file."""
    result = await session.execute(select(ConfigRatingORM).where(ConfigRatingORM.id == 1))
    obj = result.scalar_one_or_none()
    if not obj:
        raise HTTPException(status_code=404, detail="Rating config not initialized")

    data = orm_to_dict(obj)
    yaml_str = yaml.dump(data, sort_keys=False, allow_unicode=True)

    return Response(
        content=yaml_str,
        media_type="application/x-yaml",
        headers={"Content-Disposition": 'attachment; filename="rating_config.yaml"'}
    )

@router.post("/import")
async def import_config_yaml(
    file: UploadFile = File(...),
    dry_run: bool = Query(True),
    session: AsyncSession = Depends(db.get_session)
):
    """Import rating configuration from a YAML file."""
    try:
        content = await file.read()
        data = yaml.safe_load(content)

        result = await session.execute(select(ConfigRatingORM).where(ConfigRatingORM.id == 1))
        obj = result.scalar_one_or_none()
        if not obj:
            raise HTTPException(status_code=404, detail="Rating config not initialized")

        current_data = orm_to_dict(obj)
        diff = {}
        for k, v in data.items():
            if k in current_data and current_data[k] != v:
                diff[k] = {"old": current_data[k], "new": v}

        if dry_run:
            return {"success": True, "dry_run": True, "diff": diff}

        # Historize
        history = ConfigRatingHistoryORM(
            version=obj.version,
            change_summary="Imported from YAML",
            created_by="Import",
            **current_data
        )
        session.add(history)

        # Update
        for k, v in data.items():
            if hasattr(obj, k):
                setattr(obj, k, v)
        
        obj.version += 1
        await session.commit()
        return {"success": True, "dry_run": False, "updated_fields": list(diff.keys())}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")
