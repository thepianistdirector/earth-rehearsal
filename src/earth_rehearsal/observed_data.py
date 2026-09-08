"""Strict, offline USGS daily-discharge admission and descriptive calculations.

Raw observations keep their civil date, original precision, quality and source identity.
This module performs no environmental prediction or synthetic data substitution.
"""
from __future__ import annotations

from collections import Counter
from datetime import date, datetime, timedelta
from decimal import Decimal, InvalidOperation, localcontext
import hashlib
import json
import math
from pathlib import Path
import re
from urllib.parse import parse_qs, urlsplit

MAX_BYTES = 16_000_000
MAX_DAYS = 3660
POLICY = 'APPROVED_NOT_ESTIMATED_WITH_APPROVED_ESTIMATES_SENSITIVITY'
CFS_TO_SI = Decimal('0.028316846592')
TERMS = 'https://api.waterdata.usgs.gov/ogcapi/v0/?f=html'
SOURCE_KEYS = {'format', 'provider', 'kind', 'site_id', 'start_date', 'end_date',
               'parameter_code', 'statistic_id', 'original_unit', 'license',
               'terms_url', 'citation', 'retrievals', 'limitations'}
STUDY_KEYS = {'format', 'id', 'title', 'start_date', 'end_date', 'periods',
              'quality_policy', 'question', 'interpretation'}


class ObservationError(ValueError):
    """An unsupported, ambiguous, oversized or inconsistent observation input."""


def _fail(message):
    raise ObservationError(message)


def _text(value, label, maximum=500):
    if not isinstance(value, str) or not value.strip() or len(value) > maximum or any(ord(c) < 32 for c in value):
        _fail(label + ': expected bounded nonempty text')
    return value


def parse_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        _fail('daily support must be an explicit YYYY-MM-DD civil date, not a timestamp')
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ObservationError('invalid calendar date') from exc


def _timestamp(value):
    _text(value, 'source timestamp', 64)
    try:
        stamp = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if stamp.utcoffset() is None:
            _fail('source timestamp needs an explicit UTC offset')
    except ValueError as exc:
        raise ObservationError('invalid source timestamp') from exc


def date_range(start, end):
    first, last = parse_date(start), parse_date(end)
    count = (last-first).days+1
    if count < 1 or count > MAX_DAYS:
        _fail('date range must contain 1–3660 days')
    return [(first+timedelta(days=i)).isoformat() for i in range(count)]


def _pairs(pairs):
    output = {}
    for key, value in pairs:
        if key in output:
            _fail('duplicate JSON key: ' + key)
        output[key] = value
    return output


def decode(raw):
    if not isinstance(raw, bytes) or len(raw) > MAX_BYTES:
        _fail('raw observation file exceeds the 16 MB budget')
    try:
        return json.loads(raw, object_pairs_hook=_pairs,
                          parse_constant=lambda x: _fail('nonfinite JSON constant'))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as exc:
        raise ObservationError('malformed or excessively nested observation JSON') from exc


def read_bytes(path):
    path = Path(path)
    if path.is_symlink() or not path.is_file():
        _fail('source must be a regular, unlinked file: ' + path.name)
    if path.stat().st_size > MAX_BYTES:
        _fail('source file exceeds the 16 MB budget')
    with path.open('rb') as stream:
        raw = stream.read(MAX_BYTES+1)
    if len(raw) > MAX_BYTES:
        _fail('source file exceeds the 16 MB budget')
    return raw


def validate_study(study, source):
    if not isinstance(study, dict) or set(study) != STUDY_KEYS or study['format'] != 'earth-rehearsal-observed-study-v1':
        _fail('unsupported observed-study schema')
    for key, bound in [('id', 80), ('title', 180), ('question', 1000), ('interpretation', 1000)]:
        _text(study[key], key, bound)
    if not re.fullmatch(r'[A-Za-z0-9_-]+', study['id']):
        _fail('study identity must use letters, numbers, hyphens or underscores')
    dates = date_range(study['start_date'], study['end_date'])
    if dates[0] < source['start_date'] or dates[-1] > source['end_date']:
        _fail('study dates extend beyond the source request')
    if study['quality_policy'] != POLICY:
        _fail('unsupported observation quality policy')
    periods = study['periods']
    if not isinstance(periods, list) or len(periods) != 2:
        _fail('declare exactly two contiguous nonoverlapping comparison periods')
    ids, period_dates = set(), []
    for period in periods:
        if not isinstance(period, dict) or set(period) != {'id', 'start_date', 'end_date'}:
            _fail('invalid comparison-period schema')
        _text(period['id'], 'period identity', 80)
        if period['id'] in ids:
            _fail('duplicate period identity')
        ids.add(period['id'])
        period_dates += date_range(period['start_date'], period['end_date'])
    if period_dates != dates:
        _fail('comparison periods must partition the study dates in order, without gaps or overlaps')
    return study


