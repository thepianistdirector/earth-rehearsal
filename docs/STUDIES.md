# Synthetic study guide for v0.5

These workflows verify original manufactured controls. Their applicability remains `A0_KNOWN_ANSWER`; fitting and confirmation do not promote them to an environmental evidence level. The public release and independent platform verification are listed separately in [STATUS.md](../STATUS.md).

## Network study

`earth.py catchment` accepts the exact JSON grammar in [the default fixture](../scenarios/catchment-001.json). Each scalar has a value, SI unit and source-record/variable binding. Source records retain declared use/derivative/redistribution flags, variable hashes, coverage, explicit missing values and ordered transformation declarations. Editing through the API checks derivative permission and updates all aliases of the same variable. The parent values are not archived in a transformation record, so hashes establish declared chain linkage rather than replayable proof of every transformation.

Up to eight mixed compartments, sixteen directed edges, three conservative classes, eight conversions, eight capture devices and eight forcing intervals are admitted. Prescribed inflow/outflow must balance for every fixed-volume compartment. Outside inflow is clean water; pollutant inputs are explicit source rates. Class mobility and conversion rates are synthetic computational controls. Diagram coordinates have no geographic meaning.

Source prevention multiplies the declared sources. Capture intercepts a fraction on a named donor edge until a capacity shared across classes is exhausted. Capacity is cumulative and is not restored by release or leakage. Captured stock can remain stored, release to terminal unknown custody, or leak back into a named compartment. Handling energy is a separate synthetic assumption or `NOT_EVALUATED`.

Independent Euler and affine exponential implementations retain all stock and cumulative flux coordinates. Inspection reconstructs numerical rates, local/global water and mass, class balances and custody. A separate bounded ODE residual certificate verifies reference intervals and saved capacity-event states without generating a replacement trajectory. The [frozen benchmark and review corrections](benchmarks/CATCHMENT-001.md) give the equations, tolerances, reference limits and falsifiers.

Each arm uses coarse/medium/fine grids. Admission bounds total numerical work to 40000 steps per arm across refinements and retained arrays to two million scalars by the declared estimate. Reference work has its own one-million-product cap. Positive capacity below 1e-9 kg is outside computational resolution; an otherwise admitted event can still fail when its relative mass or timestamp is unresolvable. These are computational admission limits, not plausible environmental ranges.

## Explicit sensitivity campaign

A [campaign protocol](../scenarios/campaign-001.json) freezes a base study, source-bound parameter paths/units, ordered joint sample vectors, a dependence description and budgets before execution. Parameter paths cannot alias the same source variable. `ONE_AT_A_TIME` requires at most one changed parameter per case. Other supported classifications describe explicit joint samples or a scenario set. None implies probability or independence.

```sh
python3 earth.py campaign validate --protocol scenarios/campaign-001.json
python3 earth.py campaign run --protocol scenarios/campaign-001.json --out runs/campaign
python3 earth.py campaign inspect runs/campaign
python3 earth.py campaign reproduce runs/campaign --out runs/campaign-repeat
python3 earth.py campaign export runs/campaign --out runs/campaign-copy
```

The default has five valid samples and one intentional admission failure. All six remain in the denominator. The report compares all paired arm outcomes and reports ordering reversals across valid samples; an unresolved numerical order remains unresolved.

At most 32 samples and 120 seconds are admitted. Wall time is checked before cases and at network checkpoints, so an in-progress bounded numerical section can exceed the deadline before its next checkpoint. A protocol archive is bounded to 1024 files and 512 MiB at checkpoints/final sealing. These guards are not OS quotas. Cases are serial; no additional worker process or model service starts.

`INVALID` records failed study admission. `FAILED` retains available raw computation. `NOT_RUN_BUDGET` records the elapsed boundary or exhausted attempt count and has no child computation. No later sample resumes after exhaustion. An interrupted protocol has no completion marker and retains explicit unfinished statuses. A valid child directory cannot be relabelled unrun during inspection.

## Spatial and timestep controls

[The resolution protocol](../scenarios/resolution-001.json) constructs a normalized one-dimensional channel on `[0,1]`. The total volume, initial mass, prescribed flow and clean boundary are identical across 1, 2, 4 and 8 equal-volume cells. The continuous conservative front has mass `M0 * max(1 - Q*t/V, 0)` remaining. Its displacement must be between 0.1 and 0.8 of the domain for this frozen convergence control.

The report separates three quantities:

- Time error: Euler versus the independent reference for the same cell grid.
- Spatial error: that cell reference versus the continuous plug-flow control.
- Total error: Euler versus continuous plug flow; cancellation between errors is possible.

Passing requires spatial errors to decrease across all four grids and the fine/coarse ratio to be at most 0.6. This validates the manufactured control only. It is not a hydraulic or field-transport test.

