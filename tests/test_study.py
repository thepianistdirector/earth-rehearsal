import copy
import math
import pathlib
import sys
import tempfile
import unittest
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))
from earth_rehearsal.study import InvalidStudy, load, validate

ROOT = pathlib.Path(__file__).resolve().parents[1]


class StudyTests(unittest.TestCase):
    def setUp(self):
        self.study = load(ROOT / 'scenarios/box-001.json')

    def test_reject_invalid_quantities_and_units(self):
        for field, bad in [('volume', 0), ('volume', -1), ('initial_mass', -1), ('volume', True), ('volume', math.inf), ('volume', math.nan), ('volume', 10**1000)]:
            with self.subTest(field=field, bad=str(bad)[:30]):
                s = copy.deepcopy(self.study); s[field]['value'] = bad
                with self.assertRaises(InvalidStudy): validate(s)
        self.study['volume']['unit'] = 'litres'
        with self.assertRaisesRegex(InvalidStudy, 'unit m3'): validate(self.study)

    def test_reject_nonfixed_volume_and_negative_forcing(self):
        for key, value in [('inflow', 0.2), ('outflow', 0), ('source', -0.1), ('duration', -1)]:
            s = copy.deepcopy(self.study); s['segments'][0][key]['value'] = value
            with self.subTest(key=key), self.assertRaises(InvalidStudy): validate(s)

    def test_reject_unsupported_fields_and_factor(self):
        for key, value in [('capture_fraction', 1.1), ('source_factor', -0.1), ('settling', 0.5), ('schema_version', True)]:
            s = copy.deepcopy(self.study); s[key] = value
            with self.subTest(key=key), self.assertRaises(InvalidStudy): validate(s)

    def test_reject_budget_before_calculation(self):
        self.study['volume']['value'] = 1
        self.study['segments'][0]['inflow']['value'] = 1000
        self.study['segments'][0]['outflow']['value'] = 1000
        with self.assertRaisesRegex(InvalidStudy, 'step budget'): validate(self.study)

    def test_zero_duration_segment_allowed_but_not_empty_study(self):
        self.study['segments'][0]['duration']['value'] = 0
        validate(self.study)
        self.study['segments'][1]['duration']['value'] = 0
        with self.assertRaisesRegex(InvalidStudy, 'positive'): validate(self.study)

    def test_positive_duration_cannot_disappear_from_time_grid(self):
        self.study['segments'][0]['duration']['value'] = 5e-324
        self.study['segments'][1]['duration']['value'] = 0
        with self.assertRaisesRegex(InvalidStudy, 'time grid cannot advance'):
            validate(self.study)

    def test_nested_json_has_a_useful_bounded_failure(self):
        (ROOT / 'runs').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / 'runs') as folder:
            path = pathlib.Path(folder) / 'nested.json'
            path.write_text('[' * 20000 + '0' + ']' * 20000)
            with self.assertRaisesRegex(InvalidStudy, 'invalid JSON'):
                load(path)
