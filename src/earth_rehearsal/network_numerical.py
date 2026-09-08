"""Direct conservative Euler transfers, independent of the reference operator."""
from __future__ import annotations
import math
from .network_layout import Layout
from .network_study import ARMS,POLICY,grid_counts


def run_arm(study,arm,refinement):
    if arm not in ARMS or refinement not in POLICY['refinements']:raise ValueError('unknown arm/refinement')
    layout=Layout(study);state=layout.initial(study)
    nodes={n['id']:n for n in study['nodes']};caps={c['edge']:c for c in study['capture']}
    factor=study['source_factor']['value'] if arm=='SOURCE_REDUCTION' else 1.0
    records=[{'t':0.0,'segment':'initial','state':state.copy()}];offset=0.0
    counts=grid_counts(study)
    for seg,coarse in zip(study['segments'],counts):
        count=coarse*refinement;duration=seg['duration']['value']
        for step in range(count):
            end=offset+duration*(step+1)/count;start=records[-1]['t'];dt=end-start
            if dt<=0:raise ValueError('numerical time failed to advance')
            changes=[[] for _ in state]
            def add(kind,entity,cls,amount):changes[layout.at(kind,entity,cls)].append(amount)
            for node in study['nodes']:
                for cls in layout.classes:
                    amount=seg['sources'][node['id']][cls]['value']*factor*dt
                    add('mass',node['id'],cls,amount);add('source',node['id'],cls,amount)
            for edge in study['edges']:
                flow=seg['flows'][edge['id']]['value']
                add('water',edge['id'],None,flow*dt)
                if edge['from']=='outside':continue
                donor=edge['from'];cap=caps.get(edge['id']);candidate=[];flux=[]
                for cls in study['classes']:
                    amount=flow*dt*cls['mobility']['value']*state[layout.at('mass',donor,cls['id'])]/nodes[donor]['volume']['value']
                    flux.append(amount)
                    candidate.append(amount*cap['fraction']['value'] if cap and arm=='OUTLET_CAPTURE' else 0.0)
                total=math.fsum(candidate);scale=1.0
                if cap and arm=='OUTLET_CAPTURE' and total:
                    used=math.fsum(state[layout.at('captured',cap['id'],cls)] for cls in layout.classes)
                    remaining=max(0.0,cap['capacity']['value']-used)
                    scale=min(1.0,remaining/total)
                for cls,amount,wanted in zip(layout.classes,flux,candidate):
                    captured=wanted*scale
                    add('mass',donor,cls,-amount);add('edge',edge['id'],cls,amount)
                    if edge['to']=='outside':add('escaped',edge['id'],cls,amount-captured)
                    else:add('mass',edge['to'],cls,amount-captured)
                    if cap:
                        add('stored',cap['id'],cls,captured);add('captured',cap['id'],cls,captured)
            for cv in study['conversions']:
                amount=state[layout.at('mass',cv['node'],cv['from_class'])]*cv['rate']['value']*dt
                add('mass',cv['node'],cv['from_class'],-amount);add('mass',cv['node'],cv['to_class'],amount);add('converted',cv['id'],None,amount)
            for cap in study['capture']:
                for cls in layout.classes:
                    stored=state[layout.at('stored',cap['id'],cls)]
                    released=stored*cap['release_rate']['value']*dt;leaked=stored*cap['leak_rate']['value']*dt
                    add('stored',cap['id'],cls,-released-leaked);add('unknown',cap['id'],cls,released)
                    add('released',cap['id'],cls,released);add('leaked',cap['id'],cls,leaked)
                    add('mass',cap['leak_destination'],cls,leaked)
            state=[math.fsum([value,*delta]) for value,delta in zip(state,changes)]
            if any(not math.isfinite(v) or v<0 for v in state):raise ValueError('numerical state is nonfinite or negative; no clipping is allowed')
            records.append({'t':end,'segment':seg['id'],'state':state.copy()})
        offset+=duration
    return {'method':'conservative_euler','arm':arm,'refinement':refinement,'records':records,
            'claims':{name:'NOT_EVALUATED' for name in ('disposal','lifecycle','ecological','health')}}
