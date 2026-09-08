"""Independent reconstruction of numerical physics and retained network accounting.

Inspection uses this module without invoking either trajectory generator.
"""
from __future__ import annotations
import itertools
import math
from .network_layout import Layout
from .reference_certificate import certificate
from .network_study import ARMS,POLICY,grid_counts,validate

class NetworkEvaluationError(ValueError): pass
BENEFITS={k:'NOT_EVALUATED' for k in ('disposal','lifecycle','ecological','health')}

def _evaluate(study,numerical,references):
    validate(study);layout=Layout(study);dim=len(layout.slots);counts=grid_counts(study)
    def fail(message):raise NetworkEvaluationError(message)
    def close(actual,expected,scale,label,relative=1e-9,rounding=0.0):
        if not math.isfinite(actual) or abs(actual-expected)>relative*max(scale,1e-300)+rounding:fail(label+f': mismatch ({actual:.12g} versus {expected:.12g})')
    if not isinstance(numerical,list) or len(numerical)!=9 or not isinstance(references,list) or len(references)!=3:fail('exactly nine numerical and three reference trajectories required')
    numkeys=[(r.get('arm'),r.get('refinement')) for r in numerical if isinstance(r,dict)]
    if numkeys!=list(itertools.product(ARMS,POLICY['refinements'])):fail('numerical arm/refinement identity or order mismatch')
    if [r.get('arm') for r in references if isinstance(r,dict)]!=list(ARMS):fail('reference arm identity or order mismatch')
    if any(r.get('method')!='conservative_euler' for r in numerical) or any(r.get('method')!='affine_exponential_reference' for r in references):fail('trajectory method cannot substitute for the other independent path')
    node_map={n['id']:n for n in study['nodes']};caps={c['edge']:c for c in study['capture']}
    initial=layout.initial(study);initial_total=math.fsum(initial)
    base_source=math.fsum(seg['duration']['value']*seg['sources'][n['id']][c]['value'] for seg in study['segments'] for n in study['nodes'] for c in layout.classes)
    mass_scale=max(1.0,initial_total+base_source)
    summaries=[];water_ledgers=[];mass_ledgers=[]
    for result in [*numerical,*references]:
        is_euler=result['method']=='conservative_euler' if 'method' in result else False
        expected_keys={'method','arm','refinement','records','claims'} if is_euler else {'method','arm','refinement','records','claims','capacity_events','products'}
        if set(result)!=expected_keys or result['claims']!=BENEFITS:fail('trajectory schema or unsupported benefit claim')
        if result['method'] not in ('conservative_euler','affine_exponential_reference'):fail('unknown trajectory method')
        level=result['refinement'];arm=result['arm']
        if type(level) is not int or level not in POLICY['refinements'] or (not is_euler and level!=4):fail('invalid trajectory refinement')
        records=result['records']
        if not isinstance(records,list) or len(records)!=1+sum(counts)*level:fail('missing or extra trajectory records')
        for record in records:
            if not isinstance(record,dict) or set(record)!= {'t','segment','state'}:fail('invalid trajectory record schema')
            if type(record['t']) not in (int,float) or not math.isfinite(record['t']):fail('nonfinite or invalid record time')
            if not isinstance(record['state'],list) or len(record['state'])!=dim or any(type(v) not in (int,float) or not math.isfinite(v) or v<0 for v in record['state']):fail('nonfinite, negative or malformed state')
        if records[0]!= {'t':0.0,'segment':'initial','state':initial}:fail('initial state must match exact admitted study')
        if not is_euler:
            if type(result['products']) is not int or not 0<=result['products']<=POLICY['max_reference_products']:fail('reference work budget')
            if not isinstance(result['capacity_events'],list) or len(result['capacity_events'])>len(study['capture']):fail('reference capacity event list')
            seen=set()
            for event in result['capacity_events']:
                if not isinstance(event,dict) or set(event)!= {'capture','t','captured_kg','state'}:fail('reference capacity event schema')
                device=next((c for c in study['capture'] if c['id']==event['capture']),None)
                if device is None or event['capture'] in seen or arm!='OUTLET_CAPTURE':fail('reference capacity event identity')
                seen.add(event['capture'])
                if type(event['t']) not in (int,float) or not math.isfinite(event['t']) or not 0<=event['t']<=records[-1]['t']:fail('reference capacity event time')
                if type(event['captured_kg']) not in (int,float):fail('reference event mass type')
                close(event['captured_kg'],device['capacity']['value'],device['capacity']['value'],'reference capacity event',1e-10)
                if not isinstance(event['state'],list) or len(event['state'])!=dim or any(type(v) not in (int,float) or not math.isfinite(v) or v<0 for v in event['state']):fail('invalid reference event state')
                close(math.fsum(event['state'][layout.at('captured',device['id'],c)] for c in layout.classes),event['captured_kg'],device['capacity']['value'],'reference event state saturation',1e-10)
            if any(a['t']>b['t'] for a,b in zip(result['capacity_events'],result['capacity_events'][1:])):fail('reference event order')
        factor=study['source_factor']['value'] if arm=='SOURCE_REDUCTION' else 1.0
        cursor=1;offset=0.0;event_cursor=0
        active={c['id'] for c in study['capture'] if arm=='OUTLET_CAPTURE' and c['capacity']['value']>0 and c['fraction']['value']>0}
        for segment,coarse in zip(study['segments'],counts):
            count=coarse*level;duration=segment['duration']['value'];start_state=records[cursor-1]['state'];start_index=cursor-1
            for step in range(count):
                before=records[cursor-1];after=records[cursor];x=before['state'];y=after['state']
                expected_t=offset+duration*(step+1)/count
                if after['t']!=expected_t or after['segment']!=segment['id']:fail('time grid, segment identity or order mismatch')
                dt=after['t']-before['t']
                if dt<=0:fail('nonadvancing retained time')
                if not is_euler:
                    proof_x=x;proof_t=before['t'];events=result['capacity_events']
                    while event_cursor<len(events) and events[event_cursor]['t']<=after['t']:
                        event=events[event_cursor]
                        if event['t']<proof_t or event['capture'] not in active:fail('reference event continuity/activity')
                        try:certificate(study,segment,arm,active,proof_x,event['state'],event['t']-proof_t,8*math.ulp(max(event['t'],proof_t)))
                        except ValueError as exc:fail(str(exc))
                        proof_x=event['state'];proof_t=event['t'];active.remove(event['capture']);event_cursor+=1
                    try:certificate(study,segment,arm,active,proof_x,y,after['t']-proof_t,8*math.ulp(max(after['t'],proof_t)))
                    except ValueError as exc:fail(str(exc))
                change=[b-a for a,b in zip(x,y)]
                def amount(kind,entity,cls=None):return change[layout.at(kind,entity,cls)]
                def ledger_rounding(indices):return 16*math.fsum(math.ulp(x[i])+math.ulp(y[i]) for i in set(indices))
                for i,slot in enumerate(layout.slots):
                    if slot['kind'] not in ('mass','stored') and change[i]<-1e-9*mass_scale:fail('cumulative ledger decreased: '+slot['kind'])
                incoming={(n['id'],c):[] for n in study['nodes'] for c in layout.classes}
                outgoing={(n['id'],c):[] for n in study['nodes'] for c in layout.classes}
                for node in study['nodes']:
                    for cls in layout.classes:
                        source=segment['sources'][node['id']][cls]['value']*factor*dt
                        close(amount('source',node['id'],cls),source,max(abs(source),abs(y[layout.at('source',node['id'],cls)])),'source flux')
                        incoming[node['id'],cls].append(source)
                expected_capture={c['id']:{cls:0.0 for cls in layout.classes} for c in study['capture']}
                for edge in study['edges']:
                    water=segment['flows'][edge['id']]['value']*dt
                    close(amount('water',edge['id']),water,max(water,1e-12),'water edge flux',1e-10)
                    if edge['from']=='outside':
                        for cls in layout.classes:
                            close(y[layout.at('edge',edge['id'],cls)],0,abs(y[layout.at('edge',edge['id'],cls)]),'outside inflow has no implicit pollutant')
                            close(y[layout.at('escaped',edge['id'],cls)],0,abs(y[layout.at('escaped',edge['id'],cls)]),'outside inflow escaped mass')
                        continue
                    device=caps.get(edge['id']);raw={};candidate={}
                    for cls in study['classes']:
                        name=cls['id'];observed=amount('edge',edge['id'],name)
                        expected=segment['flows'][edge['id']]['value']*cls['mobility']['value']/node_map[edge['from']]['volume']['value']*x[layout.at('mass',edge['from'],name)]*dt
                        if is_euler:close(observed,expected,max(abs(expected),1e-300),'independent donor advection flux',1e-8,8*(math.ulp(y[layout.at('edge',edge['id'],name)])+math.ulp(x[layout.at('edge',edge['id'],name)])))
                        raw[name]=observed
                        candidate[name]=expected*device['fraction']['value'] if device and arm=='OUTLET_CAPTURE' else 0.0
                    multiplier=1.0
                    if device and is_euler:
                        requested=math.fsum(candidate.values())
                        already=math.fsum(x[layout.at('captured',device['id'],c)] for c in layout.classes)
                        capacity_left=max(0.0,device['capacity']['value']-already)
                        if requested:multiplier=min(1.0,capacity_left/requested)
                    for cls in layout.classes:
                        captured=amount('captured',device['id'],cls) if device else 0.0
                        if device:
                            if is_euler:close(captured,candidate[cls]*multiplier,max(abs(candidate[cls]*multiplier),abs(y[layout.at('captured',device['id'],cls)])),'independent finite-capacity capture')
                            elif arm!='OUTLET_CAPTURE':close(captured,0,abs(captured),'inactive capture')
                            if captured>raw[cls]+1e-9*max(raw[cls],captured):fail('capture exceeds donor transfer')
                            expected_capture[device['id']][cls]=captured
                        outgoing[edge['from'],cls].append(raw[cls])
                        delivered=raw[cls]-captured
                        if edge['to']=='outside':close(amount('escaped',edge['id'],cls),delivered,max(abs(delivered),abs(y[layout.at('escaped',edge['id'],cls)])),'outlet partition')
                        else:
                            incoming[edge['to'],cls].append(delivered)
                            close(amount('escaped',edge['id'],cls),0,abs(y[layout.at('escaped',edge['id'],cls)]),'internal edge cannot escape boundary')
                for cv in study['conversions']:
                    transferred=amount('converted',cv['id'])
                    if is_euler:close(transferred,x[layout.at('mass',cv['node'],cv['from_class'])]*cv['rate']['value']*dt,max(abs(transferred),abs(y[layout.at('converted',cv['id'])])),'class conversion rate')
                    outgoing[cv['node'],cv['from_class']].append(transferred);incoming[cv['node'],cv['to_class']].append(transferred)
                for device in study['capture']:
                    used=math.fsum(y[layout.at('captured',device['id'],c)] for c in layout.classes)
                    if used>device['capacity']['value']*(1+1e-10):fail('cumulative capture exceeds finite capacity')
                    for cls in layout.classes:
                        released=amount('released',device['id'],cls);leaked=amount('leaked',device['id'],cls)
                        stored=x[layout.at('stored',device['id'],cls)]
                        if is_euler:
                            close(released,stored*device['release_rate']['value']*dt,max(abs(released),abs(y[layout.at('released',device['id'],cls)])),'storage release rate')
                            close(leaked,stored*device['leak_rate']['value']*dt,max(abs(leaked),abs(y[layout.at('leaked',device['id'],cls)])),'storage leakage rate')
                        close(amount('stored',device['id'],cls),expected_capture[device['id']][cls]-released-leaked,max(abs(stored),abs(y[layout.at('stored',device['id'],cls)]),abs(expected_capture[device['id']][cls]),abs(released),abs(leaked)),'storage interval balance',rounding=ledger_rounding([layout.at(k,device['id'],cls) for k in ('captured','released','leaked','stored')]))
                        close(amount('unknown',device['id'],cls),released,max(abs(released),abs(y[layout.at('unknown',device['id'],cls)])),'terminal unknown custody')
                        incoming[device['leak_destination'],cls].append(leaked)
                for node in study['nodes']:
                    for cls in layout.classes:
                        expected=math.fsum(incoming[node['id'],cls])-math.fsum(outgoing[node['id'],cls])
                        slots=[layout.at('source',node['id'],cls),layout.at('mass',node['id'],cls)]
                        slots.extend(layout.at('edge',e['id'],cls) for e in study['edges'] if node['id'] in (e['from'],e['to']))
                        slots.extend(layout.at('captured',c['id'],cls) for c in study['capture'] if next(e for e in study['edges'] if e['id']==c['edge'])['to']==node['id'])
                        slots.extend(layout.at('converted',cv['id']) for cv in study['conversions'] if cv['node']==node['id'] and cls in (cv['from_class'],cv['to_class']))
                        slots.extend(layout.at('leaked',c['id'],cls) for c in study['capture'] if c['leak_destination']==node['id'])
                        close(amount('mass',node['id'],cls),expected,max(abs(x[layout.at('mass',node['id'],cls)]),abs(y[layout.at('mass',node['id'],cls)]),math.fsum(incoming[node['id'],cls]),math.fsum(outgoing[node['id'],cls])),'compartment/class interval balance',rounding=ledger_rounding(slots))
                for cls in layout.classes:
                    supply=math.fsum(initial[i] for i in layout.indices('mass',cls))+math.fsum(y[i] for i in layout.indices('source',cls))
                    net_conversion=math.fsum(y[layout.at('converted',cv['id'])]*(1 if cv['to_class']==cls else -1 if cv['from_class']==cls else 0) for cv in study['conversions'])
                    stock=math.fsum(y[i] for kind in ('mass','stored','unknown','escaped') for i in layout.indices(kind,cls))
                    close(stock,supply+net_conversion,max(abs(supply),abs(net_conversion),1e-300),'global class/custody balance')
                cursor+=1
            final=records[cursor-1]['state']
            for node in study['nodes']:
                water_in=math.fsum(final[layout.at('water',e['id'])]-start_state[layout.at('water',e['id'])] for e in study['edges'] if e['to']==node['id'])
                water_out=math.fsum(final[layout.at('water',e['id'])]-start_state[layout.at('water',e['id'])] for e in study['edges'] if e['from']==node['id'])
                close(water_in,water_out,max(water_in,water_out,1e-12),'fixed-volume compartment water balance',1e-10)
                water_ledgers.append({'method':result['method'],'arm':arm,'refinement':level,'segment':segment['id'],'node':node['id'],'opening_m3':node['volume']['value'],'in_m3':water_in,'out_m3':water_out,'closing_m3':node['volume']['value'],'residual_m3':water_in-water_out})
            source=math.fsum(final[i] for i in layout.indices('source'))
            terms={kind:math.fsum(final[i] for i in layout.indices(kind)) for kind in ('mass','stored','unknown','escaped')}
            residual=initial_total+source-math.fsum(terms.values());close(residual,0,mass_scale,'whole-domain mass balance')
            mass_ledgers.append({'method':result['method'],'arm':arm,'refinement':level,'segment':segment['id'],'initial_kg':initial_total,'source_kg':source,**{k+'_kg':v for k,v in terms.items()},'residual_kg':residual})
            offset+=duration
        if not is_euler and event_cursor!=len(result['capacity_events']):fail('unconsumed reference capacity event')
        final=records[-1]['state']
        totals={kind+'_kg':math.fsum(final[i] for i in layout.indices(kind)) for kind in ('mass','stored','unknown','escaped','source','captured','released','leaked')}
        resources=[]
        for device in study['capture']:
            handled=math.fsum(final[layout.at(kind,device['id'],c)] for kind in ('captured','released','leaked') for c in layout.classes)
            resources.append({'capture':device['id'],'basis':'wholly_synthetic_handling_assumption','handled_kg':handled,'kWh':handled*device['energy']['value'] if device['energy'] is not None else None,'status':'SYNTHETIC_ASSUMPTION' if device['energy'] is not None else 'NOT_EVALUATED'})
        summaries.append({'method':result['method'],'arm':arm,'refinement':level,**totals,'prevented_source_kg':base_source*(1-factor),'resources':resources})
    diagnostics=[];ref_by_arm={r['arm']:r for r in references}
    for arm in ARMS:
        ref=ref_by_arm[arm];ref_times={r['t']:r['state'] for r in ref['records']};errors=[]
        for run in [r for r in numerical if r['arm']==arm]:
            error=0.0
            for rec in run['records']:
                if rec['t'] not in ref_times:fail('unaligned reference time grid')
                error=max(error,max((abs(a-b) for i,(a,b) in enumerate(zip(rec['state'],ref_times[rec['t']])) if layout.slots[i]['unit']=='kg'),default=0.0))
            errors.append(error)
        ratio=errors[-1]/errors[0] if errors[0]>1e-9*mass_scale else None
        if errors[-1]>POLICY['fine_error_fraction']*mass_scale:fail('finest numerical/reference error exceeds frozen bound')
        if ratio is not None and ratio>POLICY['fine_coarse_ratio']:fail('numerical refinement does not meet frozen contraction gate')
        diagnostics.append({'arm':arm,'max_error_kg_by_level':errors,'fine_coarse_ratio':ratio,'rounding_floor_kg':1e-9*mass_scale,'fine_bound_kg':POLICY['fine_error_fraction']*mass_scale})
    def escaped(arm,method,level):return next(s['escaped_kg'] for s in summaries if s['arm']==arm and s['method']==method and s['refinement']==level)
    comparisons=[]
    for a,b in itertools.combinations(ARMS,2):
        differences=[escaped(a,'conservative_euler',level)-escaped(b,'conservative_euler',level) for level in POLICY['refinements']]
        differences.append(escaped(a,'affine_exponential_reference',4)-escaped(b,'affine_exponential_reference',4))
        signs={1 if d>1e-9*mass_scale else -1 if d<-1e-9*mass_scale else 0 for d in differences}
        comparisons.append({'arms':[a,b],'quantity':'escaped_kg','differences':differences,'status':'ORDER_STABLE_IN_TESTED_GRIDS' if len(signs)==1 else 'UNRESOLVED_NUMERICAL_ORDER'})
    return {'status':'VALID_SYNTHETIC_COMPARISON','applicability':'A0_KNOWN_ANSWER','claims':BENEFITS.copy(),
            'summaries':summaries,'mass_ledgers':mass_ledgers,'water_ledgers':water_ledgers,'refinement':diagnostics,'comparisons':comparisons}

def evaluate(study,numerical,references):
    try:return _evaluate(study,numerical,references)
    except (TypeError,KeyError,IndexError,OverflowError) as exc:
        raise NetworkEvaluationError('malformed or numerically unrepresentable retained network evidence') from exc
