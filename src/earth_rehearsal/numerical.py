"""Conservative explicit Euler kernel; does not call the analytic solution."""
from __future__ import annotations

import math

from .study import BENEFITS, POLICY, controls, step_counts, validate


def run_arm(study, arm, refinement):
    validate(study)
    if isinstance(refinement, bool) or refinement not in POLICY['refinements']:
        raise ValueError('unsupported refinement')
    factor, fraction = controls(study, arm)
    volume = float(study['volume']['value'])
    mass = float(study['initial_mass']['value'])
    steps = []
    start = 0.0
    for seg, base_count in zip(study['segments'], step_counts(study)):
        count = base_count * refinement
        duration = seg['duration']['value']
        q = seg['outflow']['value']
        rate = seg['source']['value'] * factor
        for i in range(count):
            t0 = start + duration * (i / count)
            t1 = start + duration * ((i + 1) / count)
            h = t1 - t0
            if h <= 0 or q * h / volume > POLICY['max_cfl'] * (1 + 1e-10):
                raise ValueError('time grid stalled or unstable; input is outside numerical support')
            source = rate * h
            outlet = (q / volume) * mass * h
            closing = mass + source - outlet
            if not math.isfinite(closing) or closing < 0:
                raise ValueError('invalid numerical stock')
            steps.append({
                'segment': seg['name'], 'index': i,
                't_start_s': t0, 't_end_s': t1,
                'opening_mass_kg': mass, 'closing_mass_kg': closing,
                'source_kg': source, 'water_in_m3': q * h, 'water_out_m3': q * h,
                'opening_volume_m3': volume, 'closing_volume_m3': volume,
                'escaped_kg': (1 - fraction) * outlet, 'captured_kg': fraction * outlet,
            })
            mass = closing
        start += duration
    captured = math.fsum(s['captured_kg'] for s in steps)
    capture_id = f'{arm}/{refinement}/capture-total'
    return {
        'arm': arm, 'refinement': refinement, 'steps': steps,
        'custody': {
            'transfers': [
                {'id': capture_id, 'source_transfer_id': None,
                 'from': 'captured', 'to': 'stored', 'mass_kg': captured},
                {'id': f'{arm}/{refinement}/terminal-unknown', 'source_transfer_id': capture_id,
                 'from': 'stored', 'to': 'destination_unknown', 'mass_kg': captured},
            ],
            'stored_kg': 0.0, 'destination_unknown_kg': captured,
            'stored_throughput_kg': captured,
        },
        'claims': {key: 'NOT_EVALUATED' for key in BENEFITS},
    }
