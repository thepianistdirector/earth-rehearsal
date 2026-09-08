#!/usr/bin/env python3
"""Render owner-defined task scopes and prospective verification; performs no native writes."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent

def read(path): return json.loads(path.read_text())
def dumps(value): return json.dumps(value,indent=2)+'\n'

# Exact current BOX files, grounded in docs/EXECUTION-PACKETS.md and the public source.
S='src/earth_rehearsal/'
BOX_SCOPES={
 '01-01':['scenarios/box-001.json','EXPERIMENTS.md'],
 '01-02':[S+'study.py','tests/test_study.py'],
 '01-03':[S+'study.py','tests/test_study.py','EXPERIMENTS.md'],
 '01-04':[S+'analytic.py',S+'numerical.py','tests/test_numerics.py','EXPERIMENTS.md'],
 '01-05':['docs/decisions/0002-numerical-policy.md',S+'study.py','tests/test_numerics.py'],
 '01-06':['SOURCES.md','NOTICE','LICENSE','scenarios/box-001.json'],
 '01-07':[S+'study.py',S+'cli.py','tests/test_study.py','tests/test_bundle.py'],
 '01-08':['docs/LIMITATIONS.md','EXPERIMENTS.md',S+'report.py','tests/test_report.py'],
 '02-01':[S+'analytic.py','tests/test_numerics.py'],
 '02-02':[S+'numerical.py','tests/test_numerics.py','tests/test_evaluator.py'],
 '02-03':['tests/test_numerics.py','docs/evidence/verification.md'],
 '02-04':[S+'study.py',S+'numerical.py','tests/test_study.py','tests/test_numerics.py'],
 '02-05':[S+'evaluator.py',S+'report.py','tests/test_evaluator.py'],
 '02-06':[S+'study.py',S+'numerical.py','tests/test_study.py'],
 '02-07':[S+'evaluator.py','tests/test_evaluator.py'],
 '02-08':[S+'cli.py','tests/test_bundle.py','tests/test_numerics.py'],
 '03-01':[S+'evaluator.py','tests/test_evaluator.py'],
 '03-02':[S+'evaluator.py','tests/test_evaluator.py'],
 '03-03':[S+'analytic.py',S+'numerical.py',S+'evaluator.py','tests/test_numerics.py','tests/test_evaluator.py'],
 '03-04':[S+'numerical.py',S+'evaluator.py','tests/test_evaluator.py'],
 '03-05':[S+'evaluator.py','tests/test_evaluator.py'],
 '03-06':[S+'evaluator.py','tests/test_evaluator.py'],
 '03-07':[S+'evaluator.py',S+'cli.py','tests/test_evaluator.py'],
 '03-08':[S+'evaluator.py','tests/test_evaluator.py'],
 '04-01':[S+'bundle.py',S+'evaluator.py','tests/test_bundle.py'],
 '04-02':[S+'report.py','tests/test_report.py'],
 '04-03':[S+'evaluator.py',S+'report.py','tests/test_evaluator.py','tests/test_report.py'],
 '04-04':[S+'evaluator.py',S+'cli.py','tests/test_evaluator.py'],
 '04-05':[S+'bundle.py',S+'study.py','tests/test_bundle.py'],
 '04-06':[S+'report.py',S+'bundle.py','tests/test_report.py'],
 '04-07':[S+'report.py','tests/test_report.py','docs/decisions/0003-report-design.md'],
 '04-08':[S+'report.py','docs/LIMITATIONS.md','tests/test_report.py'],
 '05-01':[S+'bundle.py','tests/test_bundle.py'],
 '05-02':[S+'bundle.py','tests/test_bundle.py'],
 '05-03':[S+'bundle.py',S+'cli.py','tests/test_bundle.py'],
 '05-04':['tools/package_release.py','tools/verify_package.py','README.md','NOTICE','LICENSE'],
 '05-05':['docs/REVIEW-KIT.md','docs/evidence/'],
 '05-06':['README.md','STATUS.md','docs/evidence/'],
 '05-07':['plan/','TASKS.md','ROADMAP.md','STATUS.md','tools/render_plan.py','tools/validate_plan.py','tools/prepare_tanduna.py'],
 '05-08':['docs/REVIEW-KIT.md','docs/LIMITATIONS.md','docs/evidence/'],
}
TESTS={
 'study':'python3 -m unittest discover -s tests -p test_study.py -v',
 'numerics':'python3 -m unittest discover -s tests -p test_numerics.py -v',
 'evaluator':'python3 -m unittest discover -s tests -p test_evaluator.py -v',
 'bundle':'python3 -m unittest discover -s tests -p test_bundle.py -v',
 'report':'python3 -m unittest discover -s tests -p test_report.py -v',
}

def build(root=ROOT):
 p=read(root/'plan/tasks.json'); tasks={t['id']:t for t in p['tasks']}; publication=p['publication']
 lines=(root/'plan/verification-cases.tsv').read_text().splitlines(); cases={}
 for line in lines:
  parts=line.split('\t')
  if len(parts)!=3 or parts[0] in cases or not all(part.strip() for part in parts): raise ValueError('malformed or duplicate verification case')
  cases[parts[0]]=parts[1:]
 if set(cases)!=set(tasks): raise ValueError('verification cases must cover every task exactly once')
 review=read(root/'docs/evidence/tanduna-review-2026-09-08.json'); history=review['source_identity_history']
 if set(history)!=set(tasks) or set(publication['platformMapping'])!=set(tasks):
  raise ValueError('native mapping coverage differs from canonical identities')
 if len(set(publication['platformMapping'].values()))!=len(tasks):
  raise ValueError('duplicate native successor identity')
 for tid in tasks:
  if publication['platformMapping'][tid]!=history[tid]['successor']['id']:
   raise ValueError('successor identity differs from authenticated receipt: '+tid)
  revision=publication['platformTaskRevisions'][tid]
  if type(revision) is not int or revision<1:
   raise ValueError('invalid observed task revision: '+tid)
 if set(publication['platformWaveMapping'])!={w['id'] for w in p['waves']}:
  raise ValueError('native wave mapping coverage differs from canonical waves')
 if len(set(publication['platformWaveMapping'].values()))!=len(p['waves']):
  raise ValueError('duplicate native wave identity')
 detailed=read(root/'plan/verification-procedures.json')['procedures']
 if not set(detailed)<=set(tasks): raise ValueError('unknown task in detailed verification')
 entries=[]
 for t in p['tasks']:
  tid=t['id']; positive,negative=cases[tid]
  if tid.startswith('ER-B'):
   paths=BOX_SCOPES[tid[4:]]
   if any(not (root/path).exists() for path in paths): raise ValueError('BOX source path is not observed: '+tid)
   basis=['docs/EXECUTION-PACKETS.md','Public v0.1.0 source tree']
  else:
   owners=[t] if t.get('ownedPaths') else [tasks[k] for k in t['sourceRefs'] if k in tasks and tasks[k].get('ownedPaths')]
   paths=list(dict.fromkeys(path for owner in owners for path in owner['ownedPaths']))
   basis=[owner['id']+' ownedPaths retained in immutable foundation lineage' for owner in owners]
  if not paths or any(path.startswith('/') or '..' in Path(path).parts or path in ('.','./') for path in paths): raise ValueError('unbounded task scope: '+tid)
  commands=[]
  if tid.startswith('ER-B'):
   for key,filename in [('study','test_study.py'),('numerics','test_numerics.py'),('evaluator','test_evaluator.py'),('bundle','test_bundle.py'),('report','test_report.py')]:
    if 'tests/'+filename in paths: commands.append(TESTS[key])
  if tid in ('ER-F02','ER-F03','ER-B05-07'):
   commands=['python3 tools/validate_plan.py --self-test','python3 tools/render_plan.py --check']
  expected_evidence=[
   'A versioned evidence record for '+tid+' naming exact source/build, input and output hashes, environment, performer role, dates and any missing prerequisites.',
   'Inputs and retained outputs from the positive check above, with observed quantities or exact document section references.',
   'A separate record of the failure case above, including the actual rejection/error or review objection and whether it matched the expected behavior.',
   'Actual command output or document section references for every step; expected versus observed results, all failures/skips and the final supported scope. Future evidence is NOT PERFORMED until observed.',
  ]
  steps=[
   'Read the unchanged acceptance below and the listed prerequisite outcomes. Record their actual state. Do not execute dependency-gated future work or adopt tools/data until the applicable prerequisite and authority exist.',
   'Locate the delivered artifact within allowedPaths and its documented reproduction procedure. Record exact artifact/source identity. For future implementations these paths are planned, not an assertion that code or a CLI exists now. Missing required deliverable or runnable instructions is a failed/incomplete check.',
   positive,
   negative+' Use separate synthetic fixtures or disposable copies within the project; preserve originals. Do not damage real user data or execute unapproved adapters.',
   'Compare observations with the exact acceptance, retain the evidence described below and report PASS, FAIL or BLOCKED for each clause. Automated plan consistency never proves scientific applicability, human observation or native publication.',
  ]
  if tid in detailed:
   steps=steps[:2]+detailed[tid]+steps[2:]
  e={'canonicalId':tid,'nativeTaskId':publication['platformMapping'][tid],
     'expectedTaskRevision':publication['platformTaskRevisions'][tid],
     'sourceHistory':history[tid],
     'scope':{'allowedPaths':paths,'sourceBasis':basis,'prohibitedPaths':['.git/','.env','.cache/'],
              'executionBoundary':'Only this project; evidence output may use a fresh project-local runs directory. No shared-host changes, dependency adoption, spending, credentials, publication or field action follows from a path list.'},
     'repository':publication['repository'],
     'models':{'preferred':'gpt-6-astra','reasoningEffort':'high','fallback':None,'fallbackPolicy':'none; do not substitute a model'},
     'requiredSkills':[], 'requiredSkillsPolicy':'Explicitly none, per Lucas; do not add artificial mandatory skills.',
     'deliverable':{'outcome':t['outcome'],'scopePaths':paths,'evidenceLevelNow':t['status'],'targetRelease':t['targetRelease']},
     'acceptanceCriteria':[t['acceptance']],
     'prerequisites':t['prerequisiteOutcomes'],
     'verification':{'automatedCommands':commands,'manual':{'steps':steps,'evidenceToCollect':expected_evidence},
                     'positiveCase':positive,'failureCase':negative},
     'adoptionAndHumanGates':t['riskEvidenceNeeds'],
     'publicationAccess':publication['accessInstructions'],
     'writeScopeNote':'Update only the existing successor revision through supported controls after fresh readback. Preserve the historical contract and frozen predecessor. Scope/verification are prospective preparation, not new implementation or completed evidence.'}
  entries.append(e)
 return {'format':'earth-rehearsal-native-preparation-v1','toolNeutral':True,'notReadyToSubmit':True,
         'project':'earth-rehearsal','correctedProposalId':publication['targetProposalId'],
         'expectedPlanRevision':publication['draftRevision'],'preserveExistingTaskAndWaveIds':True,
         'sourceStateSha256':hashlib.sha256((root/'plan/tasks.json').read_bytes()).hexdigest(),
         'instructions':'Map these semantics to the freshly read supported native schema. verification.manual.evidence must describe prospective records to collect; no future result is asserted. Explicit-none model/skill semantics remain a platform gate until supported. Read current revisions and preserve all unrelated fields. Do not resubmit until actual completeness readback is satisfied.',
         'tasks':entries}

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');args=ap.parse_args()
 output=ROOT/'plan/tanduna-preparation.json'; content=dumps(build())
 if args.check:
  if not output.exists() or output.read_text()!=content: raise SystemExit('FAIL: native preparation drift')
  print('PASS: 221 prepared scopes and distinct positive/failure procedures match canonical identities')
 else:
  output.write_text(content);print('Rendered prospective preparation for 221 existing successor tasks; no native writes')
if __name__=='__main__':main()
