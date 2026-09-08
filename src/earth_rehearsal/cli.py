"""Offline BOX-001 run, validation, inspection and reproduction commands."""
from __future__ import annotations

import argparse
import copy
import json
import sys
from pathlib import Path

from . import __version__
from . import bundle
from .study import ARMS, POLICY, identity, load, validate


def default_path():
    return Path(__file__).resolve().parents[2] / 'scenarios' / 'box-001.json'


def _summary(result):
    print('BOX-001 | A0_KNOWN_ANSWER | wholly synthetic | Earth Rehearsal ' + __version__)
    print('Arm                       In reservoir kg     Escaped kg    Captured kg')
    for row in result['evaluation']['summaries']:
        if row['refinement'] == 4:
            print(f"{row['arm']:24s} {row['final_mass_kg']:16.9f} {row['escaped_kg']:14.9f} {row['captured_kg']:14.9f}")
    print('Captured mass is transferred through storage to destination_unknown.')
    print('Disposal, lifecycle, ecological and health benefit: NOT_EVALUATED.')


def main(argv=None):
    args_in=list(sys.argv[1:] if argv is None else argv)
    if args_in and args_in[0]=='catchment':
        from .network_cli import main as catchment_main
        return catchment_main(args_in[1:])
    if args_in and args_in[0] in ('campaign','resolution','calibration'):
        from .protocol_cli import main as protocol_main
        return protocol_main(args_in[0],args_in[1:])
    parser = argparse.ArgumentParser(description='Offline synthetic environmental-study controls: BOX-001, catchment, sensitivity, resolution and frozen calibration.')
    parser.add_argument('--version', action='version', version=__version__)
    commands = parser.add_subparsers(dest='command', required=True)
    for name,help_text in [('catchment','source-bound compartment networks and finite capture'),('campaign','frozen sensitivity samples and reversal guards'),('resolution','separate spatial/time error and conservative remapping'),('calibration','freeze, fit, confirm and consume synthetic holdouts')]:commands.add_parser(name,help=help_text,add_help=False)
    run = commands.add_parser('run', help='run all three arms into a new evidence directory')
    run.add_argument('--study', type=Path, default=default_path())
    run.add_argument('--out', type=Path, required=True)
    run.add_argument('--source-factor', type=float, help='synthetic SOURCE_REDUCTION multiplier in [0,1]')
    run.add_argument('--capture-fraction', type=float, help='synthetic OUTLET_CAPTURE fraction in [0,1]')
    check = commands.add_parser('validate-study', help='validate study units, controls and compute budget')
    check.add_argument('study', type=Path)
    inspect = commands.add_parser('inspect', help='verify and reopen a complete bundle without rerunning')
    inspect.add_argument('bundle', type=Path)
    reproduce = commands.add_parser('reproduce', help='rerun a verified bundle from its frozen study and runtime')
    reproduce.add_argument('bundle', type=Path)
    reproduce.add_argument('--out', type=Path, required=True)
    export = commands.add_parser('export', help='copy verified JSON/CSV/HTML evidence to a new directory')
    export.add_argument('bundle', type=Path)
    export.add_argument('--out', type=Path, required=True)
    negative = commands.add_parser('negative-control', help='demonstrate rejection of an invalid conservation or disposal record')
    negative.add_argument('--kind', choices=('conservation', 'disposal', 'source', 'custody'), default='conservation')
    negative.add_argument('--out', type=Path, required=True, help='new JSON diagnostic file')
    args = parser.parse_args(args_in)
    try:
        if args.command == 'run':
            study = load(args.study)
            parent_study_id = identity(study)
            for key in ('source_factor', 'capture_fraction'):
                if getattr(args, key) is not None:
                    study[key] = getattr(args, key)
            result = bundle.run(validate(study), args.out, parent_study_id=parent_study_id if parent_study_id != identity(study) else None)
            _summary(result)
            print('Complete bundle: ' + str(args.out))
        elif args.command == 'validate-study':
            load(args.study)
            print('VALID: BOX-001 study, SI units, fixed-volume forcing and step budget')
        elif args.command == 'inspect':
            _summary(bundle.inspect(args.bundle))
            print('VERIFIED: retained evidence, hashes and independently recomputed balances')
        elif args.command == 'reproduce':
            result = bundle.reproduce(args.bundle, args.out)
            _summary(result)
            print('Reproduced into new bundle: ' + str(args.out))
        elif args.command == 'export':
            import shutil
            bundle.inspect(args.bundle)
            if args.out.exists():
                raise ValueError('export output already exists; choose a new directory')
            # Same verified bundle format preserves reopen/recovery semantics.
            args.out.mkdir(parents=True)
            for name in (*bundle.FILES, 'manifest.json'):
                bundle.atomic_write(args.out / name, (args.bundle / name).read_bytes())
            bundle.atomic_write(args.out / 'complete.json', (args.bundle / 'complete.json').read_bytes())
            print('Exported verified evidence: ' + str(args.out))
        else:
            from .evaluator import EvaluationError, evaluate
            from .numerical import run_arm
            study = load(default_path())
            runs = [run_arm(study, arm, level) for arm in ARMS for level in POLICY['refinements']]
            if args.kind == 'conservation': runs[0]['steps'][0]['closing_mass_kg'] += 0.1
            if args.kind == 'disposal': runs[-1]['claims']['disposal'] = 'SAFELY_DISPOSED'
            if args.kind == 'source': runs[0]['steps'][0]['source_kg'] *= 2
            if args.kind == 'custody': runs[-1]['custody']['transfers'].pop()
            try:
                evaluate(study, runs)
            except EvaluationError as exc:
                diagnostic = {'status': 'EXPECTED_REJECTION', 'control': args.kind, 'reason': str(exc),
                              'applicability': 'A0_KNOWN_ANSWER'}
            else:
                raise ValueError('negative control was incorrectly accepted')
            args.out.parent.mkdir(parents=True, exist_ok=True)
            with args.out.open('x', encoding='utf-8') as file:
                json.dump(diagnostic, file, indent=2)
            print(diagnostic['status'] + ': ' + diagnostic['reason'])
        return 0
    except KeyboardInterrupt:
        print('CANCELLED: partial evidence is retained; rerun study.json into a new directory.', file=sys.stderr)
        return 130
    except (ValueError, OSError, OverflowError) as exc:
        print('ERROR: ' + str(exc), file=sys.stderr)
        return 2
