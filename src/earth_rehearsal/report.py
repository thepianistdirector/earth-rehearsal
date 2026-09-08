"""Accessible, self-contained evidence report and lossless finest-grid CSV."""
from __future__ import annotations

import csv
from html import escape
import json
import math
from pathlib import Path

from .analytic import trajectory
from .study import ARMS, controls


LABELS = {'BASELINE': 'Baseline', 'SOURCE_REDUCTION': 'Source reduction', 'OUTLET_CAPTURE': 'Outlet capture'}


def _e(value):
    return escape(str(value), quote=True)


def _n(value):
    """Readable table precision; complete round-trip values remain in JSON/CSV."""
    if isinstance(value, float) and value == 0:
        return '0'
    if isinstance(value, float):
        return format(value, '.9g')
    return _e(value)


def _finest(result):
    level = max(run['refinement'] for run in result['runs'])
    return [next(run for run in result['runs'] if run['arm'] == arm and run['refinement'] == level) for arm in ARMS]


def _table(caption, headers, rows):
    return ('<div class="table-scroll" tabindex="0" role="region" aria-label="' + _e(caption) + '"><table><caption>' + _e(caption) + '</caption><thead><tr>' + ''.join('<th scope="col">' + _e(h) + '</th>' for h in headers) + '</tr></thead><tbody>' + ''.join('<tr>' + ''.join(('<th scope="row">' if i == 0 else '<td>') + _n(v) + ('</th>' if i == 0 else '</td>') for i, v in enumerate(row)) + '</tr>' for row in rows) + '</tbody></table></div>')


def _charts(result, runs):
    study = result['study']
    duration = sum(seg['duration']['value'] for seg in study['segments'])
    all_series = []
    for run in runs:
        times = [0.0] + [step['t_end_s'] for step in run['steps']]
        stocks = [study['initial_mass']['value']] + [step['closing_mass_kg'] for step in run['steps']]
        # Keep at most 1000 display vertices, including segment boundaries.
        if len(times) > 1000:
            selected = {round(i * (len(times) - 1) / 995) for i in range(996)}
            selected.update(i for i in range(1, len(times) - 1) if run['steps'][i - 1]['segment'] != run['steps'][i]['segment'])
            indices = sorted(selected)
            times, stocks = [times[i] for i in indices], [stocks[i] for i in indices]
        oracle = trajectory(study, run['arm'], times)
        all_series.append((run, times, stocks, [row['mass_kg'] for row in oracle]))
    maximum = max(max(stocks + exact) for _, _, stocks, exact in all_series)
    top = maximum * 1.08 if maximum else 1.0
    plots = []
    for index, (run, times, stocks, exact) in enumerate(all_series):
        def points(values):
            return ' '.join(f'{58 + t / duration * 338:.3f},{210 - value / top * 172:.3f}' for t, value in zip(times, values))
        title = LABELS[run['arm']]
        svg = f'<svg viewBox="0 0 420 258" role="img" aria-labelledby="chart-title-{index} chart-desc-{index}"><title id="chart-title-{index}">{_e(title)}: reservoir mass over time</title><desc id="chart-desc-{index}">Shared zero-based axes. Time 0 to {_e(duration)} seconds; mass 0 to {_e(top)} kilograms. Solid blue: explicit Euler. Dashed ochre: independent analytic solution. Initial mass {_e(stocks[0])} kg; final numerical mass {_e(stocks[-1])} kg. Exact values are in the comparison table and CSV.</desc>'
        for fraction in (0, 0.5, 1):
            y = 210 - fraction * 172
            svg += f'<path d="M58 {y}H396" class="grid"/><text x="50" y="{y + 4}" text-anchor="end">{top * fraction:.3g}</text>'
        svg += '<path d="M58 38V210H396" class="axis"/>'
        for fraction in (0, 0.5, 1):
            svg += f'<text x="{58 + fraction * 338}" y="231" text-anchor="middle">{duration * fraction:.6g}</text>'
        svg += f'<polyline points="{points(stocks)}" class="numerical"/><polyline points="{points(exact)}" class="analytic"/><text x="58" y="23">Reservoir mass (kg)</text><text x="227" y="252" text-anchor="middle">Elapsed time (s)</text></svg>'
        plots.append('<figure><figcaption>' + _e(title) + '</figcaption>' + svg + '</figure>')
    return '<div class="facets">' + ''.join(plots) + '</div>'


