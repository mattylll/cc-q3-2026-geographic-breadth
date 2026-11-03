"""Reproduce the hypothetical model from assumptions.json, using only the standard library."""
from pathlib import Path
from decimal import Decimal as D
import csv,json,argparse

p=argparse.ArgumentParser()
p.add_argument('--input-dir',default='.')
p.add_argument('--output',default='reproduced')
a=p.parse_args();base=Path(a.input_dir);out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
inputs=json.loads((base/'assumptions.json').read_text())
gdv0=D(str(inputs['base_gdv_gbp']));cost0=D(str(inputs['assumed_total_project_costs_gbp']))
units=D(str(inputs['units']));surplus0=gdv0-cost0
assert surplus0>0
rows=[]
for pc in inputs['price_changes_pct']:
 for cc in inputs['cost_changes_pct']:
  gdv=gdv0*(1+D(str(pc))/100);cost=cost0*(1+D(str(cc))/100);surplus=gdv-cost
  rows.append({'data_type':'hypothetical_scenario','exit_price_change_pct':pc,'total_cost_change_pct':cc,'units':int(units),'average_exit_price_gbp':str(gdv/units),'gdv_gbp':str(gdv),'total_costs_gbp':str(cost),'appraisal_surplus_before_tax_gbp':str(surplus),'surplus_change_vs_base_pct':str((surplus/surplus0-1)*100)})
with (out/'exit_sensitivity_scenarios.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
context=list(csv.DictReader((base/'q3_sales_context.csv').open()))
assert len(context)==8 and all(r['quarter']=='2026-Q3' for r in context)
print(f'Reproduced {len(rows)} hypothetical scenarios; retained {len(context)} observed context rows separately. No market forecasts or lender criteria inferred.')
