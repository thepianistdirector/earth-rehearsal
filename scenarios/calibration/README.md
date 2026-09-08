# Original known-answer calibration controls

These files are **wholly synthetic**, authored for Earth Rehearsal under AGPL-3.0-only. They contain no field observations or fitted environmental constants.

The manufactured truth is source multiplier **0.5** and cumulative capture capacity **10 kg**. Development uses the default fictional dry/storm network and a dry-only variant. The reserved control uses shorter dry/storm intervals. Observations are final masses from the independent affine exponential implementation for prevention escape, capture storage and release to unknown fate.

The generator is [tools/manufacture_calibration.py](../../tools/manufacture_calibration.py). Its equations and input quantities originate in [CATCHMENT-001](../../docs/benchmarks/CATCHMENT-001.md). No external paper supplies these parameter values.

The frozen candidate grid includes source multiplier 0.3 with 10 kg capacity, 0.5 with 10 kg, 0.5 with 20 kg, and an intentionally invalid multiplier of 1.1. Capacities 10 and 20 kg do not bind in these controls, so their development predictions are equivalent. An invalid candidate remains in the denominator; neither it nor equivalent valid candidates can be discarded to assert identification.

Euler predictions differ slightly from the synthetic reference observations. The protocol fixes SSE in kg², equivalence tolerance 1e-12 kg² and confirmation maximum absolute residual 0.02 kg before fitting. Passing confirmation is a computational known-answer check. It does not establish field calibration, blinded testing, statistical independence or any environmental benefit.
