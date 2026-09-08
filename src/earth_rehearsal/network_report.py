"""Offline readable network evidence, topology, trajectories and complete CSV."""
from __future__ import annotations
import csv
import html
import math
from pathlib import Path
from .network_layout import Layout
from .network_study import grid_counts, POLICY

def esc(value):return html.escape(str(value),quote=True)
def number(value):return f'{value:,.6f}' if abs(value)>=1e-4 or value==0 else f'{value:.5g}'
CSS='''
:root{color-scheme:light;--ink:#183533;--muted:#516862;--teal:#146b62;--line:#d4dfd7;--paper:#fafaf5;--orange:#b44b28}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:16px/1.5 system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif}a{color:#12645b;text-underline-offset:3px}a:focus-visible,summary:focus-visible,[tabindex]:focus-visible{outline:3px solid #aa4121;outline-offset:4px}header,main,footer{max-width:1240px;margin:auto;padding:24px 30px}header{display:flex;justify-content:space-between;gap:20px;border-bottom:1px solid var(--line);align-items:center}header .brand{font-weight:750;letter-spacing:-.03em;font-size:21px}header nav{display:flex;gap:16px;flex-wrap:wrap}h1{font-size:clamp(32px,5vw,56px);line-height:1.08;letter-spacing:-.055em;margin:18px 0}h2{font-size:25px;line-height:1.2;letter-spacing:-.025em;margin:0 0 16px}h3{font-size:18px;margin:0 0 10px}p{max-width:85ch}.eyebrow{font-size:12px;letter-spacing:.1em;font-weight:750;text-transform:uppercase;color:var(--teal)}.lede{font-size:19px;color:var(--muted);max-width:76ch}.notice{border-left:4px solid var(--orange);padding:14px 20px;background:#fff1df;margin:24px 0}.notice p{margin:0}.section{margin:38px 0}.muted{color:var(--muted)}.small{font-size:13px}.cards,.charts{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:18px}.card,.chart{background:white;border:1px solid var(--line);border-radius:12px;padding:20px;min-width:0}.value{font-size:32px;font-weight:650;font-variant-numeric:tabular-nums;letter-spacing:-.03em}.card p{margin:8px 0}.table-wrap,.diagram{overflow:auto;border:1px solid var(--line);border-radius:10px;background:white}table{border-collapse:collapse;width:100%;font-size:14px}caption{text-align:left;font-weight:650;padding:14px 16px;background:#eef2eb}th,td{padding:11px 14px;border-bottom:1px solid #e5ebe5;white-space:nowrap;text-align:left}th{background:#f0f4ed;font-size:12px;letter-spacing:.02em}td.num{text-align:right;font-variant-numeric:tabular-nums;font-family:ui-monospace,monospace}tbody tr:last-child td{border-bottom:0}.table-wrap p{padding:0 16px}details{border-top:1px solid var(--line);margin:18px 0;padding-top:14px}summary{cursor:pointer;font-weight:650;padding:4px 0}code{font-size:.88em;background:#eaf0e7;padding:2px 5px;overflow-wrap:anywhere}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#eaf0e7;padding:16px;border-radius:8px}footer{border-top:1px solid var(--line);font-size:13px;color:var(--muted)}svg{display:block;max-width:100%;height:auto}svg text{font-family:system-ui,sans-serif;fill:#34524b}.chart{overflow:auto}.chart svg{min-width:300px}.diagram svg{min-width:680px;width:100%}.legend{display:flex;gap:18px;align-items:center;font-size:13px;color:var(--muted);flex-wrap:wrap}.swatch{display:inline-block;width:22px;border-top:3px solid var(--teal);vertical-align:middle;margin-right:5px}.swatch.ref{border-top:2px dashed #313f3a}dl{display:grid;grid-template-columns:150px 1fr;gap:8px;font-size:14px}dt{font-weight:650}dd{margin:0;overflow-wrap:anywhere}.jump{position:absolute;left:-999px}.jump:focus{position:fixed;left:12px;top:12px;background:white;padding:12px;z-index:2}@media(max-width:800px){.cards,.charts{grid-template-columns:1fr}header,main,footer{padding:20px}header{align-items:flex-start;flex-direction:column}.value{font-size:29px}h1{max-width:15ch}dl{grid-template-columns:1fr;gap:2px}dd{margin-bottom:10px}}@media(prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
'''

