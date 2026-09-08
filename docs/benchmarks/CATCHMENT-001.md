# CATCHMENT-001: manufactured compartment transport

Contract frozen before implementation, September 8, 2026. Applicability: **A0_KNOWN_ANSWER**, wholly synthetic. This is a graph of prescribed-flow, well-mixed control volumes. It does not solve rainfall runoff, free-surface hydraulics, sediment mechanics, real microplastic fate or intervention effectiveness. BOX-001 remains a separate, unchanged fixture and format.

## States, forcing and boundaries

Each water compartment has a unique ID, a fixed positive volume in m3 and initial mass in kg for every declared conservative class. Class names are computational labels; no real size/density/shape claim follows. Each class has an explicitly synthetic advection multiplier in [0,1]. A multiplier of zero provides a retained-class control; it is not a field-derived settling model.

Directed edges connect named compartments or the explicit outside boundary. Each forcing segment supplies a nonnegative water flow in m3/s for every edge and a nonnegative external pollutant source in kg/s for every compartment/class. Outside inflows carry water only; any pollutant loading is separately recorded as a source. At every compartment and segment, incoming water flow must equal outgoing water flow. An isolated compartment is a separate closed-box accumulation case. Positive-duration segments must advance binary64 time. No automatic filling, unit conversion or zero substitution for missing data is permitted.

For compartment i and class c:

`dM[i,c]/dt = L[i,c] + sum(received edge mass flux) - sum(outgoing edge mass flux) + class-transfer inflow - class-transfer outflow + returned custody leakage`.

The donor edge mass flux is `Q[e] * mobility[c] * M[donor,c] / V[donor]`. Internal flux remains internal; outside outflow enters escaped mass. Computational class conversions have specified node, from/to class and synthetic first-order rate in 1/s. They conserve kg; no mass/count interchange or destruction is supported. Every conversion is retained as a ledger event. Unknown physical pathways remain explicitly unmodeled.

## Paired interventions and custody

Three arms share forcing, topology, classes and initial stocks. BASELINE has full source and zero capture. SOURCE_REDUCTION scales sources by the declared factor in [0,1], retaining prevented input as a comparison quantity, not captured waste. OUTLET_CAPTURE uses the full source and declared capture on named eligible edges, including internal edges. An internal capture reduces what the receiver obtains; capture at an outside edge partitions escaped flux. Donor water/pollutant outflow remains unchanged by capture.

Each capture device has fraction in [0,1], finite cumulative capture capacity in kg, and its own storage. Capacity is shared across classes, never restored by later storage release, and saturates explicitly. Numerical capture within a step is allocated proportionally to candidate class flux when capacity runs out. The independent reference locates the earliest capacity event and changes the linear operator at that event.

Stored material may release at a declared synthetic first-order rate into a named terminal destination, or leak at a declared rate back to one named modeled compartment. The terminal destination remains **destination_unknown**: it is a custody stock, not a disposal certificate. Cumulative capture, cumulative release and cumulative leakage are throughput records and are not added as separate terminal removal credits. The exact balance is initial mass plus source = modeled compartment stock plus storage stock plus terminal unknown stock plus escaped mass. Per-class balances additionally account for conversion inflow/outflow.

Resource factors in kWh/kg, when provided, are explicitly synthetic assumptions applied to retained handled quantities and reported separately. Missing resource factors remain NOT_EVALUATED, never zero. Disposal, lifecycle, ecology and health benefit remain NOT_EVALUATED for every arm, including zero capture.

## Independent methods and frozen numerical policy

Between forcing and capacity events the full state obeys an affine linear ODE. The reference evaluates its matrix-exponential action after augmenting with a constant coordinate and cumulative ledgers. The virtual constant coordinate is scaled to `1 + max(abs(forcing)) * segment_duration` in canonical numeric units; the affine recurrence is algebraically the same augmented action and avoids confusing a large water-flow value with stiffness. It uses an independently assembled sparse operator, a 24th-degree Taylor series and subintervals with infinity-norm times duration at most 0.25. In exact arithmetic the local remainder is bounded by `exp(0.25) * 0.25^25 / 25!` times the augmented-state norm. This is an original bounded implementation, not a claim to reproduce any external library's full algorithm. Binary64 and repeated propagation error are separately checked by closed-form scalar/chain controls and tolerance-bound conservation.

