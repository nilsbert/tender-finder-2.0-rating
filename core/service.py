import logging
from typing import List
from .scoring import ScoringPolicy
from models.schemas import TenderInput, RatingResult, RatedKeyword, Keyword

logger = logging.getLogger(__name__)

class RatingEngine:
    """
    Stateless engine for rating tenders against keywords.
    """
    
    def rate_batch(self, tenders: List[TenderInput], keywords: List[Keyword]) -> List[RatingResult]:
        """Rate multiple tenders in parallel using a provided keyword list."""
        results = []
        for tender in tenders:
            result = self.rate_single(tender, keywords)
            results.append(result)
            
        return results

    def rate_single(self, tender: TenderInput, keywords: List[Keyword]) -> RatingResult:
        """
        Core rating logic. 
        Matches tender text against weights and terms.
        """
        scoring_result = ScoringPolicy.calculate_score(
            tender_title=tender.title,
            tender_description=tender.description,
            tender_full_text=tender.full_text or "",
            keywords=keywords
        )
        
        matched_results = [
            RatedKeyword(
                term=m.keyword_term,
                score=m.score_impact,
                category=m.location.value
            ) for m in scoring_result.matches
        ]
            
        return RatingResult(
            tender_id=tender.id,
            score=scoring_result.total_score,
            matched_keywords=matched_results,
            metadata={
                "title_score": scoring_result.title_score,
                "type_scores": scoring_result.type_scores,
                "subtype_scores": scoring_result.subtype_scores
            }
        )

rating_engine = RatingEngine()
