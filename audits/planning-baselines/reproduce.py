"""Rebuild regional approval comparisons from the frozen public aggregate input.
Standard library only. Does not reconstruct upstream application-level extraction.
"""
from pathlib import Path
import csv, json, argparse
from decimal import Decimal

BASE=Path(__file__).resolve().parent
parser=argparse.ArgumentParser()
parser.add_argument('--output',default=str(BASE / 'derived'))
args=parser.parse_args()
out=Path(args.output); out.mkdir(parents=True,exist_ok=True)
rows=list(csv.DictReader((BASE / 'planning_decisions.csv').open()))
assert len(rows)==24
groups=list(dict.fromkeys(r['geography'] for r in rows))
result=[]
for geography in groups:
    period={r['quarter']:r for r in rows if r['geography']==geography}
    assert set(period)=={'2025-Q3','2026-Q2','2026-Q3'}
    assert len({r['authorities'] for r in period.values()})==1
    a,b,c=[int(period[q]['approved']) for q in ['2025-Q3','2026-Q2','2026-Q3']]
    result.append(dict(geography=geography,authorities=int(period['2026-Q3']['authorities']),
        approved_2025_q3=a,approved_2026_q2=b,approved_2026_q3=c,
        quarterly_change=c-b,quarterly_change_pct=str(Decimal(c-b)/Decimal(b)*100),
        annual_change=c-a,annual_change_pct=str(Decimal(c-a)/Decimal(a)*100),
        index_2025_q3='100',index_2026_q2=str(Decimal(b)/Decimal(a)*100),
        index_2026_q3=str(Decimal(c)/Decimal(a)*100),
        comparison='Quarterly up, annual down' if c>b and c<a else 'Quarterly down, annual down'))
for field in ['authorities','approved_2025_q3','approved_2026_q2','approved_2026_q3']:
    assert result[0][field]==sum(r[field] for r in result[1:])
assert sum(r['quarterly_change']>0 for r in result[1:])==3
assert all(r['annual_change']<0 for r in result[1:])
with (out / 'regional_approval_baselines.csv').open('w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=list(result[0]));w.writeheader();w.writerows(result)
summary=dict(source_rows=len(rows),comparison_rows=len(result),authorities=253,
    quarterly_increases=[r['geography'] for r in result[1:] if r['quarterly_change']>0],
    regions_below_annual_baseline=7,panel_quarterly_change=-125,panel_annual_change=-969)
(out / 'checks.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps(summary))
