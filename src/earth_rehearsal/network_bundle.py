"""Atomic network attempts, retained raw trajectories and offline verification."""
from __future__ import annotations
import datetime
import json
import os
from pathlib import Path
import platform
import sys
import time
import uuid
from . import __version__
from .bundle import atomic_write,digest_file,source_digest,BundleError,MAX_FILE_BYTES,require_distinct_output
from .network_study import ARMS,POLICY,identity,validate
from .sources import canonical

BASE_FILES=('study.json','result.json','trajectories.csv','report.html','attempt.json')
def raw_name(method,arm,level):return f'raw/{method}-{arm.lower()}-{level}.json'
RAW_FILES=tuple([raw_name('euler',a,l) for a in ARMS for l in POLICY['refinements']]+[raw_name('reference',a,4) for a in ARMS])
FILES=BASE_FILES+RAW_FILES

def _json(path,value):atomic_write(path,canonical(value))
def _read(path):
    if path.stat().st_size>MAX_FILE_BYTES:raise BundleError('network artifact exceeds file budget')
    try:return json.loads(path.read_text(),parse_constant=lambda v: (_ for _ in ()).throw(BundleError('nonfinite JSON in bundle')))
    except (json.JSONDecodeError,RecursionError) as exc:raise BundleError('malformed or nested network JSON') from exc

def _safe(root,name):
    path=root/name
    if not path.is_file() or path.stat().st_size>MAX_FILE_BYTES:raise BundleError(name+': missing or oversized artifact')
    relative=Path(name);current=root
    for part in relative.parts:
        current=current/part
        if current.is_symlink():raise BundleError(name+': linked artifacts are not accepted')
    return path

