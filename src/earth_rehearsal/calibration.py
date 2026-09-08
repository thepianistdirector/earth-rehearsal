"""Finite-grid calibration and frozen-selection confirmation, with retained attempts."""
import csv
import datetime
from pathlib import Path
import math
import time
import uuid
from . import cohort,network_bundle as network,study_archive as archive
from .network_bundle import _read,_json
from .network_study import set_quantity,validate,identity
from .network_layout import Layout
from .network_report import CSS,esc,table
from .bundle import BundleError,atomic_write,digest_file


def check_parent_hash(value):
    if not isinstance(value,str) or len(value)!=64 or any(c not in '0123456789abcdef' for c in value):raise BundleError('invalid replay parent archive hash')


def parameters(study,p,candidate):
    for parameter in p['parameters']:study=set_quantity(study,parameter['path'],candidate['values'][parameter['id']],validate_result=False)
    return validate(study)

def residuals(p,result,observations):
    rows=[];layout=Layout(result['study'])
    for ob,observed in zip(p['observables'],observations['observations']):
        run=next(r for r in result['numerical'] if r['arm']==ob['arm'] and r['refinement']==4)
        predicted=run['records'][-1]['state'][layout.at(ob['kind'],ob['entity'],ob['class'])]
        rows.append({'observable':ob['id'],'prediction_kg':predicted,'synthetic_observation_kg':observed['value'],'residual_kg':predicted-observed['value']})
    return rows

def selection(p,attempts):
    valid=[a for a in attempts if a['status']=='SUCCEEDED']
    if not valid:return {'status':'NO_VALID_SELECTION','selected':None,'equivalent_candidates':[],'minimum_loss_kg2':None,'candidate_denominator':len(attempts),'scope':'No global identifiability or environmental validation is established.'}
    best=min(a['loss_kg2'] for a in valid)
    tied=[a['id'] for a in valid if a['loss_kg2']<=best+p['loss']['equivalence_absolute']]
    selected=next(c for c in p['candidates'] if c['id']==tied[0])
    status='UNRESOLVED_EQUIVALENT_CANDIDATES' if len(tied)>1 else 'SINGLE_BEST_ON_TESTED_GRID'
    if len(valid)!=len(attempts):status='UNRESOLVED_INCOMPLETE_GRID'
    return {'status':status,'selected':selected,'equivalent_candidates':tied,'minimum_loss_kg2':best,'candidate_denominator':len(attempts),'scope':'Finite tested candidate grid only. Equivalent vectors remain unresolved; selection order breaks ties for reproducibility, not identifiability. No environmental validation is established.'}

def html_report(title,notice,rows,headers,files,extra=''):
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Earth Rehearsal · '+esc(title)+'</title><style>'+CSS+'</style><body><main><div class="eyebrow">Known synthetic controls · frozen protocol</div><h1>'+esc(title)+'</h1><div class="notice">'+esc(notice)+'</div>'+table(title,headers,rows)+extra+'<h2>Evidence files</h2><ul>'+''.join('<li><a href="'+esc(name)+'">'+esc(name)+'</a></li>' for name in files)+'</ul></main></body></html>'


def render_fit(attempts,chosen):
    links=['protocol.json','development.json','context.json','attempts.json','selection.json','losses.csv','archive.json','complete.json']+[a['bundle']+'/report.html' for c in attempts for a in c['cases'] if a['status']=='SUCCEEDED']
    return html_report('A frozen calibration grid','Fit execution used development observations only. These data are known synthetic controls; this is not blinded human or field validation.',[[a['id'],a['status'],a.get('loss_kg2','—')] for a in attempts],['Candidate','Status','Loss kg²'],links,'<p><strong>'+esc(chosen['status'])+'</strong>. '+esc(chosen['scope'])+'</p><p>Equivalent candidates: '+esc(', '.join(chosen['equivalent_candidates']) or 'None')+'. Selected: '+esc(chosen['selected']['id'] if chosen['selected'] else 'None')+'.</p>')

