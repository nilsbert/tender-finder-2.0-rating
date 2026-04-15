# 🧠 Domain Model: Rating Context

> **Context Type:** Supporting Domain
> **Sovereignty:** Full (Private Database, Independent Tests)

---

## 1. Bounded Context Purpose

The Rating context provides the **quantitative intelligence layer** of the Tender Finder system. It applies weighted keyword matching with location-aware multipliers to calculate relevance scores, enabling automated qualification of tender opportunities.

## 2. 🧱 Entities

### Keyword (Aggregate Root)
- **Identity**: Auto-generated `id`.
- **Attributes**: `term`, `weight` (float), `category`, `is_active`.
- **Behavior**: Used by the Scoring Engine to calculate relevance.
- **Invariant**: `weight` must be > 0. Duplicate `term` entries are rejected.

### ScoringResult
- **Identity**: `tender_id` + `scoring_run_id`.
- **Attributes**: `total_score`, `title_score`, `match_details`, `calculated_at`.
- **Lifecycle**: Created by the Scoring Engine, immutable after creation.

## 3. 💎 Value Objects

### MatchLocation
- **Values**: `HEADLINE`, `DESCRIPTION`, `FULL_TEXT`.
- **Purpose**: Determines the semantic context where a keyword was found.

### ScoreMultiplier
- **Constraint**: Coefficients applied to keyword weights based on `MatchLocation`.
- **Example**: Headline match = 3x, Description = 2x, Full Text = 1x.

### ScoringPolicy
- **Attributes**: `overall_score_threshold`, `title_score_threshold`.
- **Purpose**: Defines the minimum scores required for qualification.

## 4. 📝 Business Rules (Invariants)

- **Pure Calculation**: The Scoring Engine uses pure functions — no side effects during score calculation.
- **Location-Weighted Scoring**: A keyword match in the headline carries more weight than in the description or full text.
- **Threshold Gate**: Only tenders exceeding both `overall_score_threshold` and `title_score_threshold` are considered "qualified."
- **Gold Standard Seeding**: Initial keyword sets are seeded via `initial_data.py` to ensure a consistent baseline across environments.
- **Audit Trail**: Threshold configuration changes are tracked in `rating_config_history` with mandatory `change_summary`.

---
*Maintained by the Tender Finder Architectural Board*
