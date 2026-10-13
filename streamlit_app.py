from pathlib import Path
import io
import csv
import json
import hashlib
import streamlit as st
import altair as alt
import pandas as pd
from calculate import load_source, compare, all_results, validate, FIELDS, BASELINES

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title='Is the Q3 planning fall geographically broad? | Construction Capital',
                   page_icon='📊', layout='wide')
st.caption('CONSTRUCTION CAPITAL RESEARCH  /  Q3 2026  /  CC-DF-2026Q3-C05')
st.title('A broad fall can still have a concentrated driver')
st.header('Test the geography behind the Q3 planning headline', divider='blue')
st.markdown('Five of seven regional groups decline annually under the filtered definition, but the South West supplies **76.4% of the panel’s net decline**. Remove it from both periods and the rest still falls **9.1%**. Use the controls to distinguish the breadth of a decline from the size of its largest contributor.')
st.caption('Matt Lenzie · Construction Capital · 13 October 2026 · Frozen source edition: 5 October 2026. Q3 2026 is provisional.')
st.info('These are unit mentions in approved application records across a 253-authority panel in England and Wales. They are not unique homes, starts or completions, and the panel is not a national total.')

rows=load_source()
validate(rows)
manifest=json.loads((ROOT/'source_manifest.json').read_text())
if hashlib.sha256((ROOT/'planning_unit_sensitivity.csv').read_bytes()).hexdigest() != manifest['source_csv_sha256']:
    st.error('The source checksum differs from this edition. The comparison is unavailable until reviewed.')
    st.stop()
regions=sorted({r['geography'] for r in rows}-{'Panel'})
st.subheader('1. Choose the comparison')
c1,c2,c3=st.columns([1,1.4,1])
with c1:
    period=st.selectbox('Comparison period',list(BASELINES),key='period')
with c2:
    definition=st.selectbox('Unit-mention definition',list(FIELDS),index=1,key='definition')
with c3:
    omitted=st.selectbox('Omit one regional group', ['None',*regions],index=regions.index('South West')+1,key='omitted')
baseline=BASELINES[period]
full,_=compare(rows,baseline,definition)
result,parts=compare(rows,baseline,definition,None if omitted=='None' else omitted)
metrics=st.columns(3)
metrics[0].metric('Full 253-authority panel',f"{full['change_pct']:+.1f}%")
metrics[1].metric('Selected geography',f"{result['change_pct']:+.1f}%")
metrics[2].metric('Regional groups declining',f"{result['groups_falling']} of {result['groups']}")
st.markdown(f"**Selected geography:** {'all seven groups' if omitted=='None' else 'all groups except '+omitted}. "
            f"{result['authorities']} authorities; **{result['prior_mentions']:,} → {result['current_mentions']:,}** mentions, "
            f"a change of **{result['change_mentions']:+,}** from {baseline} to 2026-Q3.")
st.caption('The omission applies to both periods. This is arithmetic sensitivity to geographic composition, not an estimate of what would have happened without that region.')

st.subheader('2. See which groups drive the selected change')
st.markdown('The bars add to the selected percentage change above. Each divides a group’s change by the **same selected starting total**. This gives percentage-point contributions, not each group’s own growth rate.')
df=pd.DataFrame(parts)
chart=alt.Chart(df).mark_bar(cornerRadiusEnd=3).encode(
    y=alt.Y('geography:N',sort=alt.SortField('contribution_pp',order='ascending'),title=None,axis=alt.Axis(labelLimit=230)),
    x=alt.X('contribution_pp:Q',title='Contribution to selected change (percentage points)',scale=alt.Scale(zero=True)),
    color=alt.condition(alt.datum.contribution_pp<0,alt.value('#b45336'),alt.value('#087b81')),
    tooltip=[alt.Tooltip('geography:N',title='Regional group'),alt.Tooltip('prior_mentions:Q',format=',',title='Starting mentions'),alt.Tooltip('current_mentions:Q',format=',',title='Q3 2026 mentions'),alt.Tooltip('contribution_pp:Q',format='.2f',title='Contribution (pp)'),alt.Tooltip('change_pct:Q',format='.1f',title='Own change (%)')]
).properties(height=300)
st.altair_chart(chart,width='stretch')
display=df[['geography','authorities','prior_mentions','current_mentions','change_mentions','change_pct','contribution_pp']].rename(columns={
    'geography':'Regional group','authorities':'Authorities','prior_mentions':'Starting mentions',
    'current_mentions':'Q3 2026 mentions','change_mentions':'Change in mentions',
    'change_pct':'Own change (%)','contribution_pp':'Contribution (pp)'})
st.dataframe(display,hide_index=True,width='stretch',column_config={'Own change (%)':st.column_config.NumberColumn(format='%.2f'),'Contribution (pp)':st.column_config.NumberColumn(format='%.2f')})

st.subheader('3. Compare all seven omissions')
summary,omissions,contributions=all_results(rows)
selected=[r for r in omissions if r['baseline']==baseline and r['definition']==definition]
st.markdown('A result that keeps the same sign after each separate omission is less dependent on any one group. It does **not** establish statistical significance, representative coverage or stability under simultaneous omissions.')
odf=pd.DataFrame(selected)[['omitted_region','authorities','change_pct','difference_from_full_pp','direction_reversed']].rename(columns={'omitted_region':'Omitted regional group','authorities':'Remaining authorities','change_pct':'Remaining change (%)','difference_from_full_pp':'Difference from full panel (pp)','direction_reversed':'Direction reversed?'})
st.dataframe(odf,hide_index=True,width='stretch',column_config={'Remaining change (%)':st.column_config.NumberColumn(format='%.2f'),'Difference from full panel (pp)':st.column_config.NumberColumn(format='%.2f')})
st.markdown('Across the **28 separate omissions** in this edition, the aggregate change remains negative. The size of the decline varies considerably. Region counting and volume-weighted change therefore answer different questions.')