def fit(cohort_path,output,*,checkpoint=None):
    cohort_path=Path(cohort_path)
    with cohort.exclusive(cohort_path):
        if (cohort_path/'holdout-access.json').exists():raise BundleError('holdout already exposed; further fitting against this cohort is refused')
        m,p,data=cohort.development_only(cohort_path);archive.require_matching_source(m)
        root=archive.fresh(output);fit_id=uuid.uuid4().hex
        context={'format':'earth-rehearsal-fit-context-v1','fit_id':fit_id,'cohort_sha256':digest_file(cohort_path/'cohort.json'),'cohort_manifest':m,'holdout_read_by_fit':False}
        for name,value in [('protocol.json',p),('development.json',data),('context.json',context)]:_json(root/name,value)
        receipts=cohort_path/'fit-attempts';receipts.mkdir(exist_ok=True)
        receipt={'fit_id':fit_id,'status':'RUNNING','cohort_sha256':context['cohort_sha256']};_json(receipts/(fit_id+'.json'),receipt)
        attempts=[{'id':c['id'],'status':'NOT_STARTED','cases':[]} for c in p['candidates']];_json(root/'attempts.json',attempts)
        start=time.perf_counter();current=None
        def within(phase):
            archive.files(root)
            if checkpoint:checkpoint(phase)
            if time.perf_counter()-start>=p['budget']['max_seconds']:raise ValueError('calibration wall-time budget exhausted at checkpoint')
        try:
            for index,candidate in enumerate(p['candidates']):
                current=attempts[index]
                if index>=p['budget']['max_candidates'] or time.perf_counter()-start>=p['budget']['max_seconds']:
                    current.update(status='NOT_RUN_BUDGET',reason='Frozen candidate or wall-time budget exhausted',elapsed_seconds=time.perf_counter()-start);_json(root/'attempts.json',attempts);continue
                current['status']='RUNNING';losses=[]
                for ci,(case,observed) in enumerate(zip(p['development'],data['cases'])):
                    attempt={'id':case['id'],'status':'RUNNING'};current['cases'].append(attempt);_json(root/'attempts.json',attempts)
                    try:study=parameters(case['study'],p,candidate)
                    except ValueError as exc:
                        attempt.update(status='INVALID',reason=str(exc));continue
                    name=f'candidates/{index:02d}/cases/{ci:02d}'
                    attempt.update(bundle=name,study_id=identity(study));_json(root/'attempts.json',attempts)
                    try:
                        result=network.run(study,root/name,parent_study_id=identity(case['study']),checkpoint=within)
                    except (ValueError,OSError) as exc:
                        if (root/name/'complete.json').exists():result=network.inspect(root/name)
                        else:attempt.update(status='FAILED',reason=str(exc));_json(root/'attempts.json',attempts);continue
                    rows=residuals(p,result,observed);attempt.update(status='SUCCEEDED',residuals=rows);losses.extend(r['residual_kg']**2 for r in rows);_json(root/'attempts.json',attempts)
                current['status']='SUCCEEDED' if all(a['status']=='SUCCEEDED' for a in current['cases']) else 'INVALID' if any(a['status']=='INVALID' for a in current['cases']) else 'FAILED'
                if current['status']=='SUCCEEDED':current['loss_kg2']=math.fsum(losses)
                _json(root/'attempts.json',attempts)
            chosen=selection(p,attempts);_json(root/'selection.json',chosen)
            with (root/'losses.csv').open('x',newline='') as f:
                w=csv.writer(f);w.writerow(['candidate','status','loss_kg2']);w.writerows([a['id'],a['status'],a.get('loss_kg2')] for a in attempts)
            atomic_write(root/'report.html',render_fit(attempts,chosen))
            archive.seal(root,'calibration-fit');receipt.update(status='SUCCEEDED',selection_sha256=digest_file(root/'selection.json'));_json(receipts/(fit_id+'.json'),receipt);return chosen
        except BaseException as exc:
            if current and current['status']=='RUNNING':
                current['status']='CANCELLED' if isinstance(exc,KeyboardInterrupt) else 'FAILED'
                for item in current['cases']:
                    if item['status']=='RUNNING':item['status']='CANCELLED'
            for item in attempts:
                if item['status']=='NOT_STARTED':item['status']='NOT_RUN_INTERRUPTION'
            _json(root/'attempts.json',attempts);receipt.update(status='CANCELLED' if isinstance(exc,KeyboardInterrupt) else 'FAILED',failure_type=type(exc).__name__);_json(receipts/(fit_id+'.json'),receipt);raise


