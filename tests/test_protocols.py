"""Protocol-level evidence controls: denominators, reversals, exposure and replay."""
import copy
import math
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from test_network import simple_study
from earth_rehearsal import campaign,resolution,calibration,cohort,study_archive,network_bundle
from earth_rehearsal.network_study import identity,set_quantity
from earth_rehearsal.bundle import BundleError
from earth_rehearsal.network_bundle import _read,_json


def small_campaign():
    return {'format':'earth-rehearsal-campaign-v1','id':'control','base_study':simple_study(flow=0,duration=60),'parameters':[{'id':'factor','path':['source_factor'],'unit':'1'}],'dependence':{'kind':'ONE_AT_A_TIME','description':'Explicit manufactured factor control, no probability interpretation'},'cases':[{'id':'valid','values':{'factor':.5}},{'id':'invalid','values':{'factor':1.1}},{'id':'last','values':{'factor':.8}}],'budget':{'max_attempts':3,'max_seconds':120}}

def small_cohort():
    dev=simple_study(flow=0,duration=60);hold=simple_study(flow=0,duration=120)
    p={'format':'earth-rehearsal-calibration-v1','id':'cohort_control','classification':'wholly_synthetic_known_answer','development':[{'id':'dev','study':dev}],'holdout':[{'id':'hold','study':hold}],'parameters':[{'id':'factor','path':['source_factor'],'unit':'1'}],'candidates':[{'id':'lower','values':{'factor':.25}},{'id':'truth','values':{'factor':.5}},{'id':'higher','values':{'factor':.75}}],'observables':[{'id':'mass','arm':'SOURCE_REDUCTION','kind':'mass','entity':'a','class':'mobile','time':'final','unit':'kg'}],'loss':{'kind':'SUM_SQUARED_ERROR','unit':'kg2','equivalence_absolute':1e-20,'confirmation_max_abs':1e-10},'budget':{'max_candidates':3,'max_seconds':120}}
    def observations(split):
        return {'format':'earth-rehearsal-observations-v1','split':split,'classification':'wholly_synthetic_reference','cases':[{'id':c['id'],'input_study_id':identity(c['study']),'observations':[{'observable':'mass','value':2+.003*.5*c['study']['segments'][0]['duration']['value'],'unit':'kg','quality':'SYNTHETIC_CONTROL'}]} for c in p[split]]}
    return p,observations('development'),observations('holdout')

