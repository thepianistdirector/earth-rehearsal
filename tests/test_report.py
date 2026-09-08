import copy
import csv
from html.parser import HTMLParser
import pathlib
import sys
import tempfile
import unittest

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / 'src'))
from earth_rehearsal.evaluator import evaluate
from earth_rehearsal.numerical import run_arm
from earth_rehearsal.report import render, write_csv
from earth_rehearsal.study import ARMS, POLICY, identity, load

ROOT = pathlib.Path(__file__).resolve().parents[1]


class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class ReportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        study = load(ROOT / 'scenarios/box-001.json')
        runs = [run_arm(study, arm, level) for arm in ARMS for level in POLICY['refinements']]
        cls.result = dict(schema_version=1, version='0.1.0', study=study, study_id=identity(study), policy=POLICY, runs=runs, evaluation=evaluate(study, runs), provenance={'python_version': '3.12', 'threads': 1})

    def test_complete_exact_comparison_and_offline_semantics(self):
        html = render(self.result)
        parsed = Document(html)
        for summary in self.result['evaluation']['summaries']:
            if summary['refinement'] == 4:
                for field in ('final_mass_kg', 'escaped_kg', 'captured_kg', 'analytic_final_mass_kg'):
                    self.assertIn(format(summary[field], '.9g') if summary[field] else '>0<', html)
        tags = [tag for tag, _ in parsed.tags]
        self.assertEqual(tags.count('svg'), 3)
        self.assertEqual(tags.count('table'), tags.count('caption'))
        self.assertNotIn('script', tags)
        for tag, attrs in parsed.tags:
            self.assertFalse(attrs.get('src', '').startswith(('http:', 'https:', '//')))
            if tag == 'th':
                self.assertIn(attrs['scope'], ('col', 'row'))
            if tag == 'svg':
                self.assertIn('aria-labelledby', attrs)
        self.assertIn('NOT_EVALUATED', html)
        self.assertIn('Stored throughput (transfer)', html)
        self.assertIn('Destination unknown (terminal stock)', html)
        self.assertIn('trajectories.csv', html)

    def test_supplied_metadata_is_escaped(self):
        result = copy.deepcopy(self.result)
        attack = '<script>alert("x")</script><img src=x onerror=alert(1)>'
        result['provenance']['platform'] = attack
        result['version'] = attack
        result['study_id'] = attack
        result['study']['applicability'] = attack
        html = render(result)
        self.assertNotIn(attack, html)
        self.assertNotIn('script', [tag for tag, _ in Document(html).tags])
        self.assertIn('&lt;script&gt;', html)

    def test_csv_preserves_every_finest_step_and_forcing(self):
        (ROOT / 'runs').mkdir(exist_ok=True)
        with tempfile.TemporaryDirectory(dir=ROOT / 'runs') as directory:
            path = pathlib.Path(directory) / 'steps.csv'
            write_csv(self.result, path)
            with path.open(newline='') as stream:
                rows = list(csv.DictReader(stream))
        finest = [r for r in self.result['runs'] if r['refinement'] == 4]
        self.assertEqual(len(rows), sum(len(r['steps']) for r in finest))
        for run in finest:
            exported = [row for row in rows if row['arm'] == run['arm']]
            self.assertEqual({row['segment'] for row in exported}, {'dry', 'storm'})
            for raw, row in zip(run['steps'], exported):
                for key, value in raw.items():
                    self.assertEqual(row[key] if isinstance(value, str) else float(row[key]), value)
                self.assertAlmostEqual(float(row['source_rate_kg_s']) * float(row['duration_s']), raw['source_kg'])
                self.assertAlmostEqual(float(row['closing_mass_kg']) - float(row['analytic_closing_mass_kg']), float(row['stock_error_kg']))

    def test_large_chart_is_bounded_without_losing_segment_boundary(self):
        result = copy.deepcopy(self.result)
        for segment in result['study']['segments']:
            segment['duration']['value'] = 18000
        result['runs'] = [run_arm(result['study'], arm, level) for arm in ARMS for level in POLICY['refinements']]
        result['evaluation'] = evaluate(result['study'], result['runs'])
        html = render(result)
        for tag, attrs in Document(html).tags:
            if tag == 'polyline':
                points = attrs['points'].split()
                self.assertLessEqual(len(points), 1000)
                self.assertEqual(points[0].split(',')[0], '58.000')
                self.assertEqual(points[-1].split(',')[0], '396.000')
                self.assertIn('227.000', [point.split(',')[0] for point in points])

    def test_zero_trajectory_has_finite_accessible_chart(self):
        result = copy.deepcopy(self.result)
        for segment in result['study']['segments']:
            segment['source']['value'] = 0
        result['runs'] = [run_arm(result['study'], arm, level) for arm in ARMS for level in POLICY['refinements']]
        result['evaluation'] = evaluate(result['study'], result['runs'])
        html = render(result)
        for tag, attrs in Document(html).tags:
            if tag == 'polyline':
                self.assertNotIn('nan', attrs['points'])
                self.assertNotIn('inf', attrs['points'])


if __name__ == '__main__':
    unittest.main()