def inspect_fit(output):
    root=Path(output);archive.verify(root,'calibration-fit');p=cohort.validate_protocol(_read(root/'protocol.json'));data=cohort.validate_observations(_read(root/'development.json'),p,'development');context=_read(root/'context.json')
    if not isinstance(context,dict) or set(context)!= {'format','fit_id','cohort_sha256','cohort_manifest','holdout_read_by_fit'} or context['format']!='earth-rehearsal-fit-context-v1' or context['holdout_read_by_fit'] is not False:raise BundleError('invalid fit context')
    from .sources import digest
    import re
    if not isinstance(context['fit_id'],str) or not re.fullmatch('[0-9a-f]{32}',context['fit_id']):raise BundleError('invalid frozen fit identity')
    cohort.validate_manifest(context['cohort_manifest'])
    if context['cohort_sha256']!=digest(context['cohort_manifest']):raise BundleError('fit cohort identity mismatch')
    for name in ('protocol.json','development.json'):
        entry=context['cohort_manifest']['files'][name]
        if entry['sha256']!=digest_file(root/name) or entry['bytes']!=(root/name).stat().st_size:raise BundleError('fit data differs from frozen cohort')
    attempts=_read(root/'attempts.json')
    if not isinstance(attempts,list) or len(attempts)!=len(p['candidates']):raise BundleError('candidate count mismatch')
    for index,(candidate,current) in enumerate(zip(p['candidates'],attempts)):
        if not isinstance(current,dict) or current.get('id')!=candidate['id']:raise BundleError('candidate identity mismatch')
        if current.get('status')=='NOT_RUN_BUDGET':
            if set(current)!= {'id','status','cases','reason','elapsed_seconds'} or current['cases']!=[] or not isinstance(current['reason'],str):raise BundleError('invalid budget attempt')
            elapsed=current['elapsed_seconds']
            if type(elapsed) not in (int,float) or not math.isfinite(elapsed) or elapsed<0 or (index<p['budget']['max_candidates'] and elapsed<p['budget']['max_seconds']):raise BundleError('candidate omitted without exhausted frozen budget')
            if (root/f'candidates/{index:02d}').exists():raise BundleError('unrun candidate retains computation artifacts')
            if any(a.get('status')!='NOT_RUN_BUDGET' for a in attempts[index:]):raise BundleError('fitting resumed after exhausted budget')
            continue
        if index>=p['budget']['max_candidates']:raise BundleError('fit exceeded frozen candidate budget')
        if not isinstance(current.get('cases'),list) or len(current['cases'])!=len(p['development']):raise BundleError('missing development attempt')
        losses=[];states=[]
        for ci,(case,observed,attempt) in enumerate(zip(p['development'],data['cases'],current['cases'])):
            if attempt.get('id')!=case['id'] or attempt.get('status') not in ('SUCCEEDED','INVALID','FAILED'):raise BundleError('invalid development attempt')
            states.append(attempt['status'])
            try:study=parameters(case['study'],p,candidate)
            except ValueError:
                if set(attempt)!= {'id','status','reason'} or attempt['status']!='INVALID':raise BundleError('invalid parameter case not retained correctly')
                continue
            name=f'candidates/{index:02d}/cases/{ci:02d}'
            if attempt.get('bundle')!=name or attempt.get('study_id')!=identity(study):raise BundleError('development child identity mismatch')
            if attempt['status']=='FAILED':
                if set(attempt)!= {'id','status','bundle','study_id','reason'} or (root/name/'complete.json').exists():raise BundleError('invalid failed development case')
                continue
            if set(attempt)!= {'id','status','bundle','study_id','residuals'} or attempt['status']!='SUCCEEDED':raise BundleError('invalid successful development case')
            result=network.inspect(root/name)
            if result['study']!=study or result['provenance']['parent_study_id']!=identity(case['study']):raise BundleError('development evidence differs from candidate study')
            rows=residuals(p,result,observed)
            if rows!=attempt['residuals']:raise BundleError('development residual mismatch')
            losses.extend(r['residual_kg']**2 for r in rows)
        expected='SUCCEEDED' if all(s=='SUCCEEDED' for s in states) else 'INVALID' if 'INVALID' in states else 'FAILED'
        if current['status']!=expected or set(current)!= ({'id','status','cases','loss_kg2'} if expected=='SUCCEEDED' else {'id','status','cases'}):raise BundleError('candidate aggregation mismatch')
        if expected=='SUCCEEDED' and current['loss_kg2']!=math.fsum(losses):raise BundleError('candidate loss mismatch')
    if (root/'reproduction.json').exists():
        replay=_read(root/'reproduction.json')
        if not isinstance(replay,dict) or set(replay)!= {'format','parent_archive_sha256','mode','scope'} or replay['format']!='earth-rehearsal-frozen-fit-replay-v1' or replay['mode']!='REPLAY_COMPLETED_CASES_WITH_UNCHANGED_SELECTION' or not isinstance(replay['scope'],str) or not replay['scope']:raise BundleError('invalid frozen fit replay marker')
        check_parent_hash(replay['parent_archive_sha256'])
    chosen=selection(p,attempts)
    if _read(root/'selection.json')!=chosen:raise BundleError('frozen selection differs from independent loss reconstruction')
    from .evidence_tables import verify_csv,verify_html
    verify_csv(root/'losses.csv',[['candidate','status','loss_kg2'],*[[a['id'],a['status'],a.get('loss_kg2')] for a in attempts]])
    verify_html(root/'report.html',render_fit(attempts,chosen))
    return chosen


