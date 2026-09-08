"""Append-only run attempts and atomically activated portable evidence bundles."""
from __future__ import annotations

import datetime
import hashlib
import json
import os
import platform
import sys
import time
import uuid
from pathlib import Path

from . import __version__
from .study import ARMS, POLICY, InvalidStudy, canonical, identity, read_json, validate

FILES = ('study.json', 'result.json', 'trajectories.csv', 'report.html')
MAX_FILE_BYTES = 256_000_000


class BundleError(ValueError):
    """An incomplete, incompatible or altered evidence bundle."""


def source_digest():
    package = Path(__file__).resolve().parent
    digest = hashlib.sha256()
    for file in sorted(package.glob('*.py')):
        digest.update(file.name.encode() + b'\0' + file.read_bytes())
    entry = package.parent.parent / 'earth.py'
    digest.update(b'earth.py\0' + entry.read_bytes())
    return digest.hexdigest()


def digest_file(path):
    digest = hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def _sync_dir(path):
    if os.name == 'posix':
        fd = os.open(path, os.O_RDONLY)
        try:
            os.fsync(fd)
        finally:
            os.close(fd)


def atomic_write(path, data):
    path = Path(path)
    temporary = path.with_name('.' + path.name + '.' + uuid.uuid4().hex + '.partial')
    if isinstance(data, str):
        data = data.encode('utf-8')
    if len(data) > MAX_FILE_BYTES:
        raise BundleError('artifact exceeds 256 MB per-file budget')
    with temporary.open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temporary, path)
    _sync_dir(path.parent)


def _json_write(path, value):
    atomic_write(path, canonical(value))


def _checkpoint(hook, phase):
    if hook is not None:
        hook(phase)


