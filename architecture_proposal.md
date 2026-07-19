# Architecture Proposal — Apex Capital Compliance Trade Review

**Goal:** Remove repetitive triage work by auto-clearing unambiguous L1 exceptions (35% of daily volume based on the PoC) and correctly routing everything else, while ensuring the Head of Compliance + CIO (L4) and Head of Compliance (L3) capture every necessary escalation.

## Principle: Automate the *clearing*, never the *judgment*

The system only takes work *away* from humans by auto-clearing cases that are genuinely unambiguous: Notional <= $500k with no mandatory escalation flags (pricing, restricted list, related party, or timing violations). Every other trade is *routed* to the correct authority.

## Required Data Sources

| Source | Used for | Freshness Need |
|---|---|---|
| Daily Exception Batch (CSV) | Ingestion of trades to review | Batch, Morning |
| LOA Matrix Policy | Deterministic routing limits | Versioned |

## End-to-End Flow

1. **INGEST + VALIDATE:** Pydantic strictly types each row and calculates derived fields (Price Variance %, Booking Delay). Rows that fail validation are escalated to a human rather than auto-tiered — the LOA matrix does not define routing for malformed data, so the exact queue is flagged as an open question for the customer session.
2. **PHASE 1 (MANDATORY FLAGS → L3):** Qualitative flags are checked *first*, before notional: Restricted List `Y`, Related Party `Y`, Booking Time > 24h, or Price Variance > 3%. Any flag routes the trade to Head of Compliance (L3), regardless of notional. This ordering enforces the LOA's Auto-Clear Exclusions — a flagged trade never auto-clears, even under $500k.
3. **PHASE 2 (L4 — HIGH NOTIONAL):** For unflagged trades, Notional > $25M escalates to L4 (Head of Compliance + CIO sign-off).
4. **PHASE 3 (L3 — MID NOTIONAL):** For unflagged trades, Notional > $5M escalates to L3 (Head of Compliance).
5. **PHASE 4 (L2 — LOWER NOTIONAL):** For unflagged trades, Notional > $500k routes to L2 reviewers.
6. **PHASE 5 (L1 ELIGIBILITY):** Remaining trades (<= $500k, no flags) are marked `AUTO_CLEAR`. An immutable decision, tier, and explicit reason is emitted for every trade for regulatory audit.

## Failure Modes & System Responses

**Design rule:** False escalations are an operational cost; false clears are a regulatory breach. Every failure mode therefore fails *closed* — toward human review, never toward auto-clear.

1. **Bad / missing field (non-numeric notional, price <= 0, etc.):** Row fails Pydantic validation → escalated to a human for manual inspection, not auto-tiered (a row that cannot be parsed cannot be reliably sized). Exact routing queue is an open customer question.
2. **Null / unparseable timestamps:** Fails validation at ingest (the timestamp coercion step), so the row never reaches the booking-delay check → handled as a bad-field escalation per item 1, not assigned a notional tier.
3. **Zero or negative market price:** Rejected by the `market_price > 0` validation constraint before any variance division occurs → handled as a bad-field escalation per item 1. (This also prevents a divide-by-zero in the variance calculation by construction.)