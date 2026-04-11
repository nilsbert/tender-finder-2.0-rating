from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
import uuid

class KeywordBase(BaseModel):
    term: str
    weight: float = 1.0
    type: str = "Sector"
    sub_type: Optional[str] = None
    sub_category: Optional[str] = None
    category: Optional[str] = "Uncategorized"

class KeywordCreate(KeywordBase):
    pass

class Keyword(KeywordBase):
    """
    Minimal Keyword model for parity in the monolith's sourcing domain.
    The source of truth is now in the qualification microservice.
    """
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    multiplier: float = 1.0
    location: str = "description"
    created_at: datetime = Field(default_factory=datetime.utcnow)