st.subheader('What the annual and quarterly stories reveal')
st.markdown('The annual filtered panel falls from **47,693 to 34,775 mentions**, a net change of **-12,918**. The South West contributes **-9,874**. Its 76.4% share uses the **net panel change**, after increases elsewhere offset part of the decline. It is not its share of all gross regional decreases. Excluding the South West leaves **33,284 to 30,240**, a fall of **9.1%**.')
st.markdown('The quarterly comparison has a different concentration. London & South East contributes **-10,824 of the -13,806** filtered net change, or **78.4%**. Omitting that group leaves **25,284 to 22,302**, down **11.8%**. The largest contributor depends on the comparison period; neither result shows a sudden change in deliverable housing supply.')
st.markdown('The [South West Q3 report](https://constructioncapital.co.uk/market-reports/south-west-market-overview-q3-2026-review-v2) provides the regional context for the annual finding. The [Hugging Face Q3 planning dataset](https://huggingface.co/datasets/constructioncapital/q3-2026-planning-pipeline-definition-sensitivity) contains the 24 source observations and their definitions.')

st.subheader('Use in development finance research')
st.markdown('A panel headline can help frame a planning-market question, but an appraisal needs evidence for the project’s actual geography, consent and programme. Identify the comparator, check its coverage and then look at the scheme’s own permission conditions. Construction Capital’s [Development Finance guide and service overview](https://constructioncapital.co.uk/services/development-finance/) explains the funding process in which that evidence is used.')
st.markdown('For different evidence questions, the [ICPSR Q3 decision dataset](https://www.icpsr.umich.edu/sites/icpsr/view/studies/317061/versions/V1) separates decided outcomes, while the [Kaggle Q3 sales dataset](https://www.kaggle.com/datasets/constructioncapital/q3-2026-housing-sales-registration-lag-and-mix) documents the dated sales extract. These aggregates cannot be joined to trace an individual scheme from approval to sale. The existing [planning definition lab](https://huggingface.co/spaces/constructioncapital/q3-2026-planning-definition-lab) varies proposal-stage inclusion; this app instead tests geographic omission.')

st.subheader('Download the calculation')
def csv_bytes(table):
    s=io.StringIO(newline='');w=csv.DictWriter(s,fieldnames=list(table[0]));w.writeheader();w.writerows(table)
    return s.getvalue().encode('utf-8')
d1,d2=st.columns(2)
with d1:
    st.download_button('Selected regional contributions (CSV)',csv_bytes(parts),'selected_regional_contributions.csv','text/csv')
    st.download_button('All 28 omission comparisons (CSV)',csv_bytes(omissions),'leave_one_region_out.csv','text/csv')
with d2:
    st.download_button('Unchanged 24-row source (CSV)',(ROOT/'planning_unit_sensitivity.csv').read_bytes(),'planning_unit_sensitivity.csv','text/csv')
    st.download_button('Complete data and code package (ZIP)',(ROOT/'research-package.zip').read_bytes(),'q3-geographic-breadth-data-code.zip','application/zip')

st.subheader('Method, coverage and interests')
st.markdown('For a selected set of groups S, change = 100 × [sum(current) − sum(prior)] ÷ sum(prior). Each group’s contribution replaces the numerator with that group’s change. Omitting a group removes its values from **both** sums. The seven custom regional groups reconcile to the source panel; the overlapping Panel row is never added to them. Authority counts are constant across the three source quarters, but that alone does not establish complete or consistent record capture.')
st.markdown('The panel covers 253 authorities, including only seven in Wales. Groups have unequal numbers of authorities and different sizes. “Five of seven declining” is a count of groups, not a population estimate. Unit mentions may include repeated stages, inferred quantities or non-dwelling units; missing quantities contribute zero in the source. The reserved-matters filter is a case-insensitive proposal-text match, not scheme deduplication. Q3 is provisional and neither definition is a forecast of completions. No confidence intervals, causal effects or lender decisions are inferred.')
st.markdown('**Citation:** Lenzie, Matt (2026), *A broad fall can still have a concentrated driver*, Construction Capital, version 1.0, 13 October 2026, CC-DF-2026Q3-C05. Derived from CC-DF-2026Q3-04, frozen source edition 5 October 2026.')
st.caption('This app and linked Construction Capital studies share authorship and evidence. This is a supporting analytical adaptation, not an additional independent study or endorsement by a host. Source, derived tables, Python reproduction and component rights are included in the download. Original commentary: CC BY 4.0; original code: MIT. Underlying source rights remain with their holders; no upstream database licence is granted.')
st.caption('Construction Capital is a trading name of Lenzie Consulting Ltd, registered in England and Wales, company number 08174104. We are a commercial finance broker and introducer, not a lender, and we are not authorised by the FCA. Where a deal is a regulated activity we arrange it through lenders who hold the relevant FCA permissions. Every figure is indicative, varies by lender and deal, and is never an offer of finance.')