def table(caption,headers,rows):
    head=''.join('<th scope="col">'+esc(h)+'</th>' for h in headers)
    body=''.join('<tr>'+''.join('<td'+(' class="num"' if isinstance(v,(int,float)) else '')+'>'+esc(number(v) if isinstance(v,(int,float)) else v)+'</td>' for v in row)+'</tr>' for row in rows)
    return '<div class="table-wrap" tabindex="0" aria-label="Scrollable '+esc(caption)+'"><table><caption>'+esc(caption)+'</caption><thead><tr>'+head+'</tr></thead><tbody>'+body+'</tbody></table></div>'

def topology(study):
    positions={n['id']:(70+680*n['position']['x'],60+170*n['position']['y']) for n in study['nodes']}
    parts=['<div class="diagram" tabindex="0" aria-label="Scrollable synthetic compartment diagram"><svg viewBox="0 0 860 300" role="img" aria-labelledby="topology-title topology-desc"><title id="topology-title">Prescribed-flow compartment network</title><desc id="topology-desc">Directed edges connect fictional water compartments. The table below provides every edge and forcing value. Diagram positions have no geographic interpretation.</desc><defs><marker id="arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="#779c89"/></marker></defs>']
    for edge in study['edges']:
        a=positions.get(edge['from'],(20,145));b=positions.get(edge['to'],(835,145));dx=b[0]-a[0];dy=b[1]-a[1];length=math.hypot(dx,dy) or 1
        offset=28 if edge['from']!='outside' else 0;endoffset=30 if edge['to']!='outside' else 0
        parts.append(f'<line x1="{a[0]+offset*dx/length:.2f}" y1="{a[1]+offset*dy/length:.2f}" x2="{b[0]-endoffset*dx/length:.2f}" y2="{b[1]-endoffset*dy/length:.2f}" stroke="#779c89" stroke-width="2" marker-end="url(#arrow)"/>')
        parts.append(f'<text x="{(a[0]+b[0])/2:.2f}" y="{(a[1]+b[1])/2-20:.2f}" font-size="10" text-anchor="middle">{esc(edge["id"])}</text>')
        device=next((c for c in study['capture'] if c['edge']==edge['id']),None)
        if device:
            x=(a[0]+b[0])/2;y=(a[1]+b[1])/2
            parts.append(f'<rect x="{x-7:.2f}" y="{y-7:.2f}" width="14" height="14" fill="#b44b28" transform="rotate(45 {x:.2f} {y:.2f})"/><text x="{x:.2f}" y="{y+55:.2f}" font-size="11" text-anchor="middle">capacity {device["capacity"]["value"]:g} kg</text>')
    for node in study['nodes']:
        x,y=positions[node['id']]
        parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="25" fill="#e0efe4" stroke="#186b61" stroke-width="2"/><text x="{x:.2f}" y="{y+5:.2f}" font-size="11" text-anchor="middle">{node["volume"]["value"]:g} m³</text><text x="{x:.2f}" y="{y+43:.2f}" font-size="13" font-weight="650" text-anchor="middle">{esc(node["id"])}</text>')
    parts.append('</svg></div>');return ''.join(parts)

