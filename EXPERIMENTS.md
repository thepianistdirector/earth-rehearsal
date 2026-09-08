# Earth Rehearsal experiment and evaluation contract

Current implementation: BOX-001 remains the preserved reservoir benchmark. v0.5 additionally implements [CATCHMENT-001](docs/benchmarks/CATCHMENT-001.md), [frozen campaign/confirmation decisions](docs/decisions/0005-study-campaigns.md) and [the executable study workflows](docs/STUDIES.md). All are original A0 manufactured controls; the later environmental experiments below retain their separate evidence gates.


Status: accepted architecture-foundation requirements; the narrow BOX-001 runtime now has local numerical and recovery evidence. Public release and human review remain pending; see STATUS.md.

## Research programme contract

The programme asks whether a declared intervention changes pollutant transport and downstream consequences within a bounded environmental model. Every study must define the system boundary, conserved quantities, comparison arms, applicability class, uncertainty sources, invalidity rules and harmful or negative outcomes before execution.

The first milestone is deliberately smaller than a watershed simulator: verify a hand-computable, well-mixed control volume and its accounting boundary. It creates the contract used later for a synthetic catchment. It does not represent a real river or establish intervention effectiveness.

## BOX-001: first analytic benchmark

### Purpose

Falsify errors in units, time integration, source/capture separation, mass custody and evaluator independence before spatial transport is attempted. This is `A0_KNOWN_ANSWER` evidence only.

### System

A fixed-volume, perfectly mixed reservoir has equal water inflow and outflow. One conservative pollutant enters at a constant mass rate during each forcing segment. There is no settling, resuspension, fragmentation, reaction, evaporation, groundwater exchange or spatial variability. Those exclusions are part of the case, not claims that the processes are negligible in nature.

For one interval with constant volume `V > 0`, outflow/inflow `Q > 0`, duration `t >= 0`, pollutant input `L >= 0`, and initial mass `M0 >= 0`:

```text
dM/dt = L - (Q / V) M
M(t) = M0 exp(-Qt/V) + (LV/Q) [1 - exp(-Qt/V)]
C(t) = M(t) / V
```

The interval water balance is zero because inflow equals outflow. Integrated pollutant accounting is:

```text
M0 + source_mass = M_end + escaped_mass + captured_mass + residual
```

The evaluator computes escaped and captured outflow by integrating the same accepted outlet flux over time or, for the analytic reference, from the exact stock balance. Numerical tolerances are proposed and justified during implementation from floating-point behavior and convergence; this plan invents no passing number.

BOX-001 rejects `Q = 0`; the quotient form above is outside its domain. A later closed-box case may specify and test the separate zero-flow solution `M(t) = M0 + Lt`, but an implementation must not reach it by division or silently substitute it into this fixture.

### Synthetic fixture

The scenario uses explicitly synthetic values chosen for easy independent calculation:

| Field | Dry segment | Storm segment | Meaning |
| --- | ---: | ---: | --- |
| Duration | `3600 s` | `1800 s` | Two piecewise-constant intervals |
| Reservoir volume | `1000 m3` | `1000 m3` | Fixed by matched inflow/outflow |
| Water flow | `0.10 m3/s` | `0.50 m3/s` | Synthetic forcing, not a site estimate |
| Pollutant source | `0.001 kg/s` | `0.003 kg/s` | Synthetic mass input |
| Initial mass | `0 kg` | Previous segment's end stock | Continuous state between intervals |

Three paired arms share the same forcing:

1. `BASELINE`: source multiplier `1`; no capture.
2. `SOURCE_REDUCTION`: source multiplier `0.5`; no capture. This factor is a computational fixture, not a claimed feasible reduction.
3. `OUTLET_CAPTURE`: source multiplier `1`; half of the pollutant mass crossing the outlet is transferred from `escaped` to `captured`. The capture fraction is a contract test value, not device performance.

Captured mass enters custody state `stored` and then `destination_unknown`. The benchmark may compare in-reservoir, escaped and captured mass. It must mark disposal completion, lifecycle benefit, ecological benefit and health benefit `NOT_EVALUATED`. Assigning captured mass directly to “removed” or “disposed” is the representative invalid fixture and must fail evaluation.

### Required artifacts and checks

- A human-readable scenario with every numeric value and unit above.
- An independently implemented analytic reference that evaluates both intervals and all arms.
- A numerical reference kernel using the same accepted contract, with timestep refinement reported rather than tuned to a hidden threshold.
- Water and pollutant ledgers for each interval and the full run.
- An evaluator-owned recomputation of residuals from raw inputs, states and fluxes.
- Failure fixtures for incompatible units, negative duration/source/initial mass, non-positive volume/flow, capture outside `[0, 1]`, missing terminal custody state and a perturbed output that breaks conservation.
- A result bundle that can be reproduced from a clean checkout using a single local command once the runtime exists.

