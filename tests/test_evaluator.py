"""Independent expected values plus representative raw-evidence corruptions."""
import copy
import json
import math
import pathlib
import sys
import unittest
from unittest.mock import patch

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))
from earth_rehearsal.evaluator import EvaluationError, evaluate
from earth_rehearsal.numerical import run_arm
from earth_rehearsal.study import ARMS, load

ROOT = pathlib.Path(__file__).resolve().parents[1]


def execute(study):
    return [run_arm(study, arm, refinement) for arm in ARMS for refinement in (1, 2, 4)]


class EvaluatorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.study = load(ROOT / 'scenarios/box-001.json')
        cls.runs = execute(cls.study)

    def test_default_independent_reference_and_refinement(self):
        result = evaluate(self.study, self.runs)
        json.dumps(result, allow_nan=False)
        self.assertTrue(result['valid'])
        self.assertEqual(len(result['summaries']), 9)
        finest = {s['arm']: s for s in result['summaries'] if s['refinement'] == 4}
        self.assertAlmostEqual(finest['BASELINE']['analytic_final_mass_kg'], 4.789738373964693, places=12)
        self.assertAlmostEqual(finest['BASELINE']['analytic_escaped_kg'], 4.210261626035308, places=12)
        self.assertEqual(finest['BASELINE']['final_mass_kg'], finest['OUTLET_CAPTURE']['final_mass_kg'])
        self.assertAlmostEqual(finest['OUTLET_CAPTURE']['captured_kg'], finest['OUTLET_CAPTURE']['escaped_kg'], places=12)
        for item in result['refinement']:
            self.assertLess(item['max_stock_error_kg_fine_coarse_ratio'], .35)

    def test_reject_malformed_runs_and_nonfinite_fields(self):
        for field, value in [('arm', []), ('refinement', True), ('refinement', 1.0),
                             ('steps', None), ('claims', {}), ('custody', {})]:
            runs = copy.deepcopy(self.runs)
            runs[0][field] = value
            with self.subTest(field=field, value=value), self.assertRaises(EvaluationError):
                evaluate(self.study, runs)
        for field, value in [('closing_mass_kg', math.nan), ('source_kg', math.inf),
                             ('opening_mass_kg', True), ('captured_kg', -1), ('index', False)]:
            runs = copy.deepcopy(self.runs)
            runs[0]['steps'][0][field] = value
            with self.subTest(field=field), self.assertRaises(EvaluationError):
                evaluate(self.study, runs)

    def test_reject_missing_duplicate_extra_and_reordered_steps(self):
        for mutation in ('missing_run', 'duplicate', 'missing_step', 'extra_field', 'reordered'):
            runs = copy.deepcopy(self.runs)
            if mutation == 'missing_run': runs.pop()
            elif mutation == 'duplicate': runs[-1] = copy.deepcopy(runs[0])
            elif mutation == 'missing_step': runs[0]['steps'].pop()
            elif mutation == 'extra_field': runs[0]['steps'][0]['removed_kg'] = 0
            else: runs[0]['steps'][0], runs[0]['steps'][1] = runs[0]['steps'][1], runs[0]['steps'][0]
            with self.subTest(mutation=mutation), self.assertRaises(EvaluationError):
                evaluate(self.study, runs)

    def test_reject_mass_water_and_time_corruption(self):
        for field in ('closing_mass_kg', 'opening_mass_kg', 'water_in_m3', 'water_out_m3',
                      'opening_volume_m3', 'closing_volume_m3', 't_start_s', 't_end_s'):
            runs = copy.deepcopy(self.runs)
            runs[0]['steps'][2][field] += 1
            with self.subTest(field=field), self.assertRaises(EvaluationError):
                evaluate(self.study, runs)

    def test_conserving_wrong_source_and_outlet_cannot_pass(self):
        runs = copy.deepcopy(self.runs)
        # Equal input/output additions leave every stored stock and mass residual unchanged.
        runs[0]['steps'][1]['source_kg'] += .01
        runs[0]['steps'][1]['escaped_kg'] += .01
        with self.assertRaisesRegex(EvaluationError, 'source flux'):
            evaluate(self.study, runs)
        runs = copy.deepcopy(self.runs)
        runs[0]['steps'][1]['escaped_kg'] += .01
        runs[0]['steps'][1]['closing_mass_kg'] -= .01
        with self.assertRaisesRegex(EvaluationError, 'outlet physics'):
            evaluate(self.study, runs)

    def test_analytic_gate_is_independent_of_conservation(self):
        from earth_rehearsal.analytic import interval
        def faulty_reference(*args):
            mass, outlet = interval(*args)
            return mass + 1, outlet
        with patch('earth_rehearsal.evaluator.interval', side_effect=faulty_reference):
            with self.assertRaisesRegex(EvaluationError, 'analytic stock'):
                evaluate(self.study, self.runs)

    def test_custody_does_not_allow_disposal_or_duplicate_terminal_stock(self):
        for mutation in ('missing', 'disposed', 'stored', 'throughput', 'unknown', 'identity', 'reference', 'transfer'):
            runs = copy.deepcopy(self.runs)
            custody = runs[6]['custody']
            if mutation == 'missing': custody['transfers'].pop()
            elif mutation == 'disposed': custody['transfers'][1]['to'] = 'disposed'
            elif mutation == 'stored': custody['stored_kg'] = custody['stored_throughput_kg']
            elif mutation == 'throughput': custody['stored_throughput_kg'] += 1
            elif mutation == 'unknown': custody['destination_unknown_kg'] = 0
            elif mutation == 'identity': custody['transfers'][1]['id'] = custody['transfers'][0]['id']
            elif mutation == 'reference': custody['transfers'][1]['source_transfer_id'] = 'missing'
            else: custody['transfers'][0]['mass_kg'] += 1
            with self.subTest(mutation=mutation), self.assertRaises(EvaluationError):
                evaluate(self.study, runs)
        for benefit in ('disposal', 'lifecycle', 'ecological', 'health'):
            runs = copy.deepcopy(self.runs)
            runs[0]['claims'][benefit] = 'BENEFIT_PROVEN'
            with self.subTest(benefit=benefit), self.assertRaises(EvaluationError):
                evaluate(self.study, runs)

    def test_stationary_control_does_not_claim_observed_order(self):
        study = copy.deepcopy(self.study)
        study['initial_mass']['value'] = 2
        study['volume']['value'] = 1
        study['source_factor'] = 1
        for seg in study['segments']:
            seg['duration']['value'] = 1
            seg['inflow']['value'] = seg['outflow']['value'] = 1
            seg['source']['value'] = 2
        result = evaluate(study, execute(study))
        for item in result['refinement']:
            self.assertEqual(item['status'], 'ARITHMETIC_FLOOR_NO_OBSERVED_ORDER')
        for summary in result['summaries']:
            self.assertAlmostEqual(summary['final_mass_kg'], 2)
            self.assertAlmostEqual(summary['escaped_kg'] + summary['captured_kg'], 4)

    def test_zero_segment_and_extreme_capture_controls(self):
        for fraction in (0, 1):
            study = copy.deepcopy(self.study)
            study['segments'][0]['duration']['value'] = 0
            study['capture_fraction'] = fraction
            result = evaluate(study, execute(study))
            self.assertTrue(result['valid'])
            for summary in result['summaries']:
                if summary['arm'] == 'OUTLET_CAPTURE':
                    self.assertEqual(summary['captured_kg'] if fraction == 0 else summary['escaped_kg'], 0)

    def test_custom_cap_bound_grid_really_refines(self):
        study = copy.deepcopy(self.study)
        study['volume']['value'] = 1
        for seg in study['segments']:
            seg['duration']['value'] = .23
            seg['inflow']['value'] = seg['outflow']['value'] = 1
        result = evaluate(study, execute(study))
        baseline = [s for s in result['summaries'] if s['arm'] == 'BASELINE']
        self.assertEqual([s['step_count'] for s in baseline], [10, 20, 40])


if __name__ == '__main__':
    unittest.main()