def write_csv(result, path):
    """Export every retained finest-grid step, with forcing and oracle context."""
    study = result['study']
    columns = ['arm', 'refinement', 'segment', 'index', 't_start_s', 't_end_s', 'duration_s', 'source_factor', 'capture_fraction', 'inflow_m3_s', 'outflow_m3_s', 'source_rate_kg_s', 'opening_volume_m3', 'closing_volume_m3', 'opening_mass_kg', 'closing_mass_kg', 'source_kg', 'water_in_m3', 'water_out_m3', 'escaped_kg', 'captured_kg', 'analytic_closing_mass_kg', 'analytic_cumulative_escaped_kg', 'analytic_cumulative_captured_kg', 'stock_error_kg']
    with Path(path).open('w', encoding='utf-8', newline='') as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for run in _finest(result):
            factor, fraction = controls(study, run['arm'])
            exact = trajectory(study, run['arm'], [step['t_end_s'] for step in run['steps']])
            for step, oracle in zip(run['steps'], exact):
                seg = next(s for s in study['segments'] if s['name'] == step['segment'])
                row = dict(step)
                row.update(arm=run['arm'], refinement=run['refinement'], duration_s=step['t_end_s'] - step['t_start_s'], source_factor=factor, capture_fraction=fraction, inflow_m3_s=seg['inflow']['value'], outflow_m3_s=seg['outflow']['value'], source_rate_kg_s=seg['source']['value'] * factor, analytic_closing_mass_kg=oracle['mass_kg'], analytic_cumulative_escaped_kg=oracle['escaped_kg'], analytic_cumulative_captured_kg=oracle['captured_kg'], stock_error_kg=step['closing_mass_kg'] - oracle['mass_kg'])
                writer.writerow(row)


