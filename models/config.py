from sqlalchemy import String, Integer, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from .database import Base

class ConfigRatingORM(Base):
    """Current Rating engine configuration"""
    __tablename__ = "config_rating_current"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, default=1)
    overall_score_threshold: Mapped[int] = mapped_column(Integer, default=70)
    title_score_threshold: Mapped[int] = mapped_column(Integer, default=50)
    
    version: Mapped[int] = mapped_column(Integer, default=1)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class ConfigRatingHistoryORM(Base):
    """Audit trail for rating configuration changes"""
    __tablename__ = "config_rating_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    overall_score_threshold: Mapped[int] = mapped_column(Integer)
    title_score_threshold: Mapped[int] = mapped_column(Integer)
    
    version: Mapped[int] = mapped_column(Integer)
    change_summary: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    created_by: Mapped[str] = mapped_column(String(100), default="Alex (Admin)")
