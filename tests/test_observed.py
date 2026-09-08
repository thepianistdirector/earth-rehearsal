"""Synthetic API-shaped falsifiers; these fixtures are NOT USGS observations."""
import copy
from datetime import date, timedelta
import hashlib
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from earth_rehearsal import observed_data as data, observed_bundle as bundle, study_archive
from earth_rehearsal.observed_reference import verify_statistics
from earth_rehearsal.observed_report import daily_csv, summary_csv

REAL = Path(__file__).resolve().parents[1]/'scenarios/observations/potomac-2021-2024'


def fixture(values=('1', '2', '3', '4'), start='2024-02-27'):
    source = json.loads((REAL/'source.json').read_text())
    site = json.loads((REAL/'site.json').read_text())
    site['properties']['monitoring_location_name'] = 'Synthetic known-answer test station; NOT a real observation'
    start_date = date.fromisoformat(start)
    end = (start_date+timedelta(days=len(values)-1)).isoformat()
    features = []
    for i, value in enumerate(values):
        features.append({'type': 'Feature', 'id': 'synthetic-'+str(i), 'geometry': site['geometry'],
                         'properties': {'time_series_id': 'synthetic-series', 'monitoring_location_id': source['site_id'],
                                        'parameter_code': '00060', 'statistic_id': '00003', 'time': (start_date+timedelta(days=i)).isoformat(),
                                        'value': value, 'unit_of_measure': 'ft^3/s', 'approval_status': 'Approved',
                                        'qualifier': None, 'last_modified': '2026-09-08T00:00:00+00:00'}})
    raw = {'type': 'FeatureCollection', 'features': features, 'numberReturned': len(features), 'links': [], 'timeStamp': '2026-09-08T00:00:00Z'}
    source.update(start_date=start, end_date=end, citation='Synthetic known-answer unit-test input, NOT a USGS observation or public download.')
    source['retrievals']['daily']['url'] = f'https://api.waterdata.usgs.gov/ogcapi/v0/collections/daily/items?f=json&monitoring_location_id={source["site_id"]}&parameter_code=00060&statistic_id=00003&datetime={start}/{end}&limit=10000'
    study = json.loads((REAL/'study.json').read_text())
    cut = start_date+timedelta(days=len(values)//2)
    study.update(id='SYNTHETIC-TEST', title='Synthetic test only', start_date=start, end_date=end,
                 periods=[{'id': 'first', 'start_date': start, 'end_date': (cut-timedelta(days=1)).isoformat()},
                          {'id': 'second', 'start_date': cut.isoformat(), 'end_date': end}])
    return source, site, raw, study


def encode(source, site, raw):
    daily_raw, site_raw = json.dumps(raw).encode(), json.dumps(site).encode()
    for key, value in [('daily', daily_raw), ('site', site_raw)]:
        source['retrievals'][key]['sha256'] = hashlib.sha256(value).hexdigest()
        source['retrievals'][key]['bytes'] = len(value)
    return daily_raw, site_raw


def normalize(source, site, raw):
    return data.normalize(source, *encode(source, site, raw))


def snapshot(path, source, site, raw):
    path.mkdir()
    daily_raw, site_raw = encode(source, site, raw)
    (path/'source.json').write_text(json.dumps(source));(path/'daily.json').write_bytes(daily_raw);(path/'site.json').write_bytes(site_raw)
    return path


def reseal(root):
    (root/'archive.json').unlink();(root/'complete.json').unlink();study_archive.seal(root, bundle.KIND)


class ObservationArithmetic(unittest.TestCase):
    def test_hand_computable_leap_day_and_quantiles(self):
        source, site, raw, study = fixture()
        station, rows = normalize(source, site, raw)
        self.assertEqual([r['date'] for r in rows], ['2024-02-27', '2024-02-28', '2024-02-29', '2024-03-01'])
        summary = data.analyze(study, station, rows)
        values = summary['summaries'][0]['primary'];factor = .3048**3
        self.assertAlmostEqual(values['mean_m3_s'], 2.5*factor)
        self.assertAlmostEqual(values['p10_m3_s'], 1.3*factor)
        self.assertAlmostEqual(values['median_m3_s'], 2.5*factor)
        self.assertAlmostEqual(values['p90_m3_s'], 3.7*factor)
        self.assertAlmostEqual(summary['period_difference']['primary']['mean_difference_m3_s'], 2*factor)
        verify_statistics(study, encode(source, site, raw)[0], summary)

    def test_zero_is_real_missing_and_absent_stay_distinct(self):
        source, site, raw, study = fixture(('0', None, '3', '4'))
        raw['features'].pop(2);raw['numberReturned'] -= 1
        station, rows = normalize(source, site, raw)
        self.assertEqual([r['state'] for r in rows], ['ACCEPTED', 'MISSING_VALUE', 'ABSENT_DATE', 'ACCEPTED'])
        s = data.analyze(study, station, rows)
        self.assertEqual(s['received_records'], 3);self.assertEqual(s['summaries'][0]['primary']['coverage_fraction'], .5)
        self.assertAlmostEqual(s['summaries'][0]['primary']['mean_m3_s'], 2*.3048**3)
        verify_statistics(study, encode(source, site, raw)[0], s)

    def test_quality_overlap_and_negative_flow_not_silently_removed(self):
        source, site, raw, study = fixture(('1', '2', '3', '-4'))
        raw['features'][0]['properties']['qualifier'] = ['REVISED']
        raw['features'][1]['properties']['qualifier'] = ['ESTIMATED', 'REVISED']
        raw['features'][2]['properties']['approval_status'] = 'Provisional'
        station, rows = normalize(source, site, raw);s = data.analyze(study, station, rows)
        self.assertEqual(s['state_counts'], {'ACCEPTED': 1, 'ESTIMATED': 1, 'NEGATIVE_OUTSIDE_SCOPE': 1, 'PROVISIONAL': 1})
        self.assertEqual(s['overlapping_quality_counts'], {'ESTIMATED': 1, 'REVISED': 2})
        self.assertEqual(s['summaries'][0]['primary']['accepted_days'], 1)
        self.assertEqual(s['summaries'][0]['with_approved_estimates']['accepted_days'], 2)
        self.assertLess(rows[-1]['flow_m3_s'], 0)
        verify_statistics(study, encode(source, site, raw)[0], s)

    def test_all_excluded_yields_null_metrics_and_no_difference(self):
        source, site, raw, study = fixture((None, None, None, None))
        station, rows = normalize(source, site, raw);s = data.analyze(study, station, rows)
        self.assertIsNone(s['summaries'][0]['primary']['mean_m3_s'])
        self.assertEqual(s['summaries'][0]['primary']['status'], 'NO_ACCEPTED_OBSERVATIONS')
        self.assertIsNone(s['period_difference']['primary']['mean_difference_m3_s'])
        verify_statistics(study, encode(source, site, raw)[0], s)

    def test_independent_reference_detects_arithmetic_and_denominator_forgery(self):
        source, site, raw, study = fixture();station, rows = normalize(source, site, raw)
        summary = data.analyze(study, station, rows)
        for mutate in [lambda s: s['summaries'][0]['primary'].update(mean_m3_s=7),
                       lambda s: s['summaries'][0]['primary'].update(accepted_days=3),
                       lambda s: s['summaries'].pop(1),
                       lambda s: s['summaries'][0]['primary'].update(p10_m3_s=0)]:
            with self.subTest(mutate=mutate):
                forged = copy.deepcopy(summary);mutate(forged)
                with self.assertRaises(data.ObservationError):verify_statistics(study, encode(source, site, raw)[0], forged)


class ObservationAdmission(unittest.TestCase):
    def test_wrong_grain_identity_units_and_quality_rejected(self):
        mutations = [('monitoring_location_id', 'USGS-00000000'), ('parameter_code', '00065'), ('statistic_id', '00001'),
                     ('unit_of_measure', 'm^3/s'), ('time_series_id', 'other'), ('time', '2024-02-27T00:00:00Z'),
                     ('time', '2025-01-01'), ('approval_status', 'Unknown'), ('qualifier', 'ESTIMATED'),
                     ('qualifier', ['UNKNOWN']), ('qualifier', ['REVISED', 'REVISED']), ('value', True), ('value', 'NaN'),
                     ('value', '1e999'), ('value', '1e-999'), ('value', '=EXEC()'), ('value', 4), ('last_modified', '2024-01-01')]
        for key, value in mutations:
            with self.subTest(key=key, value=value):
                source, site, raw, study = fixture();raw['features'][1]['properties'][key] = value
                with self.assertRaises(data.ObservationError):normalize(source, site, raw)

    def test_duplicate_dates_ids_pagination_and_response_count(self):
        for mutation in ('date', 'id', 'next', 'count', 'matched', 'geometry', 'empty'):
            with self.subTest(mutation=mutation):
                source, site, raw, study = fixture()
                if mutation == 'date':raw['features'][1]['properties']['time'] = raw['features'][0]['properties']['time']
                elif mutation == 'id':raw['features'][1]['id'] = raw['features'][0]['id']
                elif mutation == 'next':raw['links'].append({'rel': 'next', 'href': 'https://example.invalid'})
                elif mutation == 'count':raw['numberReturned'] = 3
                elif mutation == 'matched':raw['numberMatched'] = 5
                elif mutation == 'geometry':raw['features'][1]['geometry'] = {'type': 'Point', 'coordinates': [0, 0]}
                else:raw['features'] = [];raw['numberReturned'] = 0
                with self.assertRaises(data.ObservationError):normalize(source, site, raw)

    def test_raw_identity_query_and_license_are_binding(self):
        for key in ('sha', 'query', 'license', 'auth', 'terms'):
            source, site, raw, study = fixture();daily, site_raw = encode(source, site, raw)
            if key == 'sha':source['retrievals']['daily']['sha256'] = '0'*64
            elif key == 'query':source['retrievals']['daily']['url'] += '&api_key=secret'
            elif key == 'license':source['license'] = 'unreviewed'
            elif key == 'auth':source['retrievals']['daily']['authentication_used'] = True
            else:source['terms_url'] = 'javascript:alert(1)'
            with self.subTest(key=key), self.assertRaises(data.ObservationError):data.normalize(source, daily, site_raw)

    def test_duplicate_json_keys_nonfinite_and_size(self):
        for raw in (b'{"value":1,"value":2}', b'{"value":NaN}', b'{'*2000):
            with self.assertRaises(data.ObservationError):data.decode(raw)
        with patch.object(data, 'MAX_BYTES', 10), self.assertRaises(data.ObservationError):data.decode(b' '*11)

    def test_period_overlap_gap_out_of_range_and_oversized_window(self):
        source, site, raw, study = fixture()
        for key, value in [('start_date', '2024-02-28'), ('end_date', '2024-02-28')]:
            p = copy.deepcopy(study);p['periods'][1][key] = value
            with self.assertRaises(data.ObservationError):data.validate_study(p, source)
        with self.assertRaises(data.ObservationError):data.date_range('1900-01-01', '2026-01-01')


class ObservationBundles(unittest.TestCase):
    def test_offline_roundtrip_export_and_html_escape(self):
        source, site, raw, study = fixture();study['title'] = '<script>alert(1)</script>'
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp);snap = snapshot(tmp/'source', source, site, raw)
            with patch('urllib.request.urlopen', side_effect=AssertionError('network during offline study')):
                output = tmp/'run';result = bundle.run(snap, study, output)
                self.assertEqual(bundle.inspect(output), result)
                repeated = bundle.reproduce(output, tmp/'repeated');self.assertEqual(result, repeated)
                bundle.export(output, tmp/'exported');self.assertEqual(bundle.inspect(tmp/'exported'), result)
            report = (output/'report.html').read_text()
            self.assertNotIn('<script>', report);self.assertIn('&lt;script&gt;', report)
            self.assertEqual((output/'daily.json').read_bytes(), (snap/'daily.json').read_bytes())
            with self.assertRaises(ValueError):bundle.run(snap, study, output)

    def test_export_and_reproduction_cannot_mutate_source_through_nested_output(self):
        source, site, raw, study = fixture()
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp);snap = snapshot(tmp/'source', source, site, raw)
            output = tmp/'bundle';expected = bundle.run(snap, study, output)
            before = {str(p.relative_to(output)): p.read_bytes() for p in output.rglob('*') if p.is_file()}
            for action in (bundle.export, bundle.reproduce):
                with self.assertRaisesRegex(ValueError, 'outside the source'):
                    action(output, output/'nested')
            self.assertEqual(before, {str(p.relative_to(output)): p.read_bytes() for p in output.rglob('*') if p.is_file()})
            self.assertEqual(bundle.inspect(output), expected)

    def test_rehashed_report_csv_summary_and_row_forgery_are_rejected(self):
        source, site, raw, study = fixture()
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp);snap = snapshot(tmp/'source', source, site, raw)
            for filename in ('report.html', 'summary.csv', 'daily.csv', 'summary.json', 'days.json', 'provenance.json'):
                with self.subTest(filename=filename):
                    output = tmp/filename;bundle.run(snap, study, output)
                    path = output/filename
                    if filename == 'summary.json':
                        s = json.loads(path.read_text());s['received_records'] = 0;path.write_text(json.dumps(s))
                    elif filename == 'days.json':
                        s = json.loads(path.read_text());s.pop();path.write_text(json.dumps(s))
                    elif filename == 'provenance.json':
                        s = json.loads(path.read_text());s['source_record_id'] = '0'*64;path.write_text(json.dumps(s))
                    else:path.write_text(path.read_text()+'forged')
                    reseal(output)
                    with self.assertRaises(ValueError):bundle.inspect(output)

    def test_interrupted_activation_retains_raw_and_requires_fresh_output(self):
        source, site, raw, study = fixture()
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp);snap = snapshot(tmp/'source', source, site, raw)
            def stop(phase):
                if phase == 'before_activation':raise KeyboardInterrupt
            with self.assertRaises(KeyboardInterrupt):bundle.run(snap, study, tmp/'interrupted', checkpoint=stop)
            self.assertTrue((tmp/'interrupted/daily.json').is_file())
            self.assertEqual(json.loads((tmp/'interrupted/attempt.json').read_text())['state'], 'CANCELLED')
            with self.assertRaises(ValueError):bundle.inspect(tmp/'interrupted')
            self.assertEqual(bundle.run(snap, study, tmp/'recovered')['received_records'], 4)

    @unittest.skipUnless(os.name == 'posix', 'SIGKILL requires POSIX')
    def test_actual_process_death_preserves_unactivated_evidence(self):
        source, site, raw, study = fixture()
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp);snap = snapshot(tmp/'source', source, site, raw);(snap/'study.json').write_text(json.dumps(study))
            code = "import os,signal,json,sys;from pathlib import Path;sys.path.insert(0,sys.argv[1]);from earth_rehearsal.observed_bundle import run;run(Path(sys.argv[2]),json.loads((Path(sys.argv[2])/'study.json').read_text()),Path(sys.argv[3]),checkpoint=lambda phase:os.kill(os.getpid(),signal.SIGKILL) if phase=='before_activation' else None)"
            process = subprocess.run([sys.executable, '-I', '-c', code, str(Path(__file__).resolve().parents[1]/'src'), str(snap), str(tmp/'killed')], capture_output=True, timeout=15)
            self.assertEqual(process.returncode, -signal.SIGKILL, process.stderr)
            self.assertTrue((tmp/'killed/daily.json').is_file());self.assertFalse((tmp/'killed/complete.json').exists())
            with self.assertRaises(ValueError):bundle.inspect(tmp/'killed')
            bundle.run(snap, study, tmp/'fresh');bundle.inspect(tmp/'fresh')

    def test_real_pinned_case_has_recorded_quality_not_synthetic_measurements(self):
        source, daily, site = bundle.load_snapshot(REAL);station, rows = data.normalize(source, daily, site)
        study = data.decode(data.read_bytes(REAL/'study.json'));data.validate_study(study, source)
        summary = data.analyze(study, station, rows)
        self.assertEqual(summary['received_records'], 1461)
        self.assertEqual(summary['state_counts'], {'ACCEPTED': 1431, 'ESTIMATED': 30})
        self.assertEqual(summary['overlapping_quality_counts'], {'ESTIMATED': 30, 'REVISED': 116})
        verify_statistics(study, daily, summary)
        # Freeze the actual source hash, not just the semantic record counts.
        self.assertEqual(hashlib.sha256(daily).hexdigest(), source['retrievals']['daily']['sha256'])

