from __future__ import annotations
import copy
import json
import math
from pathlib import Path
import sys
import unittest
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
from earth_rehearsal import network_study as contract
from earth_rehearsal.network_layout import Layout
from earth_rehearsal.network_numerical import run_arm as numerical
from earth_rehearsal.network_analytic import run_arm as reference
from earth_rehearsal.network_evaluator import evaluate,NetworkEvaluationError
from earth_rehearsal.sources import digest,validate_record,scale_record,SourceError


def simple_study(nodes=1,flow=.1,initial=2.0,source=.003,duration=600.0,second_class=False,capture=False,release=0.0,leak=0.0,capacity=10.0):
    s=contract.load(ROOT/'scenarios/catchment-001.json');s['source_records'][0]['values']={};s['source_records'][0]['transforms']=[]
    values=s['source_records'][0]['values']
    def q(name,value,unit):
        values[name]={'value':value,'unit':unit,'quality_flags':[]}
        return {'value':value,'unit':unit,'source':{'record':'manufactured_catchment','variable':name}}
    classes=['mobile','retained'] if second_class else ['mobile']
    s['classes']=[{'id':c,'mobility':q(c+'_mobility',1 if c=='mobile' else 0,'1')} for c in classes]
    names=['a','b'][:nodes]
    s['nodes']=[{'id':name,'volume':q(name+'_volume',1000,'m3'),'initial_mass':{c:q(name+'_initial_'+c,initial if i==0 and c=='mobile' else 0,'kg') for c in classes},'position':{'x':.25+.5*i,'y':.5}} for i,name in enumerate(names)]
    s['edges']=[] if not flow else ([{'id':'inflow','from':'outside','to':'a'}]+([{'id':'exchange','from':'a','to':'b'}] if nodes==2 else [])+[{'id':'outflow','from':names[-1],'to':'outside'}])
    s['segments']=[{'id':'control','duration':q('duration',duration,'s'),'flows':{e['id']:q('flow_'+e['id'],flow,'m3/s') for e in s['edges']},'sources':{name:{c:q('source_'+name+'_'+c,source if name=='a' and c=='mobile' else 0,'kg/s') for c in classes} for name in names}}]
    s['conversions']=[]
    s['capture']=[{'id':'cap','edge':'outflow','fraction':q('capture_fraction',1,'1'),'capacity':q('capacity',capacity,'kg'),'release_rate':q('release',release,'1/s'),'leak_rate':q('leak',leak,'1/s'),'leak_destination':names[-1],'energy':None}] if capture else []
    s['source_factor']=q('source_factor',.5,'1');s['source_records'][0]['content_sha256']=digest(values)
    return contract.validate(s)

def evaluated(s):
    n=[numerical(s,a,l) for a in contract.ARMS for l in contract.POLICY['refinements']]
    r=[reference(s,a) for a in contract.ARMS]
    return n,r,evaluate(s,n,r)

