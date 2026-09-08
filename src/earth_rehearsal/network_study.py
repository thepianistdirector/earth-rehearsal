"""Strict manufactured-network contract, source binding and bounded time grids."""
from __future__ import annotations
import hashlib
import json
import math
from pathlib import Path
from .sources import ID, SourceError, canonical, validate_catalog

class NetworkStudyError(ValueError): pass
ARMS=('BASELINE','SOURCE_REDUCTION','OUTLET_CAPTURE')
POLICY={'id':'NETWORK-EULER-TAYLOR-1','max_step_s':60.0,'max_loss_fraction':0.025,
        'refinements':[1,2,4],'max_steps_per_arm':40000,'max_retained_scalars':2000000,
        'mass_relative_tolerance':1e-9,'water_relative_tolerance':1e-10,
        'fine_error_fraction':0.02,'fine_coarse_ratio':0.6,
        'taylor_degree':24,'reference_norm_step':0.25,'max_reference_products':1000000}

def keys(obj,expected,where):
    if not isinstance(obj,dict) or set(obj)!=set(expected):raise NetworkStudyError(where+': expected exactly '+', '.join(expected))
def number(value,lo,hi,where):
    if type(value) not in (int,float):raise NetworkStudyError(where+': finite non-Boolean number required')
    try:ok=math.isfinite(value) and lo<=value<=hi
    except OverflowError:ok=False
    if not ok:raise NetworkStudyError(where+f': finite value in [{lo:g}, {hi:g}] required')
    return float(value)
def identifier(value,where):
    if not isinstance(value,str) or not ID.fullmatch(value) or value=='outside':raise NetworkStudyError(where+': bounded identifier required; outside is reserved')
    return value
def collection(value,maximum,where,minimum=0):
    if not isinstance(value,list) or not minimum<=len(value)<=maximum:raise NetworkStudyError(where+f': {minimum}..{maximum} entries required')
    seen=set()
    for item in value:
        if not isinstance(item,dict):raise NetworkStudyError(where+': object entries required')
        name=identifier(item.get('id'),where+'.id')
        if name in seen:raise NetworkStudyError(where+': duplicate ID '+name)
        seen.add(name)
    return seen

def quantity(value,unit,lo,hi,where,catalog):
    keys(value,('value','unit','source'),where)
    if value['unit']!=unit:raise NetworkStudyError(where+': expected unit '+unit)
    result=number(value['value'],lo,hi,where)
    keys(value['source'],('record','variable'),where+'.source')
    record_id=value['source']['record'];variable=value['source']['variable']
    if not isinstance(record_id,str) or record_id not in catalog or not isinstance(variable,str):raise NetworkStudyError(where+': unresolved source identity')
    record=catalog[record_id];item=record['values'].get(variable)
    if item is None or item['value'] is None:raise NetworkStudyError(where+': missing source variable cannot become zero')
    if item['unit']!=unit or item['value']!=value['value']:raise NetworkStudyError(where+': quantity differs from its exact retained source variable')
    return result

def identity(study):return hashlib.sha256(canonical(study)).hexdigest()