def confirmation_summary(p,attempts,replay):
    residual=[abs(r['residual_kg']) for a in attempts if a['status']=='SUCCEEDED' for r in a['residuals']]
    passed=len(attempts)==len(p['holdout']) and all(a['status']=='SUCCEEDED' for a in attempts) and all(v<=p['loss']['confirmation_max_abs'] for v in residual)
    return {'status':'PASSED_FROZEN_SYNTHETIC_CONFIRMATION' if passed else 'FAILED_FROZEN_SYNTHETIC_CONFIRMATION','mode':'FROZEN_SELECTION_REPLAY' if replay else 'FIRST_RECORDED_HOLDOUT_EVALUATION','threshold_kg':p['loss']['confirmation_max_abs'],'max_absolute_residual_kg':max(residual) if residual else None,'case_denominator':len(p['holdout']),'successful_cases':sum(a['status']=='SUCCEEDED' for a in attempts),'scope':'Known synthetic controls only. Replay provides no new independent holdout evidence; no real-world benefit or global identifiability follows.'}

def render_confirmation(attempts,summary,*,reproduction=False):
    links=['fit/report.html','protocol.json','selection.json','fit-context.json','access.json','holdout.json','attempts.json','summary.json','archive.json','complete.json']+[a['bundle']+'/report.html' for a in attempts if a['status']=='SUCCEEDED']
    if reproduction:links.append('reproduction.json')
    rows=[[a['id'],a['status'],max(abs(r['residual_kg']) for r in a['residuals']) if a['status']=='SUCCEEDED' else a.get('reason','—')] for a in attempts]
    return html_report('Frozen synthetic confirmation',summary['scope'],rows,['Case','Status','Maximum residual kg or failure'],links,'<p><strong>'+esc(summary['status'])+'</strong> · '+esc(summary['mode'])+'. Frozen threshold: '+esc(summary['threshold_kg'])+' kg.</p>')


def confirm(cohort_path,fit_path,output,*,replay=False,checkpoint=None):
    cohort_path=Path(cohort_path);fit_path=Path(fit_path)
    with cohort.exclusive(cohort_path):
        m,p,_=cohort.development_only(cohort_path);archive.require_matching_source(m);chosen=inspect_fit(fit_path)
        if chosen['selected'] is None:raise BundleError('no valid frozen parameter selection to confirm')
        context=_read(fit_path/'context.json')
        if context['cohort_sha256']!=digest_file(cohort_path/'cohort.json'):raise BundleError('fit belongs to a different frozen cohort')
        receipt=_read(network._safe(cohort_path,'fit-attempts/'+context['fit_id']+'.json'))
        expected_receipt={'fit_id':context['fit_id'],'status':'SUCCEEDED','cohort_sha256':context['cohort_sha256'],'selection_sha256':digest_file(fit_path/'selection.json')}
        if receipt!=expected_receipt:raise BundleError('fit selection differs from original successful cohort receipt')
        root=archive.fresh(output);attempts=[{'id':c['id'],'status':'NOT_STARTED'} for c in p['holdout']];_json(root/'attempts.json',attempts)
        archive.export(fit_path,root/'fit','calibration-fit',inspect_fit)
        for name,value in [('protocol.json',p),('selection.json',chosen),('fit-context.json',context)]:_json(root/name,value)
        started=time.perf_counter()
        def within(phase):
            archive.files(root)
            if checkpoint:checkpoint(phase)
            if time.perf_counter()-started>=p['budget']['max_seconds']:raise ValueError('confirmation wall-time budget exhausted at checkpoint')
        try:
            event=cohort.expose(cohort_path,context['fit_id'],digest_file(fit_path/'selection.json'),replay=replay)
            _json(root/'access.json',{'event':event,'replay':replay})
            if checkpoint:checkpoint('after_exposure_before_read')
            data=cohort.validate_observations(cohort.read_frozen(cohort_path,m,'holdout.json'),p,'holdout');_json(root/'holdout.json',data)
            for ci,(case,observed) in enumerate(zip(p['holdout'],data['cases'])):
                attempt=attempts[ci];attempt['status']='RUNNING';_json(root/'attempts.json',attempts)
                try:study=parameters(case['study'],p,chosen['selected'])
                except ValueError as exc:attempt.update(status='INVALID',reason=str(exc));_json(root/'attempts.json',attempts);continue
                name=f'cases/{ci:02d}';attempt.update(bundle=name,study_id=identity(study));_json(root/'attempts.json',attempts)
                try:result=network.run(study,root/name,parent_study_id=identity(case['study']),checkpoint=within)
                except (ValueError,OSError) as exc:
                    if (root/name/'complete.json').exists():result=network.inspect(root/name)
                    else:attempt.update(status='FAILED',reason=str(exc));_json(root/'attempts.json',attempts);continue
                attempt.update(status='SUCCEEDED',residuals=residuals(p,result,observed));_json(root/'attempts.json',attempts)
            summary=confirmation_summary(p,attempts,replay);_json(root/'summary.json',summary)
            atomic_write(root/'report.html',render_confirmation(attempts,summary))
            archive.seal(root,'calibration-confirmation');return summary
        except BaseException:
            for a in attempts:
                if a['status']=='RUNNING':a['status']='CANCELLED'
                elif a['status']=='NOT_STARTED':a['status']='NOT_RUN_INTERRUPTION'
            _json(root/'attempts.json',attempts);raise


