from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime, timezone
import uuid

class KeywordBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    term: str
    weight: float = 1.0
    type: str = "Sector"
    sub_type: Optional[str] = None
    sub_category: Optional[str] = None
    category: Optional[str] = "Uncategorized"

class KeywordCreate(KeywordBase):
    pass

class Keyword(KeywordBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TenderInput(BaseModel):
    """Stateless input for rating"""
    id: str
    title: Optional[str] = None
    description: Optional[str] = None
    full_text: Optional[str] = None
    cpv_codes: List[str] = []

class RatedKeyword(BaseModel):
    term: str
    score: float
    category: str = "unknown"

class RatingResult(BaseModel):
    tender_id: str
    score: float
    matched_keywords: List[RatedKeyword]
    metadata: dict = {}

class RatingBatchRequest(BaseModel):
    tenders: List[TenderInput]

class RatingBatchResponse(BaseModel):
    results: List[RatingResult]

# --- Import / Export ---
class KeywordYamlModel(BaseModel):
    keywords: List[KeywordCreate]

class KeywordImportSummary(BaseModel):
    created: List[KeywordCreate]
    updated: List[KeywordCreate]
    deleted: List[Keyword]
    total_count: int

class KeywordImportResult(BaseModel):
    summary: KeywordImportSummary
    dry_run: bool
    success: bool
    message: str
