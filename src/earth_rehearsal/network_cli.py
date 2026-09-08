"""Offline manufactured-catchment command surface."""
from __future__ import annotations
import argparse
import copy
import json
from pathlib import Path
import sys
from . import __version__
from . import network_bundle as bundle
from . import network_study as study_api

def summary(result):
    print('CATCHMENT-001 | A0_KNOWN_ANSWER | wholly synthetic | Earth Rehearsal '+__version__)
    print('Arm                      In compartments kg     Stored kg    Unknown kg    Escaped kg')
    for row in result['evaluation']['summaries']:
        if row['method']=='conservative_euler' and row['refinement']==4:
            print(f"{row['arm']:24s} {row['mass_kg']:18.9f} {row['stored_kg']:13.9f} {row['unknown_kg']:13.9f} {row['escaped_kg']:13.9f}")
    print('Capture and handling quantities are transfers. All disposal/lifecycle/ecological/health benefit: NOT_EVALUATED.')

def main(argv=None):
    parser=argparse.ArgumentParser(prog='earth.py catchment',description='Run and inspect a fictional prescribed-flow compartment study, offline.')
    commands=parser.add_subparsers(dest='command',required=True)
    run=commands.add_parser('run',help='run all paired arms, refinements and independent references')
    run.add_argument('--study',type=Path,default=Path(__file__).resolve().parents[2]/'scenarios/catchment-001.json')
    run.add_argument('--out',type=Path,required=True);run.add_argument('--source-factor',type=float)
    run.add_argument('--capture-capacity',type=float,help='replace each synthetic device capacity in kg')
    check=commands.add_parser('validate',help='validate units, source binding, topology and resource bounds');check.add_argument('study',type=Path)
    inspect=commands.add_parser('inspect',help='reconstruct retained evaluation without rerunning either kernel');inspect.add_argument('bundle',type=Path)
    for action in ('reproduce','export'):
        p=commands.add_parser(action,help=action+' into a fresh evidence directory');p.add_argument('bundle',type=Path);p.add_argument('--out',type=Path,required=True)
    control=commands.add_parser('negative-control',help='demonstrate independent rejection of corrupt evidence')
    control.add_argument('--kind',choices=('conservation','source','exchange','custody','capacity','disposal'),required=True);control.add_argument('--out',type=Path,required=True)
    args=parser.parse_args(argv)
    try:
        if args.command=='run':
            study=study_api.load(args.study);parent=study_api.identity(study)
            if args.source_factor is not None:study=study_api.set_quantity(study,['source_factor'],args.source_factor)
            if args.capture_capacity is not None:
                for i in range(len(study['capture'])):study=study_api.set_quantity(study,['capture',i,'capacity'],args.capture_capacity)
            result=bundle.run(study,args.out,parent_study_id=parent if parent!=study_api.identity(study) else None)
            summary(result);print('Complete bundle: '+str(args.out))
        elif args.command=='validate':
            study=study_api.load(args.study);print('VALID: source-bound SI quantities, balanced water topology, declared synthetic classes and bounded compute; '+study_api.identity(study))
        elif args.command=='inspect':summary(bundle.inspect(args.bundle));print('VERIFIED: hashes, retained raw paths and independently reconstructed balances')
        elif args.command=='reproduce':summary(bundle.reproduce(args.bundle,args.out));print('Reproduced into new bundle: '+str(args.out))
        elif args.command=='export':bundle.export(args.bundle,args.out);print('Exported verified evidence: '+str(args.out))
        else:
            from .network_numerical import run_arm
            from .network_analytic import run_arm as reference
            from .network_evaluator import evaluate,NetworkEvaluationError
            from .network_layout import Layout
            study=study_api.load(Path(__file__).resolve().parents[2]/'scenarios/catchment-001.json');l=Layout(study)
            nums=[run_arm(study,a,k) for a in study_api.ARMS for k in study_api.POLICY['refinements']];refs=[reference(study,a) for a in study_api.ARMS]
            if args.kind=='conservation':nums[0]['records'][1]['state'][l.at('mass','headwater','mobile')]+=.1
            elif args.kind=='source':
                nums[0]['records'][1]['state'][l.at('source','headwater','mobile')]+=.1;nums[0]['records'][1]['state'][l.at('mass','headwater','mobile')]+=.1
            elif args.kind=='exchange':nums[0]['records'][1]['state'][l.at('edge','head_to_middle','mobile')]+=.1
            elif args.kind=='custody':nums[-1]['records'][-1]['state'][l.at('unknown','interceptor','mobile')]=0
            elif args.kind=='capacity':nums[-1]['records'][-1]['state'][l.at('captured','interceptor','mobile')]=1
            elif args.kind=='disposal':nums[-1]['claims']['disposal']='SAFELY_DISPOSED'
            try:evaluate(study,nums,refs)
            except NetworkEvaluationError as exc:diagnostic={'status':'EXPECTED_REJECTION','kind':args.kind,'reason':str(exc),'applicability':'A0_KNOWN_ANSWER'}
            else:raise ValueError('corrupted network evidence was incorrectly accepted')
            args.out.parent.mkdir(parents=True,exist_ok=True)
            with args.out.open('x') as file:json.dump(diagnostic,file,indent=2)
            print(diagnostic['status']+': '+diagnostic['reason'])
        return 0
    except KeyboardInterrupt:
        print('CANCELLED: raw attempts are retained; rerun study.json into a fresh directory.',file=sys.stderr);return 130
    except (ValueError,OSError,OverflowError) as exc:
        print('ERROR: '+str(exc),file=sys.stderr);return 2
