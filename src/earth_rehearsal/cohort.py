"""Frozen synthetic cohorts with durable holdout exposure and exclusive operations."""
from contextlib import contextmanager
import datetime
import fcntl
import json
import os
from pathlib import Path
from . import __version__
from .bundle import BundleError,digest_file,source_digest
from .network_bundle import _read,_json,_safe
from .network_study import keys,identifier,number,identity,validate
from .network_layout import Layout
from . import campaign,study_archive


def support_identity(study,parameters):
    """Identity of experimental controls, excluding metadata and fitted values."""
    from .sources import digest
    bindings={}
    for parameter in parameters:
        obj=study
        for key in parameter['path']:obj=obj[key]
        bindings[(obj['source']['record'],obj['source']['variable'])]=parameter['id']
    def physical(value):
        if isinstance(value,dict):
            if set(value)=={'value','unit','source'}:
                binding=(value['source']['record'],value['source']['variable'])
                return {'parameter':bindings[binding],'unit':value['unit']} if binding in bindings else {'value':value['value'],'unit':value['unit']}
            return {k:physical(v) for k,v in value.items() if k!='position'}
        if isinstance(value,list):return [physical(v) for v in value]
        return value
    return digest({k:physical(study[k]) for k in ('classes','nodes','edges','segments','conversions','capture','source_factor')})


def validate_protocol(p):
    keys(p,('format','id','classification','development','holdout','parameters','candidates','observables','loss','budget'),'calibration protocol')
    if p['format']!='earth-rehearsal-calibration-v1' or p['classification']!='wholly_synthetic_known_answer':raise ValueError('synthetic calibration protocol required')
    identifier(p['id'],'cohort id');seen=set()
    for split in ('development','holdout'):
        if not isinstance(p[split],list) or not 1<=len(p[split])<=4:raise ValueError('1..4 cases per split required')
        for case in p[split]:
            keys(case,('id','study'),'calibration case');identifier(case['id'],'case id')
            if case['id'] in seen:raise ValueError('development and holdout case IDs must be distinct')
            seen.add(case['id']);validate(case['study'])
    # Reuse source-bound parameter admission; the explicit values may later fail
    # study admission and remain invalid candidate attempts.
    proxy={'format':'earth-rehearsal-campaign-v1','id':p['id'],'base_study':p['development'][0]['study'],'parameters':p['parameters'],'dependence':{'kind':'EXPLICIT_JOINT_SAMPLES','description':'Frozen finite calibration grid; no probability distribution'},'cases':p['candidates'],'budget':{'max_attempts':p['budget'].get('max_candidates'),'max_seconds':p['budget'].get('max_seconds')}}
    campaign.validate_protocol(proxy)
    if len(p['candidates'])>8:raise ValueError('at most eight frozen candidates admitted')
    for case in p['development']+p['holdout']:
        proxy['base_study']=case['study'];campaign.validate_protocol(proxy)
    development_ids={support_identity(c['study'],p['parameters']) for c in p['development']}
    if any(support_identity(c['study'],p['parameters']) in development_ids for c in p['holdout']):raise ValueError('holdout must use distinct experimental controls; metadata or fitted-value edits do not create unseen support')
    if not isinstance(p['observables'],list) or not 1<=len(p['observables'])<=16:raise ValueError('1..16 explicit observables required')
    ids=set()
    for ob in p['observables']:
        keys(ob,('id','arm','kind','entity','class','time','unit'),'observable');identifier(ob['id'],'observable id')
        if ob['id'] in ids:raise ValueError('duplicate observable')
        ids.add(ob['id'])
        if ob['arm'] not in ('BASELINE','SOURCE_REDUCTION','OUTLET_CAPTURE') or ob['time']!='final' or ob['unit']!='kg' or ob['kind'] not in ('mass','stored','unknown','escaped','captured','released','leaked'):raise ValueError('unsupported final mass observable')
        for case in p['development']+p['holdout']:
            try:Layout(case['study']).at(ob['kind'],ob['entity'],ob['class'])
            except (KeyError,TypeError) as exc:raise ValueError('observable does not resolve in every frozen study') from exc
    keys(p['loss'],('kind','unit','equivalence_absolute','confirmation_max_abs'),'loss')
    if p['loss']['kind']!='SUM_SQUARED_ERROR' or p['loss']['unit']!='kg2':raise ValueError('frozen sum-of-squares loss in kg2 required')
    number(p['loss']['equivalence_absolute'],0,1,'equivalence tolerance kg2');number(p['loss']['confirmation_max_abs'],0,1e6,'confirmation maximum residual kg')
    keys(p['budget'],('max_candidates','max_seconds'),'budget')
    if type(p['budget']['max_candidates']) is not int or not 1<=p['budget']['max_candidates']<=8:raise ValueError('1..8 candidate attempts admitted')
    return p

