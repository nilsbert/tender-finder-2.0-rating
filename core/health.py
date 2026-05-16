import logging
from datetime import datetime, timezone
from typing import Dict

logger = logging.getLogger("health-tracker")

class HealthTracker:
    """
    Singleton to track the health of the Rating Microservice.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HealthTracker, cls).__new__(cls)
            cls._instance._init_tracker()
        return cls._instance

    def _init_tracker(self):
        self.start_time = datetime.now(timezone.utc)
        self.stats = {
            "total_ratings": 0,
            "avg_latency_ms": 0.0,
            "last_rating_at": None
        }

    def record_rating(self, latency_ms: float):
        self.stats["last_rating_at"] = datetime.now(timezone.utc)
        count = self.stats["total_ratings"]
        avg = self.stats["avg_latency_ms"]
        
        self.stats["total_ratings"] += 1
        self.stats["avg_latency_ms"] = (avg * count + latency_ms) / (count + 1)

    def get_status(self) -> dict:
        now = datetime.now(timezone.utc)
        uptime = (now - self.start_time).total_seconds()
        
        return {
            "status": "healthy",
            "uptime_seconds": int(uptime),
            "timestamp": now.isoformat(),
            "rating_stats": {
                "total_ratings": self.stats["total_ratings"],
                "avg_latency_ms": round(self.stats["avg_latency_ms"], 2),
                "last_rating": self.stats["last_rating_at"].isoformat() if self.stats["last_rating_at"] else None
            }
        }

tracker = HealthTracker()
