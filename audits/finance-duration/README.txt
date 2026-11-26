Development Finance: repayment duration and pricing assumptions
Author: Matt Lenzie / Construction Capital
Prepared: 26 November 2026
Research ID: CC-DF-2026Q3-A12

Entirely hypothetical. No lender quotes, market rates, loan observations,
extension permissions or delay forecasts. Case labels A/B are pricing
assumptions, not lender identities. Compare pricing cases over the same
duration. B20 versus A18 is only a comparison with an earlier assumed budget.

Run: python3 reproduce.py
Python3.9+; standard library only. Recreates the two CSV files and model-results.json.
The six summary rows and114monthly rows cross-check monthly summation with
a closed-form formula. Output CSV amounts are GBP, rounded to pence with
ROUND_HALF_UP. Calculations use Decimal and round for presentation only.
The chosen inputs produce exact penny amounts without summation differences.

Principal: GBP1,200,000, fully drawn before period1, unchanged until final
repayment. Equal periods are each1/12year. Simple interest paid separately
in cash. Fee is paid separately once in period1 and never finances interest.
Finance-cost totals exclude repayment of principal. The monthly schedule
keeps principal repayment in its own column. No actual dates are modelled.

The model omits drawdown changes, compounding, retained interest, day counts,
minimum interest, repayments before maturity, extension/exit fees, other
charges, taxes and the whole project appraisal. It grants no extension right.
Existing Q3 datasets are context only, not model inputs; frozen5October2026.

Rights: Original model, inputs, outputs and guide CC BY4.0:
https://creativecommons.org/licenses/by/4.0/
Reproduction code MIT; see LICENSE-CODE.txt. Third-party rights unchanged.