Overlap remapping requires identical `[0,1]` support, strictly ordered source/target edges and one extensive mass per source cell. It assumes piecewise-constant cell averages. The mass residual and integrated absolute profile difference are separate. The default preserves 1 kg to rounding precision while changing the reconstructed profile by 0.4 kg in L1 distance.

## Frozen calibration and confirmation

The [default protocol](../scenarios/calibration/protocol.json) freezes development and holdout input studies, observable identities/units, candidate vectors, SSE loss in kg², an equivalence tolerance in kg² and a maximum confirmation residual in kg. The current schema calls these `equivalence_absolute` and `confirmation_max_abs`; their units are fixed by this contract. Up to eight candidates, four cases in each split and sixteen final-mass observables are admitted.

```sh
python3 earth.py calibration freeze --out runs/cohort
python3 earth.py calibration fit runs/cohort --out runs/fit
python3 earth.py calibration inspect runs/fit
python3 earth.py calibration confirm runs/cohort --fit runs/fit --out runs/confirmation
python3 earth.py calibration inspect runs/confirmation
```

Freezing sees and hashes both synthetic datasets. Fitting reads only the frozen protocol, development observations and optional lineage; it does not open or stat the holdout observations. The protocol may disclose holdout input conditions, and the data author knows the manufactured truth. This tests software separation, not human blinding.

Experimental support identity excludes source metadata, diagram positions and fitted parameter values. Giving the same controls another title or a different initial fitted value cannot make them a distinct holdout. Distinct input controls still do not establish statistical independence or field transfer.

Every candidate/case outcome is retained. Only candidates with complete valid development results enter SSE selection. Equivalent valid vectors within the frozen tolerance remain unresolved; the first in declared order is selected reproducibly. An incomplete grid remains `UNRESOLVED_INCOMPLETE_GRID`. A single best grid entry is not global identifiability.

A successful fit records its selection hash in the cohort's fit receipt. Before confirmation, that original receipt, the cohort and the complete fit evidence must agree. An exclusive operation lock prevents concurrent fitting/exposure. The exposure file is exclusively created and fsynced before the first holdout observation read. All scheduled confirmation cases already have attempt records at that point.

After exposure, further fitting against that cohort is refused, even if the read or calculation fails. Confirmation preserves selected parameters and thresholds. A failed threshold produces a completed protocol with `FAILED_FROZEN_SYNTHETIC_CONFIRMATION`; it is never silently tuned or removed.

## Replay and portable evidence

```sh
python3 earth.py calibration confirm runs/cohort --fit runs/fit --out runs/replay --replay
python3 earth.py calibration reproduce runs/fit --out runs/fit-replay
python3 earth.py calibration reproduce runs/confirmation --out runs/portable-replay
python3 earth.py calibration export runs/confirmation --out runs/confirmation-copy
```

An explicit confirmation replay must use the originally exposed selection. A portable confirmation contains the complete original development fit, selected values, cohort identity, holdout observations, access record, child results and thresholds. It can be reopened or reproduced without the mutable cohort directory.

Portable reproduction reruns completed computations with the matching source, preserves original failed/invalid/unrun attempts, checks identical physics and keeps the original selection. It is labelled `FROZEN_SELECTION_REPLAY`; it supplies no fresh holdout evidence. The replay marker and displayed mode must agree during inspection.

All successful network/protocol inspections verify exact artifact sets and hashes, reconstruct conclusions, and check CSV/HTML against that reconstruction. These are integrity and consistency checks. An author controlling all files can replace every identity and receipt; hashes are not signatures or proof of external authenticity.

## Consume an exposed holdout

To use previous holdout outcomes in further development, prepare a new protocol and observations. Keep every old development and holdout case, unchanged and in order, at the start of the new development split. Keep observable definitions. Give the new cohort a new identity and use distinct experimental controls for its new holdout.

```sh
python3 earth.py calibration consume runs/cohort \
  --protocol new-protocol.json \
  --development new-development.json \
  --holdout new-holdout.json \
  --out runs/new-cohort
```

The command verifies the old exposure, retains a lineage record naming the consumed holdout and freezes the new data. It does not modify the old cohort. This is a bounded software workflow; newly authored synthetic cases are not observations of nature.

## Recovery and platform scope

Every output directory is fresh. No CLI command overwrites completed evidence. Partial directories retain their protocol, attempts and completed raw children. Inspect rejects missing activation markers. Re-run a campaign/resolution protocol into a fresh directory, or use explicit confirmation replay after exposure. Preserve the partial attempt for the denominator and failure history.

Cohort locking uses POSIX `flock`, so this workflow targets verified Linux/macOS environments. Python 3.12 is the supported runtime line. Actual candidate and public-artifact evidence must identify the exact version and platform. Process interruption tests do not prove power-loss durability or universal filesystem behavior.