class NetworkControls(unittest.TestCase):
    def test_closed_zero_flow_is_separate_accumulation(self):
        s=simple_study(flow=0);r=reference(s,'BASELINE');l=Layout(s)
        self.assertAlmostEqual(r['records'][-1]['state'][l.at('mass','a','mobile')],2+.003*600,places=12)
        _,_,e=evaluated(s);self.assertIsNone(e['refinement'][0]['fine_coarse_ratio'])
    def test_scalar_reference_matches_closed_form(self):
        s=simple_study();r=reference(s,'BASELINE');l=Layout(s);k=.1/1000;t=600
        expected=2*math.exp(-k*t)+.003/k*(-math.expm1(-k*t))
        self.assertAlmostEqual(r['records'][-1]['state'][l.at('mass','a','mobile')],expected,places=11)
        self.assertAlmostEqual(r['records'][-1]['state'][l.at('escaped','outflow','mobile')],2+.003*t-expected,places=11)
    def test_equal_rate_cascade_matches_independent_formula(self):
        s=simple_study(nodes=2);r=reference(s,'BASELINE');l=Layout(s);k=.0001;t=600
        expected=2*k*t*math.exp(-k*t)+.003/k*(1-(1+k*t)*math.exp(-k*t))
        self.assertAlmostEqual(r['records'][-1]['state'][l.at('mass','b','mobile')],expected,places=11)
        evaluated(s)
    def test_finite_capacity_event_has_closed_form_time(self):
        s=simple_study(source=0,duration=1000,capture=True,capacity=.1);r=reference(s,'OUTLET_CAPTURE');l=Layout(s)
        self.assertEqual(len(r['capacity_events']),1)
        self.assertAlmostEqual(r['capacity_events'][0]['t'],-math.log1p(-.1/2)/.0001,places=8)
        self.assertAlmostEqual(r['records'][-1]['state'][l.at('captured','cap','mobile')],.1,places=12)
        evaluated(s)
    def test_storage_release_matches_convolution(self):
        s=simple_study(source=0,duration=1000,capture=True,release=.0002);r=reference(s,'OUTLET_CAPTURE');l=Layout(s)
        expected=.0001*2*(math.exp(-.0001*1000)-math.exp(-.0002*1000))/(.0002-.0001)
        self.assertAlmostEqual(r['records'][-1]['state'][l.at('stored','cap','mobile')],expected,places=11)
        evaluated(s)
    def test_leakage_returns_to_named_compartment(self):
        s=simple_study(source=0,duration=1000,capture=True,leak=.0002);r=reference(s,'OUTLET_CAPTURE');l=Layout(s)
        expected=2*.0002/.0003+2*.0001/.0003*math.exp(-.0003*1000)
        self.assertAlmostEqual(r['records'][-1]['state'][l.at('mass','a','mobile')],expected,places=11)
        self.assertAlmostEqual(r['records'][-1]['state'][l.at('stored','cap','mobile')],2-expected,places=11)
        evaluated(s)
    def test_mass_conserving_class_conversion(self):
        s=simple_study(flow=0,source=0,second_class=True);record=s['source_records'][0]
        record['values']['conversion_rate']={'value':.001,'unit':'1/s','quality_flags':[]};record['content_sha256']=digest(record['values'])
        s['conversions']=[{'id':'change','node':'a','from_class':'mobile','to_class':'retained','rate':{'value':.001,'unit':'1/s','source':{'record':record['id'],'variable':'conversion_rate'}}}]
        contract.validate(s);r=reference(s,'BASELINE');l=Layout(s)
        self.assertAlmostEqual(r['records'][-1]['state'][l.at('mass','a','mobile')],2*math.exp(-.6),places=11)
        self.assertAlmostEqual(r['records'][-1]['state'][l.at('mass','a','retained')],2*(1-math.exp(-.6)),places=11)
        evaluated(s)
    def test_default_refines_and_preserves_paired_sources(self):
        s=contract.load(ROOT/'scenarios/catchment-001.json');n,r,e=evaluated(s)
        self.assertTrue(all(d['fine_coarse_ratio']<.3 for d in e['refinement']))
        summaries=[x for x in e['summaries'] if x['method']=='conservative_euler' and x['refinement']==4]
        self.assertAlmostEqual(summaries[1]['source_kg'],summaries[0]['source_kg']/2)
        self.assertAlmostEqual(summaries[2]['captured_kg'],.4)
        self.assertGreater(summaries[2]['leaked_kg'],0)
        self.assertGreater(summaries[2]['unknown_kg'],0)