The numerical path constructs transfers directly from left-endpoint stocks with explicit Euler. It does not call the reference operator. Its timestep is at most 60 seconds and enforces total admitted donor-loss-rate times dt <= 0.025, including outgoing advection and class conversion; storage loss obeys the same bound. Three levels use n, 2n and 4n steps per segment. A fresh evaluation reconstructs the rates and all ledgers from retained input and numerical states.

Bounded admitted input: up to 8 compartments, 16 water edges, 3 classes, 8 conversion processes, 8 capture devices, 8 forcing segments; volume 1..1e6 m3; total modeled duration at most 86400 s. Per-arm sum of refinement steps is at most 40000; retained output and reference work have explicit bounds. Oversized studies reject before calculation. All numeric values must be finite non-Boolean numbers. IDs are bounded safe ASCII identifiers; duplicate or missing identities reject.

Arithmetic closure tolerance is `1e-9 * max(1 kg, initial + source throughput)` for whole-study mass, with corresponding interval/class scales and 1e-10 relative water closure. The default manufactured fixture must demonstrate first-order refinement: where coarse error exceeds the rounding floor, fine/coarse endpoint error ratio <= 0.6. Finest endpoint error must be <= 0.02 times the source-plus-initial-mass scale. Stationary/degenerate cases retain their actual error and do not invent an observed order. These are numerical contract bounds, not environmental plausibility or field-validation tolerances.

## Falsifiers and portable evidence

Test separate zero-flow accumulation, scalar decay/source, equal-rate two-compartment cascade and internal-exchange cancellation against independently derived closed forms. Include edge reversal, zero source, nonzero initial stock, forcing changes and synthetic class conversion. Demonstrate finite-capacity exhaustion, release/leakage and their conservation under both methods.

Independently reject a duplicated/dropped exchange, conserving-but-wrong source or advection flux, a missing class/compartment, incompatible units, unbalanced water boundaries, a capacity overrun, duplicated custody credit, wrong terminal fate, a changed result provenance or a benefit assertion. Failed evaluation cannot activate a successful bundle. Retain exact study, raw attempts, numerical and reference trajectories, local/global water/mass/class/custody ledgers, diagnostics, full CSV, offline report, source digest and environment. Fresh output directories, atomic final activation, inspect without rerunning either kernel, exact-version reproduction and explicit incomplete-state recovery are mandatory.

## Later analysis and evidence boundary

Parameter campaigns must predeclare admitted values/covariance, preserve all attempts and expose changes or reversals without invented probability claims. A spatial remap preserves integrated quantity while reporting interpolation error separately. A changed compartment discretization changes the model unless its physical support and boundary equivalence are declared; grid count alone cannot assert refinement.

Calibration and confirmation use versioned synthetic observations initially. Before tuning, freeze development/holdout hashes, candidate bounds, objective, algorithm/budget and thresholds. Record confounded fits honestly. Any holdout used to change a model or threshold is consumed into development evidence for the next version. Numerical/known-answer confirmation does not become environmental validation.

## Review correction: retained reference certification

Before accepting any reference interval, inspection now evaluates a separate direct-flux ODE endpoint identity of degree 12. For `x'=Ax+b`, its terms are `x`, `h(Ax+b)`, …, `h^12 A^11(Ax+b)/12!`. The positive absolute-derivative tail is accumulated for degrees 13 through 16; all later coordinates are bounded by `max(t16) * (||A||∞ h) / 17 * exp(||A||∞ h)`, where `t16` is the nonnegative degree-16 term. This uniform tail bound also covers coordinates first reachable after degree 13. A conservative row-norm bound, per-coordinate arithmetic allowance and event timestamp uncertainty are included. Cumulative flux differences include the ulps of both retained endpoints. This check imports neither trajectory generator, constructs no replacement trajectory, and covers every stock and cumulative flux. Its direct derivative has separately authored flux expressions. A labelled producer or self-reported work count does not prove independence; the residual certificate and closed-form controls support the stated computational claim.

Each capacity event retains its full state. Inspection partitions the enclosing interval at those states, verifies continuity, saturation against that device's capacity, chronological order and active-device transitions, and certifies both sides. Deleting an event cannot turn off capture. Positive capacities below 1e-9 kg are outside this computational contract; zero is supported as an inactive device. Even admitted events fail closed when their time or relative capacity cannot resolve at binary64 precision. Capacity overruns use a device-relative tolerance. Class conservation and donor transfer checks use their own quantities, preventing a large unrelated class from hiding total loss of a small class.

This is a documented correction to the preimplementation numerical validation contract, prompted by retained falsifiers. It makes no environmental applicability change.
