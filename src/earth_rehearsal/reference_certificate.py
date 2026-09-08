"""Local ODE residual certificates; never generate or replace a retained trajectory.

A degree-12 endpoint identity with a rigorous induced-norm remainder verifies
piecewise affine physics. Direct flux derivatives are independent of both kernels.
"""
import math
from .network_layout import Layout


def certificate(study, segment, arm, active, x, y, dt, time_error=0.0):
    layout=Layout(study); nodes={n['id']:n for n in study['nodes']}
    devices={c['edge']:c for c in study['capture']}
    factor=study['source_factor']['value'] if arm=='SOURCE_REDUCTION' else 1.0
    def derivative(v, forcing, absolute=False):
        d=[0.0]*len(v)
        def add(kind,entity,cls,value):d[layout.at(kind,entity,cls)]+=abs(value) if absolute else value
        for node in study['nodes']:
            for cls in layout.classes:
                flux=segment['sources'][node['id']][cls]['value']*factor if forcing else 0.0
                add('mass',node['id'],cls,flux);add('source',node['id'],cls,flux)
        for edge in study['edges']:
            flow=segment['flows'][edge['id']]['value']
            add('water',edge['id'],None,flow if forcing else 0.0)
            if edge['from']=='outside':continue
            device=devices.get(edge['id'])
            for cls in study['classes']:
                name=cls['id'];flux=flow*cls['mobility']['value']/nodes[edge['from']]['volume']['value']*v[layout.at('mass',edge['from'],name)]
                intercepted=flux*device['fraction']['value'] if device and device['id'] in active else 0.0
                add('mass',edge['from'],name,-flux);add('edge',edge['id'],name,flux)
                add('escaped' if edge['to']=='outside' else 'mass',edge['id'] if edge['to']=='outside' else edge['to'],name,flux-intercepted)
                if device:
                    add('captured',device['id'],name,intercepted);add('stored',device['id'],name,intercepted)
        for cv in study['conversions']:
            flux=v[layout.at('mass',cv['node'],cv['from_class'])]*cv['rate']['value']
            add('mass',cv['node'],cv['from_class'],-flux);add('mass',cv['node'],cv['to_class'],flux);add('converted',cv['id'],None,flux)
        for device in study['capture']:
            for cls in layout.classes:
                stock=v[layout.at('stored',device['id'],cls)]
                release=stock*device['release_rate']['value'];leak=stock*device['leak_rate']['value']
                add('stored',device['id'],cls,-release-leak);add('unknown',device['id'],cls,release)
                add('released',device['id'],cls,release);add('leaked',device['id'],cls,leak);add('mass',device['leak_destination'],cls,leak)
        return d
    # Four times the sum of physical transfer coefficients bounds every absolute
    # row sum, including capture partitions and cumulative diagnostic coordinates.
    rates=[segment['flows'][e['id']]['value']/nodes[e['from']]['volume']['value']*c['mobility']['value'] for e in study['edges'] if e['from']!='outside' for c in study['classes']]
    rates.extend(c['rate']['value'] for c in study['conversions'])
    rates.extend(c[k]['value'] for c in study['capture'] for k in ('release_rate','leak_rate'))
    norm=4*math.fsum(rates);z=norm*dt
    if dt<0 or z>16:raise ValueError('reference certificate interval exceeds admitted residual budget')
    first=derivative(x,True);term=[dt*v for v in first];columns=[[a,b] for a,b in zip(x,term)]
    bound=[abs(v) for v in term]
    for degree in range(2,13):
        bound=[dt/degree*v for v in derivative(bound,False,True)]
        term=[dt/degree*v for v in derivative(term,False)]
        for col,v in zip(columns,term):col.append(v)
    # Positive Taylor tail through degree 16 plus a valid uniform norm bound
    # on all later powers. Multiplying individual coordinates by exp(z)
    # would miss mass first reachable after degree 13.
    tails=[[] for _ in x]
    for degree in range(13,17):
        bound=[dt/degree*v for v in derivative(bound,False,True)]
        for col,v in zip(tails,bound):col.append(v)
    uniform=max(bound,default=0.0)*z/17*math.exp(z)
    bounds=[math.fsum(col)+uniform for col in tails]
    # Absolute event times are rounded separately from the producer's local
    # propagation duration. Bound their uncertainty by the endpoint rate scale.
    end_rate=derivative(y,True)
    time_bounds=[time_error*max(abs(a),abs(b))*math.exp(z) for a,b in zip(first,end_rate)]
    for i,(col,actual) in enumerate(zip(columns,y)):
        expected=math.fsum(col)
        rounding=256*math.ulp(max(abs(x[i]),abs(actual),math.fsum(abs(v) for v in col),1e-300))
        if abs(expected-actual)>bounds[i]+rounding+time_bounds[i]:
            raise ValueError('reference ODE residual failed for '+str(layout.slots[i]))
