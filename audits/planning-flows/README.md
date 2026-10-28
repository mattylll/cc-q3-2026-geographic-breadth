# More decisions per receipt, but fewer decisions

Matt Lenzie / Construction Capital | CC-DF-2026Q3-A04 | 28 October 2026

This supporting methods adaptation compares separate receipt and known-decision flows in the public ICPSR study CC-DF-2026Q3-01. It adds no new observations or independent study. It is separate from the approved-unit-mention analysis at the repository root.

Source record: https://www.icpsr.umich.edu/sites/icpsr/view/studies/317061/versions/V1

The 24-row input is unchanged from the frozen 5 October 2026 edition. It covers a matched 253-authority panel, not a national census. There are seven custom regional groups and three selected quarters. The Wales group contains seven authorities.

## Reproduce

Run `python3 reproduce.py --output reproduced` from this folder. Python 3 standard library only. Compare the two CSV files with `derived/`. No account, private repository or credentials are needed. This does not rebuild the source extraction process.

Outputs: 24 flow-comparison rows and eight year-on-year balance-change decompositions. Panel Q3 2026: 8,082 receipts, 8,750 known decisions, balance +668, ratio 108.265281 per 100 receipts. The Q3 year-on-year balance change is +1,960 = -911 from fewer decisions +2,871 from fewer receipts.

## Interpretation

Known decisions are approvals plus refusals. They exclude withdrawals and explicitly unknown outcomes. Receipt and decision rows do not track the same application cohort. A ratio above 100 is possible and is neither an approval probability nor a speed measure. Without a complete stock reconciliation, the balance is not a measured backlog change. Missing cases, timing, application mix and coverage remain unresolved.

Source/component rights are in LICENSE.txt. Planning source rights remain with their holders. No blanket OGL or CC0 claim is made. Original adaptation and chart CC BY 4.0; original reproduction code MIT.
