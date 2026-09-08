# TEMPORAL-CUSTODY-001: temporal exchange and capture-to-destination control

Initial contract frozen September 8, 2026, before implementation. This is a wholly synthetic known-answer control (`A0_KNOWN_ANSWER`), separate from USGS-DAILY-001 observations. It adds concrete temporal and downstream-custody behavior to the v1.0 workbench; it does not complete real freshwater-particle or lifecycle applicability contracts.

## Question and controlled alternatives

How much material enters, is prevented, escapes the stream, is captured and subsequently leaks or reaches a declared accounting destination when an ideal finite-capacity capture unit is serviced on a fixed schedule?

Three arms share water forcing and time support: BASELINE, SOURCE_REDUCTION and OUTLET_CAPTURE. Source reduction multiplies pollutant source rates only. Capture is an ideal instantaneous fraction of incoming material, bounded by cumulative capacity since the last explicit media replacement. Filling storage does not destroy material. Service transfers all retained material into a downstream handling ledger and explicitly renews the capacity; it is not a silent reset. Final unserviced stock stays stored.

Inputs use two or more named manufactured mass classes, fixed piecewise-constant source rates (kg/s), piecewise-constant water flow (m³/s), explicit interval edges (s), capture fraction/capacity, service times and a separately defined handling chain. These are artificial accounting controls, not plausible particle/device parameters.

## Temporal contract

`interval_mean_rate` values carry a unit, strictly increasing interval bounds and no missing entries. Conservative temporal exchange onto new bounds integrates overlaps, then divides by the target interval width. Preserve each target integral and the whole covered interval. Source and target supports must match exactly; reject extrapolation, gap filling, mismatched units and invalid bounds. Rates are nonnegative within this control. The independent reference expresses a cumulative piecewise-linear integral; it does not call the overlap routine.

Checks: constant rate; a finite pulse; step forcing; unequal widths; identical grids; coarse-to-fine and fine-to-coarse exchange; fractional boundaries; missing coverage; negative/duplicate bounds; whole-interval conservation. A coarse average can preserve mass while losing pulse timing; report this information loss separately from conservation. Coarsening is not evidence of temporal fidelity.

## Capture events and timing

Split at every source boundary, service time and capacity-hit time. For a constant incoming class-rate vector and available capacity C, active capture rate is capture_fraction times total incoming mass rate. If nonzero, saturation occurs after C / capture_rate. Split there exactly, then pass subsequent mass downstream until the next service. Capture allocation across classes uses their constant incoming capture rates before saturation; never smear the remaining capacity across a whole mixed interval.

At a shared time, finish the preceding half-open flow interval, then service the retained stock before processing the following interval. A service at the final bound is included exactly once. Record capacity before/after and the actual renewals. Refining a constant-forcing interval cannot change captured class totals, final stored mass, escaped mass or handling destinations beyond the declared floating-point tolerance.

The independent mass reference computes capacity-limited integrals across the frozen forcing/service intervals with Decimal arithmetic and a separate loop. It checks each arm's input, prevented, captured, escaped and final stored/destination totals. Water always passes through unchanged; the control does not solve hydraulics.

## Handling chain and resources

For every service and class:

1. Move captured stock from on-site storage to transport; preserve a unique transfer identity and gross mass.
2. Apply the declared transport leakage fraction; record material leaked to the environment and material arriving at sorting as separate transfers.
3. Apply the declared sorting leakage fraction; split remaining material into the four explicit terminal accounting states: `recovery_unverified`, `treatment_residue`, `disposal_unverified`, `destination_unknown`. Fractions must sum to one. All treatment output remains material; no generic destruction or contaminant-removal sink exists.
4. Record independently declared collection/transport/sorting energy factors in J/kg applied to their explicit gross input basis. Terminal resource factors are outside this control and cannot be silently added as credits.

For every transfer: opening stock + incoming = closing stock + outgoing, per class and globally. Capture is an internal transfer, so gross capture cannot be added to final storage and destinations in a whole-system balance. The terminal balance is input = stream escape + leaked handling material + final stored stock + named terminal destination stocks. Source-reduced material is reported separately relative to baseline and never enters the physical input twice.

No captured amount, named accounting destination, recovery fraction or treatment-residue label establishes real disposal, recycling, substitution credit, ecological benefit, health benefit or net lifecycle benefit. All foreground resource factors are manufactured, retained assumptions. Comparison is multidimensional: environmental release within this artificial boundary, unresolved destination stock and handling energy remain separate.

## Evidence and failure behavior

Outputs: input contract, version/source identity, per-interval flow and capture ledger, service and transfer events, per-class/global final balance, foreground resource basis, independent-reference comparison, conservative-remapping diagnostics, paired-arm summary, CSV tables and offline inspectable report. Include every declared arm and every source interval. Inspection reconstructs balances from raw records, verifies exact event times/order/identities and rejects omitted, duplicated, reordered or altered transfers even after hash regeneration. Reproduction uses the matching runtime and a fresh output directory outside its input. Interrupted or invalid execution cannot activate a successful bundle.

Runtime envelopes and tolerances will be made explicit in the schema before kernel implementation. They are computational admission bounds, not physical applicability ranges. Test fractional capacity events, no flow, zero capture/capacity, no service, final-bound service, repeated service rejection, total leakage, zero unknown fraction, all-unknown destination, tiny class alongside a large class, incompatible temporal bounds, malformed schema, altered event ledger, source/summary substitution and interruption. Preserve failures and do not loosen tolerances to obtain a preferred arm ranking.
