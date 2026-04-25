from sqlalchemy.orm import declarative_base

Base = declarative_base()
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, Integer, String
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
    sub_type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    sub_category: Mapped[str | None] = mapped_column(String(100), nullable=True)
    category: Mapped[str | None] = mapped_column(String(100), nullable=True, default="Uncategorized")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())

class ConfigORM(Base):
    """Configuration storage for service-level settings (e.g., multipliers)."""
    __tablename__ = "configs"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    value_json: Mapped[str] = mapped_column(String(4000), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class ConfigRatingORM(Base):
    """Current Rating engine configuration with precise thresholds"""
    __tablename__ = "config_rating_current"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    overall_score_threshold: Mapped[int] = mapped_column(Integer, default=70)
    title_score_threshold: Mapped[int] = mapped_column(Integer, default=50)

    version: Mapped[int] = mapped_column(Integer, default=1)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())

class ConfigRatingHistoryORM(Base):
    """Audit trail for rating configuration changes"""
    __tablename__ = "config_rating_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    overall_score_threshold: Mapped[int] = mapped_column(Integer)
    title_score_threshold: Mapped[int] = mapped_column(Integer)

    version: Mapped[int] = mapped_column(Integer)
    change_summary: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    created_by: Mapped[str] = mapped_column(String(100), default="Alex (Admin)")