def run(study, output, *, checkpoint=None, parent_study_id=None):
    """Run into a fresh directory; injection hook supports actual interruption tests."""
    from .evaluator import evaluate
    from .numerical import run_arm
    from .report import render, write_csv

    validate(study)
    if parent_study_id is not None and (not isinstance(parent_study_id, str) or len(parent_study_id) != 64 or any(c not in '0123456789abcdef' for c in parent_study_id)):
        raise BundleError('parent study identity must be a SHA-256 digest or null')
    output = Path(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    try:
        output.mkdir()
    except FileExistsError as exc:
        raise BundleError('output already exists; preserve it and choose a new directory') from exc
    started = time.perf_counter()
    attempt = {'schema_version': 1, 'attempt_id': uuid.uuid4().hex,
               'study_id': identity(study), 'state': 'RUNNING'}
    try:
        _json_write(output / 'attempt.json', attempt)
        _json_write(output / 'study.json', study)
        _checkpoint(checkpoint, 'before_calculation')
        runs = []
        for arm in ARMS:
            for refinement in POLICY['refinements']:
                runs.append(run_arm(study, arm, refinement))
                _checkpoint(checkpoint, 'after_arm')
        # Retain raw data even when independent evaluation fails.
        result = {'schema_version': 1, 'version': __version__, 'study': study,
                  'study_id': identity(study), 'policy': POLICY, 'runs': runs,
                  'provenance': {
                      'python_version': platform.python_version(),
                      'implementation': platform.python_implementation(),
                      'platform': sys.platform, 'machine': platform.machine(),
                      'source_digest': source_digest(), 'threads': 1,
                      'parent_study_id': parent_study_id,
                      'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                      'elapsed_seconds': time.perf_counter() - started,
                  }}
        _json_write(output / 'raw-result.json', result)
        result['evaluation'] = evaluate(study, runs)
        result['provenance']['elapsed_seconds'] = time.perf_counter() - started
        _json_write(output / 'result.json', result)
        temporary_csv = output / '.trajectories.csv.partial'
        write_csv(result, temporary_csv)
        if temporary_csv.stat().st_size > MAX_FILE_BYTES:
            raise BundleError('CSV exceeds artifact budget')
        with temporary_csv.open('rb') as stream:
            os.fsync(stream.fileno())
        os.replace(temporary_csv, output / 'trajectories.csv')
        atomic_write(output / 'report.html', render(result))
        manifest = {
            'schema_version': 1, 'bundle_version': __version__,
            'study_id': result['study_id'], 'source_digest': result['provenance']['source_digest'],
            'files': {name: {'sha256': digest_file(output / name), 'bytes': (output / name).stat().st_size}
                      for name in FILES},
            'reproduce': 'python3 earth.py reproduce BUNDLE --out NEW_DIRECTORY',
        }
        _json_write(output / 'manifest.json', manifest)
        _checkpoint(checkpoint, 'before_activation')
        attempt['state'] = 'SUCCEEDED'
        _json_write(output / 'attempt.json', attempt)
        _json_write(output / 'complete.json', {
            'schema_version': 1, 'status': 'SUCCEEDED',
            'manifest_sha256': digest_file(output / 'manifest.json'),
        })
        _checkpoint(checkpoint, 'after_activation')
        return result
    except BaseException as exc:
        # A completion marker is the sole activation authority. Never revoke a
        # durable complete bundle if the caller is interrupted after activation.
        if not (output / 'complete.json').is_file():
            attempt['state'] = 'CANCELLED' if isinstance(exc, KeyboardInterrupt) else 'FAILED'
            attempt['reason_type'] = type(exc).__name__
            attempt['elapsed_seconds'] = time.perf_counter() - started
            try:
                _json_write(output / 'attempt.json', attempt)
            except OSError:
                pass
        raise


def _safe_file(root, name):
    path = root / name
    if path.is_symlink() or not path.is_file() or path.stat().st_size > MAX_FILE_BYTES:
        raise BundleError(f'{name}: missing, linked, or oversized artifact')
    return path


def inspect(output):
    """Verify retained evidence without executing the numerical kernel."""
    from .evaluator import evaluate

    root = Path(output)
    if not (root / 'complete.json').is_file():
        raise BundleError('incomplete attempt: complete.json is absent; rerun its study.json into a new directory')
    try:
        complete = read_json(_safe_file(root, 'complete.json'))
        if set(complete) != {'schema_version', 'status', 'manifest_sha256'} or complete['schema_version'] != 1 or isinstance(complete['schema_version'], bool) or complete['status'] != 'SUCCEEDED':
            raise BundleError('unsupported or incomplete activation record')
        manifest_path = _safe_file(root, 'manifest.json')
        if digest_file(manifest_path) != complete['manifest_sha256']:
            raise BundleError('manifest hash mismatch')
        manifest = read_json(manifest_path)
        if set(manifest) != {'schema_version', 'bundle_version', 'study_id', 'source_digest', 'files', 'reproduce'} or manifest['schema_version'] != 1 or isinstance(manifest['schema_version'], bool) or manifest['bundle_version'] != __version__:
            raise BundleError('unsupported bundle manifest')
        if set(manifest['files']) != set(FILES):
            raise BundleError('manifest must contain the exact required artifact set')
        for name in FILES:
            file = _safe_file(root, name)
            expected = manifest['files'][name]
            if set(expected) != {'sha256', 'bytes'} or isinstance(expected['bytes'], bool) or file.stat().st_size != expected['bytes'] or digest_file(file) != expected['sha256']:
                raise BundleError(f'{name}: size or hash mismatch')
        study = validate(read_json(root / 'study.json', max_bytes=64_000))
        result = read_json(root / 'result.json', max_bytes=MAX_FILE_BYTES)
        if set(result) != {'schema_version', 'version', 'study', 'study_id', 'policy', 'runs', 'provenance', 'evaluation'} or result['schema_version'] != 1 or isinstance(result['schema_version'], bool) or result['version'] != __version__:
            raise BundleError('unsupported result schema')
        if result['study'] != study or result['study_id'] != identity(study) or manifest['study_id'] != identity(study):
            raise BundleError('study identity mismatch')
        if result['policy'] != POLICY:
            raise BundleError('unsupported numerical policy')
        if result['provenance']['source_digest'] != manifest['source_digest']:
            raise BundleError('runtime identity mismatch')
        evaluation = evaluate(study, result['runs'])
        if result['evaluation'] != evaluation:
            raise BundleError('saved evaluation differs from independent re-evaluation')
        return result
    except (KeyError, TypeError, AttributeError, OSError, InvalidStudy) as exc:
        raise BundleError(f'invalid bundle: {type(exc).__name__}') from exc


def reproduce(output, new_output):
    previous = inspect(output)
    if previous['provenance']['source_digest'] != source_digest():
        raise BundleError('runtime source differs from saved bundle; use the matching source package to reproduce')
    return run(previous['study'], new_output, parent_study_id=previous['provenance'].get('parent_study_id'))
