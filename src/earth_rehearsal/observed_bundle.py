"""Portable, source-bound observed-data study bundles and retained failed attempts."""
from __future__ import annotations
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import time
import uuid
from . import __version__
from .bundle import atomic_write, BundleError, source_digest
from .observed_data import decode, read_bytes, validate_study, normalize, analyze, ObservationError
from .observed_reference import verify_statistics
from . import study_archive

KIND = 'observed_daily_discharge'
ARTIFACTS = {'source.json', 'daily.json', 'site.json', 'study.json', 'days.json', 'summary.json',
             'daily.csv', 'summary.csv', 'report.html', 'attempt.json', 'reference.json', 'provenance.json'}


def canonical(value):
    return json.dumps(value, sort_keys=True, ensure_ascii=False, allow_nan=False, separators=(',', ':')).encode()


def identity(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def write_json(path, value):
    atomic_write(path, json.dumps(value, indent=2, ensure_ascii=False, allow_nan=False)+'\n')


def load_snapshot(snapshot):
    snapshot = Path(snapshot)
    return decode(read_bytes(snapshot/'source.json')), read_bytes(snapshot/'daily.json'), read_bytes(snapshot/'site.json')


def run(snapshot, study, output, *, parent_study_id=None, checkpoint=None):
    from .observed_report import render, daily_csv, summary_csv
    study_archive.require_distinct_output(snapshot, output)
    source, daily_raw, site_raw = load_snapshot(snapshot)
    station, rows = normalize(source, daily_raw, site_raw)
    validate_study(study, source)
    if parent_study_id is not None and (not isinstance(parent_study_id, str) or len(parent_study_id) != 64 or any(c not in '0123456789abcdef' for c in parent_study_id)):
        raise ObservationError('invalid parent study identity')
    output = study_archive.fresh(output)
    attempt = {'format': 'earth-rehearsal-observed-attempt-v1', 'id': uuid.uuid4().hex,
               'state': 'RUNNING', 'started_utc': datetime.now(timezone.utc).isoformat(), 'study_id': identity(study)}
    started = time.monotonic()
    try:
        write_json(output/'attempt.json', attempt)
        for name, value in [('source.json', source), ('study.json', study)]:
            write_json(output/name, value)
        atomic_write(output/'daily.json', daily_raw)
        atomic_write(output/'site.json', site_raw)
        if checkpoint:
            checkpoint('after_source')
        summary = analyze(study, station, rows)
        reference = verify_statistics(study, daily_raw, summary)
        selected = [r for r in rows if study['start_date'] <= r['date'] <= study['end_date']]
        write_json(output/'days.json', selected)
        write_json(output/'summary.json', summary)
        write_json(output/'reference.json', reference)
        provenance = {'format': 'earth-rehearsal-observed-provenance-v1', 'version': __version__,
                      'source_digest': source_digest(), 'study_id': identity(study),
                      'source_record_id': identity(source), 'parent_study_id': parent_study_id,
                      'python': platform.python_version(), 'platform': platform.system(), 'machine': platform.machine(),
                      'network_during_study': False,
                      'source_authenticity': 'Pinned bytes and source assertions; hashes alone do not authenticate a provider.'}
        write_json(output/'provenance.json', provenance)
        atomic_write(output/'daily.csv', daily_csv(selected))
        atomic_write(output/'summary.csv', summary_csv(summary))
        atomic_write(output/'report.html', render(study, source, summary, selected))
        if checkpoint:
            checkpoint('before_activation')
        attempt.update(state='SUCCEEDED', seconds=time.monotonic()-started)
        write_json(output/'attempt.json', attempt)
        study_archive.seal(output, KIND)
        return summary
    except BaseException as exc:
        # SIGKILL can leave RUNNING with no completion marker. Inspection refuses it.
        attempt.update(state='CANCELLED' if isinstance(exc, (KeyboardInterrupt, SystemExit)) else 'FAILED',
                       error=type(exc).__name__, seconds=time.monotonic()-started)
        write_json(output/'attempt.json', attempt)
        raise


def inspect(root):
    from .observed_report import render, daily_csv, summary_csv
    root = Path(root)
    manifest = study_archive.verify(root, KIND)
    if set(manifest['files']) != ARTIFACTS:
        raise BundleError('observed archive artifact set differs')
    source, daily_raw, site_raw = load_snapshot(root)
    station, rows = normalize(source, daily_raw, site_raw)
    study = decode(read_bytes(root/'study.json'))
    validate_study(study, source)
    summary = analyze(study, station, rows)
    reference = verify_statistics(study, daily_raw, summary)
    selected = [r for r in rows if study['start_date'] <= r['date'] <= study['end_date']]
    for name, expected in [('summary.json', summary), ('days.json', selected), ('reference.json', reference)]:
        if decode(read_bytes(root/name)) != expected:
            raise BundleError('retained '+name+' differs from recomputed observed evidence')
    for name, expected in [('daily.csv', daily_csv(selected)), ('summary.csv', summary_csv(summary)),
                           ('report.html', render(study, source, summary, selected))]:
        if read_bytes(root/name) != expected.encode():
            raise BundleError('observed presentation differs: '+name)
    provenance = decode(read_bytes(root/'provenance.json'))
    expected_keys = {'format', 'version', 'source_digest', 'study_id', 'source_record_id', 'parent_study_id',
                     'python', 'platform', 'machine', 'network_during_study', 'source_authenticity'}
    if not isinstance(provenance, dict) or set(provenance) != expected_keys:
        raise BundleError('observed provenance schema differs')
    if provenance['format'] != 'earth-rehearsal-observed-provenance-v1' or provenance['version'] != manifest['version'] or provenance['source_digest'] != manifest['source_digest'] or provenance['study_id'] != identity(study) or provenance['source_record_id'] != identity(source) or provenance['network_during_study'] is not False:
        raise BundleError('observed source/study provenance differs')
    parent = provenance['parent_study_id']
    if parent is not None and (not isinstance(parent, str) or len(parent) != 64 or any(c not in '0123456789abcdef' for c in parent)):
        raise BundleError('invalid observed parent identity')
    attempt = decode(read_bytes(root/'attempt.json'))
    if not isinstance(attempt, dict) or attempt.get('format') != 'earth-rehearsal-observed-attempt-v1' or attempt.get('state') != 'SUCCEEDED' or attempt.get('study_id') != identity(study):
        raise BundleError('observed attempt was not successfully completed')
    return summary


def reproduce(root, output):
    root = Path(root)
    inspect(root)
    study_archive.require_matching_source(study_archive.verify(root, KIND))
    study = decode(read_bytes(root/'study.json'))
    return run(root, study, output, parent_study_id=identity(study))


def export(root, output):
    study_archive.export(root, output, KIND, inspect)
