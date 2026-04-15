from dataclasses import dataclass, field
from typing import List, Optional, Dict
from enum import Enum
from models.schemas import Keyword as KeywordSchema

class MatchLocation(str, Enum):
    HEADLINE = "headline"
    DESCRIPTION = "description"
    FULL_TEXT = "full_text"

@dataclass(frozen=True)
class Match:
    keyword_term: str
    location: MatchLocation
    score_impact: float

@dataclass(frozen=True)
class ScoringResult:
    total_score: float
    title_score: float
    matches: List[Match]
    type_scores: Dict[str, float] = field(default_factory=dict)
    subtype_scores: Dict[str, float] = field(default_factory=dict)
    subcategory_scores: Dict[str, float] = field(default_factory=dict)

class ScoringPolicy:
    MULTIPLIERS = {
        MatchLocation.HEADLINE: 5.0,
        MatchLocation.DESCRIPTION: 3.0,
        MatchLocation.FULL_TEXT: 1.0
    }

    @staticmethod
    def calculate_score(tender_title: str, tender_description: str, tender_full_text: str, keywords: List[KeywordSchema]) -> ScoringResult:
        headline = (tender_title or "").lower()
        description = (tender_description or "").lower()
        full_text = (tender_full_text or "").lower()
        
        matches = []
        title_score = 0.0
        
        for kw in keywords:
            kw_matches, kw_title_impact = ScoringPolicy._match_keyword(kw, headline, description, full_text)
            matches.extend(kw_matches)
            title_score += kw_title_impact

        total_score = sum(m.score_impact for m in matches)
        aggregates = ScoringPolicy._aggregate_scores(matches, keywords)

        return ScoringResult(
            total_score=round(total_score, 2),
            title_score=round(title_score, 2),
            matches=matches,
            **aggregates
        )

    @staticmethod
    def _match_keyword(kw: KeywordSchema, headline: str, description: str, full_text: str):
        term = kw.term.lower()
        matches = []
        title_impact = 0.0
        
        # Match per location (Safe for BDD deduplication rules)
        if term in headline:
            impact = kw.weight * ScoringPolicy.MULTIPLIERS[MatchLocation.HEADLINE]
            matches.append(Match(kw.term, MatchLocation.HEADLINE, impact))
            title_impact = kw.weight
            
        if term in description:
            impact = kw.weight * ScoringPolicy.MULTIPLIERS[MatchLocation.DESCRIPTION]
            matches.append(Match(kw.term, MatchLocation.DESCRIPTION, impact))
            
        if term in full_text:
            impact = kw.weight * ScoringPolicy.MULTIPLIERS[MatchLocation.FULL_TEXT]
            matches.append(Match(kw.term, MatchLocation.FULL_TEXT, impact))
            
        return matches, title_impact

    @staticmethod
    def _aggregate_scores(matches: List[Match], keywords: List[KeywordSchema]):
        # Map term to keyword object for quick lookup
        kw_map = {kw.term: kw for kw in keywords}
        type_scores, subtype_scores, subcategory_scores = {}, {}, {}
        
        for m in matches:
            kw = kw_map.get(m.keyword_term)
            if not kw: continue
            
            kw_type = kw.type or "Sector"
            type_scores[kw_type] = round(type_scores.get(kw_type, 0.0) + m.score_impact, 2)
            
            if kw.sub_type:
                subtype_scores[kw.sub_type] = round(subtype_scores.get(kw.sub_type, 0.0) + m.score_impact, 2)
            if hasattr(kw, 'sub_category') and kw.sub_category:
                subcategory_scores[kw.sub_category] = round(subcategory_scores.get(kw.sub_category, 0.0) + m.score_impact, 2)
                
        return {
            "type_scores": type_scores,
            "subtype_scores": subtype_scores,
            "subcategory_scores": subcategory_scores
        }