def inspect_confirmation(output):
    root=Path(output);archive.verify(root,'calibration-confirmation');p=cohort.validate_protocol(_read(root/'protocol.json'));data=cohort.validate_observations(_read(root/'holdout.json'),p,'holdout');chosen=_read(root/'selection.json');context=_read(root/'fit-context.json');access=_read(root/'access.json')
    from .sources import digest
    if chosen!=inspect_fit(root/'fit') or context!=_read(root/'fit/context.json') or p!=_read(root/'fit/protocol.json'):raise BundleError('confirmation selection differs from retained development evidence')
    if context.get('cohort_sha256')!=digest(context['cohort_manifest']):raise BundleError('confirmation cohort identity mismatch')
    for name in ('protocol.json','holdout.json'):
        entry=context['cohort_manifest']['files'][name]
        if entry['sha256']!=digest_file(root/name) or entry['bytes']!=(root/name).stat().st_size:raise BundleError('confirmation data differs from frozen cohort')
    if not isinstance(access,dict) or set(access)!= {'event','replay'} or type(access['replay']) is not bool:raise BundleError('invalid holdout access descriptor')
    ev=access['event']
    if not isinstance(ev,dict) or set(ev)!= {'format','fit_id','selection_sha256','opened_utc','status'} or ev['format']!='earth-rehearsal-holdout-access-v1' or ev['status']!='EXPOSURE_RECORDED_BEFORE_OBSERVATION_READ' or ev['fit_id']!=context['fit_id'] or ev['selection_sha256']!=digest_file(root/'selection.json'):raise BundleError('holdout access does not bind frozen selection')
    try:date=datetime.datetime.fromisoformat(ev['opened_utc'])
    except (TypeError,ValueError) as exc:raise BundleError('invalid exposure timestamp') from exc
    if date.tzinfo is None:raise BundleError('exposure timestamp requires timezone')
    if chosen.get('selected') not in p['candidates']:raise BundleError('confirmation candidate is outside frozen grid')
    attempts=_read(root/'attempts.json')
    if not isinstance(attempts,list) or len(attempts)!=len(p['holdout']):raise BundleError('confirmation attempt count mismatch')
    for ci,(case,observed,a) in enumerate(zip(p['holdout'],data['cases'],attempts)):
        if not isinstance(a,dict) or a.get('id')!=case['id'] or a.get('status') not in ('SUCCEEDED','INVALID','FAILED'):raise BundleError('invalid confirmation attempt')
        try:study=parameters(case['study'],p,chosen['selected'])
        except ValueError:
            if a['status']!='INVALID' or set(a)!= {'id','status','reason'}:raise BundleError('invalid confirmation admission record')
            continue
        name=f'cases/{ci:02d}'
        if a.get('bundle')!=name or a.get('study_id')!=identity(study):raise BundleError('confirmation child identity mismatch')
        if a['status']=='FAILED':
            if set(a)!= {'id','status','bundle','study_id','reason'} or (root/name/'complete.json').exists():raise BundleError('invalid failed confirmation')
            continue
        if a['status']!='SUCCEEDED' or set(a)!= {'id','status','bundle','study_id','residuals'}:raise BundleError('invalid successful confirmation')
        child=network.inspect(root/name)
        if child['study']!=study or child['provenance']['parent_study_id']!=identity(case['study']) or a['residuals']!=residuals(p,child,observed):raise BundleError('confirmation physics/residual mismatch')
    if (root/'reproduction.json').exists():
        replay=_read(root/'reproduction.json')
        if not isinstance(replay,dict) or set(replay)!= {'format','parent_archive_sha256','mode','fresh_holdout_evidence'} or replay['format']!='earth-rehearsal-frozen-confirmation-replay-v1' or replay['mode']!='FROZEN_SELECTION_REPLAY' or replay['fresh_holdout_evidence'] is not False or access['replay'] is not True:raise BundleError('portable replay cannot become first holdout evidence')
        check_parent_hash(replay['parent_archive_sha256'])
    summary=confirmation_summary(p,attempts,access['replay'])
    if _read(root/'summary.json')!=summary:raise BundleError('confirmation threshold/outcome mismatch')
    from .evidence_tables import verify_html
    verify_html(root/'report.html',render_confirmation(attempts,summary,reproduction=(root/'reproduction.json').exists()))
    return summary


