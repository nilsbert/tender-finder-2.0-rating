import re
import logging
from dataclasses import dataclass, field
from enum import Enum
from models.schemas import Keyword as KeywordSchema

# Try to import NLTK for better stemming, fallback to basic if not available
try:
    from nltk.stem.snowball import SnowballStemmer
    german_stemmer = SnowballStemmer("german")
    english_stemmer = SnowballStemmer("english")
except ImportError:
    german_stemmer = None
    english_stemmer = None

logger = logging.getLogger(__name__)

class MatchLocation(str, Enum):
    HEADLINE = "headline"
    DESCRIPTION = "description"
    FULL_TEXT = "full_text"

@dataclass(frozen=True)
class Match:
    keyword_term: str
    location: MatchLocation
    score_impact: float
    entity_type: str = "Sector"
    entity_name: str = "Unknown"

@dataclass(frozen=True)
class ScoringResult:
    total_score: float
    title_score: float
    matches: list[Match]
    type_scores: dict[str, float] = field(default_factory=dict)
    subtype_scores: dict[str, float] = field(default_factory=dict)
    subcategory_scores: dict[str, float] = field(default_factory=dict)

class ScoringPolicy:
    MULTIPLIERS = {
        MatchLocation.HEADLINE: 5.0,
        MatchLocation.DESCRIPTION: 3.0,
        MatchLocation.FULL_TEXT: 1.0
    }

    @staticmethod
    def calculate_score(tender_title: str, tender_description: str, tender_full_text: str, keywords: list[KeywordSchema]) -> ScoringResult:
        headline = tender_title or ""
        description = tender_description or ""
        full_text = tender_full_text or ""

        matches = []
        title_score = 0.0

        # 1. Deduplicate keywords by term, keeping the one with the highest weight
        # This ensures that even if 'SAP' is in the taxonomy multiple times, it only counts once.
        unique_keywords = {}
        for kw in keywords:
            term_lower = kw.term.strip().lower()
            if term_lower not in unique_keywords or kw.weight > unique_keywords[term_lower].weight:
                unique_keywords[term_lower] = kw

        # 2. Match each unique keyword
        for kw in unique_keywords.values():
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
        term = kw.term.strip()
        
        # 1. Exact/Plural Match Pattern (Handles SAP vs Sapphire)
        escaped_term = re.escape(term)
        # Suffixes: e, s, en, er, es, n (German/English)
        pattern = re.compile(rf"\b{escaped_term}(?:e|s|en|er|es|n)?\b", re.IGNORECASE)
        
        # 2. Stemming-based fallback for complex inflections (e.g. Strategy -> Strategies)
        stem_patterns = []
        for stemmer in [german_stemmer, english_stemmer]:
            if stemmer and len(term) > 3:
                stem = stemmer.stem(term)
                if stem != term.lower() and len(stem) > 2:
                    stem_patterns.append(re.compile(rf"\b{re.escape(stem)}[a-z]{{0,5}}\b", re.IGNORECASE))

        matches = []
        title_impact = 0.0

        def check_match(text: str) -> bool:
            if pattern.search(text): return True
            for sp in stem_patterns:
                if sp.search(text): return True
            return False

        # 3. Match per location - EXCLUSIVE (Every match counts only once per keyword)
        # Priority: Headline > Description > Full Text
        if check_match(headline):
            impact = kw.weight * ScoringPolicy.MULTIPLIERS[MatchLocation.HEADLINE]
            matches.append(Match(
                keyword_term=kw.term, 
                location=MatchLocation.HEADLINE, 
                score_impact=impact,
                entity_type=kw.type or "Sector",
                entity_name=kw.sub_type or "General"
            ))
            title_impact = kw.weight
        elif check_match(description):
            impact = kw.weight * ScoringPolicy.MULTIPLIERS[MatchLocation.DESCRIPTION]
            matches.append(Match(
                keyword_term=kw.term, 
                location=MatchLocation.DESCRIPTION, 
                score_impact=impact,
                entity_type=kw.type or "Sector",
                entity_name=kw.sub_type or "General"
            ))
        elif check_match(full_text):
            impact = kw.weight * ScoringPolicy.MULTIPLIERS[MatchLocation.FULL_TEXT]
            matches.append(Match(
                keyword_term=kw.term, 
                location=MatchLocation.FULL_TEXT, 
                score_impact=impact,
                entity_type=kw.type or "Sector",
                entity_name=kw.sub_type or "General"
            ))

        return matches, title_impact


    @staticmethod
    def _aggregate_scores(matches: list[Match], keywords: list[KeywordSchema]):
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