def validate(study):
    keys(study,('schema_version','study','study_version','source_class','applicability','support','source_records','classes','nodes','edges','segments','conversions','capture','source_factor','omissions'),'network study')
    for key,expected in [('schema_version',1),('study','CATCHMENT-001'),('study_version','1.0.0'),('source_class','wholly_synthetic'),('applicability','A0_KNOWN_ANSWER')]:
        if study[key]!=expected or type(study[key]) is bool:raise NetworkStudyError(key+': expected '+str(expected))
    keys(study['support'],('coordinate_reference','spatial_extent','temporal'),'support')
    if study['support']['coordinate_reference']!='LOCAL_SYNTHETIC':raise NetworkStudyError('support: only LOCAL_SYNTHETIC coordinates admitted')
    if any(not isinstance(v,str) or not v.strip() or len(v)>500 for v in study['support'].values()):raise NetworkStudyError('support: bounded explicit spatial and temporal description required')
    if not isinstance(study['omissions'],list) or not study['omissions'] or len(study['omissions'])>32 or any(not isinstance(v,str) or not v.strip() or len(v)>500 for v in study['omissions']):raise NetworkStudyError('omissions: explicit bounded model exclusions required')
    try:catalog=validate_catalog(study['source_records'],require_redistribution=True,synthetic_only=True)
    except SourceError as exc:raise NetworkStudyError(str(exc)) from exc
    def q(value,unit,lo,hi,where):return quantity(value,unit,lo,hi,where,catalog)
    classes=collection(study['classes'],3,'classes',1);nodes=collection(study['nodes'],8,'nodes',1);edges=collection(study['edges'],16,'edges')
    for c in study['classes']:
        keys(c,('id','mobility'),'class');q(c['mobility'],'1',0,1,'class.'+c['id']+'.mobility')
    for n in study['nodes']:
        keys(n,('id','volume','initial_mass','position'),'node');q(n['volume'],'m3',1,1e6,'node.'+n['id']+'.volume')
        keys(n['initial_mass'],classes,'node.'+n['id']+'.initial_mass')
        for c in classes:q(n['initial_mass'][c],'kg',0,1e6,'node.'+n['id']+'.'+c)
        keys(n['position'],('x','y'),'node.position')
        for axis in ('x','y'):number(n['position'][axis],0,1,'node.position.'+axis)
    for e in study['edges']:
        keys(e,('id','from','to'),'edge')
        if not isinstance(e['from'],str) or not isinstance(e['to'],str) or e['from'] not in nodes|{'outside'} or e['to'] not in nodes|{'outside'} or e['from']==e['to']:raise NetworkStudyError('edge.'+e['id']+': invalid directed endpoint')
    collection(study['segments'],8,'segments',1)
    total=0.0
    for seg in study['segments']:
        keys(seg,('id','duration','flows','sources'),'segment')
        duration=q(seg['duration'],'s',0,86400,'segment.'+seg['id']+'.duration')
        if duration>0 and total+duration<=total:raise NetworkStudyError('segment.duration: time cannot advance at binary64 precision')
        total+=duration;keys(seg['flows'],edges,'segment.flows');keys(seg['sources'],nodes,'segment.sources')
        for e in edges:q(seg['flows'][e],'m3/s',0,1000,'segment.'+seg['id']+'.flow.'+e)
        for n in nodes:
            keys(seg['sources'][n],classes,'segment.sources.'+n)
            for c in classes:q(seg['sources'][n][c],'kg/s',0,1000,'segment.source.'+n+'.'+c)
            incoming=math.fsum(seg['flows'][e['id']]['value'] for e in study['edges'] if e['to']==n)
            outgoing=math.fsum(seg['flows'][e['id']]['value'] for e in study['edges'] if e['from']==n)
            if abs(incoming-outgoing)>1e-10*max(incoming,outgoing,1e-300):raise NetworkStudyError('segment.'+seg['id']+'.'+n+': fixed volume requires balanced incoming/outgoing water')
    if not 0<total<=86400:raise NetworkStudyError('total duration: must be positive and <=86400 s')
    collection(study['conversions'],8,'conversions')
    for cv in study['conversions']:
        keys(cv,('id','node','from_class','to_class','rate'),'conversion')
        if any(not isinstance(cv[k],str) for k in ('node','from_class','to_class')) or cv['node'] not in nodes or cv['from_class'] not in classes or cv['to_class'] not in classes or cv['from_class']==cv['to_class']:raise NetworkStudyError('conversion: invalid node/class transfer')
        q(cv['rate'],'1/s',0,1,'conversion.'+cv['id']+'.rate')
    collection(study['capture'],8,'capture');used=set();edge_map={e['id']:e for e in study['edges']}
    for cap in study['capture']:
        keys(cap,('id','edge','fraction','capacity','release_rate','leak_rate','leak_destination','energy'),'capture')
        if not isinstance(cap['edge'],str) or cap['edge'] not in edge_map or edge_map[cap['edge']]['from']=='outside' or cap['edge'] in used:raise NetworkStudyError('capture: unique internal/outlet donor edge required')
        used.add(cap['edge'])
        if not isinstance(cap['leak_destination'],str) or cap['leak_destination'] not in nodes:raise NetworkStudyError('capture: leakage must name a modeled receiving compartment')
        q(cap['fraction'],'1',0,1,'capture.fraction');q(cap['capacity'],'kg',0,1e6,'capture.capacity')
        if 0<cap['capacity']['value']<1e-9:raise NetworkStudyError('positive capacity below 1e-9 kg computational resolution')
        q(cap['release_rate'],'1/s',0,1,'capture.release_rate');q(cap['leak_rate'],'1/s',0,1,'capture.leak_rate')
        if cap['energy'] is not None:q(cap['energy'],'kWh/kg',0,1e6,'capture.energy')
    q(study['source_factor'],'1',0,1,'source_factor')
    grid_counts(study)
    return study

