"""Shared serialization coordinates, without solver/evaluator physics."""
from __future__ import annotations

class Layout:
    def __init__(self,study):
        self.classes=[c['id'] for c in study['classes']]
        self.slots=[];self.index={}
        def add(kind,entity,cls=None,unit='kg'):
            self.index[(kind,entity,cls)]=len(self.slots)
            self.slots.append({'kind':kind,'entity':entity,'class':cls,'unit':unit})
        for kind,items in [('mass',study['nodes']),('stored',study['capture']),('unknown',study['capture']),('escaped',study['edges']),('source',study['nodes']),('captured',study['capture']),('released',study['capture']),('leaked',study['capture']),('edge',study['edges'])]:
            for item in items:
                for cls in self.classes:add(kind,item['id'],cls)
        for cv in study['conversions']:add('converted',cv['id'])
        for edge in study['edges']:add('water',edge['id'],unit='m3')
    def at(self,kind,entity,cls=None):return self.index[(kind,entity,cls)]
    def initial(self,study):
        state=[0.0]*len(self.slots)
        for node in study['nodes']:
            for cls in self.classes:state[self.at('mass',node['id'],cls)]=float(node['initial_mass'][cls]['value'])
        return state
    def indices(self,kind,cls=None):
        return [i for i,s in enumerate(self.slots) if s['kind']==kind and (cls is None or s['class']==cls)]
