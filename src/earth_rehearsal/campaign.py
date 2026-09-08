"""Frozen ordered sensitivity cases; invalid and unrun samples stay in denominators."""
import csv
import math
from pathlib import Path
import time
from . import network_bundle as network
from . import study_archive as archive
from .network_study import validate,identity,set_quantity,keys,identifier,number
from .network_bundle import _json,_read
from .network_report import CSS,esc,table
from .bundle import BundleError

class CampaignDeadline(ValueError):pass

def validate_protocol(p):
    keys(p,('format','id','base_study','parameters','dependence','cases','budget'),'campaign')
    if p['format']!='earth-rehearsal-campaign-v1':raise ValueError('unsupported campaign format')
    identifier(p['id'],'campaign.id');validate(p['base_study'])
    keys(p['dependence'],('kind','description'),'dependence')
    if p['dependence']['kind'] not in ('EXPLICIT_JOINT_SAMPLES','ONE_AT_A_TIME','SCENARIO_SET'):raise ValueError('explicit dependence classification required')
    if not isinstance(p['dependence']['description'],str) or not 1<=len(p['dependence']['description'])<=1000:raise ValueError('bounded dependence description required')
    if not isinstance(p['parameters'],list) or not 1<=len(p['parameters'])<=16:raise ValueError('1..16 explicit parameters required')
    seen=set();paths=set();bindings=set()
    for parameter in p['parameters']:
        keys(parameter,('id','path','unit'),'parameter');identifier(parameter['id'],'parameter.id')
        if parameter['id'] in seen:raise ValueError('duplicate parameter');
        seen.add(parameter['id']);path=parameter['path']
        if not isinstance(path,list) or not 1<=len(path)<=8 or any(type(k) not in (str,int) or isinstance(k,str) and len(k)>100 or isinstance(k,int) and k<0 for k in path):raise ValueError('invalid source quantity path')
        if tuple(path) in paths:raise ValueError('duplicate parameter path')
        paths.add(tuple(path));obj=p['base_study']
        try:
            for key in path:obj=obj[key]
        except (KeyError,IndexError,TypeError) as exc:raise ValueError('unresolved parameter path') from exc
        if not isinstance(obj,dict) or set(obj)!= {'value','unit','source'} or obj['unit']!=parameter['unit']:raise ValueError('parameter must bind an existing quantity and exact unit')
        binding=(obj['source']['record'],obj['source']['variable'])
        if binding in bindings:raise ValueError('parameters cannot alias the same source variable')
        bindings.add(binding)
    if not isinstance(p['cases'],list) or not 1<=len(p['cases'])<=32:raise ValueError('1..32 explicit cases required')
    seen_cases=set()
    for case in p['cases']:
        keys(case,('id','values'),'case');identifier(case['id'],'case.id')
        if case['id'] in seen_cases:raise ValueError('duplicate case')
        seen_cases.add(case['id']);keys(case['values'],seen,'case.values')
        for value in case['values'].values():number(value,-1e12,1e12,'sample')
        if p['dependence']['kind']=='ONE_AT_A_TIME':
            changed=0
            for parameter in p['parameters']:
                obj=p['base_study']
                for key in parameter['path']:obj=obj[key]
                changed+=case['values'][parameter['id']]!=obj['value']
            if changed>1:raise ValueError('ONE_AT_A_TIME sample changes multiple parameters')
    keys(p['budget'],('max_attempts','max_seconds'),'budget')
    if type(p['budget']['max_attempts']) is not int or not 1<=p['budget']['max_attempts']<=32:raise ValueError('attempt budget must be 1..32')
    number(p['budget']['max_seconds'],.01,120,'wall budget')
    return p

def case_study(protocol,case):
    result=protocol['base_study']
    for parameter in protocol['parameters']:
        result=set_quantity(result,parameter['path'],case['values'][parameter['id']],validate_result=False)
    return validate(result)

