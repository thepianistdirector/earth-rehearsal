"""Command-line observed-data study workflow."""
import argparse
import copy
from datetime import timedelta
from pathlib import Path
import sys
from . import observed_bundle as bundle
from .observed_data import decode, read_bytes, parse_date, ObservationError


def default_snapshot():
    return Path(__file__).resolve().parents[2]/'scenarios/observations/potomac-2021-2024'


def main(argv=None):
    parser = argparse.ArgumentParser(description='Offline descriptive study of pinned USGS daily discharge. No environmental prediction.')
    sub = parser.add_subparsers(dest='command', required=True)
    run = sub.add_parser('run', help='analyze a pinned public-data snapshot into a fresh bundle')
    run.add_argument('--snapshot', type=Path, default=default_snapshot())
    run.add_argument('--study', type=Path, help='default: study.json in the snapshot')
    run.add_argument('--split-date', help='first date of the second comparison period; creates a derived study')
    run.add_argument('--out', type=Path, required=True)
    for command in ('inspect', 'reproduce', 'export'):
        child = sub.add_parser(command)
        child.add_argument('bundle', type=Path)
        if command != 'inspect':
            child.add_argument('--out', type=Path, required=True)
    fetch = sub.add_parser('fetch', help='explicit optional unauthenticated public USGS download; uses network')
    fetch.add_argument('--site', required=True, help='USGS numeric station identifier')
    fetch.add_argument('--start', required=True, help='YYYY-MM-DD, inclusive')
    fetch.add_argument('--end', required=True, help='YYYY-MM-DD, inclusive')
    fetch.add_argument('--split-date', required=True, help='first day in the second comparison period')
    fetch.add_argument('--out', type=Path, required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == 'fetch':
            from .observed_fetch import fetch
            fetch(args.site, args.start, args.end, args.split_date, args.out)
            print('FETCHED_PINNED_PUBLIC_SNAPSHOT: '+str(args.out))
            print('Next: python3 earth.py observations run --snapshot '+str(args.out)+' --out NEW_DIRECTORY')
            return 0
        if args.command == 'run':
            study = decode(read_bytes(args.study or args.snapshot/'study.json'))
            parent = None
            if args.split_date:
                parent = bundle.identity(study)
                split = parse_date(args.split_date)
                study = copy.deepcopy(study)
                study['question'] = 'How do daily-flow distributions and coverage compare before '+split.isoformat()+' and from that date through '+study['end_date']+'?'
                study['periods'] = [
                    {'id': 'Before '+split.isoformat(), 'start_date': study['start_date'], 'end_date': (split-timedelta(days=1)).isoformat()},
                    {'id': 'From '+split.isoformat(), 'start_date': split.isoformat(), 'end_date': study['end_date']}]
            result = bundle.run(args.snapshot, study, args.out, parent_study_id=parent)
        elif args.command == 'inspect':
            result = bundle.inspect(args.bundle)
        elif args.command == 'reproduce':
            result = bundle.reproduce(args.bundle, args.out)
        else:
            bundle.export(args.bundle, args.out)
            print('EXPORTED_VERIFIED_OBSERVATIONS: '+str(args.out))
            return 0
        print('OBSERVED_DESCRIPTIVE | USGS daily mean discharge | no intervention-effect claim')
        print(f'{result["received_records"]} source records / {result["requested_days"]} calendar days')
        print('Retained inclusion states: '+str(result['state_counts']))
        if args.command == 'inspect':
            print('VERIFIED: raw inputs, quality policy, independent decimal statistics and presentation')
        else:
            print('Report: '+str(args.out/'report.html'))
        return 0
    except (ValueError, OSError, KeyError, TypeError, OverflowError) as exc:
        print('ERROR: '+str(exc), file=sys.stderr)
        return 2
