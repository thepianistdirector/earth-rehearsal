#!/usr/bin/env python3
"""Generate review and publication views from the sole canonical task ledger."""
from __future__ import annotations
import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

def dumps(value):
    return json.dumps(value, indent=2, ensure_ascii=False) + '\n'

def render(plan):
    tasks = {t['id']: t for t in plan['tasks']}
    intro = ('Generated from `plan/tasks.json`; edit the canonical ledger, then run '
             '`python3 tools/render_plan.py`. Historical acceptance is preserved in '
             '[lineage](plan/lineage/architecture-foundation-2026-09-07/manifest.json). '
             'A mapped BOX-001 portion does not complete a broader original contract.\n\n')
    task_lines = ['# Earth Rehearsal tasks\n\n', intro,
                  f"{len(tasks)} rows: 27 historical umbrella contracts and {len(tasks)-27} delivery outcomes. "
                  'Umbrellas preserve acceptance; they are not duplicate deliverables. New proposals start PLANNED. '
                  'Implementation, automated checks, runtime evidence, human review and public release are separate evidence levels.\n\n']
    road = ['# Earth Rehearsal roadmap\n\n', intro, plan['objective']+'\n\n',
            'The 0.1 route is W01 → W02 → W03 → W04 → W05. It depends only on the accepted '
            'foundation, not on unfinished catchment or lifecycle contracts. Later 0.x and long-term waves are '
            'proposed research outcomes, not promised dates or allocated reviewer/compute capacity. '
            'The original nine waves remain intact in lineage.\n\n',
            'Cut maps, adapters, scenario breadth and optimization before independent numerics, conservation, custody or reproduction. '
            'Stop ranking on failed conservation, unsupported fate parameters, unresolved rights, or refinement reversal. '
            'Qualified review is required before real environmental interpretation.\n\n',
            '| Order | Wave | Horizon | Rows | Outcome |\n| --- | --- | --- | ---: | --- |\n']
    for w in plan['waves']:
        road.append(f"| {w['order']} | {w['id']} | {w['targetRelease']} | {len(w['tasks'])} | {w['outcome']} |\n")
        task_lines.append(f"## {w['id']} — {w['title']}\n\n")
        for tid in w['tasks']:
            t=tasks[tid]
            task_lines.append(f"### {tid} — {t['title']}\n\n"
                f"- Status: **{t['status']}**; release: {t['targetRelease']}; basis: {t['basis']}; kind: {t['kind']}.\n"
                f"- Outcome: {t['outcome']}\n- Area: {t['featureArea']}; original/canonical wave: {t['wave']}; publication wave: {t['publicationWave']}.\n"
                f"- Prerequisites: {', '.join(t['dependsOn']) or 'none'}.\n- Acceptance: {t['acceptance']}\n"
                f"- Sources: {', '.join(t['sourceRefs'])}.\n- Evidence needs: {' '.join(t['riskEvidenceNeeds'])}\n"
                f"- Recorded evidence: {json.dumps(t.get('evidence', []), ensure_ascii=False)}.\n\n")
    for w in plan['waves']:
        road.append(f"\n## {w['id']} — {w['title']}\n\nOutcome: {w['outcome']}.\n\n"
            f"Entry dependencies: {', '.join(w['entryDependencies']) or 'none'}. "
            'Original umbrella prerequisites remain separately binding in the task graph.\n\n'
            f"Assigned tasks: {', '.join(w['tasks'])}.\n\nExit evidence: {' '.join(w['exitEvidence'])}\n\n"
            f"Release horizon: {w['targetRelease']}.\n")
    road.append('\n## Publication gate\n\n'+plan['publication']['gate']+'\n\n'+plan['publication']['accessInstructions']+'\n')
    task_lines.append('## Source identity mapping\n\n| Original | Treatment | Successors |\n| --- | --- | --- |\n')
    for m in plan['sourceMappings']:
        task_lines.append(f"| {m['sourceKey']} | {m['treatment']} | {', '.join(m['successorIds'])} |\n")
    export={'format':'earth-rehearsal-publication-v1','notPublished':True,'canonicalContract':plan['contractVersion'],
            'objective':plan['objective'],'limits':plan['limits'],'counts':plan['counts'],
            'publication':plan['publication'],'sources':plan['sources'],'waves':plan['waves'],
            'tasks':plan['tasks'],'sourceMappings':plan['sourceMappings']}
    # Placeholders are conspicuous, not fabricated server IDs. This is never directly submitted.
    ids=plan['publication']['platformMapping']
    def native(tid): return ids.get(tid) or '${TASK_ID:'+tid+'}'
    template={'projectSlug':plan['project'],'proposalId':plan['publication'].get('targetProposalId') or '${PROPOSAL_ID:EXPANDED_BOX_001_PROGRAMME}',
              'expectedRevision':None,'plan':{'optionKey':None,
                'waves':[{'name':w['title'],'taskIds':[native(t) for t in w['tasks']]} for w in plan['waves']],
                'unassignedTaskIds':[],
                'dependencies':[{'taskId':native(t['id']),'dependsOnTaskIds':[native(d) for d in t['dependsOn']]} for t in plan['tasks']]}}
    task_templates=[]
    for t in plan['tasks']:
        body=(f"Canonical source identity: earth-rehearsal:{t['id']}\n\n"
              f"Outcome: {t['outcome']}\n\nRelease horizon: {t['targetRelease']}. Publication wave: {t['publicationWave']}.\n\n"
              f"Repository evidence level: {t['status']}. This is not a native runner-reviewed completion.\n\n"
              f"Prerequisite source identities: {', '.join(t['dependsOn']) or 'none'}. Resolve native links from the canonical mapping.\n\n"
              f"Source/decision references: {', '.join(t['sourceRefs'])}.\n\nEvidence needs: {' '.join(t['riskEvidenceNeeds'])}\n\n"
              f"Retained evidence: {', '.join(t.get('evidence', [])) or 'none; planned work'}.\n\n"
              "Preparation record only. Bind repository connection, current base, owned paths, commands, reviewers and scope before execution. "
              "No publication, spending, network authority, untrusted model execution, field action or benefit claim follows from this task. "
              "Historical umbrella acceptance remains unchanged; a narrower successor does not complete it.")
        task_templates.append({'canonicalId':t['id'],'arguments':{'projectSlug':plan['project'],'fields':{
            'title':t['id']+' — '+t['title'],'goal':t['outcome'],'body':body,
            'acceptanceCriteria':[t['acceptance']],'repositoryId':None,'baseSha':None,
            'allowedPaths':t.get('ownedPaths',[]),'prohibitedPaths':['.git/','.env','.cache/'],
            'requiredCommands':[],'networkPolicy':'none','secretScope':[],
            'maxExecutionPermissions':[],'expectedArtifactType':'Scoped outcome evidence; see canonical contract'}}})
    instruction=('Generated native task/create and save_draft argument templates, NOT ready to submit. First read all owner-visible tasks, including unpublished drafts, and reuse matching source identities; do not duplicate unseen drafts. '
                 'Create a new expanded-programme proposal through the supported workflow, preserving the original discussion proposal in source history. '
                 'Resolve every ${PROPOSAL_ID:...} and ${TASK_ID:...} through supported creation/readback, '
                 'read the current saved draft revision and optionKey, preserve server-issued wave IDs on updates, and obtain required authorization. '
                 'Null repository/base values and empty execution permissions are deliberately unready, not fabricated execution authority. Complete required preparation through the supported workflow before requesting review. '
                 'Save/submit only prepares review; it does not establish accepted publication. Read back public counts/dependencies/status separately.\n')
    return {'TASKS.md':''.join(task_lines),'ROADMAP.md':''.join(road),'plan/publication.json':dumps(export),
            'plan/tanduna-save-draft.template.json':dumps(template),
            'plan/tanduna-tasks.template.json':dumps({'notReadyToSubmit':True,'tasks':task_templates}),
            'plan/PUBLICATION.md':instruction}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');parser.add_argument('--root',type=Path,default=ROOT)
    args=parser.parse_args();plan=json.loads((args.root/'plan/tasks.json').read_text())
    drift=[]
    for name,content in render(plan).items():
        p=args.root/name
        if args.check:
            if not p.exists() or p.read_text()!=content:drift.append(name)
        else:p.write_text(content)
    if drift:print('FAIL: generated view drift: '+', '.join(drift));return 1
    print('PASS: generated views match' if args.check else 'Rendered task, roadmap and publication views');return 0

if __name__=='__main__':raise SystemExit(main())