def reproduce_fit(output,new_output):
    """Replay completed development computations without selecting new parameters."""
    source=Path(output);inspect_fit(source);archive.require_matching_source(archive.verify(source,'calibration-fit'))
    target=archive.fresh(new_output);attempts=_read(source/'attempts.json')
    successful=[a['bundle'] for c in attempts for a in c['cases'] if a['status']=='SUCCEEDED']
    for name,path in archive.files(source).items():
        if name in ('archive.json','complete.json','reproduction.json') or any(name.startswith(prefix+'/') for prefix in successful):continue
        (target/name).parent.mkdir(parents=True,exist_ok=True);atomic_write(target/name,path.read_bytes())
    for prefix in successful:
        old=network.inspect(source/prefix);new=network.reproduce(source/prefix,target/prefix)
        if any(old[k]!=new[k] for k in ('study','numerical','references','evaluation')):raise BundleError('frozen fit replay differs from original numerical evidence')
    _json(target/'reproduction.json',{'format':'earth-rehearsal-frozen-fit-replay-v1','parent_archive_sha256':digest_file(source/'archive.json'),'mode':'REPLAY_COMPLETED_CASES_WITH_UNCHANGED_SELECTION','scope':'Original invalid, failed and unrun attempts remain retained. This replay cannot introduce new candidates, retune thresholds or establish fresh holdout evidence.'})
    archive.seal(target,'calibration-fit');return inspect_fit(target)


def reproduce_confirmation(output,new_output):
    source=Path(output);inspect_confirmation(source);archive.require_matching_source(archive.verify(source,'calibration-confirmation'))
    target=archive.fresh(new_output);attempts=_read(source/'attempts.json');successful=[a['bundle'] for a in attempts if a['status']=='SUCCEEDED']
    for name,path in archive.files(source).items():
        if name in ('archive.json','complete.json','reproduction.json') or name.startswith('fit/') or any(name.startswith(prefix+'/') for prefix in successful):continue
        (target/name).parent.mkdir(parents=True,exist_ok=True);atomic_write(target/name,path.read_bytes())
    reproduce_fit(source/'fit',target/'fit')
    for prefix in successful:
        old=network.inspect(source/prefix);new=network.reproduce(source/prefix,target/prefix)
        if any(old[k]!=new[k] for k in ('study','numerical','references','evaluation')):raise BundleError('frozen confirmation replay differs from original evidence')
    access=_read(target/'access.json');access['replay']=True;_json(target/'access.json',access)
    p=_read(target/'protocol.json');summary=confirmation_summary(p,attempts,True);_json(target/'summary.json',summary)
    atomic_write(target/'report.html',render_confirmation(attempts,summary,reproduction=True))
    _json(target/'reproduction.json',{'format':'earth-rehearsal-frozen-confirmation-replay-v1','parent_archive_sha256':digest_file(source/'archive.json'),'mode':'FROZEN_SELECTION_REPLAY','fresh_holdout_evidence':False})
    archive.seal(target,'calibration-confirmation');return inspect_confirmation(target)
