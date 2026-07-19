# Apex Capital Compliance Trade Review (PoC)

Proof of concept for automating the daily flagged trade review against the Limit of Authority (LOA) matrix. Automatically clears unambiguous Level 1 (L1) cases, routes everything else to the correct human authority (L2, L3, or L4), and records an auditable reason for every decision.

## Contents
* `architecture_proposal.md` one page end to end design, failure modes, and system architecture.
* `wandaidemo.py` working core mechanic (stdlib + Pydantic, no pandas or frameworks).
* `customer_questions.md` six targeted questions addressing genuine ambiguity discovered in the dataset, policy, and production delivery boundary.
* `pushback.md` strategic pushback on the core premise of "automating the review."
* `exceptions.csv` daily exception batch.
* `LOA_matrix.md` the approval policy this engine implements.

## Run Instructions
```bash
pip install pydantic
python wandaidemo.py
```

## Posture and Scope

This system automates the *triage*. It automatically clears L1 standard bounds (<= $500k Notional, no flags) and routes L2, L3, and L4 escalations to humans. It calculates specific derived fields (like >3% price variance and >24hr booking delays). It does **not** employ AI to make subjective compliance judgments, by design.

**Escalation ordering:** Mandatory qualitative flags (Restricted List, Related Party, Late Booking, Price Variance) are checked *before* notional size. Any flagged trade routes to Head of Compliance (L3), exactly as the LOA matrix specifies, regardless of dollar amount. Notional based tiers (L2, L3, or L4) apply only to trades that carry no mandatory flags.

**Failsafe posture:** A row that fails Pydantic validation is escalated to a human for manual inspection, never silently bypassed or automatically cleared. It is deliberately *not* assigned a notional tier, because a row that cannot be parsed cannot be reliably sized. The exact human queue for malformed data is raised as an open question for the customer (see `customer_questions.md`).

## Projected Business Impact (ROI)

The brief establishes the customer's daily baseline: ~40 flagged trades each morning at ~5 minutes of analyst time per review, roughly 200 minutes (~3.3 hours) of senior analyst capacity spent on triage per day.

On the PoC batch, the engine automatically cleared 14 of 40 trades (35%), returning that share of the daily review load:

* **Daily:** ~70 minutes of analyst capacity returned (35% of the ~200 minute load)
* **Weekly:** ~5.8 hours
* **Annually:** ~294 hours (assuming the standard 252 trading day year)

**Note on scaling:** This is the *baseline*, day one value from automatically clearing unambiguous L1s. The larger opportunity is instrumenting the L2 through L4 escalations, then using that decision data to propose new, evidence backed auto clear rules, safely expanding the 35% boundary over time without adding regulatory risk (see `pushback.md`).