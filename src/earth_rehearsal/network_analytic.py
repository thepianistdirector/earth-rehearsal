"""Independent affine exponential action with exact capacity-event partitioning.

Original bounded Taylor-action implementation; no numerical Euler code is imported.
"""
from __future__ import annotations
import math
from .network_layout import Layout
from .network_study import ARMS,POLICY,grid_counts


def operator(study,segment,arm,active,layout):
    rows=[{} for _ in layout.slots];forcing=[0.0]*len(rows)
    def coefficient(target,origin,rate):
        row=rows[target];row[origin]=row.get(origin,0.0)+rate
    node_map={n['id']:n for n in study['nodes']};devices={c['edge']:c for c in study['capture']}
    source_scale=study['source_factor']['value'] if arm=='SOURCE_REDUCTION' else 1.0
    for node in study['nodes']:
        for cls in layout.classes:
            rate=segment['sources'][node['id']][cls]['value']*source_scale
            forcing[layout.at('mass',node['id'],cls)]=rate;forcing[layout.at('source',node['id'],cls)]=rate
    for edge in study['edges']:
        water=segment['flows'][edge['id']]['value'];forcing[layout.at('water',edge['id'])]=water
        if edge['from']=='outside':continue
        device=devices.get(edge['id']);fraction=device['fraction']['value'] if device and device['id'] in active else 0.0
        for cls in study['classes']:
            origin=layout.at('mass',edge['from'],cls['id'])
            rate=(water/node_map[edge['from']]['volume']['value'])*cls['mobility']['value']
            coefficient(origin,origin,-rate)
            coefficient(layout.at('edge',edge['id'],cls['id']),origin,rate)
            receiver=layout.at('escaped',edge['id'],cls['id']) if edge['to']=='outside' else layout.at('mass',edge['to'],cls['id'])
            coefficient(receiver,origin,rate*(1-fraction))
            if device:
                coefficient(layout.at('stored',device['id'],cls['id']),origin,rate*fraction)
                coefficient(layout.at('captured',device['id'],cls['id']),origin,rate*fraction)
    for cv in study['conversions']:
        origin=layout.at('mass',cv['node'],cv['from_class']);rate=cv['rate']['value']
        coefficient(origin,origin,-rate)
        coefficient(layout.at('mass',cv['node'],cv['to_class']),origin,rate)
        coefficient(layout.at('converted',cv['id']),origin,rate)
    for device in study['capture']:
        for cls in layout.classes:
            origin=layout.at('stored',device['id'],cls)
            release=device['release_rate']['value'];leak=device['leak_rate']['value']
            coefficient(origin,origin,-release-leak)
            coefficient(layout.at('unknown',device['id'],cls),origin,release)
            coefficient(layout.at('released',device['id'],cls),origin,release)
            coefficient(layout.at('leaked',device['id'],cls),origin,leak)
            coefficient(layout.at('mass',device['leak_destination'],cls),origin,leak)
    sparse=[[(j,v) for j,v in sorted(row.items()) if v] for row in rows]
    # The affine vector is the last column of a virtual augmented matrix.
    # Scale its constant coordinate to avoid treating a large water-source value
    # as stiffness. The Taylor recurrence below is algebraically the same action.
    constant_scale=1.0+max((abs(v) for v in forcing),default=0.0)*segment['duration']['value']
    norm=max((math.fsum(abs(v) for _,v in row)+abs(b)/constant_scale for row,b in zip(sparse,forcing)),default=0.0)
    return sparse,forcing,norm

def propagate(state,duration,op,budget):
    rows,forcing,norm=op
    if duration==0:return state.copy()
    chunks=max(1,math.ceil(duration*norm/POLICY['reference_norm_step']))
    budget['products']+=chunks*POLICY['taylor_degree']
    if budget['products']>POLICY['max_reference_products']:raise ValueError('reference work budget exceeded')
    dt=duration/chunks;result=state.copy()
    for _ in range(chunks):
        derivative=[math.fsum([b,*(rate*result[j] for j,rate in row)]) for row,b in zip(rows,forcing)]
        term=[dt*v for v in derivative]
        columns=[[value,first] for value,first in zip(result,term)]
        for degree in range(2,POLICY['taylor_degree']+1):
            term=[dt/degree*math.fsum(rate*term[j] for j,rate in row) for row in rows]
            for col,value in zip(columns,term):col.append(value)
        result=[math.fsum(col) for col in columns]
    if any(not math.isfinite(v) or v<0 for v in result):raise ValueError('reference state is nonfinite or negative')
    return result

def run_arm(study,arm,refinement=4):
    if arm not in ARMS or refinement not in POLICY['refinements']:raise ValueError('unknown reference arm/refinement')
    layout=Layout(study);state=layout.initial(study);records=[{'t':0.0,'segment':'initial','state':state.copy()}]
    active={c['id'] for c in study['capture'] if arm=='OUTLET_CAPTURE' and c['capacity']['value']>0 and c['fraction']['value']>0}
    caps={c['id']:c for c in study['capture']};events=[];budget={'products':0};offset=0.0
    def captured(values,cid):return math.fsum(values[layout.at('captured',cid,cls)] for cls in layout.classes)
    for segment,coarse in zip(study['segments'],grid_counts(study)):
        duration=segment['duration']['value'];count=coarse*refinement;op=operator(study,segment,arm,active,layout)
        for k in range(count):
            end=offset+duration*(k+1)/count;start=records[-1]['t'];remaining=end-start;elapsed=0.0
            for _ in range(len(caps)+1):
                trial=propagate(state,remaining,op,budget)
                crossing=[cid for cid in sorted(active) if captured(trial,cid)>=caps[cid]['capacity']['value']]
                if not crossing:
                    state=trial;break
                low=0.0;high=remaining
                for _ in range(52):
                    middle=(low+high)/2;probe=propagate(state,middle,op,budget)
                    if any(captured(probe,cid)>=caps[cid]['capacity']['value'] for cid in crossing):high=middle
                    else:low=middle
                state=propagate(state,high,op,budget);elapsed+=high;remaining-=high
                if start+elapsed<=start or any(captured(state,cid)>caps[cid]['capacity']['value']*(1+1e-10) for cid in crossing):raise ValueError('capacity event cannot be resolved at binary64 precision')
                exhausted=[cid for cid in sorted(active) if captured(state,cid)>=caps[cid]['capacity']['value']-1e-12*max(caps[cid]['capacity']['value'],1e-12)]
                if not exhausted:raise ValueError('reference capacity event did not resolve')
                for cid in exhausted:
                    active.remove(cid);events.append({'capture':cid,'t':start+elapsed,'captured_kg':captured(state,cid),'state':state.copy()})
                op=operator(study,segment,arm,active,layout)
                if remaining<=0:break
            else:raise ValueError('reference event budget exceeded')
            records.append({'t':end,'segment':segment['id'],'state':state.copy()})
        offset+=duration
    return {'method':'affine_exponential_reference','arm':arm,'refinement':refinement,'records':records,'capacity_events':events,
            'products':budget['products'],'claims':{name:'NOT_EVALUATED' for name in ('disposal','lifecycle','ecological','health')}}
