"""Observed-data view in Earth Rehearsal's existing offline report framework."""
from __future__ import annotations
import csv
import html
import io
from datetime import date
from . import __version__
from .network_report import CSS as BASE_CSS

CSS = BASE_CSS + '''
:root{--ink:#18313f;--muted:#536570;--teal:#17658b;--line:#d7dfe1;--paper:#f8faf9;--orange:#996310}a{color:#175e80}.eyebrow{color:#175e80}.notice{background:#f7efdd}.hero{padding:22px 0 12px}.tag{display:inline-block;background:#e7eff3;border:1px solid #c4d7e0;color:#194d68;padding:5px 10px;font-size:12px;font-weight:700;border-radius:5px}.cards{grid-template-columns:repeat(4,minmax(0,1fr))}.card{border-radius:7px}.value{font-size:28px}figure{margin:22px 0;background:white;border:1px solid var(--line);padding:20px;border-radius:8px;overflow:auto}figcaption{font-weight:700;margin-bottom:6px}.figure-note{font-size:13px;color:var(--muted);margin:0 0 14px}.figure-scroll{overflow:auto}.figure-scroll svg{min-width:780px;width:100%}.downloads{display:flex;gap:12px 22px;flex-wrap:wrap}.downloads a{font-weight:650}tbody th{background:white;font-weight:500;font-size:14px;letter-spacing:0}.table-wrap table th:first-child,.table-wrap table td:first-child{position:sticky;left:0;background:white}.table-wrap table thead th:first-child{background:#f0f4f5}th{background:#f0f4f5}.split{display:grid;grid-template-columns:1fr 1fr;gap:24px}.metric-note{font-size:13px;color:var(--muted)}.delta{font-size:27px;font-weight:650;font-variant-numeric:tabular-nums}.source-links a{overflow-wrap:anywhere}.quality-count{font-family:ui-monospace,monospace}section{scroll-margin-top:20px}summary{min-height:40px}.table-wrap:focus-visible{outline:3px solid #175e80;outline-offset:3px}@media(max-width:900px){.cards{grid-template-columns:repeat(2,minmax(0,1fr))}}@media(max-width:560px){.cards,.split{grid-template-columns:1fr}.hero{padding-top:4px}figure{padding:14px}.value{font-size:30px}h1{max-width:100%;font-size:34px}.table-wrap table{font-size:13px}}@media print{header nav,.jump{display:none}.cards{grid-template-columns:repeat(4,1fr)}details{break-inside:avoid}figure{break-inside:avoid}.figure-scroll svg{min-width:0}a{color:#18313f}body{background:white}.table-wrap{overflow:visible}th,td{white-space:normal;padding:5px;font-size:9pt}}
'''


def esc(value):
    return html.escape(str(value), quote=True)


def num(value, digits=2):
    return 'No accepted data' if value is None else f'{value:,.{digits}f}'


def percent(value):
    return f'{value*100:.1f}%'


def _csv(rows):
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    for row in rows:
        # Identifiers and labels are untrusted text. Numeric measures remain numbers.
        writer.writerow(["'"+v if isinstance(v, str) and v.lstrip().startswith(('=', '+', '-', '@')) else v for v in row])
    return stream.getvalue()


def daily_csv(rows):
    header = ['date', 'record_id', 'source_value_ft3_s', 'flow_m3_s', 'approval', 'qualifiers',
              'last_modified', 'state', 'primary_included', 'approved_estimates_included']
    return _csv([header]+[[r['date'], r['record_id'], r['original_value'], r['flow_m3_s'], r['approval'],
                           ';'.join(r['qualifiers']), r['last_modified'], r['state'],
                           int(r['primary_included']), int(r['sensitivity_included'])] for r in rows])


def summary_csv(summary):
    keys = ['requested_days', 'accepted_days', 'excluded_days', 'coverage_fraction', 'status',
            'mean_m3_s', 'min_daily_mean_m3_s', 'p10_m3_s', 'median_m3_s', 'p90_m3_s', 'max_daily_mean_m3_s']
    rows = [['group_kind', 'group_id', 'start_date', 'end_date', 'quality_policy']+keys]
    for group in summary['summaries']:
        for policy in ('primary', 'with_approved_estimates'):
            rows.append([group['kind'], group['id'], group['start_date'], group['end_date'], policy]+[group[policy][k] for k in keys])
    return _csv(rows)


def table(caption, headers, rows):
    body = []
    for row in rows:
        body.append('<tr>'+''.join(('<th scope="row">' if i == 0 else '<td>')+esc(v)+('</th>' if i == 0 else '</td>') for i, v in enumerate(row))+'</tr>')
    return '<div class="table-wrap" tabindex="0" role="region" aria-label="'+esc(caption)+'; scroll horizontally if needed"><table><caption>'+esc(caption)+'</caption><thead><tr>'+''.join('<th scope="col">'+esc(h)+'</th>' for h in headers)+'</tr></thead><tbody>'+''.join(body)+'</tbody></table></div>'


