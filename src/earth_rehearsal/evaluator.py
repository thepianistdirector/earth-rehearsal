"""Evaluator-owned reconstruction of BOX-001 physics, balances and custody."""
from __future__ import annotations

import math

from .analytic import interval
from .study import ARMS, BENEFITS, POLICY, controls, step_counts, validate


class EvaluationError(ValueError):
    """Raw evidence does not satisfy the frozen numerical contract."""


STEP_KEYS = ("segment", "index", "t_start_s", "t_end_s", "opening_mass_kg",
             "closing_mass_kg", "source_kg", "water_in_m3", "water_out_m3",
             "opening_volume_m3", "closing_volume_m3", "escaped_kg", "captured_kg")


def _keys(value, keys, where):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise EvaluationError(f"{where}: unexpected or missing fields")


def _number(value, where):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise EvaluationError(f"{where}: expected a finite nonnegative number")
    try:
        ok = math.isfinite(value) and value >= 0
    except OverflowError:
        ok = False
    if not ok:
        raise EvaluationError(f"{where}: expected a finite nonnegative number")
    return value


def _tol(scale):
    return POLICY["balance_relative_tolerance"] * max(1.0, scale)


def _close(actual, expected, scale, where):
    if abs(actual - expected) > _tol(scale):
        raise EvaluationError(f"{where}: mismatch ({actual!r} versus {expected!r})")


def _default(study):
    return (study["volume"]["value"] == 1000 and study["initial_mass"]["value"] == 0
            and study["source_factor"] == 0.5 and study["capture_fraction"] == 0.5
            and [(s["duration"]["value"], s["outflow"]["value"], s["source"]["value"])
                 for s in study["segments"]] == [(3600, .1, .001), (1800, .5, .003)])


