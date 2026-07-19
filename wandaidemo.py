import csv
import sys
from datetime import datetime, timezone
from typing import Tuple
from pydantic import BaseModel, Field, field_validator, ValidationError

def _parse_ts(value: str) -> datetime:
    return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone(timezone.utc)

class Trade(BaseModel):
    trade_id: str
    execution_timestamp: datetime
    booking_timestamp: datetime
    notional_usd: float = Field(ge=0)
    executed_price: float = Field(gt=0)
    market_price_at_execution: float = Field(gt=0)
    restricted_list_flag: bool
    related_party_flag: bool

    @field_validator("restricted_list_flag", "related_party_flag", mode="before")
    @classmethod
    def _yn_to_bool(cls, v: object) -> bool:
        return str(v).strip().upper() in {"Y", "YES", "TRUE", "1"}

    @field_validator("execution_timestamp", "booking_timestamp", mode="before")
    @classmethod
    def _coerce_ts(cls, v: object) -> datetime:
        return _parse_ts(str(v)) if isinstance(v, str) else v

def evaluate_trade(trade: Trade) -> Tuple[str, str, str]:
    reasons = []

    if trade.restricted_list_flag: reasons.append("restricted-list breach")
    if trade.related_party_flag: reasons.append("related-party transaction")

    hours_to_book = (trade.booking_timestamp - trade.execution_timestamp).total_seconds() / 3600
    if hours_to_book > 24.0: reasons.append(f"late booking ({hours_to_book:.1f}h)")

    variance_pct = abs(trade.executed_price - trade.market_price_at_execution) / trade.market_price_at_execution * 100
    if variance_pct > 3.0: reasons.append(f"price variance {variance_pct:.1f}% > 3%")

    # Mandatory flags strictly route to L3 — the LOA does not define an L4 override for flags.
    # Whether compounding flags should escalate further to L4 is an open question for the
    # customer (see customer_questions.md, Q3) — not decided in code.
    if reasons:
        return "ESCALATE", "L3", "Mandatory escalation: " + "; ".join(reasons)

    if trade.notional_usd > 25000000:
        return "ESCALATE", "L4", f"Tier 4 (${trade.notional_usd:,.0f}) exceeds L3 cap."
    if trade.notional_usd > 5000000:
        return "ESCALATE", "L3", f"Tier 3 (${trade.notional_usd:,.0f}) exceeds auto-clear threshold."
    if trade.notional_usd > 500000:
        return "ESCALATE", "L2", f"Tier 2 (${trade.notional_usd:,.0f}) exceeds auto-clear threshold."

    return "AUTO_CLEAR", "L1", f"Tier 1 (${trade.notional_usd:,.0f} <= $500,000), clean."

def main():
    auto, esc = 0, 0
    try:
        with open("exceptions.csv", "r", encoding="utf-8-sig") as f:
            for i, row in enumerate(csv.DictReader(f), 1):
                try:
                    t = Trade(**row)
                    dec, tier, rsn = evaluate_trade(t)
                    if dec == "AUTO_CLEAR": auto += 1
                    else: esc += 1
                    print(f"{t.trade_id:<12} | {dec:<12} | {tier:<3} | {rsn}")
                except ValidationError as e:
                    esc += 1
                    print(f"ROW-{i} INVALID | {e.errors()[0]['msg']}")
    except FileNotFoundError:
        sys.exit("Error: exceptions.csv not found.")

    print(f"\nTotal: {auto + esc} | Auto-Cleared: {auto} | Escalated: {esc}")

if __name__ == "__main__":
    main()