def validate_observations(data,p,split):
    keys(data,('format','split','classification','cases'),'observations')
    if data['format']!='earth-rehearsal-observations-v1' or data['split']!=split or data['classification']!='wholly_synthetic_reference':raise ValueError('explicit synthetic observations and split required')
    if not isinstance(data['cases'],list) or len(data['cases'])!=len(p[split]):raise ValueError('observation case count mismatch')
    for expected,actual in zip(p[split],data['cases']):
        keys(actual,('id','input_study_id','observations'),'observation case')
        if actual['id']!=expected['id'] or actual['input_study_id']!=identity(expected['study']):raise ValueError('observation support identity mismatch')
        if not isinstance(actual['observations'],list) or len(actual['observations'])!=len(p['observables']):raise ValueError('observable count mismatch')
        for ob,item in zip(p['observables'],actual['observations']):
            keys(item,('observable','value','unit','quality'),'observation')
            if item['observable']!=ob['id'] or item['unit']!='kg' or item['quality']!='SYNTHETIC_CONTROL':raise ValueError('observation identity/unit/quality mismatch')
            number(item['value'],0,1e9,'synthetic observation')
    return data

def freeze(p,development,holdout,output,*,lineage=None):
    validate_protocol(p);validate_observations(development,p,'development');validate_observations(holdout,p,'holdout')
    root=study_archive.fresh(output)
    for name,value in [('protocol.json',p),('development.json',development),('holdout.json',holdout)]:_json(root/name,value)
    names=['protocol.json','development.json','holdout.json']
    if lineage is not None:_json(root/'lineage.json',lineage);names.append('lineage.json')
    m={'format':'earth-rehearsal-cohort-v1','version':__version__,'source_digest':source_digest(),'files':{name:{'bytes':(root/name).stat().st_size,'sha256':digest_file(root/name)} for name in names},'exposure_scope':'Dataset creation/freezing necessarily sees these known synthetic controls. Fit execution reads development observations only. This is a software holdout protocol, not a blinded human or environmental validation.'}
    _json(root/'cohort.json',m);_json(root/'frozen.json',{'format':'earth-rehearsal-cohort-frozen-v1','cohort_sha256':digest_file(root/'cohort.json')})
    return m

def header(root):
    root=Path(root);f=_read(_safe(root,'frozen.json'));m=_read(_safe(root,'cohort.json'))
    if f!= {'format':'earth-rehearsal-cohort-frozen-v1','cohort_sha256':digest_file(root/'cohort.json')}:raise BundleError('cohort freeze identity mismatch')
    validate_manifest(m)
    return m

def validate_manifest(m):
    if not isinstance(m,dict) or set(m)!= {'format','version','source_digest','files','exposure_scope'} or m['format']!='earth-rehearsal-cohort-v1' or m['version']!=__version__ or not isinstance(m['files'],dict) or set(m['files']) not in ({'protocol.json','development.json','holdout.json'},{'protocol.json','development.json','holdout.json','lineage.json'}):raise BundleError('invalid frozen cohort schema')
    for entry in m['files'].values():
        if not isinstance(entry,dict) or set(entry)!= {'bytes','sha256'} or type(entry['bytes']) is not int or not 0<entry['bytes']<=32*1024*1024 or not isinstance(entry['sha256'],str) or len(entry['sha256'])!=64 or any(c not in '0123456789abcdef' for c in entry['sha256']):raise BundleError('invalid cohort artifact descriptor')
    if not isinstance(m['source_digest'],str) or len(m['source_digest'])!=64 or any(c not in '0123456789abcdef' for c in m['source_digest']):raise BundleError('invalid cohort source digest')
    if not isinstance(m['exposure_scope'],str) or not m['exposure_scope']:raise BundleError('missing cohort exposure scope')
    return m

