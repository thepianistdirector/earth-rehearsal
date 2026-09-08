"""Manufactured spatial/time separation and conservative overlap remapping."""
import csv
import math
from pathlib import Path
from . import network_bundle as network, study_archive as archive
from .manufactured import channel
from .network_layout import Layout
from .network_study import keys,number
from .network_bundle import _read,_json
from .network_report import CSS,esc,table
from .bundle import atomic_write,BundleError


def validate_protocol(p):
    keys(p,('format','id','total_volume_m3','flow_m3_s','initial_mass_kg','duration_s','cells','remap'),'resolution protocol')
    if p['format']!='earth-rehearsal-resolution-v1' or p['id']!='normalized-channel-001' or p['cells']!=[1,2,4,8]:raise ValueError('frozen normalized channel protocol required')
    number(p['total_volume_m3'],8,1e6,'total volume');number(p['flow_m3_s'],0,1000,'flow');number(p['initial_mass_kg'],1e-6,1e6,'initial mass');number(p['duration_s'],.001,86400,'duration')
    # The frozen convergence gate concerns a translating front strictly inside
    # this support; a vanished front does not provide this spatial control.
    displaced=p['flow_m3_s']*p['duration_s']/p['total_volume_m3']
    if not .1<=displaced<=.8:raise ValueError('resolution control requires front displacement in [0.1,0.8] of domain')
    keys(p['remap'],('source_edges','target_edges','source_mass_kg','profile'),'remap')
    remap(p['remap'])
    for n in p['cells']:study(p,n)
    return p

def study(p,n):return channel(n,volume=p['total_volume_m3'],flow=p['flow_m3_s'],mass=p['initial_mass_kg'],duration=p['duration_s'])

def remap(p):
    keys(p,('source_edges','target_edges','source_mass_kg','profile'),'remap')
    if p['profile']!='piecewise_constant_cell_average':raise ValueError('explicit piecewise-constant profile required')
    for k in ('source_edges','target_edges'):
        v=p[k]
        if not isinstance(v,list) or not 2<=len(v)<=33:raise ValueError('bounded cell edges required')
        for x in v:number(x,0,1,'normalized edge')
        if v[0]!=0 or v[-1]!=1 or any(b<=a for a,b in zip(v,v[1:])):raise ValueError('remapping requires strictly ordered cells on identical [0,1] support')
    mass=p['source_mass_kg'];src=p['source_edges'];dst=p['target_edges']
    if not isinstance(mass,list) or len(mass)!=len(src)-1:raise ValueError('one source mass per cell required')
    for m in mass:number(m,0,1e6,'cell mass')
    target=[math.fsum(mass[i]*max(0,min(b,src[i+1])-max(a,src[i]))/(src[i+1]-src[i]) for i in range(len(mass))) for a,b in zip(dst,dst[1:])]
    residual=math.fsum(target)-math.fsum(mass)
    if abs(residual)>1e-12*max(math.fsum(mass),1e-300):raise ValueError('remap mass conservation failed')
    # Integrate the absolute difference of the two piecewise-constant profiles
    # exactly over their common partition; conservation alone cannot measure it.
    cuts=sorted(set(src+dst));profile_error=0.0
    for a,b in zip(cuts,cuts[1:]):
        middle=(a+b)/2;i=next(i for i in range(len(mass)) if src[i]<=middle<src[i+1]);j=next(j for j in range(len(target)) if dst[j]<=middle<dst[j+1])
        profile_error+=(b-a)*abs(mass[i]/(src[i+1]-src[i])-target[j]/(dst[j+1]-dst[j]))
    return {'target_mass_kg':target,'mass_residual_kg':residual,'profile_L1_error_kg':profile_error,'status':'CONSERVATIVE_ON_IDENTICAL_SUPPORT','interpretation':'Mass closure and profile error are distinct; this overlap remap assumes piecewise-constant source cell averages.'}

