import pytest
from core.scoring import ScoringPolicy
from models.schemas import Keyword

def test_word_boundary_issue():
    # Setup keyword "SAP"
    kw = Keyword(id="1", term="SAP", weight=2.0, type="Service")
    
    # Tender containing "sapphire" (should NOT match SAP anymore)
    title = "Sapphire Implementation"
    description = "This project uses sapphire stones."
    
    result = ScoringPolicy.calculate_score(title, description, "", [kw])
    
    print(f"\nScore for SAP in Sapphire: {result.total_score}")
    assert result.total_score == 0, "SAP should NOT match Sapphire"

def test_plural_issue():
    # Setup keyword "Strategy"
    kw = Keyword(id="2", term="Strategy", weight=1.0, type="Service")
    
    # Tender containing "Strategies" (should match via inflection suffix)
    title = "Business Strategies 2024"
    
    result = ScoringPolicy.calculate_score(title, "", "", [kw])
    print(f"Score for Strategy in Strategies: {result.total_score}")
    assert result.total_score == 5.0, "Strategy should match Strategies via title multiplier"

def test_german_inflection():
    # Setup keyword "Beratung" (Consulting)
    kw = Keyword(id="3", term="Beratung", weight=1.0, type="Service")
    
    # Tender containing "Beratungen" (plural)
    title = "IT Beratungen"
    
    result = ScoringPolicy.calculate_score(title, "", "", [kw])
    print(f"Score for Beratung in Beratungen: {result.total_score}")
    assert result.total_score == 5.0, "German plural should match"