The benchmark passes only when hand calculation, analytic reference and numerical output agree within a predeclared justified tolerance; conservation and invalid fixtures pass; repeated execution does not overwrite evidence; and the report states `A0_KNOWN_ANSWER`. A surprising or negative intervention result is retained. A numerical crash, missing output, budget violation or failed invariant is `INVALID` or `FAILED`, never a low or favorable score.

### Open dependencies before implementation

- Python and supported platform versions are not yet selected.
- No numerical, unit or schema dependency is approved; the first implementation should use the standard library unless a reviewed dependency is necessary.
- Pollutant particle classes and plausible parameter ranges belong to ER-001 and require literature plus a qualified freshwater-transport reviewer.
- The synthetic values above test accounting and solver behavior only. They require no calibration and must not be presented as representative of a catchment.
- No environmental modeler, waste/lifecycle reviewer, compute allocation or paid service is committed.

## Contract for later studies

### Inputs and rights

Use lawfully reusable public inputs or wholly synthetic fixtures. Record provider, canonical URL/DOI, access date, version or retrieval window, license/terms, attribution, redistribution and derivative permissions, coverage, quality flags, transformations and missing variables. Public availability does not imply permission to redistribute. Never download controlled data, copy private records or relabel real observations as synthetic.

### Before a run

Freeze the question, hypotheses, model/scenario/study versions, system and lifecycle boundaries, units, spatial/temporal supports, initial and boundary conditions, parameters, random seeds, baseline/candidates, metric direction, invalidity and falsification rules, uncertainty plan, calibration/confirmation split, evaluator version and resource envelope. Record the repository revision, engine environments, hardware, thread count and deterministic/stochastic settings.

Each intervention includes at least one adverse-outcome pathway relevant to its scope, such as downstream displacement, leakage, resuspension, flooding/backwater, waste burden, energy/emissions increase, habitat loss, water demand, inequitable heat exposure, rebound vulnerability or maladaptation. An omitted pathway is an explicit evidence gap, not zero harm.

### Calibration, identification and validation

Calibration is parameter estimation against named development evidence. Record adjustable parameters, bounds, objective, algorithm/budget, covariance or dependence, and an identifiability diagnostic appropriate to the model. If multiple parameter combinations explain the observations, report that ambiguity and restrict interpretation.

Validation evaluates frozen model choices against withheld observations or confirmation cases that were not used to tune parameters, choose candidates or change thresholds. Report what is being tested: implementation, numerical method, a process representation, transfer to another time/place, or a decision claim. Spatially or temporally adjacent samples are not independent merely because they are different rows.

### Uncertainty and comparison

1. Establish a transparent baseline and a known-answer or manufactured numerical control.
2. Use paired forcings and seeds when applicable. Predeclare repetitions from the estimand and variability; do not choose a sample count by habit.
3. Keep measurement/input, parameter, numerical, model-form, scenario and stochastic uncertainty distinguishable. Label structural unknowns rather than invent distributions.
4. Run timestep/grid/coupling refinement and supported parameter sensitivity before ranking. Report ranking reversals.
5. Include missing outputs, numerical errors, limit violations and failed jobs in the attempt record. Never remove unfavorable runs from the denominator.
6. Test at least one perturbation that should break each protected invariant and confirm the evaluator rejects it.
7. Search on development evidence only. Once a holdout influences a change, it becomes development evidence for the next study version.
8. Independently reproduce a selected result from the retained bundle before promoting a supported research finding.

### Result bundle and claim table

Include the accepted specification; scenario, source, model and evaluator records; baseline/candidate inputs; raw outputs; diagnostics/failures; quantities with units and support; conservation and custody ledgers; uncertainty components; resource use including failed attempts; environment; exact local reproduction command; and terminal state. Every report separates source fact, synthetic input, model assumption, simulation prediction, measured software performance and human interpretation.

Each proposed claim links supporting and contradicting evidence, applicability class, uncertainty, negative outcomes, reproduction state and reviewer decision. No generic score or agent summary may erase a failed quality constraint.

## Protected evaluator and stop rules

The hypothesis producer and proposal agent cannot change scoring code, accepted constraints, holdouts, raw outputs or evidence status. Evaluators recompute conservation and applicability gates from recorded artifacts. Preserve negative and inconclusive findings.

Stop ranking when mass or water does not close, results depend on unvalidated removal/fate constants, resolution or model-form choices reverse the ranking, provenance/rights are missing, the evaluator is compromised, or the approved budget is exhausted. Stop at synthetic/numerical evidence when calibration data or qualified reviewers are unavailable. No automatic escalation to a larger model, new dataset, paid provider, distributed system or physical deployment is allowed.

## Frozen narrow 0.1 execution policy

The owner-authorized BOX-001 runtime uses [the exact default fixture](scenarios/box-001.json) and [predeclared numerical policy BOX-EULER-1](docs/decisions/0002-numerical-policy.md). Computational bounds, interval clipping, independent analytic integration, step/refinement budgets, tolerances and invalidity rules were fixed before numerical execution. This is new mapped BOX work; original catchment and human-review acceptance remains unchanged.