def monthly_chart(summary):
    """Native product chart: 48 month means; missing months break both paths."""
    groups = [g for g in summary['summaries'] if g['kind'] == 'month']
    width, height, left, right, top, bottom = 1040, 300, 72, 22, 22, 55
    plot_w, plot_h = width-left-right, height-top-bottom
    accepted = [g[p]['mean_m3_s'] for g in groups for p in ('primary', 'with_approved_estimates') if g[p]['mean_m3_s'] is not None]
    upper = max(accepted, default=1)*1.10 or 1
    parts = ['<svg viewBox="0 0 1040 300" role="img" aria-labelledby="monthly-title monthly-desc"><title id="monthly-title">Monthly mean of accepted daily discharge</title><desc id="monthly-desc">Solid blue uses approved days without estimated values. Dashed ochre also includes approved estimates. Missing accepted observations break each path. All months and coverage counts are available in the monthly table. Vertical axis starts at zero; units cubic meters per second.</desc>']
    for tick in range(5):
        value = upper*tick/4
        y = top+plot_h*(1-tick/4)
        parts += [f'<line x1="{left}" y1="{y:.2f}" x2="{width-right}" y2="{y:.2f}" stroke="#e0e5e8"/>',
                  f'<text x="{left-12}" y="{y+4:.2f}" text-anchor="end" font-size="16">{value:,.0f}</text>']
    parts.append(f'<text x="{left}" y="13" font-size="16">m³/s</text>')
    for i, group in enumerate(groups):
        x = left+plot_w*i/max(1, len(groups)-1)
        if i == 0 or i == len(groups)-1 or (group['id'].endswith('-01') and i > 2):
            anchor = 'start' if i == 0 else ('end' if i == len(groups)-1 else 'middle')
            parts.append(f'<text x="{x:.2f}" y="{height-25}" text-anchor="{anchor}" font-size="16">{esc(group["id"])}</text>')
    for policy, color, dash in [('with_approved_estimates', '#996310', ' stroke-dasharray="6 5"'), ('primary', '#17658b', '')]:
        points = []
        for i, group in enumerate(groups):
            value = group[policy]['mean_m3_s']
            if value is None:
                if points:
                    parts.append('<polyline points="'+' '.join(points)+'" fill="none" stroke="'+color+'" stroke-width="2.5"'+dash+'/>')
                    points = []
                continue
            x = left+plot_w*i/max(1, len(groups)-1)
            y = top+plot_h*(1-value/upper)
            points.append(f'{x:.2f},{y:.2f}')
            if policy == 'primary':
                parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="2.4" fill="{color}"><title>{esc(group["id"])}: {num(value)} m³/s, {group[policy]["accepted_days"]}/{group[policy]["requested_days"]} days</title></circle>')
        if points:
            parts.append('<polyline points="'+' '.join(points)+'" fill="none" stroke="'+color+'" stroke-width="2.5"'+dash+'/>')
    parts.append('</svg>')
    return ''.join(parts)