def curve_chart(result,arm,layout):
    numerical=next(r for r in result['numerical'] if r['arm']==arm and r['refinement']==4)
    ref=next(r for r in result['references'] if r['arm']==arm)
    ids=layout.indices('mass');last=numerical['records'][-1]['t'];series=[]
    for run in (numerical,ref):series.append([(r['t'],math.fsum(r['state'][i] for i in ids)) for r in run['records']])
    ymax=max(1e-12,max(math.fsum(r['state'][i] for i in ids) for run in [*result['numerical'],*result['references']] if run['refinement']==4 for r in run['records']))*1.12
    width=340;height=215;left=58;top=22;right=320;bottom=172
    cid=arm.lower();parts=[f'<svg viewBox="0 0 {width} {height}" role="img" aria-labelledby="{cid}-title {cid}-desc"><title id="{cid}-title">{esc(arm)}: mass in modeled compartments</title><desc id="{cid}-desc">Solid line is finest Euler output. Dashed line is the independent exponential reference. Time is elapsed hours; quantity is kilograms. Full records are in trajectories.csv.</desc>']
    for f in (0,.5,1):
        y=bottom-f*(bottom-top);parts.append(f'<line x1="{left}" x2="{right}" y1="{y:.2f}" y2="{y:.2f}" stroke="#e0e7de"/><text x="{left-7}" y="{y+4:.2f}" font-size="14" text-anchor="end">{ymax*f:.3g}</text>')
    for seq,dash,color in [(series[0],'','#146b62'),(series[1],' stroke-dasharray="5 4"','#283e37')]:
        selected={0,len(seq)-1};stride=max(1,len(seq)//500)
        selected.update(range(0,len(seq),stride))
        for i,r in enumerate(numerical['records']):
            if i and r['segment']!=numerical['records'][i-1]['segment']:selected.update((i-1,i))
        points=' '.join(f'{left+t/last*(right-left):.2f},{bottom-v/ymax*(bottom-top):.2f}' for i in sorted(selected) for t,v in [seq[i]])
        parts.append(f'<polyline points="{points}" fill="none" stroke="{color}" stroke-width="2"{dash}/>')
    parts.append(f'<text x="{left}" y="194" font-size="14">0</text><text x="{right}" y="194" text-anchor="end" font-size="14">{last/3600:.3g} hours</text><text x="{left}" y="11" font-size="14">kg in compartments</text></svg>')
    return ''.join(parts)

def render(result):
    study=result['study'];e=result['evaluation'];layout=Layout(study);provenance=result['provenance']
    fine=[s for s in e['summaries'] if s['method']=='conservative_euler' and s['refinement']==4]
    titles={'BASELINE':'Baseline','SOURCE_REDUCTION':'Source prevention','OUTLET_CAPTURE':'Finite-capacity capture'}
    intro={'BASELINE':'Full source · no interception','SOURCE_REDUCTION':f"Source multiplier {study['source_factor']['value']:g}",'OUTLET_CAPTURE':'Named edges · explicit storage and fate'}
    parts=['<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Earth Rehearsal · CATCHMENT-001 evidence</title><style>'+CSS+'</style><body><a class="jump" href="#main">Skip to evidence</a><header><div class="brand">Earth Rehearsal<span class="muted"> / catchment</span></div><nav aria-label="Evidence files"><a href="study.json">Study</a><a href="result.json">Full result</a><a href="trajectories.csv">Download CSV</a><a href="manifest.json">Manifest</a></nav></header><main id="main"><div class="eyebrow">A0 known answer · wholly synthetic</div><h1>Follow the mass,<br>through the whole study.</h1><p class="lede">Three paired strategies in a fictional compartment network. Compare what stays, what crosses the boundary, and what remains in custody.</p><div class="notice"><p><strong>Computational controls, not environmental evidence.</strong> Prescribed flow is not a hydraulic solution. Capture transfers material; disposal, lifecycle, ecological and health benefit are all <strong>NOT_EVALUATED</strong>.</p></div><section class="section" aria-labelledby="comparison-heading"><h2 id="comparison-heading">The same forcing. Three different controls.</h2><div class="cards">']
    for row in fine:
        parts.append('<article class="card"><div class="eyebrow">'+esc(titles[row['arm']])+'</div><p class="small muted">'+esc(intro[row['arm']])+'</p><div class="value">'+number(row['escaped_kg'])+' <span class="small">kg</span></div><p>Crossed the outside boundary</p><p class="small muted">'+number(row['mass_kg'])+' kg in compartments<br>'+number(row['stored_kg'])+' kg in storage<br>'+number(row['unknown_kg'])+' kg with unknown fate</p></article>')
    parts.append('</div><p class="small muted">Cards show finest-grid Euler output. Differences from the independent reference are reported below. Lower boundary outflow alone establishes no real-world benefit.</p>')
    parts.append(table('Complete final mass balance · finest numerical grid',['Arm','Initial kg','Source kg','Compartments kg','Storage kg','Unknown fate kg','Escaped kg'],[[titles[r['arm']],sum(n['initial_mass'][c['id']]['value'] for n in study['nodes'] for c in study['classes']),r['source_kg'],r['mass_kg'],r['stored_kg'],r['unknown_kg'],r['escaped_kg']] for r in fine]))
    parts.append('</section><section class="section"><h2>A prescribed-flow network</h2><p class="muted">'+esc(study['support']['spatial_extent'])+'</p>'+topology(study))
    parts.append(table('Exact directed water forcing',['Edge','From','To',*[s['id']+' m³/s' for s in study['segments']]],[[edge['id'],edge['from'],edge['to'],*[s['flows'][edge['id']]['value'] for s in study['segments']]] for edge in study['edges']]))
    parts.append('</section><section class="section"><h2>Independent trajectories</h2><div class="legend"><span><i class="swatch"></i>Finest Euler grid</span><span><i class="swatch ref"></i>Exponential reference</span></div><div class="charts">')
    for row in fine:parts.append('<article class="chart"><h3>'+esc(titles[row['arm']])+'</h3>'+curve_chart(result,row['arm'],layout)+'</article>')
    parts.append('</div><p class="small muted">Charts share the same vertical scale. Graphs may sample dense series. CSV retains every quantity, time and refinement from both methods.</p>')
    parts.append('<p class="small">Error is the maximum absolute difference across every retained mass quantity and aligned time, in kg. Coarse, medium and fine grids use '+', '.join(str(sum(grid_counts(study))*k)+' steps' for k in (1,2,4))+'. Fine step duration by segment: '+', '.join(seg['id']+' '+format(seg['duration']['value']/(count*4),'.6g')+' s' for seg,count in zip(study['segments'],grid_counts(study)) if count)+'. Fine error bound: '+number(e['refinement'][0]['fine_bound_kg'])+' kg. Passing requires fine error within 2% of the declared study mass scale and fine/coarse error ≤ 0.6 above rounding resolution. Status: '+esc(e['status'])+'. This is a computational gate.</p>')
    parts.append(table('Refinement against independent reference',['Arm','Coarse error kg','Medium error kg','Fine error kg','Fine / coarse'],[[titles[r['arm']],*r['max_error_kg_by_level'],r['fine_coarse_ratio'] if r['fine_coarse_ratio'] is not None else 'Not observed: rounding floor'] for r in e['refinement']]))
    parts.append('</section><section class="section"><h2>Capture is a transfer, not disappearance</h2><p>Storage releases remain in <strong>destination_unknown</strong>. Leakage returns to the named compartment. The following throughput columns describe transfers; they are not extra stocks to add to the balance above.</p>')
    parts.append(table('Custody throughput · finest numerical grid',['Arm','Captured kg','Released to unknown kg','Leaked back kg','Terminal stored kg'],[[titles[r['arm']],r['captured_kg'],r['released_kg'],r['leaked_kg'],r['stored_kg']] for r in fine]))
    events=[event for r in result['references'] for event in r['capacity_events']]
    if events:parts.append(table('Reference capacity events',['Device','Elapsed seconds','Cumulative capture kg'],[[x['capture'],x['t'],x['captured_kg']] for x in events]))
    resources=[[titles[r['arm']],x['capture'],x['handled_kg'],x['kWh'] if x['kWh'] is not None else 'NOT_EVALUATED',x['status']] for r in fine for x in r['resources']]
    if resources:parts.append('<details><summary>Synthetic handling-resource assumptions</summary><p>Handled mass counts capture, release and leakage activities. These assumptions are not measured energy use or lifecycle benefit.</p>'+table('Declared handling assumptions',['Arm','Device','Handled kg','Assumed kWh','Evidence class'],resources)+'</details>')
    parts.append('</section><section class="section"><h2>Inspect the evidence</h2><details><summary>Water balances for every compartment and segment</summary>'+table('Water ledger · finest numerical grid',['Arm','Segment','Node','Opening m³','In m³','Out m³','Closing m³','Residual m³'],[[r['arm'],r['segment'],r['node'],r['opening_m3'],r['in_m3'],r['out_m3'],r['closing_m3'],r['residual_m3']] for r in e['water_ledgers'] if r['method']=='conservative_euler' and r['refinement']==4])+'</details>')
    for cls in layout.classes:
        rows=[]
        for run in result['numerical']:
            if run['refinement']==4:
                state=run['records'][-1]['state']
                for node in study['nodes']:rows.append([titles[run['arm']],node['id'],state[layout.at('mass',node['id'],cls)]])
        parts.append('<details><summary>Class '+esc(cls)+': final compartment stocks</summary>'+table('Class-specific mass · '+cls,['Arm','Compartment','Mass kg'],rows)+'</details>')
    from .network_bundle import FILES
    parts.append('<details><summary>Complete artifact index</summary><ul>'+''.join('<li><a href="'+esc(name)+'">'+esc(name)+'</a></li>' for name in (*FILES,'manifest.json','complete.json'))+'</ul></details>')
    parts.append('<details><summary>Source rights, versions and declared omissions</summary>')
    for record in study['source_records']:
        parts.append('<h3>'+esc(record['title'])+'</h3><dl><dt>Provider / version</dt><dd>'+esc(record['provider']+' / '+record['version'])+'</dd><dt>Classification</dt><dd>'+esc(record['kind'])+'</dd><dt>Declared license</dt><dd>'+esc(record['license'])+'</dd><dt>Variable hash</dt><dd><code>'+esc(record['content_sha256'])+'</code></dd><dt>Source</dt><dd><a href="'+esc(record['url'])+'">'+esc(record['url'])+'</a></dd></dl>')
    parts.append('<ul>'+''.join('<li>'+esc(v)+'</li>' for v in study['omissions'])+'</ul></details><details><summary>Reopen, reproduce and runtime identity</summary><p>Use the exact source package whose digest matches this study. Reproduction writes a fresh directory and preserves this bundle.</p><pre>python3 earth.py catchment inspect BUNDLE\npython3 earth.py catchment reproduce BUNDLE --out NEW_DIRECTORY\npython3 earth.py catchment export BUNDLE --out EXPORTED_DIRECTORY</pre><dl><dt>Study identity</dt><dd><code>'+esc(result['study_id'])+'</code></dd><dt>Runtime</dt><dd>'+esc(result['version'])+' · Python '+esc(provenance['python_version'])+' · '+esc(provenance['platform'])+' / '+esc(provenance['machine'])+'</dd><dt>Source digest</dt><dd><code>'+esc(provenance['source_digest'])+'</code></dd><dt>Parent study</dt><dd>'+esc(provenance.get('parent_study_id') or 'No parent supplied')+'</dd></dl></details></section></main><footer>Earth Rehearsal · Original synthetic study and software by Lucas Santana · AGPL-3.0-only. Human interpretation and environmental qualification are separate evidence gates.</footer></body></html>')
    return ''.join(parts)

def csv_rows(result):
    layout=Layout(result['study'])
    yield ['method','arm','refinement','time_s','segment',*[s['kind']+'.'+s['entity']+('.'+s['class'] if s['class'] else '')+' ['+s['unit']+']' for s in layout.slots]]
    for run in [*result['numerical'],*result['references']]:
        for record in run['records']:yield [run['method'],run['arm'],run['refinement'],record['t'],record['segment'],*record['state']]

def write_csv(result,path):
    with Path(path).open('x',newline='',encoding='utf-8') as file:csv.writer(file).writerows(csv_rows(result))
