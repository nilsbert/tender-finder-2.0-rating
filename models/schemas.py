import uuid
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class KeywordBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    term: str
    weight: float = 1.0
    type: str = "Sector"
    sub_type: str | None = None
    sub_category: str | None = None
    category: str | None = "Uncategorized"

class KeywordCreate(KeywordBase):
    pass

class Keyword(KeywordBase):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = Field(default_factory=datetime.utcnow)

class TenderInput(BaseModel):
    """Stateless input for rating"""
    id: str
    title: str | None = None
    description: str | None = None
    full_text: str | None = None
    cpv_codes: list[str] = []

class RatedKeyword(BaseModel):
    term: str
    score: float
    category: str = "unknown"

class RatingResult(BaseModel):
    tender_id: str
    score: float
    matched_keywords: list[RatedKeyword]
    metadata: dict = {}

class RatingBatchRequest(BaseModel):
    tenders: list[TenderInput]

class RatingBatchResponse(BaseModel):
    results: list[RatingResult]

# --- Import / Export ---
class KeywordYamlModel(BaseModel):
    keywords: list[KeywordCreate]

class KeywordImportSummary(BaseModel):
    created: list[KeywordCreate]
    updated: list[KeywordCreate]
    deleted: list[Keyword]
    total_count: int

class KeywordImportResult(BaseModel):
    summary: KeywordImportSummary
    dry_run: bool
    success: bool
    message: str
