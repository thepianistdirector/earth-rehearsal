"""Strict, bounded SI input contract. No implicit physical-model changes."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


class InvalidStudy(ValueError):
    """A study is outside the admitted BOX-001 contract."""


POLICY = {
    "id": "BOX-EULER-1",
    "coarse_step_s": 60.0,
    "max_cfl": 0.05,
    "refinements": [1, 2, 4],
    "max_steps_per_arm": 100000,
    "balance_relative_tolerance": 1e-10,
    "default_fine_coarse_ratio_max": 0.35,
}
ARMS = ("BASELINE", "SOURCE_REDUCTION", "OUTLET_CAPTURE")
BENEFITS = ("disposal", "lifecycle", "ecological", "health")


def exact_keys(value, keys, where):
    if not isinstance(value, dict) or set(value) != set(keys):
        raise InvalidStudy(f"{where}: expected exactly {', '.join(keys)}")


def number(value, lo, hi, where):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise InvalidStudy(f"{where}: expected a finite number")
    try:
        finite = math.isfinite(value)
    except OverflowError:
        finite = False
    if not finite or not lo <= value <= hi:
        raise InvalidStudy(f"{where}: expected a finite value in [{lo:g}, {hi:g}]")
    return float(value)


def quantity(value, unit, lo, hi, where):
    exact_keys(value, ("value", "unit"), where)
    if value["unit"] != unit:
        raise InvalidStudy(f"{where}: expected unit {unit}, got {value['unit']!r}")
    return number(value["value"], lo, hi, where)


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()


def identity(study):
    return hashlib.sha256(canonical(study)).hexdigest()


def step_counts(study):
    volume = study["volume"]["value"]
    counts = []
    offset = 0.0
    for seg in study["segments"]:
        duration = seg["duration"]["value"]
        step = min(POLICY["coarse_step_s"], POLICY["max_cfl"] * volume / seg["outflow"]["value"])
        count = max(1, math.ceil(duration / step)) if duration > 0 else 0
        if count and (duration / (4 * count) <= 0 or
                      offset + duration <= offset or
                      duration / (4 * count) < 2 * math.ulp(offset + duration)):
            raise InvalidStudy(f"{seg['name']}.duration: time grid cannot advance at binary64 precision")
        counts.append(count)
        offset += duration
    if sum(counts) * sum(POLICY["refinements"]) > POLICY["max_steps_per_arm"]:
        raise InvalidStudy("step budget exceeded: increase volume, reduce flow/duration, or keep the exact default fixture")
    return counts


def validate(study):
    exact_keys(study, ("schema_version", "study", "study_version", "source_class", "applicability", "volume", "initial_mass", "segments", "source_factor", "capture_fraction"), "study")
    for key, expected in (("schema_version", 1), ("study", "BOX-001"), ("study_version", "1.0.0"), ("source_class", "wholly_synthetic"), ("applicability", "A0_KNOWN_ANSWER")):
        if study[key] != expected or isinstance(study[key], bool):
            raise InvalidStudy(f"{key}: expected {expected!r}")
    quantity(study["volume"], "m3", 1, 1e6, "volume")
    quantity(study["initial_mass"], "kg", 0, 1e6, "initial_mass")
    number(study["source_factor"], 0, 1, "source_factor")
    number(study["capture_fraction"], 0, 1, "capture_fraction")
    if not isinstance(study["segments"], list) or len(study["segments"]) != 2:
        raise InvalidStudy("segments: expected exactly dry then storm")
    total = 0
    for seg, name in zip(study["segments"], ("dry", "storm")):
        exact_keys(seg, ("name", "duration", "inflow", "outflow", "source"), name)
        if seg["name"] != name:
            raise InvalidStudy(f"segments: expected {name}")
        total += quantity(seg["duration"], "s", 0, 86400, f"{name}.duration")
        incoming = quantity(seg["inflow"], "m3/s", 1e-6, 1e3, f"{name}.inflow")
        outgoing = quantity(seg["outflow"], "m3/s", 1e-6, 1e3, f"{name}.outflow")
        if incoming != outgoing:
            raise InvalidStudy(f"{name}: fixed volume requires equal inflow and outflow")
        quantity(seg["source"], "kg/s", 0, 1e3, f"{name}.source")
    if total <= 0:
        raise InvalidStudy("total duration must be positive")
    step_counts(study)
    return study


def _pairs(pairs):
    out = {}
    for key, value in pairs:
        if key in out:
            raise InvalidStudy(f"duplicate JSON key: {key}")
        out[key] = value
    return out


def read_json(path, max_bytes=64_000_000):
    path = Path(path)
    if path.stat().st_size > max_bytes:
        raise InvalidStudy("JSON input exceeds size budget")
    try:
        return json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=_pairs,
                          parse_constant=lambda value: (_ for _ in ()).throw(InvalidStudy(f"non-finite JSON value: {value}")))
    except (json.JSONDecodeError, UnicodeError, RecursionError) as exc:
        raise InvalidStudy(f"invalid JSON: {exc}") from exc


def load(path):
    return validate(read_json(path, max_bytes=64_000))


def controls(study, arm):
    if arm not in ARMS:
        raise InvalidStudy(f"unknown arm: {arm}")
    return (study["source_factor"] if arm == "SOURCE_REDUCTION" else 1.0,
            study["capture_fraction"] if arm == "OUTLET_CAPTURE" else 0.0)