def summarize(p,attempts,results):
    rows=[];signs={};counts={k:0 for k in ('SUCCEEDED','INVALID','FAILED','NOT_RUN_BUDGET')}
    for case,attempt in zip(p['cases'],attempts):
        status=attempt['status'];counts[status]+=1
        if status!='SUCCEEDED':continue
        result=results[case['id']]
        fine=[r for r in result['evaluation']['summaries'] if r['method']=='conservative_euler' and r['refinement']==4]
        for value in fine:
            rows.append({'case':case['id'],'arm':value['arm'],**{k:value[k] for k in ('mass_kg','stored_kg','unknown_kg','escaped_kg','prevented_source_kg')}})
        for comparison in result['evaluation']['comparisons']:
            key=tuple(comparison['arms']);d=comparison['differences'][-1]
            sign=1 if d>0 else -1 if d<0 else 0
            signs.setdefault(key,[]).append({'case':case['id'],'sign':sign,'within_case_status':comparison['status']})
    reversals=[]
    for arms,items in signs.items():
        values={i['sign'] for i in items};unresolved=any(i['within_case_status']!='ORDER_STABLE_IN_TESTED_GRIDS' for i in items)
        status='UNRESOLVED_NUMERICAL_ORDER' if unresolved else 'ORDER_REVERSES_ACROSS_SAMPLES' if -1 in values and 1 in values else 'NO_REVERSAL_IN_VALID_SAMPLES'
        reversals.append({'arms':list(arms),'status':status,'cases':items})
    return {'status':'PROTOCOL_COMPLETED','applicability':'A0_KNOWN_ANSWER','counts':counts,'denominator':len(p['cases']),'rows':rows,'comparisons':reversals,'scope':'Explicit tested samples only; no probability distribution, optimum or environmental validation.'}

def report(p,attempts,summary):
    rows=[[a['id'],a['status'],a.get('reason',''),a.get('bundle','—')] for a in attempts]
    body='<div class="eyebrow">Wholly synthetic · explicit samples</div><h1>Sensitivity, with every attempt retained.</h1><div class="notice">This completed protocol does not make failed cases valid. No ecological, health, disposal or lifecycle benefit is evaluated.</div>'
    body+='<p>'+esc(p['dependence']['description'])+'</p>'+table('All '+str(summary['denominator'])+' scheduled samples',['Case','Status','Reason','Evidence directory'],rows)
    body+='<p>'+esc(summary['scope'])+'</p>'+table('Paired final quantities, valid samples only',['Case','Arm','Compartments kg','Stored kg','Unknown kg','Escaped kg','Prevented source kg'],[[r[k] for k in ('case','arm','mass_kg','stored_kg','unknown_kg','escaped_kg','prevented_source_kg')] for r in summary['rows']])
    body+=table('Ordering across sampled conditions',['Arms','Status'],[[' / '.join(c['arms']),c['status']] for c in summary['comparisons']])
    body+='<h2>Evidence files</h2><ul>'+''.join('<li><a href="'+name+'">'+name+'</a></li>' for name in ('protocol.json','attempts.json','summary.json','summary.csv','archive.json','complete.json'))
    body+=''.join('<li><a href="'+esc(a['bundle'])+'/report.html">'+esc(a['id'])+' · complete network evidence</a></li>' for a in attempts if a['status']=='SUCCEEDED')+'</ul>'
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Earth Rehearsal · sensitivity campaign</title><style>'+CSS+'</style><body><main>'+body+'</main></body></html>'

def run(p,output,*,checkpoint=None):
    validate_protocol(p);root=archive.fresh(output);_json(root/'protocol.json',p)
    attempts=[{'id':c['id'],'status':'NOT_STARTED'} for c in p['cases']];_json(root/'attempts.json',attempts)
    start=time.perf_counter();attempt_count=0;results={};current=None
    def within(phase):
        archive.files(root)
        if checkpoint:checkpoint(phase)
        if time.perf_counter()-start>=p['budget']['max_seconds']:raise CampaignDeadline('frozen wall-time budget exhausted at checkpoint')
    try:
        for index,case in enumerate(p['cases']):
            current=attempts[index]
            if attempt_count>=p['budget']['max_attempts'] or time.perf_counter()-start>=p['budget']['max_seconds']:
                current.update(status='NOT_RUN_BUDGET',reason='Frozen attempt or wall-time budget exhausted',elapsed_seconds=time.perf_counter()-start);_json(root/'attempts.json',attempts);continue
            attempt_count+=1;current['status']='RUNNING';_json(root/'attempts.json',attempts)
            try:study=case_study(p,case)
            except ValueError as exc:
                current.update(status='INVALID',reason=str(exc));_json(root/'attempts.json',attempts);continue
            current['bundle']=f'cases/{index:03d}-{case["id"]}';current['study_id']=identity(study);_json(root/'attempts.json',attempts)
            try:
                results[case['id']]=network.run(study,root/current['bundle'],parent_study_id=identity(p['base_study']),checkpoint=within)
                current['status']='SUCCEEDED'
            except (ValueError,OSError) as exc:
                # A post-activation callback may fail after valid evidence exists.
                if (root/current['bundle']/'complete.json').is_file():
                    results[case['id']]=network.inspect(root/current['bundle']);current['status']='SUCCEEDED'
                else:current.update(status='FAILED',reason=str(exc),failure_type=type(exc).__name__)
            _json(root/'attempts.json',attempts)
        summary=summarize(p,attempts,results);_json(root/'summary.json',summary)
        with (root/'summary.csv').open('x',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=['case','arm','mass_kg','stored_kg','unknown_kg','escaped_kg','prevented_source_kg']);writer.writeheader();writer.writerows(summary['rows'])
        from .bundle import atomic_write
        atomic_write(root/'report.html',report(p,attempts,summary));archive.seal(root,'campaign');return summary
    except BaseException:
        if current and current['status']=='RUNNING':current['status']='CANCELLED'
        for attempt in attempts:
            if attempt['status']=='NOT_STARTED':attempt['status']='NOT_RUN_INTERRUPTION'
        _json(root/'attempts.json',attempts);raise