class NetworkFalsifiers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s=contract.load(ROOT/'scenarios/catchment-001.json');cls.n,cls.r,_=evaluated(cls.s);cls.l=Layout(cls.s)
    def rejects(self,mutate):
        n=copy.deepcopy(self.n);r=copy.deepcopy(self.r);mutate(n,r)
        with self.assertRaises(NetworkEvaluationError):evaluate(self.s,n,r)
    def test_conserving_wrong_advection_fails(self):
        def corrupt(n,r):
            l=self.l;x=n[0]['records'][3]['state'];x[l.at('edge','head_to_middle','mobile')]+=.1;x[l.at('mass','headwater','mobile')]-=.1;x[l.at('mass','middle','mobile')]+=.1
        self.rejects(corrupt)
    def test_conserving_wrong_source_fails(self):
        def corrupt(n,r):
            l=self.l;x=n[0]['records'][1]['state'];x[l.at('source','headwater','mobile')]+=.1;x[l.at('mass','headwater','mobile')]+=.1
        self.rejects(corrupt)
    def test_custody_capacity_and_benefit_falsifiers(self):
        self.rejects(lambda n,r:n[-1]['claims'].__setitem__('disposal','SAFELY_DISPOSED'))
        self.rejects(lambda n,r:n[-1]['records'][-1]['state'].__setitem__(self.l.at('captured','interceptor','mobile'),1.0))
        self.rejects(lambda n,r:n[-1]['records'][-1]['state'].__setitem__(self.l.at('unknown','interceptor','mobile'),0.0))
    def test_missing_duplicate_reordered_malformed_records(self):
        self.rejects(lambda n,r:n[0]['records'].pop())
        self.rejects(lambda n,r:n[0]['records'].__setitem__(2,n[0]['records'][1]))
        self.rejects(lambda n,r:n[0]['records'][1]['state'].__setitem__(0,float('nan')))
        self.rejects(lambda n,r:n[0]['records'][1].__setitem__('t',True))
        self.rejects(lambda n,r:n.__setitem__(0,n[1]))
    def test_reference_cannot_replace_numerical_path(self):
        self.rejects(lambda n,r:n.__setitem__(2,copy.deepcopy(r[0])))
    def test_evaluation_does_not_execute_either_solver(self):
        from unittest.mock import patch
        with patch('earth_rehearsal.network_numerical.run_arm',side_effect=AssertionError('kernel executed')),patch('earth_rehearsal.network_analytic.run_arm',side_effect=AssertionError('reference executed')):
            evaluate(self.s,self.n,self.r)

class NetworkContract(unittest.TestCase):
    def test_invalid_units_missing_classes_and_rights(self):
        s=contract.load(ROOT/'scenarios/catchment-001.json')
        for mutation in [lambda x:x['nodes'][0]['volume'].__setitem__('unit','litres'),lambda x:x['nodes'][0]['initial_mass'].pop('retained'),lambda x:x['source_records'][0]['rights'].__setitem__('redistribution',False),lambda x:x['capture'][0].__setitem__('leak_destination','missing'),lambda x:x['edges'][0].__setitem__('from',[]),lambda x:x['conversions'][0].__setitem__('node',[])]:
            q=copy.deepcopy(s);mutation(q)
            with self.assertRaises(ValueError):contract.validate(q)
    def test_unbalanced_water_and_missing_provenance_reject(self):
        s=contract.load(ROOT/'scenarios/catchment-001.json')
        with self.assertRaisesRegex(ValueError,'balanced'):contract.set_quantity(s,['segments',0,'flows','inflow'],.2)
        q=copy.deepcopy(s);q['source_factor']['value']=.2
        with self.assertRaisesRegex(ValueError,'source variable'):contract.validate(q)
    def test_edits_preserve_ordered_source_identity(self):
        s=contract.load(ROOT/'scenarios/catchment-001.json');q=contract.set_quantity(s,['source_factor'],.25);r=contract.set_quantity(q,['source_factor'],.75)
        self.assertNotEqual(contract.identity(s),contract.identity(q));self.assertEqual(len(r['source_records'][0]['transforms']),2)
        self.assertEqual(r['source_records'][0]['transforms'][1]['parent_sha256'],q['source_records'][0]['content_sha256'])
    def test_source_missingness_and_flags_survive_scaling(self):
        record=copy.deepcopy(contract.load(ROOT/'scenarios/catchment-001.json')['source_records'][0]);record['values']['unobserved']={'value':None,'unit':'kg','quality_flags':['not sampled']};record['missing_variables']=['unobserved'];record['content_sha256']=digest(record['values'])
        scaled=scale_record(record,'unobserved',2)
        self.assertIsNone(scaled['values']['unobserved']['value']);self.assertEqual(scaled['values']['unobserved']['quality_flags'],['not sampled']);self.assertEqual(scaled['missing_variables'],['unobserved'])
        scaled['values']['unobserved']['value']=0
        with self.assertRaises(SourceError):validate_record(scaled)
    def test_excessive_budget_and_nonadvancing_time_reject(self):
        s=contract.load(ROOT/'scenarios/catchment-001.json')
        with self.assertRaisesRegex(ValueError,'budget'):contract.set_quantity(s,['conversions',0,'rate'],1)
        with self.assertRaisesRegex(ValueError,'advance'):contract.set_quantity(s,['segments',1,'duration'],1e-300)
