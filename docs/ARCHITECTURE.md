# Architecture Definition: Rating Service

## Architectural Style: Analytical Scoring Engine
The Rating service operates as the "Evaluator" in the ecosystem:
- **Stateless Scoring**: Receives enriched tender data and applies weighted algorithms to generate scores.
- **Data Dependency**: Relies on the **Enriching** service for high-quality metadata.
- **Sovereign Configuration**: Owns the `rating_schemes` and `historical_benchmarks` tables.

## Technology Stack
- **Framework**: FastAPI (Async)
- **Calculations**: NumPy / Pandas (for complex scoring matrices)
- **Database**: SQLite (Development) / MSSQL (Production)
- **Testing**: Pact (as a Consumer of Enriching)

## Core Logic: The Scoring Lifecycle
1.  **Trigger**: Receives an event or request for a tender to be scored.
2.  **Data Retrieval**: Fetches enriched metadata (CPVs, labels, summary) from the **Enriching** service.
3.  **Scheme Selection**: Identifies the relevant scoring scheme based on Sector or Service.
4.  **Calculation**: Executes the weighted scoring algorithm across multiple dimensions.
5.  **Persistence**: Stores the final scores and their components in the `rating.db`.

## Scoring Dimensions
- **Strategic Fit**: Alignment with cluster and ressort goals.
- **Technical Relevancy**: Match between tender requirements and organizational labels.
- **Probability of Success (PoS)**: Based on historical win rates for similar profiles.
- **Economic Value**: Estimated margin and contract duration.

## UI Integration
Provides a **Rating Control Center** (PDS-based) for **Björn** and **Sascha** to adjust scoring weights and review historical rating performance.
