# Pushback

The brief frames the win as "automate the review process," but the LOA matrix as currently written does not allow us to automate the *review*—it only allows us to automate the *triage*.

Based on the daily batch PoC, we successfully auto-cleared 14 out of 40 trades (35%). The remaining 65% of the batch is not being resolved by the system; it is simply being *sorted into the queue a human still has to work*.

That provides real value. It saves analysts significant daily organization time, provides an instant audit log of why a trade escalated, and guarantees that no risky, high-variance, or restricted trades slip through. However, it is not "automating the review," and we should be transparent about that reality before delivery expectations are set.

The genuinely expensive analyst time is spent in L2, L3, and L4 escalations. The current matrix gives us no basis to reduce those escalations because it defines authority purely by hard notional caps and static flags.

If the real goal is to *shrink* the human review burden rather than just organize it, the higher-leverage move is instrumenting these escalations. After a few weeks of recording human decisions, we can identify sub-populations that reviewers are approving 100% of the time (e.g., L2 trades between $500k and $1M for a specific, trusted counterparty) and propose *new, evidence-backed L1 auto-clear rules* to Apex Capital.

In other words: the first version routes safely; the version that actually pays for itself learns from the routing to expand the auto-clear boundary safely. We should align on that as the real target before we scope delivery.