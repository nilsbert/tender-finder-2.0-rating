import httpx
import logging
import os
from typing import List, Optional
from .models import Keyword

logger = logging.getLogger(__name__)

# Use host 'qualification' if inside Docker, or localhost if running locally.
QUALIFICATION_SERVICE_URL = os.getenv("QUALIFICATION_SERVICE_URL", "http://qualification:8002")

class RatingService:
    """
    Proxy service in the monolith that forwards rating requests
    to the decoupled Qualification Microservice.
    """
    
    @staticmethod
    async def rate_tender(tender, keywords: List[Keyword] = None):
        """
        Calculates score by calling the qualification microservice.
        Updates the tender object's score and matched_keywords in place.
        """
        try:
            # We ignore the 'keywords' argument in the proxy because the
            # microservice uses its own local keywords source of truth.
            
            # 1. Prepare payload for the stateless endpoint
            payload = {
                "id": tender.id,
                "title": tender.headline,
                "description": tender.description,
                "full_text": tender.full_text,
                "enrichment_locked": getattr(tender, "enrichment_locked", False)
            }
            
            # 2. Call the microservice
            url = f"{QUALIFICATION_SERVICE_URL}/api/keywords/rate-stateless"
            logger.info(f"Forwarding rating request for tender {tender.id} to {url}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(url, json=payload)
                
                if response.status_code != 200:
                    logger.error(f"Qualification microservice returned {response.status_code}: {response.text}")
                    return tender
                
                result = response.json()
                
                # 3. Apply results to the monolith tender object
                tender.score = float(result.get("score", 0.0))
                # Map back to monolith's expected field names if necessary
                if hasattr(tender, 'rating_total'):
                    tender.rating_total = float(result.get("rating_total", tender.score))
                
                # Monolith expects list of dicts for matched_keywords
                tender.matched_keywords = result.get("matched_keywords", [])
                
                logger.info(f"✓ Tender {tender.id} rated by microservice. Score: {tender.score}")
                return tender
                
        except Exception as e:
            logger.error(f"Failed to rate tender via microservice: {e}", exc_info=True)
            return tender

    # Mock/Dummy implementation of internal rerate if needed
    @staticmethod
    def _calculate_score(tender, keywords):
        """LEGACY: This is no longer used but some older code might still reference it."""
        # Returns a dummy 6-tuple to satisfy old signatures during transition
        return (0.0, {}, [], {}, {}, {})

# Singleton instance for the monolith
rating_service = RatingService()
