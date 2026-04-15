from fastapi import APIRouter, HTTPException, Depends, UploadFile, File, Query, Response, status
from typing import List, Optional
import json
import yaml
from sqlalchemy.ext.asyncio import AsyncSession

from core.database import db
from core.repository import RatingRepository
from core.service import rating_engine
from models.schemas import (
    TenderInput, RatingResult, RatingBatchRequest, RatingBatchResponse, 
    Keyword, KeywordCreate, KeywordYamlModel, KeywordImportResult, KeywordImportSummary
)

router = APIRouter(prefix="/api", tags=["rating"])

# --- Dependencies ---

async def get_repository(session: AsyncSession = Depends(db.get_session)):
    return RatingRepository(session)

# --- Scoring Endpoints (Stateless) ---

@router.post("/rate", response_model=RatingResult)
async def rate_single_tender(tender: TenderInput, repo: RatingRepository = Depends(get_repository)):
    """
    Rate a single tender. Returns scores and matched keywords.
    Does NOT persist any tender information.
    """
    async with repo.session.begin():
        # Fetch keywords from repo for the engine
        db_keywords = await repo.get_all_keywords()
        
        # Map ORM to Schema for the engine
        keywords = [
            Keyword(
                id=k.id,
                term=k.term,
                weight=k.weight,
                type=k.type,
                category=k.category,
                sub_type=k.sub_type,
                sub_category=k.sub_category,
                created_at=k.created_at
            ) for k in db_keywords
        ]
        
        return rating_engine.rate_single(tender, keywords)

@router.post("/rate-batch", response_model=RatingBatchResponse, dependencies=[Depends(db.get_session)])
async def rate_tenders_batch(request: RatingBatchRequest, repo: RatingRepository = Depends(get_repository)):
    """
    Rate a list of tenders. Returns results for each tender.
    Does NOT persist any tender information.
    """
    async with repo.session.begin():
        db_keywords = await repo.get_all_keywords()
        keywords = [Keyword.model_validate(k, from_attributes=True) for k in db_keywords]
        results = rating_engine.rate_batch(request.tenders, keywords)
        return RatingBatchResponse(results=results)

# --- Keyword Management Endpoints ---

@router.get("/keywords", response_model=List[Keyword])
async def list_keywords(repo: RatingRepository = Depends(get_repository)):
    """Retrieve all keywords."""
    async with repo.session.begin():
        orms = await repo.get_all_keywords()
        return [Keyword.model_validate(o, from_attributes=True) for o in orms]

@router.get("/keywords/categories", response_model=List[str])
async def list_categories(repo: RatingRepository = Depends(get_repository)):
    """Retrieve all unique keyword sub-types/categories."""
    async with repo.session.begin():
        return await repo.get_categories()

@router.get("/keywords/tree")
async def get_keyword_tree(repo: RatingRepository = Depends(get_repository)):
    """Retrieve keyword tree structure (Type -> Sub-type hierarchy)."""
    async with repo.session.begin():
        return await repo.get_keyword_tree()

@router.post("/keywords", response_model=Keyword, status_code=status.HTTP_201_CREATED)
async def create_keyword(kw: KeywordCreate, repo: RatingRepository = Depends(get_repository)):
    """Create a new keyword."""
    async with repo.session.begin():
        existing = await repo.get_keyword_by_term(kw.term)
        if existing:
            raise HTTPException(status_code=409, detail=f"Keyword '{kw.term}' already exists.")
            
        orm = await repo.add_keyword(**kw.model_dump())
        await repo.session.flush()
        return Keyword.model_validate(orm, from_attributes=True)

@router.put("/keywords/{keyword_id}", response_model=Keyword)
async def update_keyword(keyword_id: str, kw_input: KeywordCreate, repo: RatingRepository = Depends(get_repository)):
    """Update an existing keyword."""
    async with repo.session.begin():
        updated = await repo.update_keyword(keyword_id, **kw_input.model_dump())
        if not updated:
            raise HTTPException(status_code=404, detail="Keyword not found")
        return Keyword.model_validate(updated, from_attributes=True)

@router.delete("/keywords/{keyword_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_keyword(keyword_id: str, repo: RatingRepository = Depends(get_repository)):
    """Delete a keyword."""
    async with repo.session.begin():
        await repo.delete_keyword(keyword_id)
        return Response(status_code=status.HTTP_204_NO_CONTENT)

# --- Import / Export ---

@router.get("/keywords/export", response_class=Response)
async def export_keywords_yaml(repo: RatingRepository = Depends(get_repository)):
    """Download all keywords as a YAML file."""
    async with repo.session.begin():
        orms = await repo.get_all_keywords()
        
        export_data = {
            "keywords": [
                {
                    "term": k.term,
                    "weight": k.weight,
                    "type": k.type,
                    "sub_type": k.sub_type,
                    "sub_category": k.sub_category,
                    "category": k.category
                }
                for k in orms
            ]
        }
        
        yaml_str = yaml.dump(export_data, sort_keys=False, allow_unicode=True)
        
        return Response(
            content=yaml_str,
            media_type="application/x-yaml",
            headers={"Content-Disposition": 'attachment; filename="rating_keywords.yaml"'}
        )

@router.post("/keywords/import", response_model=KeywordImportResult)
async def import_keywords_file(
    file: UploadFile = File(...),
    dry_run: bool = Query(True),
    delete_missing: bool = Query(False),
    repo: RatingRepository = Depends(get_repository)
):
    """
    Import keywords from YAML or JSON file.
    Supports Dry Run and Sync/Merge modes.
    """
    try:
        content = await file.read()
        data = yaml.safe_load(content) if not file.filename.endswith(".json") else json.loads(content)
        parsed = KeywordYamlModel(**data)
        
        uploaded_keywords = parsed.keywords
        
        async with repo.session.begin():
            current_orms = await repo.get_all_keywords()
            current_map = {k.term.lower(): k for k in current_orms}
            
            created, updated, deleted = [], [], []
            
            for up_kw in uploaded_keywords:
                term_key = up_kw.term.lower()
                if term_key not in current_map:
                    created.append(up_kw)
                else:
                    existing = current_map[term_key]
                    if (existing.weight != up_kw.weight or existing.type != up_kw.type or 
                        existing.sub_type != up_kw.sub_type or existing.category != up_kw.category):
                        updated.append(up_kw)
            
            summary = KeywordImportSummary(created=created, updated=updated, deleted=[], total_count=len(uploaded_keywords))
            
            if dry_run:
                return KeywordImportResult(summary=summary, dry_run=True, success=True, message="Dry run successful.")
                
            uploaded_terms = {k.term.lower() for k in uploaded_keywords}
            if delete_missing:
                for curr_kw in current_orms:
                    if curr_kw.term.lower() not in uploaded_terms:
                        await repo.delete_keyword(curr_kw.id)
            
            for c in created: await repo.add_keyword(**c.model_dump())
            for u in updated:
                existing = current_map[u.term.lower()]
                await repo.update_keyword(existing.id, **u.model_dump())
                
            return KeywordImportResult(summary=summary, dry_run=False, success=True, message="Import successful.")
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=400, detail=f"Import failed: {str(e)}")
