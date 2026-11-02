CC-DF-2026Q3-A06 | Approval rates versus approval volume
Matt Lenzie / Construction Capital | Prepared 2 November 2026
Source study CC-DF-2026Q3-01, fixed 5 October 2026 edition.

Run: python3 reproduce.py --output reproduced
Calculations use Python standard library only. Chart: python3 build_chart.py (Pillow required).

The original planning_decisions.csv has 24 aggregate rows. The comparison selects 16 Q3 observations across the panel and seven custom regional groups. rate_volume_comparison.csv contains eight derived rows. The panel covers 253 authorities, not a national census. Seven authorities are in Wales.

Approval rate = approved / (approved + refused). Withdrawn and unknown outcomes are excluded. Application records are not unique projects, homes or construction starts. No loan amounts, terms, finance availability or individual permission probabilities are inferred. The fixed-rate benchmark is arithmetic, not causal.

All public reproductions start at the aggregate CSV. No private application-level records or upstream extraction code are included. The work adds analysis to an existing study, without new observations or another independent study.

Source: https://www.icpsr.umich.edu/sites/icpsr/view/studies/317061/versions/V1
Q3 context: https://constructioncapital.co.uk/market-reports/london-and-south-east-market-overview-q3-2026-review
Service context: https://constructioncapital.co.uk/services/development-finance/

Read LICENSE.txt for component rights. Planning aggregates retain underlying source rights and are not blanket OGL, CC0 or CC BY data. Original explanatory text and chart CC BY 4.0; original code MIT.