def inspect(output):
    root=Path(output);archive.verify(root,'campaign');p=validate_protocol(_read(root/'protocol.json'));attempts=_read(root/'attempts.json');results={}
    if not isinstance(attempts,list) or len(attempts)!=len(p['cases']):raise BundleError('campaign attempt count mismatch')
    for index,(case,attempt) in enumerate(zip(p['cases'],attempts)):
        if not isinstance(attempt,dict) or attempt.get('id')!=case['id'] or attempt.get('status') not in ('SUCCEEDED','INVALID','FAILED','NOT_RUN_BUDGET'):raise BundleError('invalid terminal campaign attempt')
        status=attempt['status']
        expected={'id','status','bundle','study_id'} if status=='SUCCEEDED' else {'id','status','bundle','study_id','reason','failure_type'} if status=='FAILED' else {'id','status','reason','elapsed_seconds'} if status=='NOT_RUN_BUDGET' else {'id','status','reason'}
        if set(attempt)!=expected:raise BundleError('invalid campaign attempt schema')
        if status!='SUCCEEDED' and (not isinstance(attempt['reason'],str) or not attempt['reason']):raise BundleError('missing attempt reason')
        if status=='NOT_RUN_BUDGET':
            elapsed=attempt['elapsed_seconds']
            if type(elapsed) not in (int,float) or not math.isfinite(elapsed) or elapsed<0 or (index<p['budget']['max_attempts'] and elapsed<p['budget']['max_seconds']):raise BundleError('sample omitted without exhausted frozen budget')
            if (root/f'cases/{index:03d}-{case["id"]}').exists():raise BundleError('unrun sample retains child computation artifacts')
            if any(a.get('status')!='NOT_RUN_BUDGET' for a in attempts[index:]):raise BundleError('campaign resumed after exhausted budget')
            continue
        if index>=p['budget']['max_attempts']:raise BundleError('campaign exceeded frozen attempt budget')
        try:study=case_study(p,case)
        except ValueError:
            if status!='INVALID':raise BundleError('invalid case claimed runnable')
            continue
        if status=='INVALID':raise BundleError('admitted case falsely labelled invalid')
        name=f'cases/{index:03d}-{case["id"]}'
        if attempt['bundle']!=name or attempt['study_id']!=identity(study):raise BundleError('child identity/path mismatch')
        if status=='SUCCEEDED':
            child=network.inspect(root/name)
            if child['study']!=study or child['provenance']['parent_study_id']!=identity(p['base_study']):raise BundleError('child differs from frozen sample')
            results[case['id']]=child
        elif (root/name/'complete.json').exists():raise BundleError('failed sample has completed evidence')
    summary=summarize(p,attempts,results)
    if _read(root/'summary.json')!=summary:raise BundleError('campaign summary differs from reconstructed children')
    from .evidence_tables import verify_csv,verify_html
    fields=['case','arm','mass_kg','stored_kg','unknown_kg','escaped_kg','prevented_source_kg']
    verify_csv(root/'summary.csv',[fields,*[[r[k] for k in fields] for r in summary['rows']]])
    verify_html(root/'report.html',report(p,attempts,summary))
    return summary

def reproduce(output,new_output):
    inspect(output);archive.require_matching_source(archive.verify(Path(output),'campaign'))
    return run(_read(Path(output)/'protocol.json'),new_output)
