from sqlalchemy.orm import declarative_base
Base = declarative_base()
from datetime import datetime
from typing import Optional
import uuid

from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

class KeywordORM(Base):
    """
    Sovereign Rating Microservice - Scoring Policy Model.
    This microservice owns the scoring criteria (keywords).
    """
    __tablename__ = "keywords"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    term: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    weight: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    type: Mapped[str] = mapped_column(String(50), nullable=False, default="Sector") # Sector, Service, Exclusion
    sub_type: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    sub_category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    category: Mapped[Optional[str]] = mapped_column(String(100), nullable=True, default="Uncategorized")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

class ConfigORM(Base):
    """Configuration storage for service-level settings (e.g., multipliers)."""
    __tablename__ = "configs"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    value_json: Mapped[str] = mapped_column(String(4000), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
