#!/usr/bin/env python3
"""Validate the canonical graph, immutable lineage, scope and generated views.

--self-test executes adversarial in-memory mutations, never changes source evidence.
"""
from __future__ import annotations
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re
import sys
import shutil
import tempfile
sys.path.insert(0, str(Path(__file__).resolve().parent))
from render_plan import render

ROOT=Path(__file__).resolve().parent.parent
LINEAGE='plan/lineage/architecture-foundation-2026-09-07'
STATUSES={'PLANNED','IN_PROGRESS','IN PROGRESS','IMPLEMENTED','AUTOMATED_PASS','AUTOMATED PASS','RUNTIME_VERIFIED','RUNTIME VERIFIED','USER_VALIDATED','USER VALIDATED','RELEASE_VERIFIED','RELEASE VERIFIED','READY_FOR_REVIEW','DONE','BLOCKED','FAILED','NOT_TESTED','NOT TESTED'}
TEXT=('id','title','outcome','featureArea','targetRelease','acceptance','basis','kind','outcomeKey','publicationWave')
LIST=('dependsOn','sourceRefs','riskEvidenceNeeds','evidence')

def validate(plan, root=ROOT, views=None):
    errors=[]
    def check(condition,message):
        if not condition:errors.append(message)
    if not isinstance(plan,dict):return ['plan must be an object']
    check(plan.get('schemaVersion')==3 and not isinstance(plan.get('schemaVersion'),bool),'schemaVersion must be 3')
    check(plan.get('project')=='earth-rehearsal','wrong project')
    check(plan.get('stateAuthority')=='plan/tasks.json','canonical state authority mismatch')
    rows=plan.get('tasks');waves=plan.get('waves');maps=plan.get('sourceMappings')
    if not isinstance(rows,list) or not isinstance(waves,list) or not isinstance(maps,list):return errors+['tasks, waves and sourceMappings must be arrays']
    check(200<=len(rows)<=400,'task count outside 200–400')
    check(1<=len(waves)<=32,'active wave count exceeds native capacity')
    if any(not isinstance(t,dict) or not isinstance(t.get('id'),str) for t in rows+waves):return errors+['each task/wave requires string id']
    ids=[t['id'] for t in rows];tasks={t['id']:t for t in rows};wids=[w['id'] for w in waves]
    check(len(set(ids))==len(ids),'duplicate task IDs');check(len(set(wids))==len(wids),'duplicate wave IDs')
    for t in rows:
        for field in TEXT:check(isinstance(t.get(field),str) and bool(t[field].strip()),f"{t['id']}: missing {field}")
        for field in LIST:check(isinstance(t.get(field),list),f"{t['id']}: invalid {field}")
        check(t.get('status') in STATUSES,f"{t['id']}: invalid status")
        check(t.get('targetRelease') in {'historical','0.1','0.x','long-term','exploratory'},f"{t['id']}: invalid horizon")
        if t.get('status') not in {'PLANNED','NOT_TESTED','NOT TESTED'} and t.get('kind')!='historical_contract':check(bool(t.get('evidence')),f"{t['id']}: advanced status needs evidence")
    if errors:return errors
    keys=[t['outcomeKey'].strip().casefold() for t in rows]
    check(len(keys)==len(set(keys)),'duplicate outcome keys')
    delivery=[t for t in rows if t['kind']=='delivery_outcome']
    for field in ['title','acceptance']:
        normalized=[re.sub(r'\W+',' ',t[field]).strip().casefold() for t in delivery]
        check(len(set(normalized))==len(normalized),'duplicate delivery '+field)
    ordering={w['id']:i for i,w in enumerate(waves)}
    for t in rows:
        deps=t['dependsOn']
        if any(not isinstance(d,str) for d in deps):errors.append(t['id']+': malformed dependency');continue
        check(len(deps)==len(set(deps)),t['id']+': duplicate prerequisite')
        check(t['publicationWave'] in wids,t['id']+': orphan wave')
        cover=t.get('prerequisiteOutcomes',{})
        check(isinstance(cover,dict) and set(cover)==set(deps),t['id']+': prerequisite outcome coverage missing')
        for dep in deps:
            if dep not in tasks:errors.append(t['id']+': dangling prerequisite '+dep);continue
            check(cover.get(dep)==tasks[dep]['outcome'],t['id']+': prerequisite outcome coverage stale')
            if t['publicationWave'] in ordering and tasks[dep]['publicationWave'] in ordering:
                check(ordering[tasks[dep]['publicationWave']]<=ordering[t['publicationWave']],t['id']+': dependency wave ordering')
            if t['targetRelease']=='0.1':check(tasks[dep]['targetRelease'] in {'historical','0.1'},t['id']+': 0.1 depends on later scope')
        for ref in t['sourceRefs']:check(ref in plan.get('sources',{}) or ref in tasks,t['id']+': unresolved source reference '+str(ref))
    visiting=set();done=set()
    def visit(tid):
        if tid in visiting:errors.append('dependency cycle: '+tid);return
        if tid in done:return
        visiting.add(tid)
        for dep in tasks[tid]['dependsOn']:
            if isinstance(dep,str) and dep in tasks:visit(dep)
        visiting.remove(tid);done.add(tid)
    for tid in ids:visit(tid)
    assigned=[]
    for i,w in enumerate(waves):
        check(w.get('order')==i and not isinstance(w.get('order'),bool),'wave order mismatch '+w['id'])
        for f in ['title','outcome','targetRelease']:check(isinstance(w.get(f),str) and bool(w[f]),'wave missing '+f)
        for f in ['entryDependencies','tasks','exitEvidence']:check(isinstance(w.get(f),list) and (f=='entryDependencies' or bool(w[f])),'wave invalid '+f)
        check(len(w.get('title',''))<=80,'native wave title too long')
        if not all(isinstance(w.get(f),list) for f in ['tasks','entryDependencies']):continue
        assigned+=w['tasks']
        positions={tid:i for i,tid in enumerate(w['tasks'])}
        for tid in w['tasks']:
            if tid in tasks:
                for dep in tasks[tid]['dependsOn']:
                    if isinstance(dep,str) and dep in positions:check(positions[dep]<positions[tid],'within-wave dependency ordering '+tid)
        for tid in w['tasks']:
            check(tid in tasks,'wave dangling task')
            if tid in tasks:
                check(tasks[tid]['publicationWave']==w['id'],'wave membership mismatch '+tid)
                check(tasks[tid]['targetRelease']==w['targetRelease'],'wave release mismatch '+tid)
        for dep in w['entryDependencies']:check(dep in tasks,'wave dangling entry dependency')
        actual={d for tid in w['tasks'] if tid in tasks and tasks[tid]['kind']=='delivery_outcome' for d in tasks[tid]['dependsOn'] if d not in w['tasks']}
        # An original retained contract can itself be an entry prerequisite in its publication wave.
        check(set(w['entryDependencies'])<=actual|set(w['tasks']),'wave entry not covered by prerequisite outcomes')
    check(sorted(assigned)==sorted(ids),'orphan or multiply assigned task')
    lineage=root/LINEAGE
    try:
        manifest=json.loads((lineage/'manifest.json').read_text())
        check(manifest.get('sourceCommit')=='a7e2fe7bc47726798ef01364f692a4ceb53f36e1','lineage source revision changed')
        check(manifest['files'].get('plan--tasks.json')=='fec221969ddb9ff46831a758e1cacbf5d4d32042cd342e4f608b6212db0dedbf','lineage original plan digest changed')
        for name,digest in manifest['files'].items():check(hashlib.sha256((lineage/name).read_bytes()).hexdigest()==digest,'immutable lineage changed: '+name)
        original=json.loads((lineage/'plan--tasks.json').read_text())['tasks']
    except (OSError,ValueError,KeyError) as exc:return errors+['lineage unreadable: '+str(exc)]
    check(len(original)==27,'lineage count changed')
    mids=[m.get('sourceId') for m in maps if isinstance(m,dict)]
    check(len(mids)==27 and set(mids)=={t['id'] for t in original},'missing or duplicate source mappings')
    mapped={m['sourceId']:m for m in maps if isinstance(m,dict) and 'sourceId' in m}
    for old in original:
        tid=old['id'];new=tasks.get(tid)
        if not new:errors.append('missing original identity '+tid);continue
        for field in ['id','title','wave','acceptance','dependsOn','ownedPaths']:
            check(new.get(field)==old[field],'original contract changed: '+tid+' '+field)
        if tid.startswith('ER-F'):check(new['status']=='DONE','foundation completion lost')
        m=mapped.get(tid,{})
        check(m.get('originalAcceptance')==old['acceptance'],'source acceptance mapping changed '+tid)
        check(m.get('structuredPrerequisites')==old['dependsOn'],'source prerequisites changed '+tid)
        check(m.get('textualPrerequisites')==[],'textual prerequisite history changed '+tid)
        check(m.get('revision')=='architecture-foundation-2026-09-07','frozen revision changed '+tid)
        check(m.get('sourceKey')=='earth-rehearsal:'+tid,'source key changed '+tid)
        check(m.get('treatment') in {'retained','expanded','split','merged','deferred','superseded'} and bool(m.get('reason')),'source treatment missing '+tid)
        check(m.get('successorIds') and tid in m['successorIds'],'source successor mapping missing '+tid)
        for successor in m.get('successorIds',[]):check(successor in tasks,'dangling successor '+str(successor))
        expected={tid}|{t['id'] for t in delivery if tid in t['sourceRefs']}
        check(set(m.get('successorIds',[]))==expected,'successor coverage mismatch '+tid)
    expected_counts={'tasks':len(rows),'waves':len(waves),'historicalContracts':27,'deliveryOutcomes':len(delivery),'release01':sum(t['targetRelease']=='0.1' for t in rows)}
    check(plan.get('counts')==expected_counts,'canonical counts mismatch')
    if not errors:
        expected=render(plan)
        for path,content in expected.items():
            try:actual=views[path] if views is not None else (root/path).read_text()
            except (OSError,KeyError):actual=None
            check(actual==content,'generated view drift: '+path)
    return errors