def render(result):
    study = result['study']
    runs = _finest(result)
    level = runs[0]['refinement']
    summaries = result['evaluation']['summaries']
    finest = [next(row for row in summaries if row['arm'] == run['arm'] and row['refinement'] == level) for run in runs]
    valid = result['evaluation']['valid']
    content = '<header><p class="eyebrow">EARTH REHEARSAL / BOX-001</p><h1>Where the fictional mass goes</h1><p class="intro">One mixed reservoir. Dry and storm forcing. Three paired arms with independent numerical checks.</p><p class="status">' + ('VALID numerical benchmark' if valid else 'INVALID — comparison suspended') + ' · ' + _e(study['applicability']) + '</p></header>'
    content += '<aside class="scope" aria-label="Evidence scope"><strong>Synthetic inputs. Numerical evidence only.</strong><p>Disposal, lifecycle, ecological and health benefit: <b>NOT_EVALUATED</b>. Capture transfers material to an unknown destination.</p><details><summary>Applicability and unassessed uncertainty</summary><p>This known-answer software benchmark establishes no real-river or intervention effectiveness. Physical, parameter, scenario and model-form uncertainty are unquantified. Calibration, environmental validation and human review are not established by this report.</p></details></aside>'
    content += '<nav aria-label="Report sections"><a href="#comparison">Mass comparison</a><a href="#trajectory">Trajectories</a><a href="#accounting">Ledgers</a><a href="#numerics">Numerical checks</a><a href="#inputs">Inputs</a><a href="#provenance">Provenance</a></nav>'
    content += '<section id="comparison"><p class="eyebrow">01 / PAIRED COMPARISON</p><h2>Mass by destination</h2><p>Finest numerical grid (refinement ×' + _e(level) + '), in kilograms. Capture leaves reservoir stock unchanged. Tables show nine significant digits; JSON and CSV retain full precision. Scroll tables horizontally on narrow screens.</p>'
    content += _table('Final mass comparison — finest numerical grid (kg)', ['Arm', 'Reservoir stock', 'Escaped downstream', 'Captured transfer', 'Initial stock', 'Source added'], [[LABELS[s['arm']]] + [s[k] for k in ('final_mass_kg', 'escaped_kg', 'captured_kg', 'initial_mass_kg', 'source_kg')] for s in finest])
    content += _table('Independent analytic final values (kg)', ['Arm', 'Reservoir stock', 'Escaped downstream', 'Captured transfer'], [[LABELS[s['arm']]] + [s[k] for k in ('analytic_final_mass_kg', 'analytic_escaped_kg', 'analytic_captured_kg')] for s in finest]) + '</section>'
    content += '<section id="trajectory"><p class="eyebrow">02 / THROUGH TIME</p><h2>The same forcing, traced separately.</h2><p><span class="key blue">━━</span> Solid blue: numerical Euler · <span class="key ochre">┄┄</span> Dashed ochre: analytic. All panels use the same zero-based mass scale. Near-overlapping curves indicate agreement at this plotting scale; numerical differences appear in the error table.</p>' + _charts(result, runs) + '<p>Lines join retained finest-grid endpoints, sampled to at most 1,000 display points per panel for large studies, always retaining segment boundaries and run endpoints. Forcing is piecewise constant; closing stock opens the next segment. The CSV retains every plotted numerical point after the initial condition.</p></section>'
    content += '<section id="accounting"><p class="eyebrow">03 / CONSERVATION &amp; CUSTODY</p><h2>Count each mass once.</h2><p class="equation">Initial + source = reservoir + escaped + captured + residual</p><p>Captured → stored → destination_unknown. Stored throughput describes an intermediate transfer, not an additional stock. Terminal custody stock replaces captured in a custody boundary equation; it is never added to captured.</p>'
    content += _table('Whole-run conservation — finest grid', ['Arm', 'Water in (m3)', 'Water out (m3)', 'Water residual (m3)', 'Mass residual (kg)', 'Custody residual (kg)'], [[LABELS[s['arm']]] + [s[k] for k in ('water_in_m3', 'water_out_m3', 'water_residual_m3', 'mass_residual_kg', 'custody_residual_kg')] for s in finest])
    content += _table('Custody transfer versus terminal stock (kg)', ['Arm', 'Stored throughput (transfer)', 'Stored (terminal stock)', 'Destination unknown (terminal stock)'], [[LABELS[r['arm']], r['custody']['stored_throughput_kg'], r['custody']['stored_kg'], r['custody']['destination_unknown_kg']] for r in runs])
    # Derive interval ledgers from retained raw fluxes, using accurate summation.
    rows = []
    for run in runs:
        opening = study['initial_mass']['value']
        for seg in study['segments']:
            steps = [s for s in run['steps'] if s['segment'] == seg['name']]
            closing = steps[-1]['closing_mass_kg'] if steps else opening
            sums = {key: math.fsum(s[key] for s in steps) for key in ('source_kg', 'escaped_kg', 'captured_kg', 'water_in_m3', 'water_out_m3')}
            rows.append([LABELS[run['arm']] + ' / ' + seg['name'], opening, sums['source_kg'], closing, sums['escaped_kg'], sums['captured_kg'], opening + sums['source_kg'] - closing - sums['escaped_kg'] - sums['captured_kg'], sums['water_in_m3'], sums['water_out_m3']])
            opening = closing
    content += _table('Segment ledgers recomputed from raw finest-grid steps', ['Arm / segment', 'Opening (kg)', 'Source (kg)', 'Closing (kg)', 'Escaped (kg)', 'Captured (kg)', 'Mass residual (kg)', 'Water in (m3)', 'Water out (m3)'], rows) + '</section>'
    content += '<section id="numerics"><p class="eyebrow">04 / NUMERICAL EVIDENCE</p><h2>Agreement is measured, not assumed.</h2><p>Explicit Euler is compared with an independent exponential solution at retained time points. Bounds and tolerances are predeclared in BOX-EULER-1; observed discrepancy is numerical uncertainty only. Conservation alone cannot establish correct physics.</p>'
    content += _table('All arms and timestep refinements — absolute trajectory errors', ['Arm', 'Refinement', 'Steps', 'Max stock error (kg)', 'Max outlet error (kg)', 'A-priori error bound (kg)'], [[LABELS[s['arm']]] + [s[k] for k in ('refinement', 'step_count', 'max_stock_error_kg', 'max_outlet_error_kg', 'error_bound_kg')] for s in summaries])
    content += _table('Scale-normalized whole-run residuals — dimensionless', ['Arm', 'Mass residual / scale', 'Water residual / scale', 'Custody residual / scale'], [[LABELS[s['arm']]] + [s.get(k, 'Not recorded') for k in ('mass_residual_normalized', 'water_residual_normalized', 'custody_residual_normalized')] for s in finest])
    content += _table('Refinement response — fine/coarse maximum error ratios', ['Arm', 'Stock error ratio', 'Outlet error ratio', 'Evaluator status'], [[LABELS[r['arm']], r.get('max_stock_error_kg_fine_coarse_ratio') if r.get('max_stock_error_kg_fine_coarse_ratio') is not None else 'Arithmetic floor', r.get('max_outlet_error_kg_fine_coarse_ratio') if r.get('max_outlet_error_kg_fine_coarse_ratio') is not None else 'Arithmetic floor', r.get('status', 'Not recorded')] for r in result['evaluation'].get('refinement', [])])
    reversals = result['evaluation'].get('ranking_reversals', [])
    content += '<p>' + ('Ranking reversals recorded — comparison suspended.' if reversals else 'No ranking reversal recorded across the three timestep refinements. This compares modeled mass quantities, not environmental benefit.') + '</p>'
    content += '<details><summary>Complete refinement and pairwise ranking diagnostics</summary><pre>' + _e(json.dumps({key: result['evaluation'].get(key, []) for key in ('refinement', 'rankings', 'ranking_reversals')}, indent=2, allow_nan=False)) + '</pre></details><h3>Frozen numerical policy</h3><pre>' + _e(json.dumps(result['policy'], indent=2, allow_nan=False)) + '</pre><details><summary>Complete evaluator summaries and segment checks</summary><pre>' + _e(json.dumps(summaries, indent=2, allow_nan=False)) + '</pre></details></section>'
    content += '<section id="inputs"><p class="eyebrow">05 / DECLARED INPUTS</p><h2>A wholly synthetic fixture.</h2><p>Fixed volume: ' + _n(study['volume']['value']) + ' m3. Initial pollutant stock: ' + _n(study['initial_mass']['value']) + ' kg. Equal inflow and outflow preserve volume. No settling, resuspension, fragmentation, reaction, evaporation, groundwater exchange or spatial variability is represented.</p>'
    content += _table('Raw forcing segments — before arm controls', ['Segment', 'Duration (s)', 'Inflow (m3/s)', 'Outflow (m3/s)', 'Source (kg/s)'], [[s['name']] + [s[k]['value'] for k in ('duration', 'inflow', 'outflow', 'source')] for s in study['segments']])
    content += _table('Arm controls — dimensionless computational inputs', ['Arm', 'Source multiplier', 'Outlet capture fraction'], [[LABELS[arm], *controls(study, arm)] for arm in ARMS])
    content += '<p>Control fractions are contract-test inputs, not feasible source reductions or device performance estimates. Adverse pathways such as storage leakage, waste handling, energy demand and ecological harm remain evidence gaps.</p><details><summary>Complete frozen study, with source class and SI units</summary><pre>' + _e(json.dumps(study, indent=2, allow_nan=False)) + '</pre></details></section>'
    content += '<section id="provenance"><p class="eyebrow">06 / REPRODUCIBLE EVIDENCE</p><h2>Inspect the records behind the picture.</h2><p>Runtime version ' + _e(result['version']) + ' · schema ' + _e(result['schema_version']) + '. Study SHA-256: <code>' + _e(result['study_id']) + '</code></p>'
    content += _table('Recorded runtime identity and measured execution', ['Field', 'Value'], list(result['provenance'].items()))
    content += '<p class="downloads"><a href="result.json" download>Raw result JSON</a><a href="trajectories.csv" download>Finest-grid CSV</a><a href="manifest.json" download>Bundle manifest</a><a href="study.json" download>Frozen study JSON</a></p><p>The CSV includes each finest-grid step, source and flow context, stock and flux quantities, and independent analytic endpoint comparisons. JSON retains all refinement levels. This report is static and works offline without scripts, fonts or network requests.</p></section><footer>Earth Rehearsal · A0_KNOWN_ANSWER · Environmental benefits NOT_EVALUATED</footer>'
    return '<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta name="color-scheme" content="light"><title>BOX-001 | Earth Rehearsal evidence report</title><style>' + CSS + '</style></head><body><a class="skip" href="#main">Skip to report</a><main id="main">' + content + '</main></body></html>'


