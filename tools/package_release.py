#!/usr/bin/env python3
"""Create a deterministic source-only candidate without host/cache/private files."""
from __future__ import annotations
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import sys
import tarfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from earth_rehearsal import __version__


def inputs():
    names = {name for name in ('earth.py', 'README.md', 'LICENSE', 'NOTICE', 'CONTRIBUTING.md',
                              'ARCHITECTURE.md', 'EXPERIMENTS.md', 'SOURCES.md', 'ROADMAP.md', 'TASKS.md', 'STATUS.md', 'GOAL.md', '.gitignore')}
    for folder in ('src', 'tests', 'scenarios', 'plan', 'docs/decisions', 'docs/benchmarks'):
        names.update(str(p.relative_to(ROOT)) for p in (ROOT / folder).rglob('*')
                     if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc')
    names.update(str(p.relative_to(ROOT)) for p in (ROOT / 'tools').glob('*.py'))
    names.update(('docs/LIMITATIONS.md', 'docs/EXECUTION-PACKETS.md', 'docs/STUDIES.md', 'docs/REVIEW-KIT.md', 'docs/V05-REVIEW-KIT.md', 'docs/evidence/v05-review.md', 'docs/evidence/v05-network-review.json', 'docs/evidence/v05-protocol-review.json', 'docs/evidence/v05-package-preparation.json', 'docs/evidence/public-release-verification.json', 'docs/evidence/macos-public-release-verification.json', 'docs/evidence/tanduna-review-2026-09-08.json'))
    # Public planning sources and review provenance; never include downloaded HTML,
    # browser profiles/libraries, developer paths, credentials or private host output.
    for name in ('platform-capabilities.md', 'runtime-critic.md', 'verification.md', 'release-review.md'):
        p = ROOT / 'docs/evidence' / name
        if p.is_file(): names.add(str(p.relative_to(ROOT)))
    names.update(str(p.relative_to(ROOT)) for p in (ROOT/'docs/evidence/macos-v01-logs').glob('*') if p.is_file())
    for name in sorted(names):
        p = ROOT / name
        if p.is_symlink(): raise ValueError(f'refuse symlink in source package: {name}')
        if not p.is_file(): raise ValueError(f'missing source artifact: {name}')
        yield name, p.read_bytes()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    content = list(inputs())
    for name, data in content:
        if any(marker in data for marker in ((str(Path.home()) + '/').encode(), b'/' + b'Users/', b'gh' + b'p_', b'github' + b'_pat_')):
            raise ValueError(f'private path or credential-like marker in package file: {name}')
    manifest = {'version': __version__, 'files': {name: hashlib.sha256(data).hexdigest() for name, data in content}}
    content.append(('SOURCE-MANIFEST.json', (json.dumps(manifest, indent=2) + '\n').encode()))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    # Exclusive creation means an earlier candidate is never overwritten.
    with args.out.open('xb') as raw:
        with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0) as gz:
            with tarfile.open(fileobj=gz, mode='w|') as archive:
                for name, data in content:
                    item = tarfile.TarInfo(f'earth-rehearsal-{__version__}/{name}')
                    item.size = len(data); item.mtime = 0; item.mode = 0o644
                    archive.addfile(item, io.BytesIO(data))
    digest = hashlib.sha256(args.out.read_bytes()).hexdigest()
    args.out.with_suffix(args.out.suffix + '.sha256').write_text(digest + '  ' + args.out.name + '\n')
    print(f'{args.out.name}: {len(content)} source files, {args.out.stat().st_size} bytes, SHA256 {digest}')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