def self_test(plan,root):
    probes=[]
    def probe(name,mutate,needle):
        p=copy.deepcopy(plan);mutate(p);errors=validate(p,root,render(plan))
        if not any(needle in e for e in errors):raise AssertionError(name+' failed to detect defect: '+str(errors))
        probes.append(name)
    probe('missing original',lambda p:p['tasks'].pop(0),'missing original')
    probe('frozen acceptance',lambda p:p['tasks'][0].update(acceptance='Narrowed away'),'original contract changed')
    probe('missing mapping',lambda p:p['sourceMappings'].pop(),'source mappings')
    probe('dangling dependency',lambda p:p['tasks'][-1]['dependsOn'].append('ER-MISSING'),'dangling prerequisite')
    probe('dependency cycle',lambda p:p['tasks'][-1]['dependsOn'].append(p['tasks'][-1]['id']),'dependency cycle')
    probe('wrong project',lambda p:p.update(project='other'),'wrong project')
    probe('duplicate outcome',lambda p:p['tasks'][-1].update(outcomeKey=p['tasks'][-2]['outcomeKey']),'duplicate outcome')
    probe('orphan task',lambda p:p['waves'][-1]['tasks'].pop(),'orphan or multiply')
    probe('release scope',lambda p:next(t for t in p['tasks'] if t['targetRelease']=='0.1')['dependsOn'].append('ER-024'),'0.1 depends on later')
    probe('coverage mismatch',lambda p:p['tasks'][-1].update(prerequisiteOutcomes={}),'prerequisite outcome coverage')
    probe('task order',lambda p:p['waves'][0]['tasks'].reverse(),'within-wave dependency ordering')
    probe('wave order',lambda p:p['waves'][-1].update(order=0),'wave order')
    probe('false completion',lambda p:p['tasks'][-1].update(status='DONE'),'advanced status needs evidence')
    probe('duplicate acceptance',lambda p:p['tasks'][-1].update(acceptance=p['tasks'][-2]['acceptance']),'duplicate delivery acceptance')
    probe('malformed dependency',lambda p:p['tasks'][-1].update(dependsOn=[42]),'malformed dependency')
    probe('count drift',lambda p:p['counts'].update(tasks=200),'counts mismatch')
    probe('lost successor',lambda p:p['sourceMappings'][3]['successorIds'].pop(),'successor coverage mismatch')
    with tempfile.TemporaryDirectory(prefix='.lineage-probe-',dir=root/'plan') as directory:
        isolated=Path(directory);shutil.copytree(root/LINEAGE,isolated/LINEAGE)
        snapshot=isolated/LINEAGE/'TASKS.md';snapshot.write_text(snapshot.read_text()+'\nAltered history\n')
        assert any('immutable lineage changed' in e for e in validate(plan,isolated,render(plan)))
        probes.append('immutable history tamper')
    views=render(plan);views['TASKS.md']+='Undeclared status change\n'
    assert any('generated view drift' in e for e in validate(plan,root,views));probes.append('generated view drift')
    assert validate([],root)==['plan must be an object'];probes.append('non-object plan')
    print('PASS: '+str(len(probes))+' negative probes: '+', '.join(probes))
    return probes

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--root',type=Path,default=ROOT);parser.add_argument('--self-test',action='store_true');args=parser.parse_args()
    try:plan=json.loads((args.root/'plan/tasks.json').read_text())
    except (OSError,ValueError) as exc:print('FAIL: '+str(exc));return 1
    errors=validate(plan,args.root)
    if errors:
        for e in errors:print('FAIL: '+e,file=sys.stderr)
        return 1
    if args.self_test:self_test(plan,args.root)
    print(f"PASS: {len(plan['tasks'])} tasks, {len(plan['waves'])} active waves, {sum(len(t['dependsOn']) for t in plan['tasks'])} links; lineage, mappings, scope, DAG and generated views")
    return 0

if __name__=='__main__':raise SystemExit(main())
