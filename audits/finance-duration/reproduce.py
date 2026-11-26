"""Synthetic financing-cost illustration. No market observations or lending terms.

Run with Python 3.9+ using only the standard library. Outputs are written beside
this file. Code: MIT. Original model inputs/outputs: CC BY 4.0.
"""
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path
import csv
import json

ROOT = Path(__file__).resolve().parent
D = Decimal
MONEY = D('0.01')


def money(value):
    return str(value.quantize(MONEY, rounding=ROUND_HALF_UP))


def generate():
    source = json.loads((ROOT / 'scenarios.json').read_text())
    principal = D(source['principal_gbp'])
    summaries, schedule = [], []
    for case in source['pricing_cases']:
        rate = D(case['assumed_nominal_annual_rate'])
        fee_rate = D(case['assumed_one_off_cash_fee_rate'])
        for months in source['equal_month_periods']:
            scenario = f"{case['id']}-{months}"
            monthly_interest = principal * rate / D(12)
            fee = principal * fee_rate
            interest_sum = D(0)
            fee_sum = D(0)
            for month in range(1, months + 1):
                interest_sum += monthly_interest
                cash_fee = fee if month == 1 else D(0)
                fee_sum += cash_fee
                repayment = principal if month == months else D(0)
                schedule.append({
                    'scenario_id': scenario, 'equal_month': month,
                    'starting_drawn_principal_gbp': money(principal),
                    'cash_interest_gbp': money(monthly_interest),
                    'separate_cash_fee_gbp': money(cash_fee),
                    'principal_repaid_at_period_end_gbp': money(repayment),
                    'finance_cost_excluding_principal_gbp': money(monthly_interest + cash_fee),
                    'cumulative_finance_cost_excluding_principal_gbp': money(interest_sum + fee_sum),
                })
            # Monthly schedule independently cross-checks the closed-form total.
            interest_formula = principal * rate * D(months) / D(12)
            assert interest_sum == interest_formula
            assert fee_sum == fee
            summaries.append({
                'scenario_id': scenario, 'pricing_case': case['id'],
                'equal_months': months, 'fully_drawn_principal_gbp': money(principal),
                'assumed_nominal_annual_rate': str(rate),
                'assumed_one_off_cash_fee_rate': str(fee_rate),
                'monthly_cash_interest_gbp': money(monthly_interest),
                'separate_cash_fee_gbp': money(fee),
                'total_cash_interest_gbp': money(interest_sum),
                'total_finance_cost_excluding_principal_gbp': money(interest_sum + fee),
                'principal_repaid_at_final_period_end_gbp': money(principal),
            })
    costs = {r['scenario_id']: D(r['total_finance_cost_excluding_principal_gbp']) for r in summaries}
    assert costs == {'A-18':D(174000),'A-19':D(183000),'A-20':D(192000),
                     'B-18':D(162000),'B-19':D(170000),'B-20':D(178000)}
    assert len(schedule) == 114
    assert all(sum(D(r['principal_repaid_at_period_end_gbp']) for r in schedule
                   if r['scenario_id'] == scenario) == principal for scenario in costs)
    assert costs['B-18'] < costs['A-18'] and costs['B-20'] < costs['A-20']
    result = {
        'pricing_saving_B_vs_A_same_18_months_gbp': money(costs['A-18'] - costs['B-18']),
        'additional_B_cost_20_vs_18_months_gbp': money(costs['B-20'] - costs['B-18']),
        'B20_excess_against_original_A18_budget_gbp': money(costs['B-20'] - costs['A-18']),
        'pricing_saving_B_vs_A_same_20_months_gbp': money(costs['A-20'] - costs['B-20']),
        'assumed_B_extra_equal_months_covered_by_18_month_pricing_saving': '1.5',
        'rows': {'summary':len(summaries), 'monthly_schedule':len(schedule)},
        'scope': 'Entirely hypothetical. Same-horizon pricing and delay-versus-original-budget comparisons are separate. Not lender quotes, a valuation, market rates, a delay forecast or a funding recommendation.'
    }
    assert D(result['pricing_saving_B_vs_A_same_18_months_gbp']) / D(8000) == D('1.5')
    for name, rows in [('scenario-summary.csv',summaries),('monthly-finance-schedule.csv',schedule)]:
        with (ROOT / name).open('w', newline='') as f:
            writer = csv.DictWriter(f,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)
    (ROOT / 'model-results.json').write_text(json.dumps(result,indent=2)+'\n')
    return summaries, result


if __name__ == '__main__':
    _, result = generate()
    print(json.dumps(result,indent=2))
