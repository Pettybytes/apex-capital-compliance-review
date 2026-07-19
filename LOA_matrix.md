# Apex Capital Partners — Limit of Authority (LOA) Matrix
_Compliance Trade Review — Summary (Mock, for practice purposes only)_

## Approval Tiers by Notional Value (USD)

| Tier | Notional Range | Approval Authority |
|---|---|---|
| 1 | $0 – $500,000 | Auto-clear (no human review required) |
| 2 | $500,001 – $5,000,000 | Senior Analyst review |
| 3 | $5,000,001 – $25,000,000 | Head of Compliance review |
| 4 | Above $25,000,000 | Head of Compliance + CIO sign-off |

## Mandatory Escalation Flags (override tier above, regardless of notional)

The following conditions **always** require Head of Compliance review, regardless of notional value:

1. **Restricted List Breach** — counterparty or instrument appears on the current restricted/watch list
2. **Related Party Transaction** — counterparty flagged as an affiliate, related fund, or employee-linked entity
3. **Late Booking** — trade booked more than 24 hours after execution timestamp
4. **Price Variance Outlier** — executed price deviates more than 3% from prevailing market price at time of execution

## Instrument-Specific Notes

- **Derivatives (swaps, options)**: Tier thresholds above apply to notional exposure, not premium paid.
- **FX Trades**: Tier thresholds apply to USD-equivalent notional at trade-date spot rate.
- **Fixed Income**: Tier thresholds apply to face value, not market value.

## Auto-Clear Exclusions

Even trades under $500,000 (Tier 1) do NOT auto-clear if any Mandatory Escalation Flag above is present. In that case, the trade routes to Head of Compliance regardless of size.

## Analyst Time Assumption

Each manual review currently takes approximately 5 minutes of analyst time. Automating Tier 1 auto-clear and correctly routing Tiers 2–4 is the primary efficiency target for this engagement.
