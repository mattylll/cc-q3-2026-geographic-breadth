# When the active-lender threshold changes the headline

Matt Lenzie / Construction Capital. Prepared 29 October 2026. CC-DF-2026Q3-P07.

This analytical adaptation uses the 28 public aggregate rows in CC-DF-2026Q3-02, source edition fixed on 5 October 2026, at https://doi.org/10.7910/DVN/EK56EQ . It adds a reproducible comparison of the minimum-one-charge and minimum-three-charge lender counts across two overlapping curated cohorts and 14 quarters.

Run `python3 reproduce.py` to regenerate `derived/lender_threshold_comparison.csv` (28 rows) and `derived/cohort_summary.csv` (2 rows). Python standard library only.

## Derived definitions

- `lenders_1plus`: source any_activity_lenders.
- `lenders_3plus`: source active_lenders.
- `lenders_1or2`: difference between those counts, within the same cohort and quarter.
- `share_below_3charge_threshold_pct`: 100 x difference / lenders_1plus, rounded to six decimals.
- `quarters_with_threshold_gap`: quarters with a positive difference, within that cohort. This is not a count of unique lenders across time.
- `largest_excluded_share_quarter`: quarter with the highest calculated share in the supplied series.

The specialist Q3 2026 count is 14 under the first threshold and 13 under the second. The wider ecosystem gives 38 and 36. Relative to Q3 2025, the wider any-activity count rises from 37 to 38 while its active count remains 36. Aggregate data cannot identify which lenders entered, left or changed activity.

## Limits and reuse

Q3 2026 is provisional. The cohorts overlap and must not be added. These are curated series, not a market census. Charges do not establish monetary lending, unique facilities, credit appetite or current offers. No names or private lender mappings are released. This is an adaptation of existing research, not another independent study. Construction Capital is a property-finance brokerage and the publisher of the source dataset.

Original text, analytical tables and charts: CC BY 4.0. Original code: MIT. See LICENSE.txt for component rights. The retained source_manifest.json describes the original data edition; source-hashes.json preserves the original CSV and manifest checksums.
