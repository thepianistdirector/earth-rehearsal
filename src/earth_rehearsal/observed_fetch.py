"""Explicit, bounded, public-only USGS retrieval; no network during analysis."""
from datetime import datetime, timezone, timedelta
import hashlib
import re
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, build_opener, HTTPRedirectHandler
from pathlib import Path
from .observed_data import MAX_BYTES, TERMS, POLICY, parse_date, date_range, normalize, validate_study, ObservationError
from .observed_bundle import write_json
from .bundle import atomic_write
from .study_archive import fresh

BASE = 'https://api.waterdata.usgs.gov/ogcapi/v0/collections/'


class _PublicRedirects(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        target = urlsplit(newurl)
        if target.scheme != 'https' or target.netloc != 'api.waterdata.usgs.gov':
            raise ObservationError('USGS request redirected outside the admitted public API')
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(site, start, end, split, output):
    if not isinstance(site, str) or not re.fullmatch(r'\d{8,15}', site):
        raise ObservationError('site must be a numeric USGS station identifier')
    dates = date_range(start, end)
    split_date = parse_date(split)
    if not start < split <= end:
        raise ObservationError('split date must follow the first day and lie within the request')
    site_id = 'USGS-'+site
    output = fresh(output)
    attempt = {'status': 'FETCHING', 'authentication_used': False, 'site': site_id,
               'start_date': start, 'end_date': end, 'requested_days': len(dates),
               'started_utc': datetime.now(timezone.utc).isoformat(), 'completed_requests': []}
    write_json(output/'fetch.json', attempt)
    query = urlencode({'f': 'json', 'monitoring_location_id': site_id, 'parameter_code': '00060',
                       'statistic_id': '00003', 'datetime': start+'/'+end, 'limit': '10000'})
    urls = {'site': BASE+'monitoring-locations/items/'+site_id+'?f=json', 'daily': BASE+'daily/items?'+query}
    retrievals, raw = {}, {}
    opener = build_opener(_PublicRedirects())
    try:
        for kind, url in urls.items():
            request = Request(url, headers={'User-Agent': 'EarthRehearsal-public-observed-study', 'Accept': 'application/json'})
            with opener.open(request, timeout=25) as response:
                if urlsplit(response.geturl()).netloc != 'api.waterdata.usgs.gov':
                    raise ObservationError('unexpected final response origin')
                content_length = response.headers.get('Content-Length')
                if content_length is not None and int(content_length) > MAX_BYTES:
                    raise ObservationError('USGS response exceeds the 16 MB limit')
                body = response.read(MAX_BYTES+1)
            if len(body) > MAX_BYTES:
                raise ObservationError('USGS response exceeds the 16 MB limit')
            raw[kind] = body
            atomic_write(output/(kind+'.json'), body)
            retrievals[kind] = {'url': url, 'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(),
                                'retrieved_utc': datetime.now(timezone.utc).isoformat(), 'authentication_used': False}
            attempt['completed_requests'].append(kind)
            write_json(output/'fetch.json', attempt)
        accessed = datetime.now(timezone.utc).date().isoformat()
        source = {'format': 'earth-rehearsal-usgs-source-v1', 'provider': 'U.S. Geological Survey',
                  'kind': 'OBSERVED_DAILY_DISCHARGE', 'site_id': site_id, 'start_date': start, 'end_date': end,
                  'parameter_code': '00060', 'statistic_id': '00003', 'original_unit': 'ft^3/s',
                  'license': 'US-government-public-domain', 'terms_url': TERMS,
                  'citation': f'U.S. Geological Survey, {accessed[:4]}, USGS Water Data for the Nation: National Water Information System database, accessed {accessed}, https://doi.org/10.5066/F7P55KJN. {site_id} daily mean discharge, {start} to {end}.',
                  'retrievals': retrievals,
                  'limitations': ['Daily mean at a point station; not instantaneous flow or a catchment spatial field.',
                                  'USGS quality/approval flags are retained; data may be revised.',
                                  'No pollutant, intervention, climate-trend, ecological or health inference is supported.']}
        study = {'format': 'earth-rehearsal-observed-study-v1', 'id': 'USGS-'+site+'-'+start+'-'+end,
                 'title': 'Observed daily flow at '+site_id, 'start_date': start, 'end_date': end,
                 'periods': [{'id': 'Before '+split, 'start_date': start, 'end_date': (split_date-timedelta(days=1)).isoformat()},
                             {'id': 'From '+split, 'start_date': split, 'end_date': end}],
                 'quality_policy': POLICY,
                 'question': 'How do observed daily-flow distributions and coverage differ between the two declared periods?',
                 'interpretation': 'Descriptive comparison only; no causal, climate-trend, flood-peak or intervention-effect claim.'}
        normalize(source, raw['daily'], raw['site'])
        validate_study(study, source)
        write_json(output/'source.json', source)
        write_json(output/'study.json', study)
        attempt['status'] = 'FETCHED_AND_ADMITTED'
        write_json(output/'fetch.json', attempt)
        return source
    except BaseException as exc:
        attempt.update(status='CANCELLED' if isinstance(exc, (KeyboardInterrupt, SystemExit)) else 'FAILED',
                       error=type(exc).__name__, message=str(exc))
        write_json(output/'fetch.json', attempt)
        raise
