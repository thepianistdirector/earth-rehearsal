"""Versioned source declarations, missingness and reproducible transformations.

These checks preserve declared rights and provenance; they do not issue legal rights.
"""
from __future__ import annotations
import copy
import hashlib
import json
import re
from urllib.parse import urlparse

class SourceError(ValueError): pass
ID=re.compile(r'[A-Za-z][A-Za-z0-9_-]{0,47}\Z')
UNITS={'1','kg','m3','m3/s','kg/s','s','1/s','kWh/kg'}

def canonical(value):
    try:return json.dumps(value,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
    except (ValueError,TypeError,RecursionError) as exc:raise SourceError('source: noncanonical value') from exc

def digest(value):return hashlib.sha256(canonical(value)).hexdigest()
def _keys(obj,keys,where):
    if not isinstance(obj,dict) or set(obj)!=set(keys):raise SourceError(where+': expected exactly '+', '.join(keys))
def _strings(values,where):
    if not isinstance(values,list) or len(values)>64 or any(not isinstance(v,str) or not v.strip() or len(v)>500 for v in values):raise SourceError(where+': bounded nonempty strings required')

def validate_record(record):
    _keys(record,('id','kind','title','provider','url','version','license','rights','coverage','values','quality_flags','missing_variables','transforms','content_sha256'),'source')
    if not isinstance(record['id'],str) or not ID.fullmatch(record['id']):raise SourceError('source.id: invalid identifier')
    if not isinstance(record['kind'],str) or record['kind'] not in ('wholly_synthetic','observed','derived'):raise SourceError('source.kind: unknown classification')
    for key in ('title','provider','version','license'):
        if not isinstance(record[key],str) or not record[key].strip() or len(record[key])>500:raise SourceError('source.'+key+': bounded text required')
    if not isinstance(record['url'],str) or len(record['url'])>1000:raise SourceError('source.url: canonical public URL required')
    url=urlparse(record['url'])
    if url.scheme!='https' or not url.hostname or url.username or url.password:raise SourceError('source.url: HTTPS URL without credentials required')
    _keys(record['rights'],('use','derivatives','redistribution'),'source.rights')
    if any(type(v) is not bool for v in record['rights'].values()):raise SourceError('source.rights: explicit Booleans required')
    _keys(record['coverage'],('spatial','temporal','coordinate_reference','resolution'),'source.coverage')
    if any(not isinstance(v,str) or not v.strip() or len(v)>500 for v in record['coverage'].values()):raise SourceError('source.coverage: every support field is required')
    _strings(record['quality_flags'],'source.quality_flags');_strings(record['missing_variables'],'source.missing_variables')
    values=record['values']
    if not isinstance(values,dict) or not 1<=len(values)<=512:raise SourceError('source.values: 1..512 declared variables required')
    import math
    for name,item in values.items():
        if not isinstance(name,str) or not ID.fullmatch(name):raise SourceError('source.values: invalid variable identifier')
        _keys(item,('value','unit','quality_flags'),'source.values.'+name)
        if not isinstance(item['unit'],str) or item['unit'] not in UNITS:raise SourceError('source.values.'+name+': unsupported unit')
        value=item['value']
        if value is not None:
            if type(value) not in (int,float):raise SourceError('source.values.'+name+': finite number or explicit null required')
            try:ok=math.isfinite(value) and abs(value)<=1e12
            except OverflowError:ok=False
            if not ok:raise SourceError('source.values.'+name+': finite bounded number required')
        elif name not in record['missing_variables']:raise SourceError('source.values.'+name+': null must retain explicit missing-variable status')
        _strings(item['quality_flags'],'source.values.'+name+'.quality_flags')
    if any(name not in values or values[name]['value'] is not None for name in record['missing_variables']):raise SourceError('source.missing_variables: must identify actual null values')
    if len(record['missing_variables'])!=len(set(record['missing_variables'])):raise SourceError('source.missing_variables: duplicates')
    if not isinstance(record['transforms'],list) or len(record['transforms'])>32:raise SourceError('source.transforms: bounded ordered records required')
    for transform in record['transforms']:
        _keys(transform,('parent_sha256','operation','variable','operand','output_sha256'),'source.transform')
        if transform['operation'] not in ('scale','set') or not isinstance(transform['variable'],str) or transform['variable'] not in values:raise SourceError('source.transform: unsupported operation or variable')
        if type(transform['operand']) not in (int,float) or not math.isfinite(transform['operand']) or abs(transform['operand'])>1e6:raise SourceError('source.transform.operand: finite bounded factor required')
        for field in ('parent_sha256','output_sha256'):
            if not isinstance(transform[field],str) or not re.fullmatch('[0-9a-f]{64}',transform[field]):raise SourceError('source.transform: SHA-256 required')
    if record['content_sha256']!=digest(values):raise SourceError('source.content_sha256: variable bytes do not match')
    if record['transforms'] and record['transforms'][-1]['output_sha256']!=record['content_sha256']:raise SourceError('source.transforms: terminal output does not match current variables')
    for previous,current in zip(record['transforms'],record['transforms'][1:]):
        if previous['output_sha256']!=current['parent_sha256']:raise SourceError('source.transforms: broken ordered parent chain')
    return record

def validate_catalog(records, *, require_redistribution=False, synthetic_only=False):
    if not isinstance(records,list) or not 1<=len(records)<=16:raise SourceError('source_records: 1..16 records required')
    seen=set()
    for record in records:
        validate_record(record)
        if record['id'] in seen:raise SourceError('source_records: duplicate identity')
        seen.add(record['id'])
        if not record['rights']['use']:raise SourceError('source.rights: use is blocked')
        if require_redistribution and not record['rights']['redistribution']:raise SourceError('source.rights: redistribution is blocked')
        if synthetic_only and record['kind']!='wholly_synthetic':raise SourceError('source.kind: this manufactured fixture admits wholly synthetic quantities only')
    return {r['id']:r for r in records}

def scale_record(record,variable,factor):
    validate_record(record)
    import math
    if type(factor) not in (int,float) or not math.isfinite(factor) or abs(factor)>1e6:raise SourceError('factor: finite bounded number required')
    if variable not in record['values']:raise SourceError('unknown source variable')
    if not record['rights']['derivatives']:raise SourceError('source.rights: derivatives are blocked')
    result=copy.deepcopy(record);value=result['values'][variable]['value']
    if value is not None:result['values'][variable]['value']=value*factor
    result['version']=record['version']+'+scale'
    if record['kind']!='wholly_synthetic':result['kind']='derived'
    result['content_sha256']=digest(result['values'])
    result['transforms'].append({'parent_sha256':record['content_sha256'],'operation':'scale','variable':variable,'operand':factor,'output_sha256':result['content_sha256']})
    return validate_record(result)