def validate_source(source, daily_raw, site_raw):
    if not isinstance(source, dict) or set(source) != SOURCE_KEYS:
        _fail('unsupported source-record schema')
    expected = {'format': 'earth-rehearsal-usgs-source-v1', 'provider': 'U.S. Geological Survey',
                'kind': 'OBSERVED_DAILY_DISCHARGE', 'parameter_code': '00060',
                'statistic_id': '00003', 'original_unit': 'ft^3/s',
                'license': 'US-government-public-domain', 'terms_url': TERMS}
    if any(source[k] != v for k, v in expected.items()):
        _fail('source provider, kind, parameter, statistic, units or admitted terms do not match the USGS daily adapter')
    if not isinstance(source['site_id'], str) or not re.fullmatch(r'USGS-\d{8,15}', source['site_id']):
        _fail('invalid USGS monitoring-location identity')
    date_range(source['start_date'], source['end_date'])
    _text(source['citation'], 'attribution', 1200)
    if not isinstance(source['limitations'], list) or not 1 <= len(source['limitations']) <= 12:
        _fail('source limitations must be retained')
    for entry in source['limitations']:
        _text(entry, 'source limitation', 1200)
    retrievals = source['retrievals']
    if not isinstance(retrievals, dict) or set(retrievals) != {'daily', 'site'}:
        _fail('retain both daily and site retrievals')
    for kind, raw in [('daily', daily_raw), ('site', site_raw)]:
        item = retrievals[kind]
        if not isinstance(item, dict) or set(item) != {'url', 'bytes', 'sha256', 'retrieved_utc', 'authentication_used'}:
            _fail('invalid retrieval record')
        if type(item['bytes']) is not int or item['bytes'] != len(raw) or item['sha256'] != hashlib.sha256(raw).hexdigest():
            _fail(kind + ': source byte identity differs')
        if item['authentication_used'] is not False:
            _fail('this source adapter admits unauthenticated public retrievals only')
        _timestamp(item['retrieved_utc'])
        _text(item['url'], 'retrieval URL', 2000)
        url = urlsplit(item['url'])
        if url.scheme != 'https' or url.netloc != 'api.waterdata.usgs.gov' or url.fragment:
            _fail('source retrieval URL must identify the official public USGS API')
        query = parse_qs(url.query, keep_blank_values=True)
        if kind == 'daily':
            expected_query = {'f': ['json'], 'monitoring_location_id': [source['site_id']],
                              'parameter_code': ['00060'], 'statistic_id': ['00003'],
                              'datetime': [source['start_date']+'/'+source['end_date']]}
            if url.path != '/ogcapi/v0/collections/daily/items' or set(query) != set(expected_query) | {'limit'}:
                _fail('daily retrieval query is not the declared bounded selection')
            if any(query[k] != v for k, v in expected_query.items()) or query['limit'] != ['10000']:
                _fail('daily retrieval query differs from declared source selection')
        elif url.path != '/ogcapi/v0/collections/monitoring-locations/items/'+source['site_id'] or query != {'f': ['json']}:
            _fail('site metadata URL differs from the declared source')
    return source


def _point(obj):
    geometry = obj.get('geometry')
    if not isinstance(geometry, dict) or geometry.get('type') != 'Point':
        _fail('expected a point monitoring location')
    coords = geometry.get('coordinates')
    if not isinstance(coords, list) or len(coords) != 2 or any(type(x) not in (int, float) or not math.isfinite(x) for x in coords):
        _fail('invalid point coordinates')
    if not -180 <= coords[0] <= 180 or not -90 <= coords[1] <= 90:
        _fail('point coordinates outside longitude/latitude bounds')
    return coords


