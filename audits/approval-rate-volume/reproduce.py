"""Reproduce the rate-versus-count comparison from the public aggregate CSV.

Python standard library only. Does not rebuild the upstream private extraction.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
FIELDS = [
    'geography', 'authorities', 'approved_2025_q3', 'approved_2026_q3',
    'approved_change_count', 'approved_change_pct', 'known_decisions_2025_q3',
    'known_decisions_2026_q3', 'known_decisions_change_pct',
    'approval_rate_2025_pct', 'approval_rate_2026_pct', 'approval_rate_change_pp',
    'rate_up_count_down', 'approvals_at_2025_rate_2026_decision_volume',
    'actual_approvals_minus_fixed_rate_benchmark',
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default=str(BASE / 'derived'))
    args = parser.parse_args()
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    raw = list(csv.DictReader((BASE / 'planning_decisions.csv').open()))
    assert len(raw) == 24
    groups = list(dict.fromkeys(r['geography'] for r in raw))
    result, selected = [], []
    for geography in groups:
        pair = [next(r for r in raw if r['geography'] == geography and r['quarter'] == q)
                for q in ['2025-Q3', '2026-Q3']]
        selected.extend(pair)
        a, b = pair
        assert a['authorities'] == b['authorities']
        for r in pair:
            assert int(r['known_decisions']) == int(r['approved']) + int(r['refused'])
            assert abs(float(r['approval_pct']) - 100 * int(r['approved']) / int(r['known_decisions'])) < 1e-10
        a0, a1 = int(a['approved']), int(b['approved'])
        k0, k1 = int(a['known_decisions']), int(b['known_decisions'])
        r0, r1 = a0 / k0, a1 / k1
        benchmark = k1 * r0
        result.append(dict(zip(FIELDS, [
            geography, int(a['authorities']), a0, a1, a1-a0, 100*(a1/a0-1),
            k0, k1, 100*(k1/k0-1), 100*r0, 100*r1, 100*(r1-r0),
            r1 > r0 and a1 < a0, benchmark, a1-benchmark,
        ])))
    regions = [r for r in result if r['geography'] != 'Panel']
    panel = result[0]
    assert sum(r['authorities'] for r in regions) == 253
    for key in ['approved_2025_q3', 'approved_2026_q3', 'known_decisions_2025_q3', 'known_decisions_2026_q3']:
        assert sum(r[key] for r in regions) == panel[key]
    assert [r['geography'] for r in regions if r['rate_up_count_down']] == ['South West']
    assert all(r['approved_change_count'] < 0 for r in regions)
    with (out / 'rate_volume_comparison.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(result)
    with (out / 'selected_source_rows.csv').open('w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=list(raw[0]))
        writer.writeheader()
        writer.writerows(selected)
    sw = next(r for r in result if r['geography'] == 'South West')
    summary = {
        'source_rows': len(raw), 'selected_rows': len(selected), 'comparison_rows': len(result),
        'regional_groups': len(regions), 'source_edition': '2026-10-05',
        'source_csv_sha256': hashlib.sha256((BASE / 'planning_decisions.csv').read_bytes()).hexdigest(),
        'all_seven_regions_fewer_approvals': True, 'higher_rate_fewer_approvals': ['South West'],
        'south_west': sw,
        'interpretation': 'Fixed-rate benchmark is an arithmetic comparison, not an estimate of causality or missing approvals.',
        'reproducibility_boundary': 'Published aggregate rows only; no upstream re-extraction or case-level audit.',
    }
    (out / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
