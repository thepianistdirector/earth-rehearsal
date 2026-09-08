"""Original normalized channel fixtures, explicitly synthetic and source-bound."""
from .sources import digest
from .network_study import validate,number


def channel(cells,*,volume=1000.0,flow=1.0,mass=1.0,duration=500.0):
    if type(cells) is not int or cells not in (1,2,4,8):raise ValueError('channel supports 1, 2, 4 or 8 cells')
    number(volume,8,1e6,'channel volume');number(flow,0,1000,'channel flow');number(mass,0,1e6,'channel initial mass');number(duration,.001,86400,'channel duration')
    values={};rid='manufactured_channel'
    def q(name,value,unit):
        values[name]={'value':value,'unit':unit,'quality_flags':[]}
        return {'value':value,'unit':unit,'source':{'record':rid,'variable':name}}
    names=['cell_'+str(i) for i in range(cells)]
    nodes=[{'id':n,'volume':q(n+'_volume',volume/cells,'m3'),'initial_mass':{'mobile':q(n+'_mass',mass/cells,'kg')},'position':{'x':.1+.8*(i+.5)/cells,'y':.5}} for i,n in enumerate(names)]
    edges=[{'id':'inflow','from':'outside','to':names[0]}]+[{'id':'edge_'+str(i),'from':names[i],'to':names[i+1]} for i in range(cells-1)]+[{'id':'outflow','from':names[-1],'to':'outside'}]
    study={'schema_version':1,'study':'CATCHMENT-001','study_version':'1.0.0','source_class':'wholly_synthetic','applicability':'A0_KNOWN_ANSWER','support':{'coordinate_reference':'LOCAL_SYNTHETIC','spatial_extent':'Normalized one-dimensional channel [0,1], equal-volume cells, identical total volume and boundary support across resolution levels.','temporal':'Relative seconds under a constant prescribed flow, uniform initial concentration and clean inlet.'},'classes':[{'id':'mobile','mobility':q('mobility',1,'1')}],'nodes':nodes,'edges':edges,'segments':[{'id':'channel','duration':q('duration',duration,'s'),'flows':{e['id']:q('flow_'+e['id'],flow,'m3/s') for e in edges},'sources':{n:{'mobile':q(n+'_source',0,'kg/s')} for n in names}}],'conversions':[],'capture':[],'source_factor':q('factor',.5,'1'),'omissions':['No hydraulic solution or real channel geometry','Uniform conservative scalar control, not a field pollutant','No real environmental or intervention benefit']}
    study['source_records']=[{'id':rid,'kind':'wholly_synthetic','title':'Original normalized donor-cell channel control','provider':'Lucas Santana / Earth Rehearsal','url':'https://github.com/thepianistdirector/earth-rehearsal','version':'CHANNEL-001/1.0.0','license':'AGPL-3.0-only','rights':{'use':True,'derivatives':True,'redistribution':True},'coverage':{'spatial':'Normalized [0,1] control domain, no geographic location','temporal':'Relative elapsed seconds','coordinate_reference':'LOCAL_SYNTHETIC','resolution':str(cells)+' equal-volume compartments'},'values':values,'quality_flags':['wholly synthetic computational parameters'],'missing_variables':[],'transforms':[],'content_sha256':digest(values)}]
    return validate(study)