def read_frozen(root,m,name):
    path=_safe(Path(root),name);entry=m['files'][name]
    if path.stat().st_size!=entry['bytes'] or digest_file(path)!=entry['sha256']:raise BundleError('frozen cohort bytes changed: '+name)
    return _read(path)

def development_only(root):
    # Deliberately do not stat, hash or read holdout.json here.
    m=header(root)
    if 'lineage.json' in m['files']:read_frozen(root,m,'lineage.json')
    p=validate_protocol(read_frozen(root,m,'protocol.json'));data=validate_observations(read_frozen(root,m,'development.json'),p,'development')
    return m,p,data

@contextmanager
def exclusive(root):
    path=Path(root)/'operation.lock'
    if path.is_symlink():raise BundleError('linked operation lock is forbidden')
    with path.open('a') as file:
        try:fcntl.flock(file,fcntl.LOCK_EX|fcntl.LOCK_NB)
        except BlockingIOError as exc:raise BundleError('another cohort operation is active') from exc
        try:yield
        finally:fcntl.flock(file,fcntl.LOCK_UN)

def expose(root,fit_id,selection_hash,*,replay=False):
    root=Path(root);path=root/'holdout-access.json'
    if replay:
        event=_read(_safe(root,'holdout-access.json'))
        if event.get('fit_id')!=fit_id or event.get('selection_sha256')!=selection_hash:raise BundleError('replay must retain the originally exposed frozen selection')
        return event
    if path.exists():raise BundleError('holdout already exposed; use explicit frozen-selection replay or consume it into a new cohort')
    event={'format':'earth-rehearsal-holdout-access-v1','fit_id':fit_id,'selection_sha256':selection_hash,'opened_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'EXPOSURE_RECORDED_BEFORE_OBSERVATION_READ'}
    # Exclusive creation plus fsync precedes every read of holdout observations.
    with path.open('x',encoding='utf-8') as file:json.dump(event,file,sort_keys=True);file.flush();os.fsync(file.fileno())
    fd=os.open(root,os.O_RDONLY)
    try:os.fsync(fd)
    finally:os.close(fd)
    return event


def consume(old_root,new_protocol,new_development,new_holdout,output):
    """Explicitly consume old holdout into development and freeze disjoint controls."""
    old_root=Path(old_root)
    with exclusive(old_root):
        if not (old_root/'holdout-access.json').is_file():raise BundleError('consumption requires a recorded holdout exposure')
        m,p,dev=development_only(old_root);access=_read(_safe(old_root,'holdout-access.json'))
        hold=validate_observations(read_frozen(old_root,m,'holdout.json'),p,'holdout')
        validate_protocol(new_protocol);validate_observations(new_development,new_protocol,'development');validate_observations(new_holdout,new_protocol,'holdout')
        old_cases=p['development']+p['holdout'];old_observations=dev['cases']+hold['cases']
        if new_protocol['id']==p['id'] or new_protocol['observables']!=p['observables']:raise BundleError('consumed cohort needs a new identity and retained observable definitions')
        if new_protocol['development'][:len(old_cases)]!=old_cases or new_development['cases'][:len(old_observations)]!=old_observations:raise BundleError('new development must retain every old development and consumed holdout case unchanged')
        old_studies={support_identity(c['study'],new_protocol['parameters']) for c in old_cases}
        if any(support_identity(c['study'],new_protocol['parameters']) in old_studies for c in new_protocol['holdout']):raise BundleError('new holdout reuses an already consumed study')
        lineage={'format':'earth-rehearsal-cohort-consumption-v1','parent_cohort_sha256':digest_file(old_root/'cohort.json'),'parent_access':access,'consumed_case_ids':[c['id'] for c in p['holdout']],'scope':'Previous holdout is now development evidence. Newly frozen synthetic cases are distinct input controls, not proof of statistical independence or field validity.'}
        return freeze(new_protocol,new_development,new_holdout,output,lineage=lineage)