def render(study, source, summary, rows):
    whole = summary['summaries'][0]
    primary, sensitivity = whole['primary'], whole['with_approved_estimates']
    years = [g for g in summary['summaries'] if g['kind'] == 'year']
    periods = [g for g in summary['summaries'] if g['kind'] == 'period']
    difference = summary['period_difference']['primary']
    station = summary['station']
    parts = ['<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="color-scheme" content="light"><meta http-equiv="Content-Security-Policy" content="default-src \'none\'; style-src \'unsafe-inline\'; img-src data:; base-uri \'none\'; form-action \'none\'"><title>'+esc(study['title'])+' · Earth Rehearsal</title><style>'+CSS+'</style></head><body><a class="jump" href="#main">Skip to study</a><header><div class="brand">Earth Rehearsal <span class="small muted">/ Observed studies</span></div><nav aria-label="Study sections"><a href="#comparison">Compare</a><a href="#quality">Data quality</a><a href="#sources">Sources &amp; reproduce</a></nav></header><main id="main"><section class="hero"><span class="tag">OBSERVED DATA · DESCRIPTIVE STUDY</span><h1>'+esc(study['title'])+'</h1><p class="lede">'+esc(study['question'])+'</p><p class="muted">'+esc(station['name'])+' · '+esc(station['id'])+'<br>'+esc(study['start_date'])+' — '+esc(study['end_date'])+' · daily mean discharge</p></section>']
    cards = [('Requested days', f'{primary["requested_days"]:,}', f'{summary["received_records"]:,} source records retained'),
             ('Primary coverage', percent(primary['coverage_fraction']), f'{primary["accepted_days"]:,} accepted · {primary["excluded_days"]:,} excluded'),
             ('Mean daily flow', num(primary['mean_m3_s']), 'm³/s · accepted primary days'),
             ('Median daily flow', num(primary['median_m3_s']), 'm³/s · empirical median')]
    parts.append('<div class="cards">'+''.join('<div class="card"><div class="small muted">'+esc(label)+'</div><div class="value">'+esc(value)+'</div><p class="metric-note">'+esc(note)+'</p></div>' for label, value, note in cards)+'</div>')
    parts.append('<div class="notice"><p><strong>What this study can tell you.</strong> These are observed daily-flow summaries at one station. They do not measure pollutant load, flood peaks or the effect of a cleanup intervention. Estimated days are excluded from the primary analysis and shown in a separate sensitivity.</p></div>')
    parts.append('<section class="section" id="comparison"><div class="eyebrow">01 / Compare the retained record</div><h2>Daily flow across the two periods</h2>')
    delta = difference['mean_difference_m3_s']
    if delta is None:
        parts.append('<p>At least one period has no accepted observations. A mean difference cannot be calculated; inspect the exclusions below.</p>')
    else:
        direction = 'higher' if delta > 0 else ('lower' if delta < 0 else 'unchanged')
        parts.append('<p>The second period’s mean daily discharge was <strong>'+num(abs(delta))+' m³/s '+direction+'</strong> in the retained primary record. This is a descriptive comparison of different dates; it does not establish a trend or its cause.</p>')
    parts.append(table('Preselected periods · arithmetic means of accepted daily means', ['Period', 'Accepted / days', 'Coverage', 'Mean m³/s', 'Median m³/s', 'p10 m³/s', 'p90 m³/s', 'Mean incl. estimates m³/s'],
                       [[g['id'], f'{g["primary"]["accepted_days"]} / {g["primary"]["requested_days"]}', percent(g['primary']['coverage_fraction']), num(g['primary']['mean_m3_s']), num(g['primary']['median_m3_s']), num(g['primary']['p10_m3_s']), num(g['primary']['p90_m3_s']), num(g['with_approved_estimates']['mean_m3_s'])] for g in periods]))
    parts.append('<p class="small muted">p10 and p90 are ordinary empirical quantiles, not exceedance probabilities or uncertainty bounds. A period with excluded days summarizes only the included observations.</p>')
    if len([g for g in summary['summaries'] if g['kind'] == 'month']) >= 8:
        parts.append('<figure><figcaption>Monthly daily-flow means</figcaption><p class="figure-note">'+esc(study['start_date'])+' to '+esc(study['end_date'])+' · m³/s · monthly means of included daily means</p><div class="legend"><span><span class="swatch" style="border-color:#17658b"></span>Primary: approved, not estimated</span><span><span class="swatch ref" style="border-color:#996310"></span>Including approved estimates</span></div><div class="figure-scroll" tabindex="0" aria-label="Scrollable monthly discharge chart">'+monthly_chart(summary)+'</div></figure>')
        parts.append('<p>The chart shows variation within the selected record. Both series use the same monthly boundaries; a month’s excluded days change its support. Consult the coverage table before comparing months. Overlapping lines mean the estimate-inclusion sensitivity is small at that scale.</p>')
    else:
        parts.append('<p>The selected window is too short for a monthly trend chart. Use the exact period and monthly tables to compare its observed values.</p>')
    parts.append(table('Calendar-year summaries', ['Year', 'Accepted / days', 'Mean m³/s', 'Median m³/s', 'Maximum daily mean m³/s'],
                       [[g['id'], f'{g["primary"]["accepted_days"]} / {g["primary"]["requested_days"]}', num(g['primary']['mean_m3_s']), num(g['primary']['median_m3_s']), num(g['primary']['max_daily_mean_m3_s'])] for g in years]))
    months = [g for g in summary['summaries'] if g['kind'] == 'month']
    parts.append('<details><summary>All monthly values and denominators</summary>'+table('Monthly coverage and mean flow', ['Month', 'Primary days', 'Requested days', 'Primary mean m³/s', 'Days incl. estimates', 'Mean incl. estimates m³/s'], [[g['id'], g['primary']['accepted_days'], g['primary']['requested_days'], num(g['primary']['mean_m3_s']), g['with_approved_estimates']['accepted_days'], num(g['with_approved_estimates']['mean_m3_s'])] for g in months])+'</details></section>')
    parts.append('<section class="section" id="quality"><div class="eyebrow">02 / Inspect the denominator</div><h2>Coverage and source quality</h2><p>Every requested date is retained. An absent date, a missing value, an estimate and a provisional value remain distinct. No gap is filled and no observation is replaced with a simulated value.</p>')
    states = {'ACCEPTED': 'Approved; not estimated', 'ESTIMATED': 'Approved estimate; sensitivity only', 'PROVISIONAL': 'Provisional; excluded', 'MISSING_VALUE': 'Source row has no value', 'ABSENT_DATE': 'No source row for this date', 'NEGATIVE_OUTSIDE_SCOPE': 'Negative discharge; outside this analysis scope'}
    parts.append(table('Disjoint daily inclusion states', ['State', 'Days', 'Share of requested dates'], [[label, summary['state_counts'].get(key, 0), percent(summary['state_counts'].get(key, 0)/summary['requested_days'])] for key, label in states.items()]))
    parts.append('<p><strong>'+str(summary['overlapping_quality_counts']['REVISED'])+' revised days</strong> and <strong>'+str(summary['overlapping_quality_counts']['ESTIMATED'])+' estimated days</strong> are flagged in the source. These labels can overlap; they must not be added as disjoint categories. USGS approval is permission to publish the measurements, not validation of this study.</p>')
    parts.append('<div class="split"><div><h3>Estimate sensitivity</h3><p>Including approved estimates uses '+str(sensitivity['accepted_days'])+' of '+str(sensitivity['requested_days'])+' days ('+percent(sensitivity['coverage_fraction'])+'). Its mean is <strong>'+num(sensitivity['mean_m3_s'])+' m³/s</strong>, compared with '+num(primary['mean_m3_s'])+' m³/s for the primary record.</p></div><div><h3>Temporal and spatial support</h3><p>Dates label daily observations in the station record. They are not inferred UTC timestamps. A daily mean cannot reconstruct an instantaneous flood peak; a point station is not a spatial catchment model.</p></div></div>')
    parts.append('<details><summary>Inspect all '+str(len(rows))+' retained calendar days</summary>'+table('Daily source observations and inclusion', ['Date', 'Source ft³/s', 'Converted m³/s', 'USGS approval', 'Qualifiers', 'State'], [[r['date'], 'No source value' if r['original_value'] is None else r['original_value'], num(r['flow_m3_s']), r['approval'] or 'No record', ', '.join(r['qualifiers']) or 'None', states[r['state']]] for r in rows])+'</details></section>')
    parts.append('<section class="section source-links" id="sources"><div class="eyebrow">03 / Keep the evidence portable</div><h2>Sources, methods and reproduction</h2><p>'+esc(source['citation'])+'</p><p>USGS API data is US Government work in the public domain. Project code and original analysis are AGPL-3.0-only. <a href="'+esc(source['terms_url'])+'">Source terms</a> · <a href="https://waterdata.usgs.gov/provisional-data-statement/">Provisional data statement</a></p><div class="downloads"><a href="daily.csv">Daily CSV</a><a href="summary.csv">Summary CSV</a><a href="summary.json">Summary JSON</a><a href="daily.json">Original observations</a><a href="source.json">Source record</a><a href="reference.json">Arithmetic verification</a></div><details><summary>Exact source requests and identities</summary><dl>')
    for key in ('daily', 'site'):
        item = source['retrievals'][key]
        parts.append('<dt>'+esc(key.title())+' source</dt><dd><a href="'+esc(item['url'])+'">'+esc(item['url'])+'</a><br>Accessed '+esc(item['retrieved_utc'])+'<br>SHA-256 <code>'+esc(item['sha256'])+'</code></dd>')
    parts.append('</dl><p>Hashes establish byte consistency, not authenticity against a person who controls every file. The retained response may differ from a later upstream retrieval.</p></details><details><summary>Calculation rules</summary><p>Primary: nonnegative approved daily means with no qualifier except REVISED. Sensitivity additionally includes approved estimates. '+esc(summary['quantile_method'])+'</p><p>Conversion: ft³/s × '+esc(summary['exact_unit_factor'])+' = m³/s. Extra display digits do not add measurement precision. Means are arithmetic means over included dates, without gap filling or weighting by inferred clock-hour duration. No sum is presented as total water volume.</p><p>A separate decimal-arithmetic evaluator recomputes each group directly from the raw records. Software checks do not supply human or qualified review.</p></details><h3>Reopen or reproduce this bundle</h3><p>Use the matching Earth Rehearsal source package. Replace BUNDLE with this directory. Every output directory must be new; preserve partial evidence when recovering an interrupted run.</p><pre>python3 earth.py observations inspect BUNDLE\npython3 earth.py observations reproduce BUNDLE --out runs/reproduced\npython3 earth.py observations export BUNDLE --out runs/exported</pre></section></main><footer>Earth Rehearsal '+esc(__version__)+' · Observed descriptive evidence. Required human review and environmental applicability remain separate. No remote script, font or image is needed.</footer></body></html>')
    return ''.join(parts)
