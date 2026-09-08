"""Separate decimal arithmetic check of descriptive metrics against raw observations."""
from decimal import Decimal, localcontext
from datetime import date, timedelta
import json
import math
from .observed_data import ObservationError


def verify_statistics(study, raw, summary):
    """Reconstruct groups directly from raw records without normalized rows/statistics()."""
    records = json.loads(raw)['features']
    boundaries = [(s['kind'], s['id'], s['start_date'], s['end_date']) for s in summary['summaries']]
    expected = [('whole_record', 'All dates', study['start_date'], study['end_date'])]
    first, last = date.fromisoformat(study['start_date']), date.fromisoformat(study['end_date'])
    for year in range(first.year, last.year+1):
        expected.append(('year', str(year), max(first, date(year, 1, 1)).isoformat(), min(last, date(year, 12, 31)).isoformat()))
    cursor = date(first.year, first.month, 1)
    while cursor <= last:
        following = date(cursor.year+1, 1, 1) if cursor.month == 12 else date(cursor.year, cursor.month+1, 1)
        expected.append(('month', cursor.strftime('%Y-%m'), max(cursor, first).isoformat(), min(last, following-timedelta(days=1)).isoformat()))
        cursor = following
    expected += [('period', p['id'], p['start_date'], p['end_date']) for p in study['periods']]
    if boundaries != expected:
        raise ObservationError('independent reference: group boundaries or denominator omitted')
    with localcontext() as ctx:
        ctx.prec = 80
        factor = Decimal('0.3048') ** 3
        for output in summary['summaries']:
            days = (date.fromisoformat(output['end_date'])-date.fromisoformat(output['start_date'])).days+1
            for label, estimated_allowed in [('primary', False), ('with_approved_estimates', True)]:
                values = []
                for feature in records:
                    prop = feature['properties']
                    if not output['start_date'] <= prop['time'] <= output['end_date']:
                        continue
                    if prop['value'] is None or prop['approval_status'] != 'Approved':
                        continue
                    qualifiers = prop['qualifier'] or []
                    if not estimated_allowed and 'ESTIMATED' in qualifiers:
                        continue
                    value = Decimal(prop['value'])
                    if value >= 0:
                        values.append(value*factor)
                values.sort()
                n = len(values)
                row = output[label]
                expected_state = 'NO_ACCEPTED_OBSERVATIONS' if not n else ('COMPLETE_COVERAGE' if n == days else 'PARTIAL_COVERAGE')
                if row['requested_days'] != days or row['accepted_days'] != n or row['excluded_days'] != days-n or row['status'] != expected_state:
                    raise ObservationError('independent reference: accepted/excluded denominator or coverage state differs')
                def percentile(numerator):
                    if not n:
                        return None
                    place = Decimal(n-1)*Decimal(numerator)/100
                    low = int(place)
                    high = min(low+1, n-1)
                    return values[low]*(1-(place-low))+values[high]*(place-low)
                reference = {'coverage_fraction': Decimal(n)/days,
                             'mean_m3_s': sum(values)/n if n else None,
                             'min_daily_mean_m3_s': values[0] if n else None,
                             'max_daily_mean_m3_s': values[-1] if n else None,
                             'p10_m3_s': percentile(10), 'median_m3_s': percentile(50), 'p90_m3_s': percentile(90)}
                for key, expected_value in reference.items():
                    actual = row[key]
                    if expected_value is None:
                        if actual is not None:
                            raise ObservationError('independent reference: empty metric must be null')
                    elif type(actual) not in (int, float) or not math.isclose(actual, float(expected_value), rel_tol=2e-12, abs_tol=5e-324):
                        raise ObservationError('independent raw/decimal reference differs: '+key)
    return {'method': 'Separate raw-record selection and Decimal arithmetic with independently derived unit conversion and group boundaries',
            'groups_checked': len(boundaries), 'policies_checked': 2,
            'relative_tolerance': 2e-12, 'absolute_tolerance': 5e-324,
            'scope': 'Computational agreement only; not independent measurements, field validation or author authentication.'}
