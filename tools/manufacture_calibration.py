"""Regenerate original known synthetic controls with the independent reference.

Developer fixture authoring only; fitting never invokes this generator.
"""
import sys,json,copy
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from earth_rehearsal import cohort,calibration
from earth_rehearsal.network_study import load,set_quantity,identity
from earth_rehearsal.network_analytic import run_arm
from earth_rehearsal.network_layout import Layout

def generate():
    s=load(ROOT/'scenarios/catchment-001.json');dry=set_quantity(s,['segments',1,'duration'],0)
    hold=set_quantity(set_quantity(s,['segments',0,'duration'],1800),['segments',1,'duration'],1200)
    p={'format':'earth-rehearsal-calibration-v1','id':'synthetic-cohort-001','classification':'wholly_synthetic_known_answer','development':[{'id':'development_dry','study':dry},{'id':'development_storm','study':s}],'holdout':[{'id':'confirmation_shorter_storm','study':hold}], 'parameters':[{'id':'source_factor','path':['source_factor'],'unit':'1'},{'id':'capacity','path':['capture',0,'capacity'],'unit':'kg'}], 'candidates':[{'id':'strong_prevention','values':{'source_factor':.3,'capacity':10}},{'id':'equivalent_a','values':{'source_factor':.5,'capacity':10}},{'id':'equivalent_b','values':{'source_factor':.5,'capacity':20}},{'id':'invalid_candidate','values':{'source_factor':1.1,'capacity':10}}], 'observables':[{'id':'prevention_escape','arm':'SOURCE_REDUCTION','kind':'escaped','entity':'escape','class':'mobile','time':'final','unit':'kg'},{'id':'capture_storage','arm':'OUTLET_CAPTURE','kind':'stored','entity':'interceptor','class':'mobile','time':'final','unit':'kg'},{'id':'capture_unknown','arm':'OUTLET_CAPTURE','kind':'unknown','entity':'interceptor','class':'mobile','time':'final','unit':'kg'}], 'loss':{'kind':'SUM_SQUARED_ERROR','unit':'kg2','equivalence_absolute':1e-12,'confirmation_max_abs':.02},'budget':{'max_candidates':8,'max_seconds':120}}
    cohort.validate_protocol(p)
    outputs={'protocol.json':p}
    for split in ('development','holdout'):
     data={'format':'earth-rehearsal-observations-v1','split':split,'classification':'wholly_synthetic_reference','cases':[]}
     for case in p[split]:
      truth=calibration.parameters(case['study'],p,p['candidates'][1]);l=Layout(truth);runs={arm:run_arm(truth,arm) for arm in {ob['arm'] for ob in p['observables']}}
      data['cases'].append({'id':case['id'],'input_study_id':identity(case['study']),'observations':[{'observable':ob['id'],'value':runs[ob['arm']]['records'][-1]['state'][l.at(ob['kind'],ob['entity'],ob['class'])],'unit':'kg','quality':'SYNTHETIC_CONTROL'} for ob in p['observables']]})
     cohort.validate_observations(data,p,split);outputs[split+'.json']=data
    return outputs

def main():
    import argparse
    parser=argparse.ArgumentParser(description='Verify or author original known synthetic calibration controls')
    choice=parser.add_mutually_exclusive_group(required=True)
    choice.add_argument('--check',action='store_true',help='compare generated controls with tracked fixtures without writing')
    choice.add_argument('--out',type=Path,help='new directory for generated JSON controls')
    args=parser.parse_args();outputs=generate()
    if args.check:
        for name,value in outputs.items():
            if json.loads((ROOT/'scenarios/calibration'/name).read_text())!=value:raise SystemExit('Generated control differs: '+name)
        print('PASS: original independent-reference calibration controls match tracked fixtures')
    else:
        args.out.mkdir(parents=True,exist_ok=False)
        for name,value in outputs.items():(args.out/name).write_text(json.dumps(value,indent=2)+'\n')
        print('Authored known synthetic controls: '+str(args.out))

if __name__=='__main__':main()