def normalize(source, daily_raw, site_raw):
    validate_source(source, daily_raw, site_raw)
    data, site = decode(daily_raw), decode(site_raw)
    if not isinstance(site, dict) or site.get('type') != 'Feature' or site.get('id') != source['site_id']:
        _fail('site metadata identity differs')
    meta = site.get('properties')
    if not isinstance(meta, dict) or meta.get('id') != source['site_id'] or meta.get('agency_code') != 'USGS':
        _fail('invalid site properties')
    name = _text(meta.get('monitoring_location_name'), 'monitoring location name', 250)
    timezone = _text(meta.get('time_zone_abbreviation'), 'station timezone metadata', 32)
    if meta.get('uses_daylight_savings') not in ('Y', 'N'):
        _fail('unknown station daylight-saving metadata')
    point = _point(site)
    if not isinstance(data, dict) or data.get('type') != 'FeatureCollection' or not isinstance(data.get('features'), list):
        _fail('expected a USGS GeoJSON feature collection')
    features = data['features']
    if not 1 <= len(features) <= MAX_DAYS:
        _fail('daily response must contain 1–3660 records')
    if type(data.get('numberReturned')) is not int or data['numberReturned'] != len(features):
        _fail('daily returned-row count differs')
    links = data.get('links')
    if not isinstance(links, list) or len(links) > 30 or any(not isinstance(link, dict) for link in links):
        _fail('invalid daily response links')
    if any(link.get('rel') == 'next' for link in links):
        _fail('paginated response is incomplete; narrow the date range and fetch a complete snapshot')
    if 'numberMatched' in data and (type(data['numberMatched']) is not int or data['numberMatched'] != len(features)):
        _fail('matched and returned counts differ; incomplete snapshot')
    _timestamp(data.get('timeStamp'))
    dates = date_range(source['start_date'], source['end_date'])
    rows, seen_ids, series_ids = {}, set(), set()
    for feature in features:
        if not isinstance(feature, dict) or feature.get('type') != 'Feature' or _point(feature) != point:
            _fail('feature geometry/type differs from the station')
        feature_id = _text(feature.get('id'), 'feature identity', 100)
        if feature_id in seen_ids:
            _fail('duplicate feature identity')
        seen_ids.add(feature_id)
        prop = feature.get('properties')
        required = {'time_series_id', 'monitoring_location_id', 'parameter_code', 'statistic_id', 'time', 'value', 'unit_of_measure', 'approval_status', 'qualifier', 'last_modified'}
        if not isinstance(prop, dict) or set(prop) != required:
            _fail('daily property schema changed; review the adapter before importing')
        for key, value in [('monitoring_location_id', source['site_id']), ('parameter_code', '00060'), ('statistic_id', '00003'), ('unit_of_measure', 'ft^3/s')]:
            if prop[key] != value:
                _fail('mixed or unexpected daily '+key)
        series_ids.add(_text(prop['time_series_id'], 'time-series identity', 100))
        if len(series_ids) != 1:
            _fail('multiple time-series identities; choose one unambiguous series')
        day = prop['time']
        parse_date(day)
        if not dates[0] <= day <= dates[-1]:
            _fail('daily observation lies outside the declared request')
        if day in rows:
            _fail('duplicate daily grain; no automatic deduplication')
        approval, qualifier = prop['approval_status'], prop['qualifier']
        if approval not in ('Approved', 'Provisional'):
            _fail('unknown approval semantics')
        qualifier = [] if qualifier is None else qualifier
        if not isinstance(qualifier, list) or len(qualifier) > 2 or any(not isinstance(q, str) or q not in ('ESTIMATED', 'REVISED') for q in qualifier) or len(set(qualifier)) != len(qualifier):
            _fail('unsupported qualifier semantics; preserve the response and review the adapter')
        _timestamp(prop['last_modified'])
        raw_value, si = prop['value'], None
        if raw_value is not None:
            if not isinstance(raw_value, str) or not re.fullmatch(r'[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?', raw_value) or len(raw_value) > 64:
                _fail('daily value must be a finite decimal string or explicit null')
            try:
                number = Decimal(raw_value)
                if not number.is_finite() or abs(number) > Decimal('1e12') or (number != 0 and abs(number) < Decimal('1e-100')):
                    _fail('daily value outside finite supported arithmetic range')
                with localcontext() as ctx:
                    ctx.prec = 80
                    si = float(number*CFS_TO_SI)
            except InvalidOperation as exc:
                raise ObservationError('invalid decimal observation') from exc
        if si is None:
            state = 'MISSING_VALUE'
        elif si < 0:
            state = 'NEGATIVE_OUTSIDE_SCOPE'
        elif approval != 'Approved':
            state = 'PROVISIONAL'
        elif 'ESTIMATED' in qualifier:
            state = 'ESTIMATED'
        else:
            state = 'ACCEPTED'
        rows[day] = {'date': day, 'record_id': feature_id, 'original_value': raw_value,
                     'flow_m3_s': si, 'approval': approval, 'qualifiers': sorted(qualifier),
                     'last_modified': prop['last_modified'], 'state': state,
                     'primary_included': state == 'ACCEPTED',
                     'sensitivity_included': state in ('ACCEPTED', 'ESTIMATED')}
    normalized = []
    for day in dates:
        normalized.append(rows.get(day, {'date': day, 'record_id': None, 'original_value': None,
                         'flow_m3_s': None, 'approval': None, 'qualifiers': [], 'last_modified': None,
                         'state': 'ABSENT_DATE', 'primary_included': False, 'sensitivity_included': False}))
    station = {'id': source['site_id'], 'name': name, 'coordinates': point,
               'coordinate_reference': 'OGC:CRS84', 'time_zone_abbreviation': timezone,
               'uses_daylight_savings': meta['uses_daylight_savings'],
               'support': 'One daily mean at a point station; civil date labels retained without UTC conversion.',
               'time_series_id': next(iter(series_ids))}
    return station, normalized


