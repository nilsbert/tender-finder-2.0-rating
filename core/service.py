import logging
import time

from models.schemas import Keyword, RatedKeyword, RatingResult, TenderInput

from .scoring import ScoringPolicy

logger = logging.getLogger(__name__)

class RatingEngine:
    """
    Stateless engine for rating tenders against keywords.
    """

    def rate_batch(self, tenders: list[TenderInput], keywords: list[Keyword]) -> list[RatingResult]:
        """Rate multiple tenders in parallel using a provided keyword list."""
        start_time = time.time()
        results = []
        for tender in tenders:
            result = self.rate_single(tender, keywords)
            results.append(result)

        duration = time.time() - start_time
        logger.info(f"⚖️ Batch rating of {len(tenders)} tenders took {duration:.4f}s")
        return results

    def rate_single(self, tender: TenderInput, keywords: list[Keyword]) -> RatingResult:
        """
        Core rating logic.
        Matches tender text against weights and terms.
        """
        start_time = time.time()
        scoring_result = ScoringPolicy.calculate_score(
            tender_title=tender.title,
            tender_description=tender.description,
            tender_full_text=tender.full_text,
            keywords=keywords
        )

        matched_results = [
            RatedKeyword(
                term=m.keyword_term,
                score=m.score_impact,
                category=m.location.value
            ) for m in scoring_result.matches
        ]

        result = RatingResult(
            tender_id=tender.id,
            score=scoring_result.total_score,
            matched_keywords=matched_results,
            metadata={
                "title_score": scoring_result.title_score,
                "type_scores": scoring_result.type_scores,
                "subtype_scores": scoring_result.subtype_scores
            }
        )
        duration = time.time() - start_time
        logger.debug(f"⚖️ Rating single tender {tender.id} took {duration:.4f}s")
        return result

rating_engine = RatingEngine()
