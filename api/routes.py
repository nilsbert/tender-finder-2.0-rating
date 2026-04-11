from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import httpx
import os
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["rating"])

class RateRequest(BaseModel):
    id: str
    headline: str
    description: str
    full_text: Optional[str] = None
    enrichment_locked: bool = False

@router.post("/rate")
async def rate_tender(request: RateRequest):
    """
    Endpoint to rate a tender.
    Proxies the request to the underlying qualification microservice.
    """
    QUALIFICATION_SERVICE_URL = os.getenv("QUALIFICATION_SERVICE_URL", "http://tender-qualification:8004")
    url = f"{QUALIFICATION_SERVICE_URL}/api/keywords/rate-stateless"
    
    logger.info(f"Rating request received for tender {request.id}. Forwarding to {url}")
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            payload = request.model_dump()
            # Map headline to title for qualification service
            payload["title"] = payload.pop("headline")
            
            response = await client.post(url, json=payload)
            if response.status_code != 200:
                logger.error(f"Qualification service returned error {response.status_code}: {response.text}")
                raise HTTPException(status_code=502, detail="Upstream qualification service error")
            
            return response.json()
    except Exception as e:
        logger.error(f"Failed to proxy rating request: {e}")
        raise HTTPException(status_code=500, detail=str(e))