def _run(study, run, counts):
    _keys(run, ("arm", "refinement", "steps", "custody", "claims"), "run")
    arm, refinement = run["arm"], run["refinement"]
    if not isinstance(arm, str) or arm not in ARMS:
        raise EvaluationError("unknown arm")
    if type(refinement) is not int or refinement not in POLICY["refinements"]:
        raise EvaluationError("invalid refinement")
    expected_count = sum(counts) * refinement
    if not isinstance(run["steps"], list) or len(run["steps"]) != expected_count:
        raise EvaluationError("missing or extra trajectory steps")
    _keys(run["claims"], BENEFITS, "claims")
    if any(run["claims"][key] != "NOT_EVALUATED" for key in BENEFITS):
        raise EvaluationError("unsupported disposal/lifecycle/ecological/health claim")

    volume = study["volume"]["value"]
    initial = study["initial_mass"]["value"]
    factor, capture = controls(study, arm)
    current = analytic_start = initial
    offset = 0.0
    cursor = 0
    bound = max_stock_error = max_outlet_error = max_comparison_bound = 0.0
    all_sources, all_escaped, all_captured, all_water_in, all_water_out = [], [], [], [], []
    analytic_outlets = []
    segments = []
    # Cumulative outlet has the same error bound as stock: source is exact in both paths.
    for seg, coarse_count in zip(study["segments"], counts):
        duration = seg["duration"]["value"]
        q, source = seg["outflow"]["value"], factor * seg["source"]["value"]
        k = q / volume
        count = coarse_count * refinement
        opening = current
        analytic_end, analytic_outlet = interval(analytic_start, source, q, volume, duration)
        sources, escaped, captured, water_in, water_out = [], [], [], [], []
        incoming_bound = bound
        prior_source_total = math.fsum(all_sources)
        cumulative_outlet = 0.0
        hmax = 0.0
        for index in range(count):
            row = run["steps"][cursor]
            cursor += 1
            _keys(row, STEP_KEYS, "step")
            if row["segment"] != seg["name"] or type(row["index"]) is not int or row["index"] != index:
                raise EvaluationError("step segment/index order mismatch")
            for key in STEP_KEYS[2:]:
                _number(row[key], key)
            start = offset + duration * index / count
            end = offset + duration * (index + 1) / count
            for key, expected in (("t_start_s", start), ("t_end_s", end)):
                if abs(row[key] - expected) > 8 * math.ulp(max(1.0, abs(expected))):
                    raise EvaluationError("step time grid mismatch")
            h = row["t_end_s"] - row["t_start_s"]
            if h <= 0 or k * h > POLICY["max_cfl"] * (1 + 1e-10):
                raise EvaluationError("nonadvancing or unstable time step")
            hmax = max(hmax, h)
            _close(row["opening_mass_kg"], current, current, "stock continuity")
            for key in ("opening_volume_m3", "closing_volume_m3"):
                _close(row[key], volume, volume, "fixed volume")
            _close(row["source_kg"], source * h, source * h, "source flux")
            for key in ("water_in_m3", "water_out_m3"):
                _close(row[key], q * h, q * h, "water flux")
            outlet = k * row["opening_mass_kg"] * h
            _close(row["escaped_kg"], (1 - capture) * outlet, outlet, "escaped outlet physics")
            _close(row["captured_kg"], capture * outlet, outlet, "captured outlet physics")
            residual = math.fsum((row["opening_mass_kg"], row["source_kg"],
                                  -row["closing_mass_kg"], -row["escaped_kg"], -row["captured_kg"]))
            _close(residual, 0, row["opening_mass_kg"] + row["source_kg"], "step mass balance")
            water_residual = math.fsum((row["opening_volume_m3"], row["water_in_m3"],
                                       -row["closing_volume_m3"], -row["water_out_m3"]))
            _close(water_residual, 0, volume + row["water_in_m3"], "step water balance")
            current = row["closing_mass_kg"]
            sources.append(row["source_kg"])
            escaped.append(row["escaped_kg"])
            captured.append(row["captured_kg"])
            water_in.append(row["water_in_m3"])
            water_out.append(row["water_out_m3"])
            elapsed = duration * (index + 1) / count
            exact_mass, exact_outlet = interval(analytic_start, source, q, volume, elapsed)
            point_bound = incoming_bound + elapsed * hmax * k * abs(source - k * analytic_start) / 2
            max_comparison_bound = max(max_comparison_bound, incoming_bound + point_bound)
            stock_error = abs(current - exact_mass)
            # Per-segment outflow differs by incoming minus current stock error.
            cumulative_outlet = math.fsum((cumulative_outlet, row["escaped_kg"], row["captured_kg"]))
            outlet_error = abs(cumulative_outlet - exact_outlet)
            scale = initial + prior_source_total + source * elapsed
            if stock_error > point_bound + _tol(scale):
                raise EvaluationError("analytic stock discrepancy exceeds a-priori bound")
            if outlet_error > incoming_bound + point_bound + _tol(scale):
                raise EvaluationError("analytic outlet discrepancy exceeds a-priori bound")
            max_stock_error = max(max_stock_error, stock_error)
            max_outlet_error = max(max_outlet_error, outlet_error)
        bound = incoming_bound + duration * hmax * k * abs(source - k * analytic_start) / 2
        totals = {"source_kg": math.fsum(sources), "escaped_kg": math.fsum(escaped),
                  "captured_kg": math.fsum(captured), "water_in_m3": math.fsum(water_in),
                  "water_out_m3": math.fsum(water_out)}
        residual = math.fsum((opening, totals["source_kg"], -current,
                              -totals["escaped_kg"], -totals["captured_kg"]))
        _close(residual, 0, opening + source * duration, "segment mass balance")
        _close(totals["source_kg"], source * duration, source * duration, "segment source total")
        segment_water_residual = totals["water_in_m3"] - totals["water_out_m3"]
        _close(segment_water_residual, 0, volume + totals["water_in_m3"], "segment water balance")
        segments.append({"segment": seg["name"], "opening_mass_kg": opening,
                         "closing_mass_kg": current, "analytic_final_mass_kg": analytic_end,
                         "analytic_outlet_kg": analytic_outlet, "mass_residual_kg": residual,
                         "water_residual_m3": segment_water_residual,
                         "mass_residual_normalized": residual / max(1.0, opening + source * duration),
                         "error_bound_kg": incoming_bound + bound, **totals})
        all_sources.extend(sources)
        all_escaped.extend(escaped)
        all_captured.extend(captured)
        all_water_in.extend(water_in)
        all_water_out.extend(water_out)
        analytic_outlets.append(analytic_outlet)
        analytic_start = analytic_end
        offset += duration

    source_total = math.fsum(all_sources)
    escaped_total, captured_total = math.fsum(all_escaped), math.fsum(all_captured)
    mass_residual = math.fsum((initial, source_total, -current, -escaped_total, -captured_total))
    water_in_total, water_out_total = math.fsum(all_water_in), math.fsum(all_water_out)
    water_residual = water_in_total - water_out_total
    _close(mass_residual, 0, initial + source_total, "run mass balance")
    _close(water_residual, 0, volume + water_in_total, "run water balance")
    custody = run["custody"]
    _keys(custody, ("transfers", "stored_kg", "destination_unknown_kg", "stored_throughput_kg"), "custody")
    for key in ("stored_kg", "destination_unknown_kg", "stored_throughput_kg"):
        _number(custody[key], key)
    transfers = custody["transfers"]
    capture_id = f'{arm}/{refinement}/capture-total'
    if not isinstance(transfers, list) or len(transfers) != 2:
        raise EvaluationError(f"missing custody transfer records for {capture_id}")
    for index, (transfer, (origin, destination)) in enumerate(zip(transfers, (("captured", "stored"), ("stored", "destination_unknown")))):
        _keys(transfer, ("id", "source_transfer_id", "from", "to", "mass_kg"), "custody transfer")
        expected_id = capture_id if index == 0 else f'{arm}/{refinement}/terminal-unknown'
        if transfer['id'] != expected_id or transfer['source_transfer_id'] != (None if index == 0 else capture_id):
            raise EvaluationError(f"custody transfer identity mismatch for {capture_id}")
        if transfer["from"] != origin or transfer["to"] != destination:
            raise EvaluationError("unsupported custody destination")
        _number(transfer["mass_kg"], "custody transfer mass")
        _close(transfer["mass_kg"], captured_total, captured_total, "custody transfer")
    if custody["stored_kg"] != 0:
        raise EvaluationError("terminal stored stock must be zero after transfer to unknown")
    for key in ("destination_unknown_kg", "stored_throughput_kg"):
        _close(custody[key], captured_total, captured_total, "custody stock/throughput")
    custody_residual = math.fsum((captured_total, -custody["stored_kg"], -custody["destination_unknown_kg"]))
    _close(custody_residual, 0, captured_total, "custody balance")
    return {"arm": arm, "refinement": refinement, "initial_mass_kg": initial,
            "source_kg": source_total, "final_mass_kg": current, "escaped_kg": escaped_total,
            "captured_kg": captured_total, "water_in_m3": water_in_total,
            "water_out_m3": water_out_total, "mass_residual_kg": mass_residual,
            "water_residual_m3": water_residual, "custody_residual_kg": custody_residual,
            "max_stock_error_kg": max_stock_error, "max_outlet_error_kg": max_outlet_error,
            "error_bound_kg": max_comparison_bound, "stock_error_bound_kg": bound,
            "mass_residual_normalized": mass_residual / max(1.0, initial + source_total),
            "water_residual_normalized": water_residual / max(1.0, volume + water_in_total),
            "custody_residual_normalized": custody_residual / max(1.0, captured_total),
            "analytic_final_mass_kg": analytic_start,
            "analytic_escaped_kg": (1 - capture) * math.fsum(analytic_outlets),
            "analytic_captured_kg": capture * math.fsum(analytic_outlets),
            "step_count": expected_count, "segments": segments}


