import copy
import json
import os
import pathlib
import signal
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'src'))
from earth_rehearsal import bundle
from earth_rehearsal.study import load


class BundleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        (ROOT / 'runs').mkdir(exist_ok=True)

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='test-bundle-', dir=ROOT / 'runs')
        self.root = pathlib.Path(self.temp.name)
        self.study = load(ROOT / 'scenarios/box-001.json')

    def tearDown(self):
        self.temp.cleanup()

    def test_complete_inspect_does_not_execute_numerics(self):
        out = self.root / 'first'
        result = bundle.run(self.study, out)
        with patch('earth_rehearsal.numerical.run_arm', side_effect=AssertionError('must not rerun')):
            inspected = bundle.inspect(out)
        self.assertEqual(result, inspected)
        with self.assertRaisesRegex(bundle.BundleError, 'already exists'):
            bundle.run(self.study, out)
        self.assertEqual(bundle.inspect(out), result)

    def test_reproduce_and_supported_change_produce_real_results(self):
        first = bundle.run(self.study, self.root / 'first')
        repeated = bundle.reproduce(self.root / 'first', self.root / 'again')
        self.assertEqual(first['runs'], repeated['runs'])
        self.assertEqual(first['evaluation'], repeated['evaluation'])
        changed = copy.deepcopy(self.study); changed['source_factor'] = 0.25
        second = bundle.run(changed, self.root / 'changed')
        self.assertNotEqual(first['study_id'], second['study_id'])
        self.assertNotEqual(first['runs'][5]['steps'][-1]['closing_mass_kg'], second['runs'][5]['steps'][-1]['closing_mass_kg'])

    def test_hash_and_missing_marker_rejected(self):
        out = self.root / 'first'; bundle.run(self.study, out)
        with (out / 'trajectories.csv').open('a') as file: file.write('altered')
        with self.assertRaisesRegex(bundle.BundleError, 'hash mismatch'): bundle.inspect(out)
        (out / 'complete.json').unlink()
        with self.assertRaisesRegex(bundle.BundleError, 'incomplete'): bundle.inspect(out)

    def test_caught_interruption_preserves_prior_evidence(self):
        prior = self.root / 'prior'; original = bundle.run(self.study, prior)
        for phase in ('before_calculation', 'after_arm', 'before_activation'):
            out = self.root / phase
            def interrupt(current):
                if current == phase: raise KeyboardInterrupt()
            with self.assertRaises(KeyboardInterrupt): bundle.run(self.study, out, checkpoint=interrupt)
            self.assertEqual(json.loads((out / 'attempt.json').read_text())['state'], 'CANCELLED')
            self.assertFalse((out / 'complete.json').exists())
            with self.assertRaises(bundle.BundleError): bundle.inspect(out)
            self.assertEqual(bundle.inspect(prior), original)
        recovered = bundle.run(load(self.root / 'before_activation/study.json'), self.root / 'recovered')
        self.assertEqual(recovered['runs'], original['runs'])

    @unittest.skipUnless(os.name == 'posix', 'SIGKILL is POSIX-specific')
    def test_process_death_before_calculation_and_activation(self):
        # This is a real killed child process, not a simulated exception.
        for phase in ('before_calculation', 'before_activation'):
            output = self.root / ('killed-' + phase)
            code = """
import os,signal,sys
from earth_rehearsal.bundle import run
from earth_rehearsal.study import load
run(load(sys.argv[1]),sys.argv[2],checkpoint=lambda phase: os.kill(os.getpid(),signal.SIGKILL) if phase==sys.argv[3] else None)
"""
            env = {**os.environ, 'PYTHONPATH': str(ROOT / 'src')}
            child = subprocess.run([sys.executable, '-c', code, str(ROOT / 'scenarios/box-001.json'), str(output), phase], cwd=ROOT, env=env, capture_output=True, timeout=30)
            self.assertEqual(child.returncode, -signal.SIGKILL, child.stderr.decode())
            self.assertTrue((output / 'study.json').exists())
            self.assertFalse((output / 'complete.json').exists())
            with self.assertRaises(bundle.BundleError): bundle.inspect(output)
            self.assertEqual(bundle.run(load(output / 'study.json'), self.root / ('retry-' + phase))['study_id'], bundle.identity(self.study))

    def test_interrupt_after_activation_leaves_complete_result(self):
        def interrupt(phase):
            if phase == 'after_activation': raise KeyboardInterrupt()
        output = self.root / 'complete'
        with self.assertRaises(KeyboardInterrupt): bundle.run(self.study, output, checkpoint=interrupt)
        self.assertTrue(bundle.inspect(output)['evaluation']['valid'])

    def test_failed_evaluation_keeps_raw_evidence_without_complete_marker(self):
        output = self.root / 'invalid'
        with patch('earth_rehearsal.evaluator.evaluate', side_effect=ValueError('injected failure')):
            with self.assertRaises(ValueError): bundle.run(self.study, output)
        self.assertTrue((output / 'raw-result.json').exists())
        self.assertFalse((output / 'complete.json').exists())
        self.assertEqual(json.loads((output / 'attempt.json').read_text())['state'], 'FAILED')

    def test_reproduce_requires_matching_runtime(self):
        bundle.run(self.study, self.root / 'first')
        with patch('earth_rehearsal.bundle.source_digest', return_value='changed-runtime'):
            with self.assertRaisesRegex(bundle.BundleError, 'runtime source differs'):
                bundle.reproduce(self.root / 'first', self.root / 'second')
        self.assertFalse((self.root / 'second').exists())
