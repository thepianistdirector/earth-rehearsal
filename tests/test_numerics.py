import copy
import math
import pathlib
import sys
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))
from earth_rehearsal.analytic import interval, trajectory
from earth_rehearsal.numerical import run_arm
from earth_rehearsal.study import load

ROOT = pathlib.Path(__file__).resolve().parents[1]


class NumericsTests(unittest.TestCase):
    def test_hand_controls(self):
        self.assertEqual(interval(2, 2, 1, 1, 1), (2.0, 2.0))
        mass, outlet = interval(2, 0, 1, 1, math.log(2))
        self.assertAlmostEqual(mass, 1)
        self.assertAlmostEqual(outlet, 1)
        self.assertEqual(interval(7, 2, 1, 1, 0), (7.0, 0.0))
        self.assertEqual(interval(0, 0, 1, 1, 8), (0.0, 0.0))

    def test_small_time_outlet_retains_positive_second_order_term(self):
        mass, outlet = interval(0, 1, 1e-6, 1e6, 1e-6)
        self.assertGreater(outlet, 0)
        self.assertAlmostEqual(outlet / 5e-25, 1, places=12)
        self.assertAlmostEqual(mass / 1e-6, 1, places=12)

    def test_default_independent_reference(self):
        s = load(ROOT / 'scenarios/box-001.json')
        rows = trajectory(s, 'BASELINE', [0, 3600, 5400])
        self.assertAlmostEqual(rows[1]['mass_kg'], 3.0232367392896893, places=12)
        self.assertAlmostEqual(rows[2]['mass_kg'], 4.789738373964693, places=12)
        self.assertAlmostEqual(rows[2]['escaped_kg'], 4.210261626035308, places=12)

    def test_independent_numerics_refine_and_capture_preserves_dynamics(self):
        s = load(ROOT / 'scenarios/box-001.json')
        truth = trajectory(s, 'BASELINE', [5400])[0]['mass_kg']
        errors = []
        for level in (1, 2, 4):
            baseline = run_arm(s, 'BASELINE', level)
            capture = run_arm(s, 'OUTLET_CAPTURE', level)
            errors.append(abs(baseline['steps'][-1]['closing_mass_kg'] - truth))
            for a, b in zip(baseline['steps'], capture['steps']):
                self.assertEqual(a['closing_mass_kg'], b['closing_mass_kg'])
                self.assertEqual(a['escaped_kg'], b['escaped_kg'] + b['captured_kg'])
        self.assertLess(errors[2] / errors[0], 0.35)

    def test_cap_bound_grid_actually_refines(self):
        s = load(ROOT / 'scenarios/box-001.json')
        s['volume']['value'] = 100
        coarse = run_arm(s, 'BASELINE', 1)
        fine = run_arm(s, 'BASELINE', 4)
        self.assertEqual(len(fine['steps']), 4 * len(coarse['steps']))
        for step in fine['steps']:
            self.assertGreaterEqual(step['closing_mass_kg'], 0)

    def test_zero_segment_and_nonzero_initial_source_control(self):
        s = load(ROOT / 'scenarios/box-001.json')
        s['segments'][0]['duration']['value'] = 0
        s['initial_mass']['value'] = 2
        base = run_arm(s, 'BASELINE', 4)
        reduced = run_arm(s, 'SOURCE_REDUCTION', 4)
        self.assertEqual(base['steps'][0]['segment'], 'storm')
        self.assertGreater(reduced['steps'][-1]['closing_mass_kg'], 0.5 * base['steps'][-1]['closing_mass_kg'])
