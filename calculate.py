"""Reproduce geographic omission diagnostics from published aggregate inputs.

Standard library only. A geographic sensitivity check, not statistical inference.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FIELDS = {
    'All recorded mentions': 'all_approval_unit_mentions',
    'Exclude reserved-matters text matches': 'excluding_reserved_matters_unit_mentions',
}
BASELINES = {'Annual: Q3 2025': '2025-Q3', 'Quarterly: Q2 2026': '2026-Q2'}
CURRENT = '2026-Q3'


def load_source(path=None):
    path = Path(path or ROOT / 'planning_unit_sensitivity.csv')
    with path.open(newline='', encoding='utf-8') as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for k in ['authorities', *FIELDS.values(), 'removed_unit_mentions']:
            r[k] = int(r[k])
    return rows


def compare(rows, baseline, definition, omit=None):
    field = FIELDS[definition]
    lookup = {(r['geography'], r['quarter']): r for r in rows}
    regions = sorted({r['geography'] for r in rows} - {'Panel'})
    if baseline not in BASELINES.values() or omit not in [None, *regions]:
        raise ValueError('Unknown comparison or regional group')
    selected = [g for g in regions if g != omit]
    before = sum(lookup[g, baseline][field] for g in selected)
    after = sum(lookup[g, CURRENT][field] for g in selected)
    authorities = sum(lookup[g, CURRENT]['authorities'] for g in selected)
    regional = []
    for g in selected:
        a, b = lookup[g, baseline][field], lookup[g, CURRENT][field]
        regional.append(dict(geography=g, baseline=baseline, current=CURRENT,
            definition=definition, authorities=lookup[g, CURRENT]['authorities'],
            prior_mentions=a, current_mentions=b, change_mentions=b-a,
            change_pct=100*(b-a)/a if a else None,
            contribution_pp=100*(b-a)/before if before else None))
    result = dict(baseline=baseline, current=CURRENT, definition=definition,
        omitted_region=omit or 'None', authorities=authorities, groups=len(selected),
        prior_mentions=before, current_mentions=after, change_mentions=after-before,
        change_pct=100*(after-before)/before if before else None,
        groups_falling=sum(r['change_mentions'] < 0 for r in regional),
        groups_rising=sum(r['change_mentions'] > 0 for r in regional),
        groups_unchanged=sum(r['change_mentions'] == 0 for r in regional))
    return result, regional


def all_results(rows):
    regions = sorted({r['geography'] for r in rows} - {'Panel'})
    summaries, omitted, contributions = [], [], []
    for baseline in BASELINES.values():
        for definition in FIELDS:
            full, region_rows = compare(rows, baseline, definition)
            summaries.append(full)
            contributions.extend(region_rows)
            for g in regions:
                r, _ = compare(rows, baseline, definition, g)
                r['full_panel_change_pct'] = full['change_pct']
                r['difference_from_full_pp'] = r['change_pct'] - full['change_pct']
                r['direction_reversed'] = (r['change_mentions']*full['change_mentions']) < 0
                omitted.append(r)
    return summaries, omitted, contributions


def validate(rows):
    lookup = {(r['geography'], r['quarter']): r for r in rows}
    regions = sorted({r['geography'] for r in rows} - {'Panel'})
    assert len(rows) == len(lookup) == 24
    assert len(regions) == 7
    for q in ['2025-Q3', '2026-Q2', CURRENT]:
        for k in ['authorities', *FIELDS.values(), 'removed_unit_mentions']:
            assert sum(lookup[g, q][k] for g in regions) == lookup['Panel', q][k], (q, k)
    for r in rows:
        assert r['all_approval_unit_mentions'] - r['excluding_reserved_matters_unit_mentions'] == r['removed_unit_mentions']
    for g in regions:
        assert len({lookup[g,q]['authorities'] for q in ['2025-Q3','2026-Q2',CURRENT]}) == 1
    summaries, omitted, contributions = all_results(rows)
    for s in summaries:
        parts = [r for r in contributions if r['baseline'] == s['baseline'] and r['definition'] == s['definition']]
        assert sum(r['change_mentions'] for r in parts) == s['change_mentions']
        assert abs(sum(r['contribution_pp'] for r in parts)-s['change_pct']) < 1e-9
        assert s['groups_falling']+s['groups_rising']+s['groups_unchanged'] == 7
    for r in omitted:
        source = lookup[r['omitted_region'], r['baseline']]
        field = FIELDS[r['definition']]
        assert r['prior_mentions'] + source[field] == lookup['Panel',r['baseline']][field]
        assert r['current_mentions'] + lookup[r['omitted_region'],CURRENT][field] == lookup['Panel',CURRENT][field]
    return {'source_rows':24, 'groups':7, 'full_comparisons':4,
        'omission_comparisons':28, 'regional_contributions':28,
        'aggregate_reconciliation':True, 'additive_contributions':True,
        'authority_counts_stable':True,
        'direction_reversals':sum(r['direction_reversed'] for r in omitted)}


def write_csv(path, rows):
    with Path(path).open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)


if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',default=str(ROOT/'derived'))
    args=parser.parse_args()
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    rows=load_source();checks=validate(rows)
    for name, table in zip(['panel_comparisons.csv','leave_one_region_out.csv','regional_contributions.csv'],all_results(rows)):
        write_csv(out/name,table)
    checks['source_sha256']=hashlib.sha256((ROOT/'planning_unit_sensitivity.csv').read_bytes()).hexdigest()
    (out/'validation.json').write_text(json.dumps(checks,indent=2)+'\n')
    print(json.dumps(checks,indent=2))