class CampaignControls(unittest.TestCase):
    def test_invalid_and_budget_samples_stay_in_denominator(self):
        p=small_campaign();p['budget']['max_attempts']=2
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run';s=campaign.run(p,root)
            self.assertEqual(s['counts'],{'SUCCEEDED':1,'INVALID':1,'FAILED':0,'NOT_RUN_BUDGET':1});self.assertEqual(s['denominator'],3)
            self.assertEqual(campaign.inspect(root),s)
            with patch('earth_rehearsal.network_numerical.run_arm',side_effect=AssertionError('solver called')),patch('earth_rehearsal.network_analytic.run_arm',side_effect=AssertionError('reference called')):campaign.inspect(root)
            study_archive.export(root,Path(tmp)/'export','campaign',campaign.inspect);campaign.inspect(Path(tmp)/'export')
    def test_interruption_preserves_first_raw_and_denominator(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run'
            def stop(phase):
                if phase=='after_raw':raise KeyboardInterrupt
            with self.assertRaises(KeyboardInterrupt):campaign.run(small_campaign(),root,checkpoint=stop)
            attempts=_read(root/'attempts.json');self.assertEqual(attempts[0]['status'],'CANCELLED');self.assertEqual(attempts[1]['status'],'NOT_RUN_INTERRUPTION')
            self.assertEqual(len(list((root/'cases/000-valid/raw').glob('*.json'))),1)
            with self.assertRaises(BundleError):campaign.inspect(root)
    def test_forged_summary_fails_even_after_rehash(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run';campaign.run(small_campaign(),root);s=_read(root/'summary.json');s['rows'][0]['escaped_kg']=100;_json(root/'summary.json',s)
            (root/'archive.json').unlink();(root/'complete.json').unlink();study_archive.seal(root,'campaign')
            with self.assertRaisesRegex(BundleError,'summary'):campaign.inspect(root)

class RemapControls(unittest.TestCase):
    def test_conserved_mass_is_not_profile_accuracy(self):
        p={'source_edges':[0,.25,.5,.75,1],'target_edges':[0,.5,1],'source_mass_kg':[0,.1,.3,.6],'profile':'piecewise_constant_cell_average'}
        r=resolution.remap(p);self.assertLess(abs(r['mass_residual_kg']),1e-15);self.assertAlmostEqual(r['profile_L1_error_kg'],.4)
        p['target_edges']=p['source_edges'];r=resolution.remap(p);self.assertEqual(r['profile_L1_error_kg'],0)
        p['target_edges']=[.1,1]
        with self.assertRaises(ValueError):resolution.remap(p)
    def test_resolution_separates_spatial_and_time_reference(self):
        p=_read(Path(__file__).resolve().parents[1]/'scenarios/resolution-001.json')
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'run';s=resolution.run(p,root);self.assertEqual(s['status'],'PASSED_MANUFACTURED_REFINEMENT')
            self.assertLess(s['spatial_fine_coarse_ratio'],.05);self.assertEqual(resolution.inspect(root),s)
            for n in (1,2,4,8):
                rows=[r for r in s['rows'] if r['cells']==n];self.assertEqual(len({r['spatial_error_kg'] for r in rows}),1)
                self.assertLess(rows[-1]['time_error_kg'],rows[0]['time_error_kg'])

class CalibrationControls(unittest.TestCase):
    def test_fit_never_reads_holdout_and_confirmation_locks_fitting(self):
        p,d,h=small_cohort()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cohort.freeze(p,d,h,root/'cohort');original_open=Path.open
            def guarded(path,*args,**kwargs):
                if path==root/'cohort/holdout.json':raise AssertionError('fitting read holdout observations')
                return original_open(path,*args,**kwargs)
            with patch.object(Path,'open',guarded):s=calibration.fit(root/'cohort',root/'fit')
            self.assertEqual(s['selected']['id'],'truth');self.assertEqual(calibration.inspect_fit(root/'fit'),s)
            c=calibration.confirm(root/'cohort',root/'fit',root/'confirmation');self.assertEqual(c['status'],'PASSED_FROZEN_SYNTHETIC_CONFIRMATION')
            self.assertTrue((root/'cohort/holdout-access.json').exists())
            with self.assertRaisesRegex(BundleError,'already exposed'):calibration.fit(root/'cohort',root/'forbidden-fit')
            self.assertFalse((root/'forbidden-fit').exists())
            with self.assertRaisesRegex(BundleError,'already exposed'):calibration.confirm(root/'cohort',root/'fit',root/'forbidden-confirm')
            replay=calibration.confirm(root/'cohort',root/'fit',root/'replay',replay=True);self.assertEqual(replay['mode'],'FROZEN_SELECTION_REPLAY')
            self.assertEqual(calibration.inspect_confirmation(root/'replay'),replay)
            reproduced=calibration.reproduce_confirmation(root/'confirmation',root/'portable-replay');self.assertEqual(reproduced['mode'],'FROZEN_SELECTION_REPLAY')
    def test_interruption_after_exposure_before_read_is_consumed(self):
        p,d,h=small_cohort()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cohort.freeze(p,d,h,root/'cohort');calibration.fit(root/'cohort',root/'fit')
            def stop(phase):
                if phase=='after_exposure_before_read':raise KeyboardInterrupt
            with self.assertRaises(KeyboardInterrupt):calibration.confirm(root/'cohort',root/'fit',root/'confirmation',checkpoint=stop)
            self.assertTrue((root/'cohort/holdout-access.json').is_file());self.assertFalse((root/'confirmation/holdout.json').exists())
            with self.assertRaises(BundleError):calibration.fit(root/'cohort',root/'newfit')
            self.assertEqual(calibration.confirm(root/'cohort',root/'fit',root/'replay',replay=True)['mode'],'FROZEN_SELECTION_REPLAY')
    def test_changed_holdout_fails_after_durable_exposure(self):
        p,d,h=small_cohort()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cohort.freeze(p,d,h,root/'cohort');calibration.fit(root/'cohort',root/'fit');h['cases'][0]['observations'][0]['value']+=1;_json(root/'cohort/holdout.json',h)
            with self.assertRaisesRegex(BundleError,'bytes changed'):calibration.confirm(root/'cohort',root/'fit',root/'confirmation')
            self.assertTrue((root/'cohort/holdout-access.json').exists())
    def test_failed_confirmation_is_retained_not_relabelled(self):
        p,d,h=small_cohort();h['cases'][0]['observations'][0]['value']+=.1
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cohort.freeze(p,d,h,root/'cohort');calibration.fit(root/'cohort',root/'fit');s=calibration.confirm(root/'cohort',root/'fit',root/'confirmation')
            self.assertEqual(s['status'],'FAILED_FROZEN_SYNTHETIC_CONFIRMATION');self.assertEqual(calibration.inspect_confirmation(root/'confirmation'),s)
    def test_explicit_consumption_retains_old_evidence(self):
        p,d,h=small_cohort()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cohort.freeze(p,d,h,root/'old');calibration.fit(root/'old',root/'fit');calibration.confirm(root/'old',root/'fit',root/'confirmation')
            new=copy.deepcopy(p);new['id']='new_cohort';new['development']+=new['holdout'];study=simple_study(flow=0,duration=180);new['holdout']=[{'id':'new_hold','study':study}]
            nd=copy.deepcopy(d);nd['cases']+=h['cases'];nh={'format':h['format'],'split':'holdout','classification':h['classification'],'cases':[{'id':'new_hold','input_study_id':identity(study),'observations':[{'observable':'mass','value':2+.003*.5*180,'unit':'kg','quality':'SYNTHETIC_CONTROL'}]}]}
            cohort.consume(root/'old',new,nd,nh,root/'new');self.assertTrue((root/'new/lineage.json').exists());self.assertEqual(len(cohort.development_only(root/'new')[1]['development']),2)
            self.assertEqual(calibration.fit(root/'new',root/'newfit')['selected']['id'],'truth')

class ProtocolFalsifiers(unittest.TestCase):
    def reseal(self,root,kind):
        (root/'archive.json').unlink();(root/'complete.json').unlink();study_archive.seal(root,kind)
    def test_completed_campaign_sample_cannot_be_omitted_as_budget(self):
        p=small_campaign()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'campaign';campaign.run(p,root);a=_read(root/'attempts.json')
            a[0]={'id':'valid','status':'NOT_RUN_BUDGET','reason':'forged exhaustion','elapsed_seconds':120}
            _json(root/'attempts.json',a);self.reseal(root,'campaign')
            with self.assertRaises(BundleError):campaign.inspect(root)
    def test_completed_fit_candidate_cannot_be_omitted_as_budget(self):
        p,d,h=small_cohort()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cohort.freeze(p,d,h,root/'cohort');calibration.fit(root/'cohort',root/'fit');a=_read(root/'fit/attempts.json')
            a[1]={'id':'truth','status':'NOT_RUN_BUDGET','cases':[],'reason':'forged exhaustion','elapsed_seconds':120}
            _json(root/'fit/attempts.json',a);_json(root/'fit/selection.json',calibration.selection(p,a));self.reseal(root/'fit','calibration-fit')
            with self.assertRaises(BundleError):calibration.inspect_fit(root/'fit')
            with self.assertRaises(BundleError):calibration.confirm(root/'cohort',root/'fit',root/'confirmation')
            self.assertFalse((root/'cohort/holdout-access.json').exists())
    def test_confirmation_requires_original_successful_fit_receipt(self):
        p,d,h=small_cohort()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cohort.freeze(p,d,h,root/'cohort');calibration.fit(root/'cohort',root/'fit')
            receipt=next((root/'cohort/fit-attempts').glob('*.json'));value=_read(receipt);value['selection_sha256']='0'*64;_json(receipt,value)
            with self.assertRaisesRegex(BundleError,'original successful'):calibration.confirm(root/'cohort',root/'fit',root/'confirmation')
            self.assertFalse((root/'cohort/holdout-access.json').exists())
    def test_holdout_support_is_not_new_after_metadata_or_parameter_edit(self):
        p,_,_=small_cohort()
        for mode in ('identical','metadata','fitted_value'):
            case=copy.deepcopy(p);case['holdout'][0]['study']=copy.deepcopy(p['development'][0]['study'])
            if mode=='metadata':case['holdout'][0]['study']['source_records'][0]['title']='A different title for the same data'
            if mode=='fitted_value':case['holdout'][0]['study']=set_quantity(case['holdout'][0]['study'],['source_factor'],.3)
            with self.assertRaisesRegex(ValueError,'distinct experimental controls'):cohort.validate_protocol(case)
    def test_csv_cannot_disagree_with_reconstructed_campaign(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp)/'campaign';campaign.run(small_campaign(),root)
            path=root/'summary.csv';text=path.read_text();path.write_text(text.replace('0.0','999999',1));self.reseal(root,'campaign')
            with self.assertRaisesRegex(BundleError,'CSV differs'):campaign.inspect(root)
    def test_fit_loss_csv_cannot_disagree_with_retained_candidates(self):
        p,d,h=small_cohort()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cohort.freeze(p,d,h,root/'cohort');calibration.fit(root/'cohort',root/'fit')
            path=root/'fit/losses.csv';rows=path.read_text().splitlines();parts=rows[1].split(',');parts[-1]='999999';rows[1]=','.join(parts);path.write_text('\n'.join(rows)+'\n');self.reseal(root/'fit','calibration-fit')
            with self.assertRaisesRegex(BundleError,'CSV differs'):calibration.inspect_fit(root/'fit')
    def test_portable_replay_cannot_be_relabelled_first_confirmation(self):
        p,d,h=small_cohort()
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);cohort.freeze(p,d,h,root/'cohort');calibration.fit(root/'cohort',root/'fit');calibration.confirm(root/'cohort',root/'fit',root/'confirmation');calibration.reproduce_confirmation(root/'confirmation',root/'replay')
            access=_read(root/'replay/access.json');access['replay']=False;_json(root/'replay/access.json',access)
            attempts=_read(root/'replay/attempts.json');summary=calibration.confirmation_summary(p,attempts,False);_json(root/'replay/summary.json',summary)
            (root/'replay/report.html').write_text(calibration.render_confirmation(attempts,summary,reproduction=True));self.reseal(root/'replay','calibration-confirmation')
            with self.assertRaisesRegex(BundleError,'cannot become first'):calibration.inspect_confirmation(root/'replay')