def summarize(p,children):
    exact=p['initial_mass_kg']*(1-p['flow_m3_s']*p['duration_s']/p['total_volume_m3']);rows=[]
    for n,child in zip(p['cells'],children):
        ref=next(s for s in child['evaluation']['summaries'] if s['method']=='affine_exponential_reference' and s['arm']=='BASELINE')
        for level in (1,2,4):
            num=next(s for s in child['evaluation']['summaries'] if s['method']=='conservative_euler' and s['arm']=='BASELINE' and s['refinement']==level)
            rows.append({'cells':n,'time_refinement':level,'numerical_kg':num['mass_kg'],'semidiscrete_reference_kg':ref['mass_kg'],'continuous_plug_flow_kg':exact,'time_error_kg':abs(num['mass_kg']-ref['mass_kg']),'spatial_error_kg':abs(ref['mass_kg']-exact),'total_error_kg':abs(num['mass_kg']-exact)})
    spatial=[r['spatial_error_kg'] for r in rows if r['time_refinement']==4]
    ratio=spatial[-1]/spatial[0] if spatial[0] else None
    passed=all(b<a for a,b in zip(spatial,spatial[1:])) and ratio is not None and ratio<=.6
    return {'status':'PASSED_MANUFACTURED_REFINEMENT' if passed else 'FAILED_MANUFACTURED_REFINEMENT','applicability':'A0_KNOWN_ANSWER','rows':rows,'spatial_fine_coarse_ratio':ratio,'spatial_ratio_bound':.6,'remap':remap(p['remap']),'claims':{k:'NOT_EVALUATED' for k in ('hydraulics','field_transport','disposal','lifecycle','ecological','health')}}

def render(p,summary):
    body='<div class="eyebrow">Manufactured channel · identical support</div><h1>Separate spatial and time error.</h1><div class="notice">A normalized conservative scalar front under prescribed flow. This does not validate field transport or real interventions.</div><p>Status: <strong>'+esc(summary['status'])+'</strong>. Time error compares Euler to each cell grid’s independent reference. Spatial error compares that reference to continuous plug flow. Total error can cancel these components and is never used alone to claim convergence.</p>'
    body+=table('Independent error components',['Cells','Time level','Euler kg','Cell reference kg','Plug flow kg','Time error kg','Spatial error kg','Total error kg'],[list(r.values()) for r in summary['rows']])
    body+='<h2>Remapping: conserved mass, changed profile</h2><p>Mass residual '+esc(summary['remap']['mass_residual_kg'])+' kg; profile L1 error '+esc(summary['remap']['profile_L1_error_kg'])+' kg. '+esc(summary['remap']['interpretation'])+'</p><h2>Evidence</h2><ul>'+''.join('<li><a href="cells/'+str(n)+'/report.html">'+str(n)+' cells · all raw network evidence</a></li>' for n in p['cells'])+''.join('<li><a href="'+v+'">'+v+'</a></li>' for v in ('protocol.json','summary.json','summary.csv','attempt.json','archive.json','complete.json'))+'</ul>'
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Earth Rehearsal · resolution control</title><style>'+CSS+'</style><body><main>'+body+'</main></body></html>'

def run(p,output):
    validate_protocol(p);root=archive.fresh(output);_json(root/'protocol.json',p);children=[]
    attempt={'status':'RUNNING','completed_cells':[]};_json(root/'attempt.json',attempt)
    try:
        for n in p['cells']:
            children.append(network.run(study(p,n),root/f'cells/{n}'));attempt['completed_cells'].append(n);_json(root/'attempt.json',attempt)
        summary=summarize(p,children);_json(root/'summary.json',summary)
        with (root/'summary.csv').open('x',newline='') as f:
            w=csv.DictWriter(f,fieldnames=list(summary['rows'][0]));w.writeheader();w.writerows(summary['rows'])
        atomic_write(root/'report.html',render(p,summary))
        attempt['status']='SUCCEEDED';_json(root/'attempt.json',attempt);archive.seal(root,'resolution');return summary
    except BaseException as exc:
        if not (root/'complete.json').exists():attempt.update(status='CANCELLED' if isinstance(exc,KeyboardInterrupt) else 'FAILED',failure_type=type(exc).__name__);_json(root/'attempt.json',attempt)
        raise

def inspect(output):
    root=Path(output);archive.verify(root,'resolution');p=validate_protocol(_read(root/'protocol.json'));children=[]
    if _read(root/'attempt.json')!= {'status':'SUCCEEDED','completed_cells':p['cells']}:raise BundleError('resolution attempt mismatch')
    for n in p['cells']:
        child=network.inspect(root/f'cells/{n}')
        if child['study']!=study(p,n):raise BundleError('resolution child differs from fixed support/control')
        children.append(child)
    summary=summarize(p,children)
    if _read(root/'summary.json')!=summary:raise BundleError('resolution summary differs from reconstructed evidence')
    from .evidence_tables import verify_csv,verify_html
    fields=list(summary['rows'][0]);verify_csv(root/'summary.csv',[fields,*[list(r.values()) for r in summary['rows']]])
    verify_html(root/'report.html',render(p,summary))
    return summary

def reproduce(output,new_output):
    archive.require_distinct_output(output,new_output)
    inspect(output);archive.require_matching_source(archive.verify(Path(output),'resolution'));return run(_read(Path(output)/'protocol.json'),new_output)
