"""Reproduce a hypothetical cost reconciliation. Code licence: MIT."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
BASE = 2_000_000
ALLOWANCE = 100_000
ADDITIONS = [
    {"item_id": "EX01", "description": "Previously omitted work now confirmed", "incremental_gbp": 35_000},
    {"item_id": "EX02", "description": "Confirmed specification change", "incremental_gbp": 25_000},
    {"item_id": "EX03", "description": "Utility connection increment above original provision", "incremental_gbp": 20_000},
]
STRESS = 60_000
budget = BASE + ALLOWANCE
confirmed = sum(x["incremental_gbp"] for x in ADDITIONS)
forecast = BASE + confirmed
result = {
    "research_id": "CC-DF-2026Q3-A10",
    "classification": "Hypothetical illustration, not observed project data",
    "currency": "GBP",
    "original_base_gbp": BASE,
    "original_contingency_gbp": ALLOWANCE,
    "original_budget_gbp": budget,
    "confirmed_additions": ADDITIONS,
    "confirmed_additions_gbp": confirmed,
    "updated_forecast_gbp": forecast,
    "remaining_headroom_gbp": budget - forecast,
    "headroom_pct_original_base": 100 * (budget - forecast) / BASE,
    "headroom_pct_updated_forecast": 100 * (budget - forecast) / forecast,
    "additional_stress_gbp": STRESS,
    "stressed_forecast_gbp": forecast + STRESS,
    "stressed_budget_excess_gbp": max(0, forecast + STRESS - budget),
    "exclusions": ["land", "professional fees", "finance", "sales costs", "tax", "funding availability", "payment timing", "risk probabilities"],
    "licence": "CC BY 4.0",
}
assert confirmed == 80_000 and result["remaining_headroom_gbp"] == 20_000
assert result["stressed_budget_excess_gbp"] == 40_000
(ROOT / "backing").mkdir(exist_ok=True)
(ROOT / "backing" / "worked-example.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps({k: result[k] for k in ["confirmed_additions_gbp", "remaining_headroom_gbp", "stressed_budget_excess_gbp"]}))