def quantile(values, p):
    values = sorted(values)
    if not values:
        return None
    position = (len(values)-1)*p
    left = int(position)
    right = min(left+1, len(values)-1)
    return values[left]+(values[right]-values[left])*(position-left)


def statistics(rows, flag='primary_included'):
    selected = [r['flow_m3_s'] for r in rows if r[flag]]
    n, days = len(selected), len(rows)
    return {'requested_days': days, 'accepted_days': n, 'excluded_days': days-n,
            'coverage_fraction': n/days if days else 0,
            'status': 'NO_ACCEPTED_OBSERVATIONS' if not n else ('COMPLETE_COVERAGE' if n == days else 'PARTIAL_COVERAGE'),
            'mean_m3_s': math.fsum(selected)/n if n else None,
            'min_daily_mean_m3_s': min(selected) if n else None,
            'p10_m3_s': quantile(selected, .1), 'median_m3_s': quantile(selected, .5),
            'p90_m3_s': quantile(selected, .9),
            'max_daily_mean_m3_s': max(selected) if n else None}


def analyze(study, station, rows):
    selected = [r for r in rows if study['start_date'] <= r['date'] <= study['end_date']]
    groups = [('whole_record', 'All dates', selected)]
    for year in sorted({r['date'][:4] for r in selected}):
        groups.append(('year', year, [r for r in selected if r['date'].startswith(year)]))
    for month in sorted({r['date'][:7] for r in selected}):
        groups.append(('month', month, [r for r in selected if r['date'].startswith(month)]))
    for period in study['periods']:
        groups.append(('period', period['id'], [r for r in selected if period['start_date'] <= r['date'] <= period['end_date']]))
    summaries = [{'kind': kind, 'id': label, 'start_date': data[0]['date'], 'end_date': data[-1]['date'],
                  'primary': statistics(data), 'with_approved_estimates': statistics(data, 'sensitivity_included')}
                 for kind, label, data in groups]
    periods = [s for s in summaries if s['kind'] == 'period']
    difference = {}
    for policy in ['primary', 'with_approved_estimates']:
        a, b = (p[policy]['mean_m3_s'] for p in periods)
        difference[policy] = {'first_period': periods[0]['id'], 'second_period': periods[1]['id'],
                              'mean_difference_m3_s': None if a is None or b is None else b-a,
                              'relative_difference_percent': None if a in (None, 0) or b is None else (b-a)/a*100}
    return {'format': 'earth-rehearsal-observed-summary-v1', 'study_id': study['id'],
            'classification': 'OBSERVED_DESCRIPTIVE', 'station': station, 'unit': 'm^3/s',
            'original_unit': 'ft^3/s', 'exact_unit_factor': str(CFS_TO_SI),
            'quality_policy': POLICY, 'requested_days': len(selected),
            'received_records': sum(r['record_id'] is not None for r in selected),
            'state_counts': dict(sorted(Counter(r['state'] for r in selected).items())),
            'overlapping_quality_counts': {q: sum(q in r['qualifiers'] for r in selected) for q in ('ESTIMATED', 'REVISED')},
            'approval_counts': dict(sorted(Counter(r['approval'] for r in selected if r['approval'] is not None).items())),
            'summaries': summaries, 'period_difference': difference,
            'quantile_method': 'Empirical quantile: linear interpolation at zero-based (n-1)*p; not an exceedance quantile.',
            'claims': {'observed_flow_description': 'SUPPORTED_WITH_RETAINED_QUALITY_FLAGS',
                       'causal_attribution': 'NOT_EVALUATED', 'climate_trend': 'NOT_EVALUATED',
                       'instantaneous_flood_peak': 'NOT_EVALUATED', 'pollutant_load': 'NOT_EVALUATED',
                       'intervention_effect': 'NOT_EVALUATED', 'human_or_qualified_review': 'NOT_OBSERVED'}}
