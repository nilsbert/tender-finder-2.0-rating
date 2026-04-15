# 🤝 Interaction Contracts

> **Service:** Rating MS
> **Role:** Provider (Scoring Engine)
> **Last Updated:** 2026-04-15

---

## As Provider

### [Consumer] Enriching MS
The Enriching MS sends tender data for scoring and receives relevance scores.

| Field | Contract |
| :--- | :--- |
| `total_score` | Float (0.0–100.0). Never null. |
| `title_score` | Float (0.0–100.0). Never null. |
| `matches` | Array of match objects. Never null (may be empty). |

### [Consumer] Admin Suite UI
The Admin UI reads and writes keyword configuration and threshold settings.

| Field | Contract |
| :--- | :--- |
| `keywords` | Array of keyword objects. Never null. |
| `change_summary` | Required string on every config PUT request. |

---

## As Consumer

### [Provider] Enriching MS
Rating receives tender text data for scoring.

| Expectation | Detail |
| :--- | :--- |
| `tender_id` | Non-empty, stable string. |
| `title` | Non-empty string. |
| `description` | String (may be empty). |

---
*Maintained by the Tender Finder Architectural Board*
