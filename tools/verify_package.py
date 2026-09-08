#!/usr/bin/env python3
"""Exercise the actual archive in a clean, isolated Python invocation."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tarfile
import time


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('archive', type=Path)
    parser.add_argument('--out', type=Path, required=True, help='new project-scoped evidence directory')
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=False)
    with tarfile.open(args.archive, 'r:gz') as package:
        package.extractall(args.out, filter='data')
    source = next(p for p in args.out.iterdir() if p.is_dir())
    manifest = json.loads((source / 'SOURCE-MANIFEST.json').read_text())
    for name, expected in manifest['files'].items():
        assert hashlib.sha256((source / name).read_bytes()).hexdigest() == expected, name
    # Python -I excludes PYTHONPATH/user site; no dependency or private credential setup.
    environment = {'PATH': os.defpath, 'LANG': 'C.UTF-8', 'TMPDIR': str(source / 'runs')}
    (source / 'runs').mkdir(exist_ok=True)
    commands = [
        ['earth.py', 'run', '--out', 'runs/default'],
        ['earth.py', 'run', '--source-factor', '0.25', '--out', 'runs/changed'],
        ['earth.py', 'inspect', 'runs/default'],
        ['earth.py', 'reproduce', 'runs/default', '--out', 'runs/reproduced'],
        ['earth.py', 'export', 'runs/default', '--out', 'runs/exported'],
        ['earth.py', 'inspect', 'runs/exported'],
        ['earth.py', 'negative-control', '--kind', 'conservation', '--out', 'runs/conservation.json'],
        ['earth.py', 'negative-control', '--kind', 'disposal', '--out', 'runs/disposal.json'],
        ['earth.py', 'negative-control', '--kind', 'source', '--out', 'runs/source.json'],
        ['earth.py', 'negative-control', '--kind', 'custody', '--out', 'runs/custody.json'],
        ['earth.py', 'catchment', 'run', '--out', 'runs/catchment'],
        ['earth.py', 'catchment', 'run', '--source-factor', '0.25', '--out', 'runs/catchment-changed'],
        ['earth.py', 'catchment', 'run', '--capture-capacity', '0.1', '--out', 'runs/catchment-capacity'],
        ['earth.py', 'catchment', 'inspect', 'runs/catchment'],
        ['earth.py', 'catchment', 'reproduce', 'runs/catchment', '--out', 'runs/catchment-reproduced'],
        ['earth.py', 'catchment', 'export', 'runs/catchment', '--out', 'runs/catchment-exported'],
        ['earth.py', 'catchment', 'inspect', 'runs/catchment-exported'],
        ['earth.py', 'campaign', 'run', '--out', 'runs/campaign'],
        ['earth.py', 'campaign', 'inspect', 'runs/campaign'],
        ['earth.py', 'campaign', 'reproduce', 'runs/campaign', '--out', 'runs/campaign-reproduced'],
        ['earth.py', 'campaign', 'export', 'runs/campaign', '--out', 'runs/campaign-exported'],
        ['earth.py', 'campaign', 'inspect', 'runs/campaign-exported'],
        ['earth.py', 'resolution', 'run', '--out', 'runs/resolution'],
        ['earth.py', 'resolution', 'inspect', 'runs/resolution'],
        ['earth.py', 'resolution', 'reproduce', 'runs/resolution', '--out', 'runs/resolution-reproduced'],
        ['earth.py', 'resolution', 'export', 'runs/resolution', '--out', 'runs/resolution-exported'],
        ['earth.py', 'resolution', 'inspect', 'runs/resolution-exported'],
        ['earth.py', 'catchment', 'negative-control', '--kind', 'conservation', '--out', 'runs/network-conservation.json'],
        ['earth.py', 'catchment', 'negative-control', '--kind', 'source', '--out', 'runs/network-source.json'],
        ['earth.py', 'catchment', 'negative-control', '--kind', 'exchange', '--out', 'runs/network-exchange.json'],
        ['earth.py', 'catchment', 'negative-control', '--kind', 'custody', '--out', 'runs/network-custody.json'],
        ['earth.py', 'catchment', 'negative-control', '--kind', 'capacity', '--out', 'runs/network-capacity.json'],
        ['earth.py', 'catchment', 'negative-control', '--kind', 'disposal', '--out', 'runs/network-disposal.json'],
        ['earth.py', 'calibration', 'freeze', '--out', 'runs/cohort'],
        ['earth.py', 'calibration', 'fit', 'runs/cohort', '--out', 'runs/fit'],
        ['earth.py', 'calibration', 'inspect', 'runs/fit'],
        ['earth.py', 'calibration', 'confirm', 'runs/cohort', '--fit', 'runs/fit', '--out', 'runs/confirmation'],
        ['earth.py', 'calibration', 'inspect', 'runs/confirmation'],
        ['earth.py', 'calibration', 'confirm', 'runs/cohort', '--fit', 'runs/fit', '--replay', '--out', 'runs/confirmation-explicit-replay'],
        ['earth.py', 'calibration', 'reproduce', 'runs/confirmation', '--out', 'runs/confirmation-portable-replay'],
        ['earth.py', 'calibration', 'export', 'runs/confirmation', '--out', 'runs/confirmation-exported'],
        ['earth.py', 'calibration', 'inspect', 'runs/confirmation-exported'],
        ['tools/manufacture_calibration.py', '--check'],
        ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
        ['tools/validate_plan.py', '--self-test'],
        ['tools/render_plan.py', '--check'],
    ]
    observations = []
    for command in commands:
        before = time.perf_counter()
        result = subprocess.run([sys.executable, '-I', *command], cwd=source, env=environment,
                                capture_output=True, text=True, timeout=180)
        observations.append({'command': ['python3', '-I', *command], 'exit_code': result.returncode,
                             'seconds': time.perf_counter() - before,
                             'stdout': result.stdout, 'stderr': result.stderr})
        if result.returncode:
            (args.out / 'verification.json').write_text(json.dumps(observations, indent=2))
            print(result.stdout + result.stderr)
            raise SystemExit('packaged workflow failed: ' + ' '.join(command))
    refused=subprocess.run([sys.executable,'-I','earth.py','calibration','fit','runs/cohort','--out','runs/forbidden-refit'],cwd=source,env=environment,capture_output=True,text=True,timeout=30)
    assert refused.returncode==2 and 'already exposed' in refused.stderr and not (source/'runs/forbidden-refit').exists()
    observations.append({'command':['python3','-I','earth.py','calibration','fit','runs/cohort','--out','runs/forbidden-refit'],'exit_code':refused.returncode,'expected_exit_code':2,'stdout':refused.stdout,'stderr':refused.stderr})
    network=json.loads((source/'runs/catchment/result.json').read_text());network_repeated=json.loads((source/'runs/catchment-reproduced/result.json').read_text())
    assert all(network[k]==network_repeated[k] for k in ('study','numerical','references','evaluation'))
    campaign=json.loads((source/'runs/campaign/summary.json').read_text());resolution=json.loads((source/'runs/resolution/summary.json').read_text())
    fit=json.loads((source/'runs/fit/selection.json').read_text());confirmation=json.loads((source/'runs/confirmation/summary.json').read_text());replay=json.loads((source/'runs/confirmation-portable-replay/summary.json').read_text())
    assert campaign['counts']=={'SUCCEEDED':5,'INVALID':1,'FAILED':0,'NOT_RUN_BUDGET':0}
    assert any(c['status']=='ORDER_REVERSES_ACROSS_SAMPLES' for c in campaign['comparisons'])
    assert resolution['status']=='PASSED_MANUFACTURED_REFINEMENT'
    assert fit['equivalent_candidates']==['equivalent_a','equivalent_b'] and fit['candidate_denominator']==4
    assert confirmation['status']=='PASSED_FROZEN_SYNTHETIC_CONFIRMATION' and replay['mode']=='FROZEN_SELECTION_REPLAY'
    default = json.loads((source / 'runs/default/result.json').read_text())
    changed = json.loads((source / 'runs/changed/result.json').read_text())
    reproduced = json.loads((source / 'runs/reproduced/result.json').read_text())
    assert default['runs'] == reproduced['runs']
    assert default['evaluation'] == reproduced['evaluation']
    assert default['study_id'] != changed['study_id']
    assert default['runs'][5]['steps'][-1]['closing_mass_kg'] != changed['runs'][5]['steps'][-1]['closing_mass_kg']
    assert changed['provenance']['parent_study_id'] == default['study_id']
    record = {'observer': 'Astra automated local archive extraction; not an external human/environment',
              'archive_sha256': hashlib.sha256(args.archive.read_bytes()).hexdigest(),
              'version': manifest['version'], 'runtime_source_digest': default['provenance']['source_digest'],
              'python': default['provenance']['python_version'], 'platform': default['provenance']['platform'],
              'source_files_verified': len(manifest['files']), 'commands': observations,
              'identical_reproduction': True, 'changed_input_changed_trajectory': True,
              'parent_identity_retained': True, 'publicly_obtained': False,
              'v05_controls': {'network_identical_reproduction':True,'all_sensitivity_attempts_retained':True,'ordering_reversal_detected':True,'spatial_time_separation':resolution['status'],'equivalent_candidates':fit['equivalent_candidates'],'frozen_confirmation':confirmation['status'],'portable_replay_is_not_fresh_holdout':True,'refit_after_exposure_rejected':True}}
    (args.out / 'verification.json').write_text(json.dumps(record, indent=2))
    print(f"PASS: {len(observations)} isolated packaged command outcomes, source hashes, changed trajectories, identical reproduction, recovery suite")

if __name__ == '__main__':
    main()
