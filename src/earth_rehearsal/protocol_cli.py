"""Offline sensitivity, resolution and frozen calibration command surfaces."""
import argparse
from pathlib import Path
import sys
from . import campaign,resolution,cohort,calibration,study_archive
from .network_bundle import _read

DEFAULTS=Path(__file__).resolve().parents[2]/'scenarios'

def main(kind,argv):
    parser=argparse.ArgumentParser(prog='earth.py '+kind,description='Bounded, wholly synthetic study protocols with retained attempts and offline evidence.')
    commands=parser.add_subparsers(dest='action',required=True)
    if kind in ('campaign','resolution'):
        api=campaign if kind=='campaign' else resolution
        for action in ('run','validate'):
            p=commands.add_parser(action);p.add_argument('--protocol',type=Path,default=DEFAULTS/(kind+'-001.json'))
            if action=='run':p.add_argument('--out',type=Path,required=True)
    else:
        p=commands.add_parser('freeze',help='freeze development/holdout data and thresholds before fitting')
        p.add_argument('--protocol',type=Path,default=DEFAULTS/'calibration/protocol.json');p.add_argument('--development',type=Path,default=DEFAULTS/'calibration/development.json');p.add_argument('--holdout',type=Path,default=DEFAULTS/'calibration/holdout.json');p.add_argument('--out',type=Path,required=True)
        p=commands.add_parser('fit',help='fit frozen candidates using development observations only');p.add_argument('cohort',type=Path);p.add_argument('--out',type=Path,required=True)
        p=commands.add_parser('confirm',help='record exposure before reading holdout and apply frozen selection');p.add_argument('cohort',type=Path);p.add_argument('--fit',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--replay',action='store_true',help='explicitly replay the already exposed frozen selection')
        p=commands.add_parser('consume',help='consume exposed holdout into development and freeze distinct new cases');p.add_argument('cohort',type=Path);p.add_argument('--protocol',type=Path,required=True);p.add_argument('--development',type=Path,required=True);p.add_argument('--holdout',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    p=commands.add_parser('inspect',help='verify hashes, child physics and reconstructed conclusions without either solver');p.add_argument('bundle',type=Path)
    for action in ('reproduce','export'):
        p=commands.add_parser(action,help=action+' verified evidence into a fresh directory');p.add_argument('bundle',type=Path);p.add_argument('--out',type=Path,required=True)
    args=parser.parse_args(argv)
    try:
        if kind in ('campaign','resolution'):
            if args.action=='validate':api.validate_protocol(_read(args.protocol));result={'status':'VALID_FROZEN_PROTOCOL'}
            elif args.action=='run':result=api.run(_read(args.protocol),args.out)
            elif args.action=='inspect':result=api.inspect(args.bundle)
            elif args.action=='reproduce':result=api.reproduce(args.bundle,args.out)
            else:study_archive.export(args.bundle,args.out,kind,api.inspect);result={'status':'EXPORTED_VERIFIED_PROTOCOL'}
        else:
            if args.action=='freeze':cohort.freeze(_read(args.protocol),_read(args.development),_read(args.holdout),args.out);result={'status':'FROZEN_KNOWN_SYNTHETIC_COHORT'}
            elif args.action=='fit':result=calibration.fit(args.cohort,args.out)
            elif args.action=='confirm':result=calibration.confirm(args.cohort,args.fit,args.out,replay=args.replay)
            elif args.action=='consume':cohort.consume(args.cohort,_read(args.protocol),_read(args.development),_read(args.holdout),args.out);result={'status':'OLD_HOLDOUT_CONSUMED_NEW_COHORT_FROZEN'}
            else:
                archive_kind=_read(args.bundle/'archive.json')['kind']
                if archive_kind not in ('calibration-fit','calibration-confirmation'):raise ValueError('calibration fit or confirmation archive required')
                inspect=calibration.inspect_fit if archive_kind=='calibration-fit' else calibration.inspect_confirmation
                reproduce=calibration.reproduce_fit if archive_kind=='calibration-fit' else calibration.reproduce_confirmation
                if args.action=='inspect':result=inspect(args.bundle)
                elif args.action=='reproduce':result=reproduce(args.bundle,args.out)
                else:study_archive.export(args.bundle,args.out,archive_kind,inspect);result={'status':'EXPORTED_VERIFIED_PROTOCOL'}
        print(result['status'])
        if 'counts' in result:print('Retained sample counts: '+str(result['counts']))
        if 'equivalent_candidates' in result:print('Equivalent candidates: '+', '.join(result['equivalent_candidates']))
        if 'mode' in result:print(result['mode'])
        print('Wholly synthetic controls only. Environmental, ecological, health, disposal and lifecycle benefits: NOT_EVALUATED.')
        if hasattr(args,'out'):print('Evidence: '+str(args.out))
        return 0
    except KeyboardInterrupt:print('CANCELLED: retained attempts and any exposure record remain; use a fresh output directory.',file=sys.stderr);return 130
    except (ValueError,OSError,OverflowError,TypeError,KeyError,IndexError,AttributeError) as exc:print('ERROR: '+str(exc),file=sys.stderr);return 2
