"""Independent-review falsifiers: reference substitution and scaled evidence loss."""
import copy
import tempfile
from pathlib import Path
import unittest
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from test_network import simple_study,evaluated,contract,Layout
from earth_rehearsal.network_evaluator import evaluate,NetworkEvaluationError
from earth_rehearsal import network_bundle as bundle
from earth_rehearsal.bundle import BundleError,digest_file

class ReviewFalsifiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=contract.load(Path(__file__).resolve().parents[1]/'scenarios/catchment-001.json')
        cls.n,cls.r,_=evaluated(cls.s)
    def test_long_transfer_path_and_near_simultaneous_events(self):
        for name in ('reference-long-path.json','reference-near-capacity.json'):
            study=contract.load(Path(__file__).parent/'fixtures'/name)
            self.assertEqual(evaluated(study)[2]['status'],'VALID_SYNTHETIC_COMPARISON')
    def test_cumulative_roundoff_after_twenty_efolds(self):
        study=simple_study(initial=2,source=0,flow=100,duration=200)
        self.assertEqual(evaluated(study)[2]['status'],'VALID_SYNTHETIC_COMPARISON')
    def test_custody_reclassification_beside_large_unrelated_stock(self):
        study=simple_study(source=0,initial=.001,second_class=True,capture=True,capacity=.0001,release=.0002,duration=600)
        study=contract.set_quantity(study,['nodes',0,'initial_mass','retained'],1e6)
        n,r,_=evaluated(study);layout=Layout(study)
        for run in n:
            for rec in run['records'][1:]:
                x=rec['state'];x[layout.at('stored','cap','mobile')]+=x[layout.at('unknown','cap','mobile')];x[layout.at('unknown','cap','mobile')]=0
        with self.assertRaises(NetworkEvaluationError):evaluate(study,n,r)
    def test_clean_inflow_cannot_acquire_small_pollutant_ledger(self):
        study=simple_study(initial=1e6,source=0,duration=60);n,r,_=evaluated(study);layout=Layout(study)
        for run in n:
            for rec in run['records'][1:]:rec['state'][layout.at('edge','inflow','mobile')]=.0001
        with self.assertRaises(NetworkEvaluationError):evaluate(study,n,r)
    def test_relabelled_euler_is_not_reference(self):
        refs=[]
        for arm in contract.ARMS:
            r=copy.deepcopy(next(n for n in self.n if n['arm']==arm and n['refinement']==4))
            r.update(method='affine_exponential_reference',capacity_events=[],products=0);refs.append(r)
        with self.assertRaisesRegex(NetworkEvaluationError,'residual'):evaluate(self.s,self.n,refs)
    def test_missing_moved_and_false_event_state(self):
        for mode in ('missing','moved','state'):
            r=copy.deepcopy(self.r);event=r[-1]['capacity_events'][0]
            if mode=='missing':r[-1]['capacity_events']=[]
            elif mode=='moved':event['t']=0
            else:event['state'][0]+=.1
            with self.assertRaises(NetworkEvaluationError,msg=mode):evaluate(self.s,self.n,r)
    def test_large_class_cannot_hide_erased_small_class(self):
        s=simple_study(flow=0,source=0,initial=1e6,second_class=True,duration=60)
        s=contract.set_quantity(s,['nodes',0,'initial_mass','retained'],1e-4);n,r,_=evaluated(s);layout=Layout(s)
        for run in n:
            for rec in run['records'][1:]:rec['state'][layout.at('mass','a','retained')]=0
        with self.assertRaises(NetworkEvaluationError):evaluate(s,n,r)
    def test_tiny_positive_capacity_fails_admission(self):
        with self.assertRaisesRegex(contract.NetworkStudyError,'computational resolution'):simple_study(capture=True,capacity=1e-30)
        evaluated(simple_study(capture=True,capacity=0))
    def test_no_derivative_rights_edit(self):
        s=copy.deepcopy(self.s);s['source_records'][0]['rights']['derivatives']=False;contract.validate(s)
        with self.assertRaisesRegex(contract.NetworkStudyError,'rights'):contract.set_quantity(s,['source_factor'],.4)
    def test_attempt_export_and_provenance_validation(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run';out=Path(tmp)/'export';bundle.run(simple_study(duration=60),root);bundle.export(root,out)
            bundle.inspect(out);self.assertTrue((out/'attempt.json').is_file())
            result=bundle._read(root/'result.json');result['provenance'].update(python_version=None,elapsed_seconds=-99)
            bundle._json(root/'result.json',result);m=bundle._read(root/'manifest.json')
            m['files']['result.json']={'bytes':(root/'result.json').stat().st_size,'sha256':digest_file(root/'result.json')}
            bundle._json(root/'manifest.json',m);c=bundle._read(root/'complete.json');c['manifest_sha256']=digest_file(root/'manifest.json');bundle._json(root/'complete.json',c)
            with self.assertRaises(BundleError):bundle.inspect(root)
    def test_csv_and_report_cannot_contradict_retained_network(self):
        for name in ('trajectories.csv','report.html'):
            with tempfile.TemporaryDirectory() as tmp:
                root=Path(tmp)/'run';bundle.run(simple_study(duration=60),root)
                path=root/name;text=path.read_text()
                path.write_text(text.replace('BASELINE','FORGED_ARM',1) if name.endswith('.csv') else text.replace('<h1>','<h1>Forged interpretation: ',1))
                m=bundle._read(root/'manifest.json');m['files'][name]={'bytes':path.stat().st_size,'sha256':digest_file(path)};bundle._json(root/'manifest.json',m)
                c=bundle._read(root/'complete.json');c['manifest_sha256']=digest_file(root/'manifest.json');bundle._json(root/'complete.json',c)
                with self.assertRaises(BundleError):bundle.inspect(root)