def grid_counts(study):
    rates=[];nodes={n['id']:n for n in study['nodes']};counts=[];offset=0.0
    for seg in study['segments']:
        loss=[]
        for n in study['nodes']:
            out=math.fsum(seg['flows'][e['id']]['value']/n['volume']['value'] for e in study['edges'] if e['from']==n['id'])
            for c in study['classes']:
                convert=math.fsum(cv['rate']['value'] for cv in study['conversions'] if cv['node']==n['id'] and cv['from_class']==c['id'])
                loss.append(out*c['mobility']['value']+convert)
        loss.extend(cap['release_rate']['value']+cap['leak_rate']['value'] for cap in study['capture'])
        rate=max(loss,default=0.0);rates.append(rate)
        dt=min(POLICY['max_step_s'],POLICY['max_loss_fraction']/rate) if rate else POLICY['max_step_s']
        duration=seg['duration']['value'];n=max(1,math.ceil(duration/dt)) if duration else 0
        if n and (duration/(4*n)<=0 or duration/(4*n)<2*math.ulp(offset+duration)):raise NetworkStudyError('time grid cannot advance at binary64 precision')
        counts.append(n);offset+=duration
    steps=sum(counts)*sum(POLICY['refinements'])
    if steps>POLICY['max_steps_per_arm']:raise NetworkStudyError('network step budget exceeded')
    dim=2*len(nodes)*len(study['classes'])+5*len(study['capture'])*len(study['classes'])+2*len(study['edges'])*len(study['classes'])+len(study['conversions'])+len(study['edges'])
    if (steps*len(ARMS)*2+sum(counts)*4*len(ARMS))*dim>POLICY['max_retained_scalars']:raise NetworkStudyError('network retained-trajectory budget exceeded')
    return counts

def load(path):
    path=Path(path)
    if path.stat().st_size>2_000_000:raise NetworkStudyError('network study file exceeds 2 MB')
    try:study=json.loads(path.read_text(),parse_constant=lambda v: (_ for _ in ()).throw(NetworkStudyError('nonfinite JSON value')))
    except (json.JSONDecodeError,RecursionError) as exc:raise NetworkStudyError('invalid or overly nested network JSON') from exc
    return validate(study)

def set_quantity(study,path,value,*,validate_result=True):
    """Edit a synthetic quantity and its exact variable; never silently detach provenance."""
    import copy
    result=copy.deepcopy(study);obj=result
    for key in path:obj=obj[key]
    if not isinstance(obj,dict) or 'source' not in obj:raise NetworkStudyError('editable path is not a source-bound quantity')
    record=next(r for r in result['source_records'] if r['id']==obj['source']['record'])
    if not record['rights']['derivatives']:raise NetworkStudyError('source rights forbid derivative edits')
    variable=obj['source']['variable'];parent_hash=record['content_sha256'];record['values'][variable]['value']=value;obj['value']=value
    # Source references can deliberately share one parameter. Keep all occurrences aligned.
    def align(item):
        if isinstance(item,dict):
            if item.get('source')==obj['source'] and 'value' in item:item['value']=value
            else:
                for child in item.values():align(child)
        elif isinstance(item,list):
            for child in item:align(child)
    align(result)
    from .sources import digest
    record['content_sha256']=digest(record['values']);record['version']=record['version']+'+edit'
    record['transforms'].append({'parent_sha256':parent_hash,'operation':'set','variable':variable,'operand':value,'output_sha256':record['content_sha256']})
    # Parent study identity is recorded by the caller; arbitrary edits are not falsely called scaling.
    return validate(result) if validate_result else result