def run(study,output,*,parent_study_id=None,checkpoint=None):
    from .network_numerical import run_arm as numerical
    from .network_analytic import run_arm as reference
    from .network_evaluator import evaluate
    from .network_report import render,write_csv
    validate(study)
    if parent_study_id is not None and (not isinstance(parent_study_id,str) or len(parent_study_id)!=64 or any(c not in '0123456789abcdef' for c in parent_study_id)):raise BundleError('parent identity must be SHA-256')
    output=Path(output);output.parent.mkdir(parents=True,exist_ok=True)
    try:output.mkdir()
    except FileExistsError as exc:raise BundleError('output already exists; preserve it and choose a fresh directory') from exc
    (output/'raw').mkdir();started=time.perf_counter();attempt={'format':'earth-rehearsal-network-attempt-v1','id':uuid.uuid4().hex,'study_id':identity(study),'status':'RUNNING','completed_raw':[]}
    def point(phase):
        if checkpoint:checkpoint(phase)
    try:
        _json(output/'study.json',study);_json(output/'attempt.json',attempt);point('before_calculation')
        nums=[];refs=[]
        for arm in ARMS:
            for level in POLICY['refinements']:
                value=numerical(study,arm,level);name=raw_name('euler',arm,level)
                _json(output/name,value);nums.append(value);attempt['completed_raw'].append(name);_json(output/'attempt.json',attempt);point('after_raw')
            value=reference(study,arm);name=raw_name('reference',arm,4)
            _json(output/name,value);refs.append(value);attempt['completed_raw'].append(name);_json(output/'attempt.json',attempt);point('after_raw')
        evaluation=evaluate(study,nums,refs)
        result={'format':'earth-rehearsal-network-result-v1','version':__version__,'study':study,'study_id':identity(study),'policy':POLICY,'numerical':nums,'references':refs,'evaluation':evaluation,
                'provenance':{'attempt_id':attempt['id'],'source_digest':source_digest(),'parent_study_id':parent_study_id,'python_version':platform.python_version(),'implementation':platform.python_implementation(),'platform':sys.platform,'machine':platform.machine(),'threads':1,'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'elapsed_seconds':time.perf_counter()-started}}
        _json(output/'result.json',result);point('after_evaluation')
        csv_path=output/'.trajectories.csv.partial';write_csv(result,csv_path)
        if csv_path.stat().st_size>MAX_FILE_BYTES:raise BundleError('network CSV budget exceeded')
        with csv_path.open('rb') as file:os.fsync(file.fileno())
        os.replace(csv_path,output/'trajectories.csv');atomic_write(output/'report.html',render(result))
        attempt['status']='SUCCEEDED';_json(output/'attempt.json',attempt)
        manifest={'format':'earth-rehearsal-network-bundle-v1','version':__version__,'study_id':result['study_id'],'source_digest':result['provenance']['source_digest'],'files':{name:{'bytes':(output/name).stat().st_size,'sha256':digest_file(output/name)} for name in FILES},'reproduce':'python3 earth.py catchment reproduce BUNDLE --out NEW_DIRECTORY'}
        _json(output/'manifest.json',manifest);point('before_activation')
        _json(output/'complete.json',{'format':'earth-rehearsal-network-complete-v1','status':'SUCCEEDED','manifest_sha256':digest_file(output/'manifest.json')});point('after_activation')
        return result
    except BaseException as exc:
        if not (output/'complete.json').is_file():
            attempt['status']='CANCELLED' if isinstance(exc,KeyboardInterrupt) else 'FAILED';attempt['failure_type']=type(exc).__name__
            try:_json(output/'attempt.json',attempt)
            except OSError:pass
        raise

def inspect(output):
    from .network_evaluator import evaluate
    root=Path(output)
    if not (root/'complete.json').is_file():raise BundleError('incomplete network attempt: complete.json is absent; rerun its study.json into a fresh directory')
    try:
        complete=_read(_safe(root,'complete.json'))
        if set(complete)!= {'format','status','manifest_sha256'} or complete['format']!='earth-rehearsal-network-complete-v1' or complete['status']!='SUCCEEDED':raise BundleError('network activation record mismatch')
        manifest_path=_safe(root,'manifest.json')
        if digest_file(manifest_path)!=complete['manifest_sha256']:raise BundleError('network manifest hash mismatch')
        manifest=_read(manifest_path)
        if set(manifest)!= {'format','version','study_id','source_digest','files','reproduce'} or manifest['format']!='earth-rehearsal-network-bundle-v1' or manifest['version']!=__version__:raise BundleError('network format/version mismatch; use matching source package')
        if not isinstance(manifest['files'],dict) or set(manifest['files'])!=set(FILES):raise BundleError('network manifest requires exact artifact set')
        for name in FILES:
            path=_safe(root,name);entry=manifest['files'][name]
            if set(entry)!= {'bytes','sha256'} or type(entry['bytes']) is not int or path.stat().st_size!=entry['bytes'] or digest_file(path)!=entry['sha256']:raise BundleError(name+': size/hash mismatch')
        study=validate(_read(root/'study.json'));result=_read(root/'result.json')
        if set(result)!= {'format','version','study','study_id','policy','numerical','references','evaluation','provenance'} or result['format']!='earth-rehearsal-network-result-v1' or result['version']!=__version__:raise BundleError('network result schema mismatch')
        if result['study']!=study or result['study_id']!=identity(study) or manifest['study_id']!=identity(study):raise BundleError('network study identity mismatch')
        attempt=_read(root/'attempt.json')
        expected_order=[name for a in ARMS for name in [*[raw_name('euler',a,k) for k in POLICY['refinements']],raw_name('reference',a,4)]]
        if attempt!= {'format':'earth-rehearsal-network-attempt-v1','id':result['provenance']['attempt_id'],'study_id':identity(study),'status':'SUCCEEDED','completed_raw':expected_order}:raise BundleError('invalid successful attempt record')
        p=result['provenance']
        if not isinstance(p,dict) or set(p)!= {'attempt_id','source_digest','parent_study_id','python_version','implementation','platform','machine','threads','created_utc','elapsed_seconds'}:raise BundleError('invalid provenance schema')
        import re, math
        if not isinstance(p['attempt_id'],str) or not re.fullmatch(r'[0-9a-f]{32}',p['attempt_id']):raise BundleError('invalid attempt identity')
        if not isinstance(p['source_digest'],str) or not re.fullmatch(r'[0-9a-f]{64}',p['source_digest']):raise BundleError('invalid source digest')
        if p['parent_study_id'] is not None and (not isinstance(p['parent_study_id'],str) or not re.fullmatch(r'[0-9a-f]{64}',p['parent_study_id'])):raise BundleError('invalid parent identity')
        if any(not isinstance(p[k],str) or not p[k].strip() or len(p[k])>200 for k in ('python_version','implementation','platform','machine','created_utc')):raise BundleError('invalid runtime provenance')
        if not re.fullmatch(r'\d+\.\d+\.\d+',p['python_version']):raise BundleError('invalid Python version')
        try:stamp=datetime.datetime.fromisoformat(p['created_utc'])
        except ValueError as exc:raise BundleError('invalid provenance timestamp') from exc
        if stamp.tzinfo is None or type(p['threads']) is not int or p['threads']!=1 or type(p['elapsed_seconds']) not in (int,float) or not math.isfinite(p['elapsed_seconds']) or p['elapsed_seconds']<0:raise BundleError('invalid execution provenance')
        if result['policy']!=POLICY or result['provenance']['source_digest']!=manifest['source_digest']:raise BundleError('network runtime policy/identity mismatch')
        if result['evaluation']!=evaluate(study,result['numerical'],result['references']):raise BundleError('retained network evaluation differs from independent reconstruction')
        for value in result['numerical']:
            if _read(root/raw_name('euler',value['arm'],value['refinement']))!=value:raise BundleError('numerical raw record differs from retained result')
        for value in result['references']:
            if _read(root/raw_name('reference',value['arm'],4))!=value:raise BundleError('reference raw record differs from retained result')
        from .evidence_tables import verify_csv,verify_html
        from .network_report import csv_rows,render
        verify_csv(root/'trajectories.csv',csv_rows(result));verify_html(root/'report.html',render(result))
        return result
    except (TypeError,KeyError,AttributeError,IndexError,OverflowError) as exc:raise BundleError('malformed network bundle') from exc

def reproduce(output,new_output):
    require_distinct_output(output,new_output)
    previous=inspect(output)
    if previous['provenance']['source_digest']!=source_digest():raise BundleError('source digest differs; use the exact matching source package to reproduce')
    return run(previous['study'],new_output,parent_study_id=previous['provenance']['parent_study_id'])

def export(output,new_output):
    require_distinct_output(output,new_output)
    inspect(output);source=Path(output);target=Path(new_output)
    if target.exists():raise BundleError('export output already exists')
    target.mkdir(parents=True);(target/'raw').mkdir()
    for name in (*FILES,'manifest.json'):atomic_write(target/name,(source/name).read_bytes())
    atomic_write(target/'complete.json',(source/'complete.json').read_bytes())
