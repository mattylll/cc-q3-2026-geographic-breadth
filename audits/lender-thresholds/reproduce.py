"""Reproduce the threshold comparison from public CC-DF-2026Q3-02 aggregates.

Usage: python3 reproduce.py [output_directory]
Standard library only. MIT licence, copyright 2026 Matt Lenzie / Construction Capital.
"""
import csv
import json
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
out = Path(sys.argv[1]) if len(sys.argv)>1 else BASE/'derived'
out.mkdir(parents=True,exist_ok=True)
rows = list(csv.DictReader((BASE/'charge_breadth_concentration.csv').open()))
assert len(rows)==28 and len({(r['cohort'],r['quarter']) for r in rows})==28
derived=[]
for r in rows:
    any_n=int(r['any_activity_lenders']); active=int(r['active_lenders'])
    assert 0 < active <= any_n
    gap=any_n-active
    derived.append({'cohort':r['cohort'],'quarter':r['quarter'],
      'lenders_1plus':any_n,'lenders_3plus':active,'lenders_1or2':gap,
      'share_below_3charge_threshold_pct':f'{100*gap/any_n:.6f}',
      'provisional':r['provisional']})
with (out/'lender_threshold_comparison.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(derived[0]));w.writeheader();w.writerows(derived)
summary=[]
for cohort in ['specialist','ecosystem']:
    rr=[r for r in derived if r['cohort']==cohort]
    assert len(rr)==14
    q25=next(r for r in rr if r['quarter']=='2025-Q3')
    q26=next(r for r in rr if r['quarter']=='2026-Q3')
    maxgap=max(rr,key=lambda r:float(r['share_below_3charge_threshold_pct']))
    summary.append({'cohort':cohort,'q3_2025_any':q25['lenders_1plus'],
      'q3_2026_any':q26['lenders_1plus'],'q3_2025_active':q25['lenders_3plus'],
      'q3_2026_active':q26['lenders_3plus'],'q3_any_change':q26['lenders_1plus']-q25['lenders_1plus'],
      'q3_active_change':q26['lenders_3plus']-q25['lenders_3plus'],
      'quarters_with_threshold_gap':sum(r['lenders_1or2']>0 for r in rr),
      'largest_excluded_share_quarter':maxgap['quarter'],
      'largest_excluded_share_pct':maxgap['share_below_3charge_threshold_pct']})
with (out/'cohort_summary.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(summary[0]));w.writeheader();w.writerows(summary)
assert next(r for r in derived if r['cohort']=='specialist' and r['quarter']=='2026-Q3')['lenders_1or2']==1
assert next(r for r in derived if r['cohort']=='ecosystem' and r['quarter']=='2026-Q3')['lenders_1or2']==2
print(json.dumps({'rows':len(derived),'summary':summary},indent=2))