def evaluate(study, runs):
    """Reject malformed evidence before exposing any comparison as valid."""
    try:
        validate(study)
    except ValueError as exc:
        raise EvaluationError(f"invalid accepted study: {exc}") from exc
    if not isinstance(runs, list) or len(runs) != len(ARMS) * 3:
        raise EvaluationError("expected exactly nine arm/refinement runs")
    counts = step_counts(study)
    summaries, seen = [], set()
    for run in runs:
        summary = _run(study, run, counts)
        key = (summary["arm"], summary["refinement"])
        if key in seen:
            raise EvaluationError("duplicate arm/refinement run")
        seen.add(key)
        summaries.append(summary)
    summaries.sort(key=lambda s: (ARMS.index(s["arm"]), s["refinement"]))
    refinement = []
    for arm in ARMS:
        levels = [s for s in summaries if s["arm"] == arm]
        floor = _tol(levels[0]["initial_mass_kg"] + levels[0]["source_kg"])
        item = {"arm": arm, "levels": [], "status": "REFINEMENT_VERIFIED"}
        for field in ("max_stock_error_kg", "max_outlet_error_kg"):
            errors = [s[field] for s in levels]
            if any(b > a + floor for a, b in zip(errors, errors[1:])):
                raise EvaluationError(f"{arm}: refinement increased {field}")
            ratio = errors[-1] / errors[0] if errors[0] > floor else None
            item[field + "_fine_coarse_ratio"] = ratio
            if _default(study) and ratio is not None and ratio > POLICY["default_fine_coarse_ratio_max"]:
                raise EvaluationError(f"{arm}: default refinement ratio failed")
        if max(levels[0]["max_stock_error_kg"], levels[0]["max_outlet_error_kg"]) <= floor:
            item["status"] = "ARITHMETIC_FLOOR_NO_OBSERVED_ORDER"
        item["levels"] = [{k: s[k] for k in ("refinement", "max_stock_error_kg", "max_outlet_error_kg", "error_bound_kg")} for s in levels]
        refinement.append(item)
    rankings = []
    for metric in ("final_mass_kg", "escaped_kg", "captured_kg"):
        signatures = []
        for level in POLICY["refinements"]:
            values = {s["arm"]: s[metric] for s in summaries if s["refinement"] == level}
            signature = []
            for i, arm in enumerate(ARMS):
                for other in ARMS[i + 1:]:
                    delta = values[arm] - values[other]
                    sign = 0 if abs(delta) <= _tol(max(values[arm], values[other])) else (1 if delta > 0 else -1)
                    signature.append(sign)
            signatures.append(signature)
        if any(1 in signs and -1 in signs for signs in zip(*signatures)):
            raise EvaluationError(f"ranking reversal: {metric}; signatures={signatures!r}")
        rankings.append({"metric": metric, "arm_order": list(ARMS), "refinements": list(POLICY["refinements"]), "pairwise_signatures": signatures})
    return {"summaries": summaries, "refinement": refinement, "ranking_reversals": [],
            "rankings": rankings, "valid": True}
