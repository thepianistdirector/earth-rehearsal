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
        ['-m', 'unittest', 'discover', '-s', 'tests', '-v'],
        ['tools/validate_plan.py', '--self-test'],
        ['tools/render_plan.py', '--check'],
    ]
    observations = []
    for command in commands:
        before = time.perf_counter()
        result = subprocess.run([sys.executable, '-I', *command], cwd=source, env=environment,
                                capture_output=True, text=True, timeout=60)
        observations.append({'command': ['python3', '-I', *command], 'exit_code': result.returncode,
                             'seconds': time.perf_counter() - before,
                             'stdout': result.stdout, 'stderr': result.stderr})
        if result.returncode:
            (args.out / 'verification.json').write_text(json.dumps(observations, indent=2))
            print(result.stdout + result.stderr)
            raise SystemExit('packaged workflow failed: ' + ' '.join(command))
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
              'parent_identity_retained': True, 'publicly_obtained': False}
    (args.out / 'verification.json').write_text(json.dumps(record, indent=2))
    print(f"PASS: {len(commands)} isolated packaged commands, source hashes, changed trajectories, identical reproduction, recovery suite")

if __name__ == '__main__':
    main()
