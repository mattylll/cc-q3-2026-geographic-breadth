"""Reproduce an illustrative cash requirement; no loan, interest or tax model."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CASES = {
    'late_receipts': ('All sales in month 12', {12: 10}),
    'phased_receipts': ('Phased sales from month 7', {7: 2, 8: 2, 9: 2, 10: 2, 12: 2}),
    'phased_two_months_later': ('Phased receipts two months later', {9: 2, 10: 2, 11: 2, 12: 2, 14: 2}),
}


def calculate():
    rows, summaries = [], []
    for case, (label, sales) in CASES.items():
        balance = cumulative_cost = cumulative_receipts = 0
        peak = peak_month = 0
        end_peak = 0
        for month in range(15):
            cost = 1_000_000 if month == 0 else 240_000 if month <= 10 else 0
            receipts = sales.get(month, 0) * 400_000
            before = balance - cost
            deficit = max(0, -before)
            if deficit > peak:
                peak, peak_month = deficit, month
            balance = before + receipts
            end_peak = max(end_peak, -balance)
            cumulative_cost += cost
            cumulative_receipts += receipts
            rows.append(dict(data_type='hypothetical_scenario', scenario=case, month=month,
                             project_costs_gbp=cost, sales_receipts_gbp=receipts,
                             cumulative_costs_gbp=cumulative_cost,
                             cumulative_receipts_gbp=cumulative_receipts,
                             cash_after_costs_before_receipts_gbp=before,
                             cash_at_month_end_gbp=balance,
                             pre_receipt_cash_deficit_gbp=deficit))
        summaries.append(dict(data_type='hypothetical_scenario', scenario=case, label=label,
                              first_receipt_month=min(sales), last_receipt_month=max(sales),
                              total_receipts_gbp=cumulative_receipts, total_project_costs_gbp=cumulative_cost,
                              surplus_before_finance_and_tax_gbp=balance,
                              peak_pre_receipt_cash_deficit_gbp=peak, first_peak_month=peak_month,
                              peak_month_end_cash_deficit_gbp=end_peak))
    return rows, summaries


def main():
    rows, summaries = calculate()
    for name, data in [('monthly_cashflows.csv', rows), ('scenario_summary.csv', summaries)]:
        with (ROOT / name).open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(data[0]), lineterminator='\n')
            writer.writeheader()
            writer.writerows(data)
    print(json.dumps({'months': len(rows), 'scenarios': summaries}, indent=2))


if __name__ == '__main__':
    main()