CSS = '''*{box-sizing:border-box}html{scroll-behavior:auto}body{margin:0;background:#fcfbf7;color:#182c34;font:16px/1.65 system-ui,-apple-system,sans-serif}main{max-width:1240px;margin:auto;padding:56px 40px}header{max-width:880px}.eyebrow{font-size:.76rem;letter-spacing:.16em;font-weight:750;color:#47606c;margin:0 0 18px}h1{font:600 clamp(2.6rem,6vw,5rem)/1.03 Georgia,serif;letter-spacing:-.04em;margin:20px 0 24px}h2{font:500 clamp(1.8rem,3vw,2.5rem)/1.18 Georgia,serif;margin:0 0 20px}h3{font-size:1.1rem;margin-top:30px}.intro{font-size:1.18rem;max-width:700px;color:#405661}.status{display:inline-block;padding:7px 13px;background:#e4eced;font-size:.85rem;font-weight:700}.scope{border-left:4px solid #9b6519;background:#f3ecdb;padding:22px 26px;margin:24px 0}.scope p{margin:8px 0 0}nav{display:flex;flex-wrap:wrap;gap:12px 25px;border-block:1px solid #b8c3c5;padding:18px 0;margin:32px 0}a{color:#175b7b;text-underline-offset:.2em}a:hover{text-decoration-thickness:3px}section{padding:35px 0 42px;border-bottom:1px solid #bcc7c8}section>p{max-width:900px}.table-scroll{overflow-x:auto;margin:26px 0;background:#fff;border:1px solid #ccd4d4;border-radius:3px}table{border-collapse:collapse;width:100%;font-size:.88rem;font-variant-numeric:tabular-nums}caption{text-align:left;padding:15px 17px;font-weight:750;background:#eef2f1}th,td{text-align:right;vertical-align:top;padding:13px 17px;border-bottom:1px solid #e0e5e4;white-space:nowrap}th:first-child,td:first-child{text-align:left}thead th{font-size:.78rem;background:#f8f9f7;white-space:normal;min-width:115px}tbody th{font-weight:600}tbody tr:last-child>*{border:0}.facets{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px;margin:26px 0}figure{margin:0;padding:16px 8px 6px;background:#fff;border:1px solid #ccd4d4}figcaption{font-weight:700;padding-left:12px}svg{display:block;width:100%;height:auto}svg text{font:12px system-ui;fill:#344c56}.grid{fill:none;stroke:#dce3e3;stroke-width:1}.axis{fill:none;stroke:#687f89;stroke-width:1}.numerical,.analytic{fill:none;stroke-width:2.4;stroke-linejoin:round}.numerical{stroke:#17658b}.analytic{stroke:#976119;stroke-dasharray:6 4}.blue{color:#17658b}.ochre{color:#805014}.key{font-weight:800}.equation{padding:18px;background:#edf2f1;font-weight:650}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#edf2f1;padding:20px;font-size:.82rem}code{overflow-wrap:anywhere;font-size:.85rem}details{margin:24px 0}summary{cursor:pointer;font-weight:650;padding:10px 0}.downloads{display:flex;flex-wrap:wrap;gap:14px 25px}.downloads a{font-weight:650}footer{font-size:.8rem;padding-top:30px;color:#4a6068}:focus-visible{outline:3px solid #17658b;outline-offset:4px}.skip{position:absolute;top:-80px;left:16px;background:white;padding:12px;z-index:1}.skip:focus{top:10px}@media(max-width:850px){.facets{grid-template-columns:1fr}figure{max-width:560px;width:100%}}@media(max-width:520px){main{padding:30px 18px}.scope{padding:18px}h1{font-size:2.8rem}th,td{padding:11px 13px}nav{gap:10px 18px}}@media print{body{background:white}main{padding:0}nav,.skip{display:none}.table-scroll{overflow:visible}table{font-size:8pt}th,td{padding:5px;white-space:normal}section{break-inside:avoid}.facets{grid-template-columns:repeat(3,1fr)}details{display:block}}'''

# Compact evidence-first hierarchy, especially on narrow screens.
CSS += '''main{padding-top:32px}header{max-width:980px}h1{font-family:system-ui,-apple-system,sans-serif;font-size:clamp(2rem,4vw,3.2rem);font-weight:650;line-height:1.08;margin:12px 0 14px}.intro{font-size:1.05rem;margin:12px 0}.eyebrow{margin-bottom:10px}.status{margin:4px 0 10px}.scope{padding:14px 20px;margin:14px 0}.scope details{margin:5px 0 0}.scope summary{padding:2px 0}nav{margin:20px 0;padding:12px 0;gap:8px 22px}section{padding-top:24px}h2{font-family:system-ui,-apple-system,sans-serif;font-size:clamp(1.5rem,3vw,2rem);margin-bottom:12px}@media(max-width:520px){main{padding-top:22px}h1{font-size:2rem}.scope{padding:12px 14px}.intro{font-size:1rem}nav{font-size:.9rem}.table-scroll{margin:18px 0}}'''

CSS += "tbody th:first-child{position:sticky;left:0;background:#fff;z-index:1}thead th:first-child{position:sticky;left:0;z-index:2;background:#f8f9f7}"
