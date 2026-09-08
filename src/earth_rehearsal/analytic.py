"""Independent closed-form solution of a piecewise mixed reservoir.

Original implementation, AGPL-3.0-only. This module has no numerical-kernel import.
"""
from __future__ import annotations

import math


def interval(m0, source_rate, q, volume, duration):
    """Return exact closing stock and integrated outlet mass in kilograms."""
    if duration == 0:
        return float(m0), 0.0
    x = q / volume * duration
    a = -math.expm1(-x)
    phi = a / x if x else 1.0
    if x < 1e-4:
        psi = x * (0.5 + x * (-1 / 6 + x * (1 / 24 + x * (-1 / 120 + x / 720))))
    else:
        psi = 1.0 - phi
    stock = m0 * math.exp(-x) + source_rate * duration * phi
    outlet = m0 * a + source_rate * duration * psi
    return stock, outlet


def trajectory(study, arm, times):
    """Evaluate requested global times without stepping a numerical integrator."""
    factor = study['source_factor'] if arm == 'SOURCE_REDUCTION' else 1.0
    capture = study['capture_fraction'] if arm == 'OUTLET_CAPTURE' else 0.0
    volume = study['volume']['value']
    rows = []
    duration = sum(s['duration']['value'] for s in study['segments'])
    for time in times:
        if not 0 <= time <= duration:
            raise ValueError('analytic time outside study')
        mass = study['initial_mass']['value']
        outlet = 0.0
        start = 0.0
        for seg in study['segments']:
            elapsed = min(max(time - start, 0.0), seg['duration']['value'])
            mass, flow = interval(mass, seg['source']['value'] * factor,
                                  seg['outflow']['value'], volume, elapsed)
            outlet += flow
            start += seg['duration']['value']
            if time <= start:
                break
        rows.append({'time_s': time, 'mass_kg': mass,
                     'escaped_kg': outlet * (1 - capture), 'captured_kg': outlet * capture})
    return rows