class ObservationFetchAndCLI(unittest.TestCase):
    def test_fetch_validation_and_cross_origin_redirect(self):
        from earth_rehearsal.observed_fetch import fetch, _PublicRedirects
        for site, start, end, split in [('bad', '2024-01-01', '2024-01-04', '2024-01-03'),
                                       ('01646500', '2024-01-01', '2024-01-04', '2024-01-01'),
                                       ('01646500', '1900-01-01', '2024-01-04', '2020-01-01')]:
            with tempfile.TemporaryDirectory() as tmp:
                out = Path(tmp)/'rejected'
                with self.assertRaises(data.ObservationError):fetch(site, start, end, split, out)
                self.assertFalse(out.exists())
        with self.assertRaises(data.ObservationError):
            _PublicRedirects().redirect_request(None, None, 302, '', {}, 'https://private.example/secret')

    def test_failed_fetch_preserves_request_attempt_without_faking_source(self):
        from earth_rehearsal.observed_fetch import fetch
        class Offline:
            def open(self, *args, **kwargs):raise OSError('synthetic offline probe')
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp)/'failed'
            with patch('earth_rehearsal.observed_fetch.build_opener', return_value=Offline()), self.assertRaises(OSError):
                fetch('01646500', '2024-01-01', '2024-01-04', '2024-01-03', out)
            attempt = json.loads((out/'fetch.json').read_text())
            self.assertEqual(attempt['status'], 'FAILED');self.assertEqual(attempt['completed_requests'], [])
            self.assertFalse((out/'source.json').exists())

    def test_changed_period_cli_retains_parent_and_updates_question(self):
        from earth_rehearsal.observed_cli import main
        source, site, raw, study = fixture()
        with tempfile.TemporaryDirectory() as tmp:
            tmp = Path(tmp);snap = snapshot(tmp/'source', source, site, raw);(snap/'study.json').write_text(json.dumps(study))
            result = main(['run', '--snapshot', str(snap), '--split-date', '2024-02-28', '--out', str(tmp/'changed')])
            self.assertEqual(result, 0)
            p = json.loads((tmp/'changed/provenance.json').read_text())
            self.assertEqual(p['parent_study_id'], bundle.identity(study))
            changed = json.loads((tmp/'changed/study.json').read_text())
            self.assertIn('2024-02-28', changed['question'])
            self.assertEqual(changed['periods'][0]['end_date'], '2024-02-27')
            self.assertNotIn('<svg', (tmp/'changed/report.html').read_text())
            self.assertEqual(main(['inspect', str(tmp/'changed')]), 0)
