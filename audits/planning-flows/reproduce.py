"""Reproduce the flow comparison from the frozen public aggregate input.

Standard-library Python 3. Counts are separate quarterly event flows, not a cohort.
No result estimates a backlog, case duration, completed homes or loan availability.
"""
import argparse
import csv
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
QUARTERS = ['2025-Q3', '2026-Q2', '2026-Q3']
REGIONS = ['East of England', 'London & South East', 'Midlands',
           'North East & Yorkshire', 'North West', 'South West', 'Wales']


def analyse(source):
    rows = list(csv.DictReader(source.open(newline='')))
    expected = {(g, q) for g in ['Panel'] + REGIONS for q in QUARTERS}
    keys = [(r['geography'], r['quarter']) for r in rows]
    if len(keys) != len(set(keys)) or set(keys) != expected:
        raise ValueError('Duplicate or missing geography/quarter')
    columns = ['authorities', 'received', 'approved', 'refused', 'withdrawn',
               'unknown_outcome', 'known_decisions']
    for r in rows:
        for c in columns:
            if not r[c].isdigit():
                raise ValueError('Expected a non-negative integer: ' + c)
            r[c] = int(r[c])
        if r['known_decisions'] != r['approved'] + r['refused']:
            raise ValueError('Decision outcome reconciliation failed')
        if r['received'] == 0:
            raise ValueError('Ratio denominator is zero')
    panel = {r['quarter']: r for r in rows if r['geography'] == 'Panel'}
    for q in QUARTERS:
        regional = [r for r in rows if r['quarter'] == q and r['geography'] != 'Panel']
        for c in columns:
            if sum(r[c] for r in regional) != panel[q][c]:
                raise ValueError('Panel/regional count reconciliation failed: ' + c)
        if panel[q]['authorities'] != 253:
            raise ValueError('Unexpected panel coverage')
    out = []
    for r in rows:
        out.append({k: r[k] for k in ['geography', 'quarter', 'authorities', 'received', 'known_decisions']} | {
            'decisions_minus_receipts': r['known_decisions'] - r['received'],
            'known_decisions_per_100_receipts': round(100 * r['known_decisions'] / r['received'], 6)})
    decomposition = []
    for g in ['Panel'] + REGIONS:
        a = next(r for r in rows if r['geography'] == g and r['quarter'] == '2025-Q3')
        b = next(r for r in rows if r['geography'] == g and r['quarter'] == '2026-Q3')
        dd = b['known_decisions'] - a['known_decisions']
        dr = b['received'] - a['received']
        change = (b['known_decisions'] - b['received']) - (a['known_decisions'] - a['received'])
        assert change == dd - dr
        decomposition.append({'geography': g, 'known_decision_change': dd,
            'receipt_change': dr, 'decision_contribution_to_balance_change': dd,
            'receipt_contribution_to_balance_change': -dr, 'balance_change': change,
            'known_decision_change_pct': round(100 * dd / a['known_decisions'], 6),
            'receipt_change_pct': round(100 * dr / a['received'], 6)})
    return out, decomposition


def save(rows, path):
    with path.open('w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


def main():
    a = argparse.ArgumentParser(); a.add_argument('--output', type=Path, default=BASE / 'derived')
    dest = a.parse_args().output; dest.mkdir(parents=True, exist_ok=True)
    flow, change = analyse(BASE / 'planning_decisions.csv')
    save(flow, dest / 'flow_comparison.csv'); save(change, dest / 'flow_change_decomposition.csv')
    anchor = next(r for r in flow if r['geography'] == 'Panel' and r['quarter'] == '2026-Q3')
    assert (anchor['received'], anchor['known_decisions'], anchor['decisions_minus_receipts']) == (8082, 8750, 668)
    assert change[0]['balance_change'] == 1960
    assert sum(r['decisions_minus_receipts'] > 0 for r in flow if r['quarter'] == '2026-Q3' and r['geography'] != 'Panel') == 6
    print(json.dumps({'input_rows': len(flow), 'derived_flow_rows': len(flow), 'decomposition_rows': len(change),
                     'checks': '24 unique keys, outcomes, 3 panel/regional reconciliations, 253-authority coverage, 8 decomposition identities and headline anchors passed',
                     'q3_panel': anchor, 'year_on_year_panel': change[0]}, indent=2))


if __name__ == '__main__':
    main()
