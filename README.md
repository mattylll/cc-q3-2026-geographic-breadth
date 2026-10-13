# A broad fall can still have a concentrated driver

Matt Lenzie / Construction Capital | CC-DF-2026Q3-C05 | Version 1.0 | 13 October 2026

This Streamlit research app asks whether a planning-panel trend depends on one regional group. It offers 28 separate geographic omissions across two comparison periods and two definitions. It is an analytical adaptation of the existing Q3 planning study, not new independent evidence.

## Findings

The filtered annual panel changes from 47,693 to 34,775 approved-record unit mentions, down 27.1%. Five of seven custom regional groups fall. The South West contributes 9,874 of the 12,918 net decline (76.4%). Omitting it from both periods leaves a 9.1% decline. In the filtered quarterly comparison, London & South East contributes 78.4% of the net decline; the remaining groups decline 11.8%.

All 28 one-group omission comparisons remain negative. This is arithmetic sensitivity, not a significance test, causal counterfactual or assurance of representative coverage. Simultaneous omissions are not tested.

## Reproduce

Python 3.12 or later. The calculation uses only the standard library:

```sh
python calculate.py --output reproduced
```

Compare the three generated CSVs and validation.json with `derived/`. The 24-row source CSV is unchanged from the frozen 5 October 2026 package and its SHA256 is in source_manifest.json. Reproduction begins from these selected public aggregates, not upstream application-level data.

Run the app:

```sh
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

## Files and interpretation

- `planning_unit_sensitivity.csv`: 24 source rows, seven regions plus their overlapping Panel total, three quarters.
- `derived/panel_comparisons.csv`: four full-panel comparisons.
- `derived/leave_one_region_out.csv`: 28 separate regional omissions.
- `derived/regional_contributions.csv`: 28 additive regional contributions to full-panel comparisons.
- `calculate.py`: source validation and all derived arithmetic.
- `streamlit_app.py`: interactive view and selected-result downloads.
- `source_manifest.json`, `data_dictionary.json`, `SOURCE-LICENSE.txt`, `LICENSE.txt`: provenance, units, limits and rights.

Never sum the Panel row with its regions. The 253 authorities include only seven in Wales. Group size and coverage vary. Unit mentions are not unique homes or completions; missing quantities contribute zero and records may contain repeated stages or non-dwelling units. The filter removes proposal text matching reserved matters, not all potential duplicates. Q3 2026 is provisional.

## Contextual sources

The [Hugging Face Q3 planning dataset](https://huggingface.co/datasets/constructioncapital/q3-2026-planning-pipeline-definition-sensitivity) provides the source observations. The [South West Q3 report](https://constructioncapital.co.uk/market-reports/south-west-market-overview-q3-2026-review-v2) supplies regional context. For project funding, the [Development Finance guide and service overview](https://constructioncapital.co.uk/services/development-finance/) describes the process in which scheme-specific planning evidence belongs.

For separate questions, consult the [ICPSR decision dataset](https://www.icpsr.umich.edu/sites/icpsr/view/studies/317061/versions/V1), [Kaggle sales dataset](https://www.kaggle.com/datasets/constructioncapital/q3-2026-housing-sales-registration-lag-and-mix), and [planning definition lab](https://huggingface.co/spaces/constructioncapital/q3-2026-planning-definition-lab). They are related works by the same publisher, not independent corroboration. No aggregate joins track individual schemes.

## Rights and interests

Original commentary: CC BY 4.0. Original code: MIT. Source aggregates and derivative tables retain their underlying component rights; no blanket upstream database licence is granted. See the two licence files.

Construction Capital is a trading name of Lenzie Consulting Ltd, registered in England and Wales, company number 08174104. We are a commercial finance broker and introducer, not a lender, and we are not authorised by the FCA. Where a deal is a regulated activity we arrange it through lenders who hold the relevant FCA permissions. Every figure is indicative, varies by lender and deal, and is never an offer of finance.
