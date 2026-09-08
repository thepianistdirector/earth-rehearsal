# Earth Rehearsal tasks

Generated from `plan/tasks.json`; edit the canonical ledger, then run `python3 tools/render_plan.py`. Historical acceptance is preserved in [lineage](plan/lineage/architecture-foundation-2026-09-07/manifest.json). A mapped BOX-001 portion does not complete a broader original contract.

221 rows: 27 historical umbrella contracts and 194 delivery outcomes. Umbrellas preserve acceptance; they are not duplicate deliverables. New proposals start PLANNED. Implementation, automated checks, runtime evidence, human review and public release are separate evidence levels.

## L0 — Architecture and research-programme foundation

### ER-F01 — Establish the architecture contract

- Status: **DONE**; release: historical; basis: source_requirement; kind: historical_contract.
- Outcome: Define domain-specific solver and applicability boundaries; units and spatial/temporal/scale coupling; mass, energy, capture, disposal and lifecycle ledgers; uncertainty, identifiability, calibration and validation; versioned study/run/result contracts; negative outcomes; evaluator authority; scheduler recovery; plugin isolation; and evidence-based local-to-distributed scale triggers.
- Area: historical acceptance contract; original/canonical wave: 0; publication wave: L0.
- Prerequisites: none.
- Acceptance: Define domain-specific solver and applicability boundaries; units and spatial/temporal/scale coupling; mass, energy, capture, disposal and lifecycle ledgers; uncertainty, identifiability, calibration and validation; versioned study/run/result contracts; negative outcomes; evaluator authority; scheduler recovery; plugin isolation; and evidence-based local-to-distributed scale triggers.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-F02 — Establish the outcome and dependency roadmap

- Status: **DONE**; release: historical; basis: source_requirement; kind: historical_contract.
- Outcome: Prepend Wave 0 without replacing Waves 1–8; connect the first analytic case to the original 24 tasks; state scientific gates, external reviewer/data/resource dependencies, scope cuts, stop conditions and evidence-driven replanning triggers.
- Area: historical acceptance contract; original/canonical wave: 0; publication wave: L0.
- Prerequisites: ER-F01.
- Acceptance: Prepend Wave 0 without replacing Waves 1–8; connect the first analytic case to the original 24 tasks; state scientific gates, external reviewer/data/resource dependencies, scope cuts, stop conditions and evidence-driven replanning triggers.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-F03 — Specify the executable next-work packet and validate the repository plan

- Status: **DONE**; release: historical; basis: source_requirement; kind: historical_contract.
- Outcome: Specify BOX-001 with sufficient equations, synthetic values, intervention arms, invalid cases, artifacts and gates to begin ER-001 without inventing science; add a standard-library validator for unique IDs, status/wave constraints, dependencies, acyclicity, Wave 0 ordering, roadmap/task navigation and local Markdown links.
- Area: historical acceptance contract; original/canonical wave: 0; publication wave: L0.
- Prerequisites: ER-F02.
- Acceptance: Specify BOX-001 with sufficient equations, synthetic values, intervention arms, invalid cases, artifacts and gates to begin ER-001 without inventing science; add a standard-library validator for unique IDs, status/wave constraints, dependencies, acyclicity, Wave 0 ordering, roadmap/task navigation and local Markdown links.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

## W01 — BOX-001 is an executable accounting contract

### ER-B01-01 — Freeze exact synthetic study

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Versioned fixture records 1000 m3, dry 3600 s at 0.10 m3/s and 0.001 kg/s, storm 1800 s at 0.50 m3/s and 0.003 kg/s, and zero initial mass.
- Area: BOX-001 is an executable accounting contract; original/canonical wave: W01; publication wave: W01.
- Prerequisites: ER-F03.
- Acceptance: Versioned fixture records 1000 m3, dry 3600 s at 0.10 m3/s and 0.001 kg/s, storm 1800 s at 0.50 m3/s and 0.003 kg/s, and zero initial mass.
- Sources: owner-launch, BOX-001, ER-001, ER-002, ER-003, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B01-02 — Declare supported quantity grammar

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Parser rejects incompatible units, booleans masquerading as numbers, nonfinite values and unknown fields with field paths.
- Area: BOX-001 is an executable accounting contract; original/canonical wave: W01; publication wave: W01.
- Prerequisites: ER-B01-01.
- Acceptance: Parser rejects incompatible units, booleans masquerading as numbers, nonfinite values and unknown fields with field paths.
- Sources: owner-launch, BOX-001, ER-001, ER-002, ER-003, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B01-03 — Bound the fixed-volume model

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Nonpositive flow or volume and unequal inflow/outflow are rejected; no alternate physics is silently selected.
- Area: BOX-001 is an executable accounting contract; original/canonical wave: W01; publication wave: W01.
- Prerequisites: ER-B01-01.
- Acceptance: Nonpositive flow or volume and unequal inflow/outflow are rejected; no alternate physics is silently selected.
- Sources: owner-launch, BOX-001, ER-001, ER-002, ER-003, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B01-04 — Preserve paired arm definitions

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Default baseline, 0.5 source and 0.5 outlet capture share exact exogenous segments and initial stock.
- Area: BOX-001 is an executable accounting contract; original/canonical wave: W01; publication wave: W01.
- Prerequisites: ER-B01-01.
- Acceptance: Default baseline, 0.5 source and 0.5 outlet capture share exact exogenous segments and initial stock.
- Sources: owner-launch, BOX-001, ER-001, ER-002, ER-003, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B01-05 — Freeze tolerances before observation

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Versioned numerical error policy explains scale and refinement criteria before candidate results are evaluated.
- Area: BOX-001 is an executable accounting contract; original/canonical wave: W01; publication wave: W01.
- Prerequisites: ER-B01-01.
- Acceptance: Versioned numerical error policy explains scale and refinement criteria before candidate results are evaluated.
- Sources: owner-launch, BOX-001, ER-001, ER-002, ER-003, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B01-06 — Record original fixture rights

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Distribution notice distinguishes original synthetic values from external observations and records repository license.
- Area: BOX-001 is an executable accounting contract; original/canonical wave: W01; publication wave: W01.
- Prerequisites: ER-B01-01.
- Acceptance: Distribution notice distinguishes original synthetic values from external observations and records repository license.
- Sources: owner-launch, BOX-001, ER-001, ER-002, ER-003, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B01-07 — Version editable studies

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Changing one admitted input produces a distinct content identity while retaining parent identity and explicit units.
- Area: BOX-001 is an executable accounting contract; original/canonical wave: W01; publication wave: W01.
- Prerequisites: ER-B01-01.
- Acceptance: Changing one admitted input produces a distinct content identity while retaining parent identity and explicit units.
- Sources: owner-launch, BOX-001, ER-001, ER-002, ER-003, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B01-08 — Declare model exclusions

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Study and report label A0_KNOWN_ANSWER and exclude settling, reaction, fragmentation and environmental efficacy.
- Area: BOX-001 is an executable accounting contract; original/canonical wave: W01; publication wave: W01.
- Prerequisites: ER-B01-01, ER-B01-02, ER-B01-03, ER-B01-04, ER-B01-05, ER-B01-06, ER-B01-07.
- Acceptance: Study and report label A0_KNOWN_ANSWER and exclude settling, reaction, fragmentation and environmental efficacy.
- Sources: owner-launch, BOX-001, ER-001, ER-002, ER-003, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

## W02 — Analytic and numerical paths expose real trajectories

### ER-B02-01 — Implement independent piecewise analytic reference

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Reference returns stock and integrated outlet flux for both segments without calling numerical update code.
- Area: Analytic and numerical paths expose real trajectories; original/canonical wave: W02; publication wave: W02.
- Prerequisites: ER-B01-01, ER-B01-02, ER-B01-03, ER-B01-04, ER-B01-05, ER-B01-06, ER-B01-07, ER-B01-08.
- Acceptance: Reference returns stock and integrated outlet flux for both segments without calling numerical update code.
- Sources: owner-launch, BOX-001, ER-003, ER-004, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B02-02 — Implement conservative numerical stepping

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Kernel emits actual water/source/outlet transfers and stock at each step with no fabricated success output.
- Area: Analytic and numerical paths expose real trajectories; original/canonical wave: W02; publication wave: W02.
- Prerequisites: ER-B02-01.
- Acceptance: Kernel emits actual water/source/outlet transfers and stock at each step with no fabricated success output.
- Sources: owner-launch, BOX-001, ER-003, ER-004, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B02-03 — Verify hand-computable controls

- Status: **AUTOMATED PASS**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Separate hand controls test equilibrium, initial-stock decay and zero-source behavior against reference results.
- Area: Analytic and numerical paths expose real trajectories; original/canonical wave: W02; publication wave: W02.
- Prerequisites: ER-B02-01.
- Acceptance: Separate hand controls test equilibrium, initial-stock decay and zero-source behavior against reference results.
- Sources: owner-launch, BOX-001, ER-003, ER-004, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B02-04 — Preserve segment boundaries

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: A timestep that does not divide duration lands exactly on the boundary without applying storm forcing early.
- Area: Analytic and numerical paths expose real trajectories; original/canonical wave: W02; publication wave: W02.
- Prerequisites: ER-B02-01.
- Acceptance: A timestep that does not divide duration lands exactly on the boundary without applying storm forcing early.
- Sources: owner-launch, BOX-001, ER-003, ER-004, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B02-05 — Expose refinement diagnostics

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: At least three step sizes report absolute errors, residuals and observed refinement behavior under frozen criteria.
- Area: Analytic and numerical paths expose real trajectories; original/canonical wave: W02; publication wave: W02.
- Prerequisites: ER-B02-01.
- Acceptance: At least three step sizes report absolute errors, residuals and observed refinement behavior under frozen criteria.
- Sources: owner-launch, BOX-001, ER-003, ER-004, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B02-06 — Reject unstable stepping

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: A deliberately unstable step request fails with an actionable diagnostic and no valid comparison.
- Area: Analytic and numerical paths expose real trajectories; original/canonical wave: W02; publication wave: W02.
- Prerequisites: ER-B02-01.
- Acceptance: A deliberately unstable step request fails with an actionable diagnostic and no valid comparison.
- Sources: owner-launch, BOX-001, ER-003, ER-004, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B02-07 — Detect source-term corruption

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Perturbing a source term or update coefficient causes an independent reference or balance failure.
- Area: Analytic and numerical paths expose real trajectories; original/canonical wave: W02; publication wave: W02.
- Prerequisites: ER-B02-01.
- Acceptance: Perturbing a source term or update coefficient causes an independent reference or balance failure.
- Sources: owner-launch, BOX-001, ER-003, ER-004, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B02-08 — Demonstrate responsive trajectories

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: A supported source or flow change produces reproducibly different raw trajectories and balances.
- Area: Analytic and numerical paths expose real trajectories; original/canonical wave: W02; publication wave: W02.
- Prerequisites: ER-B02-01, ER-B02-02, ER-B02-03, ER-B02-04, ER-B02-05, ER-B02-06, ER-B02-07.
- Acceptance: A supported source or flow change produces reproducibly different raw trajectories and balances.
- Sources: owner-launch, BOX-001, ER-003, ER-004, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

## W03 — Captured material retains a destination

### ER-B03-01 — Reconstruct reservoir mass balance

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Evaluator recomputes initial plus source minus stock and outlet from raw records and rejects a perturbed flux.
- Area: Captured material retains a destination; original/canonical wave: W03; publication wave: W03.
- Prerequisites: ER-B02-01, ER-B02-02, ER-B02-03, ER-B02-04, ER-B02-05, ER-B02-06, ER-B02-07, ER-B02-08.
- Acceptance: Evaluator recomputes initial plus source minus stock and outlet from raw records and rejects a perturbed flux.
- Sources: owner-launch, BOX-001, ER-005, ER-006, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B03-02 — Reconstruct fixed-volume water balance

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Per-segment and total inflow/outflow/volume residuals close independently of solver success flags.
- Area: Captured material retains a destination; original/canonical wave: W03; publication wave: W03.
- Prerequisites: ER-B03-01.
- Acceptance: Per-segment and total inflow/outflow/volume residuals close independently of solver success flags.
- Sources: owner-launch, BOX-001, ER-005, ER-006, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B03-03 — Separate capture from source reduction

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Capture leaves reservoir stock unchanged while source reduction changes incoming mass; tests distinguish these effects.
- Area: Captured material retains a destination; original/canonical wave: W03; publication wave: W03.
- Prerequisites: ER-B03-01.
- Acceptance: Capture leaves reservoir stock unchanged while source reduction changes incoming mass; tests distinguish these effects.
- Sources: owner-launch, BOX-001, ER-005, ER-006, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B03-04 — Record custody transfer events

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Every captured transfer has a unique reference and recorded stored then destination_unknown transition.
- Area: Captured material retains a destination; original/canonical wave: W03; publication wave: W03.
- Prerequisites: ER-B03-01.
- Acceptance: Every captured transfer has a unique reference and recorded stored then destination_unknown transition.
- Sources: owner-launch, BOX-001, ER-005, ER-006, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B03-05 — Prevent custody double credits

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Adding captured transfer and terminal custody as separate removed mass fails the ledger check.
- Area: Captured material retains a destination; original/canonical wave: W03; publication wave: W03.
- Prerequisites: ER-B03-01.
- Acceptance: Adding captured transfer and terminal custody as separate removed mass fails the ledger check.
- Sources: owner-launch, BOX-001, ER-005, ER-006, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B03-06 — Reject missing terminal custody

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Removing a destination record produces INVALID with the unmatched transfer identity.
- Area: Captured material retains a destination; original/canonical wave: W03; publication wave: W03.
- Prerequisites: ER-B03-01.
- Acceptance: Removing a destination record produces INVALID with the unmatched transfer identity.
- Sources: owner-launch, BOX-001, ER-005, ER-006, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B03-07 — Reject invented disposal outcomes

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: A fixture claiming safe disposal or benefit fails; disposal/lifecycle/ecology/health remain NOT_EVALUATED.
- Area: Captured material retains a destination; original/canonical wave: W03; publication wave: W03.
- Prerequisites: ER-B03-01.
- Acceptance: A fixture claiming safe disposal or benefit fails; disposal/lifecycle/ecology/health remain NOT_EVALUATED.
- Sources: owner-launch, BOX-001, ER-005, ER-006, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B03-08 — Reconcile interval and cumulative ledgers

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Segment totals sum to final stocks and terminal custody without a duplicated boundary event.
- Area: Captured material retains a destination; original/canonical wave: W03; publication wave: W03.
- Prerequisites: ER-B03-01, ER-B03-02, ER-B03-03, ER-B03-04, ER-B03-05, ER-B03-06, ER-B03-07.
- Acceptance: Segment totals sum to final stocks and terminal custody without a duplicated boundary event.
- Sources: owner-launch, BOX-001, ER-005, ER-006, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

## W04 — Invalid claims and failed runs stay visible

### ER-B04-01 — Keep invalid attempts separate

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Failed, partial and invalid attempts cannot enter valid comparison aggregates and retain their failure reason.
- Area: Invalid claims and failed runs stay visible; original/canonical wave: W04; publication wave: W04.
- Prerequisites: ER-B03-01, ER-B03-02, ER-B03-03, ER-B03-04, ER-B03-05, ER-B03-06, ER-B03-07, ER-B03-08.
- Acceptance: Failed, partial and invalid attempts cannot enter valid comparison aggregates and retain their failure reason.
- Sources: owner-launch, BOX-001, ER-008, ER-009, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B04-02 — Compare paired supported metrics

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Three-arm tables identify stock, escape and capture with identical forcings and units; unsupported metrics are absent or unassessed.
- Area: Invalid claims and failed runs stay visible; original/canonical wave: W04; publication wave: W04.
- Prerequisites: ER-B04-01.
- Acceptance: Three-arm tables identify stock, escape and capture with identical forcings and units; unsupported metrics are absent or unassessed.
- Sources: owner-launch, BOX-001, ER-008, ER-009, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B04-03 — Expose ranking sensitivity

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Refinement diagnostics state whether ordering changes, including ties, rather than silently selecting a favorable resolution.
- Area: Invalid claims and failed runs stay visible; original/canonical wave: W04; publication wave: W04.
- Prerequisites: ER-B04-01.
- Acceptance: Refinement diagnostics state whether ordering changes, including ties, rather than silently selecting a favorable resolution.
- Sources: owner-launch, BOX-001, ER-008, ER-009, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B04-04 — Retain negative controls

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Bundled invalid inputs and conservation/custody corruptions fail through the documented command path.
- Area: Invalid claims and failed runs stay visible; original/canonical wave: W04; publication wave: W04.
- Prerequisites: ER-B04-01.
- Acceptance: Bundled invalid inputs and conservation/custody corruptions fail through the documented command path.
- Sources: owner-launch, BOX-001, ER-008, ER-009, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B04-05 — Preserve provenance in raw evidence

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Run records contain study hash, evaluator version, code identity and runtime identity without developer paths or secrets.
- Area: Invalid claims and failed runs stay visible; original/canonical wave: W04; publication wave: W04.
- Prerequisites: ER-B04-01.
- Acceptance: Run records contain study hash, evaluator version, code identity and runtime identity without developer paths or secrets.
- Sources: owner-launch, BOX-001, ER-008, ER-009, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B04-06 — Generate JSON and CSV from retained data

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Exports round-trip supported numeric fields and can be reconciled to raw interval records.
- Area: Invalid claims and failed runs stay visible; original/canonical wave: W04; publication wave: W04.
- Prerequisites: ER-B04-01.
- Acceptance: Exports round-trip supported numeric fields and can be reconciled to raw interval records.
- Sources: owner-launch, BOX-001, ER-008, ER-009, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B04-07 — Render accessible evidence report

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: HTML exposes labels, units, non-color state cues and raw tables with keyboard and narrow-screen inspection evidence.
- Area: Invalid claims and failed runs stay visible; original/canonical wave: W04; publication wave: W04.
- Prerequisites: ER-B04-01.
- Acceptance: HTML exposes labels, units, non-color state cues and raw tables with keyboard and narrow-screen inspection evidence.
- Sources: owner-launch, BOX-001, ER-008, ER-009, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B04-08 — Separate interpretation from calculation

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Report labels fictional inputs and never infers environmental, disposal or health benefit from lower escaped mass.
- Area: Invalid claims and failed runs stay visible; original/canonical wave: W04; publication wave: W04.
- Prerequisites: ER-B04-01, ER-B04-02, ER-B04-03, ER-B04-04, ER-B04-05, ER-B04-06, ER-B04-07.
- Acceptance: Report labels fictional inputs and never infers environmental, disposal or health benefit from lower escaped mass.
- Sources: owner-launch, BOX-001, ER-008, ER-009, ER-011, decision-runtime, decision-numerics.
- Evidence needs: Independent numeric and custody falsifiers; no real-world efficacy inference.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

## W05 — External users reproduce and inspect the study

### ER-B05-01 — Activate bundles atomically

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Interrupted calculation or activation preserves prior complete bundles and leaves partial attempts distinguishable.
- Area: External users reproduce and inspect the study; original/canonical wave: W05; publication wave: W05.
- Prerequisites: ER-B04-01, ER-B04-02, ER-B04-03, ER-B04-04, ER-B04-05, ER-B04-06, ER-B04-07, ER-B04-08.
- Acceptance: Interrupted calculation or activation preserves prior complete bundles and leaves partial attempts distinguishable.
- Sources: owner-launch, BOX-001, ER-021, ER-023, ER-024, decision-runtime, decision-numerics.
- Evidence needs: Actual external observation and destination-specific publication authority.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B05-02 — Inspect completed bundles offline

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Documented inspect command validates and displays retained evidence without rerunning the model or fetching data.
- Area: External users reproduce and inspect the study; original/canonical wave: W05; publication wave: W05.
- Prerequisites: ER-B05-01.
- Acceptance: Documented inspect command validates and displays retained evidence without rerunning the model or fetching data.
- Sources: owner-launch, BOX-001, ER-021, ER-023, ER-024, decision-runtime, decision-numerics.
- Evidence needs: Actual external observation and destination-specific publication authority.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B05-03 — Reproduce from bundle manifest

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: A new output directory regenerates the same study from its manifest and records a separate attempt identity.
- Area: External users reproduce and inspect the study; original/canonical wave: W05; publication wave: W05.
- Prerequisites: ER-B05-02.
- Acceptance: A new output directory regenerates the same study from its manifest and records a separate attempt identity.
- Sources: owner-launch, BOX-001, ER-021, ER-023, ER-024, decision-runtime, decision-numerics.
- Evidence needs: Actual external observation and destination-specific publication authority.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B05-04 — Package standard-library first run

- Status: **RUNTIME VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Versioned archive includes executable CLI, exact fixture, notices and invalid controls; clean packaged run passes.
- Area: External users reproduce and inspect the study; original/canonical wave: W05; publication wave: W05.
- Prerequisites: ER-B05-01, ER-B05-02, ER-B05-03.
- Acceptance: Versioned archive includes executable CLI, exact fixture, notices and invalid controls; clean packaged run passes.
- Sources: owner-launch, BOX-001, ER-021, ER-023, ER-024, decision-runtime, decision-numerics.
- Evidence needs: Actual external observation and destination-specific publication authority.
- Recorded evidence: ["docs/evidence/verification.md", "tests/", "docs/decisions/0002-numerical-policy.md"].

### ER-B05-08 — Review released interpretation

- Status: **BLOCKED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Required human review is recorded honestly and all supported claims match available evidence; missing review remains a release gate.
- Area: External users reproduce and inspect the study; original/canonical wave: W05; publication wave: W05.
- Prerequisites: ER-B05-04.
- Acceptance: Required human review is recorded honestly and all supported claims match available evidence; missing review remains a release gate.
- Sources: owner-launch, BOX-001, ER-021, ER-023, ER-024, decision-runtime, decision-numerics.
- Evidence needs: Actual external observation and destination-specific publication authority.
- Recorded evidence: ["STATUS.md#unresolved-release-gates"].

### ER-B05-06 — Publish authorized GitHub release

- Status: **RELEASE VERIFIED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Exact approved tag and assets are publicly downloadable and asset hashes match locally verified artifacts.
- Area: External users reproduce and inspect the study; original/canonical wave: W05; publication wave: W05.
- Prerequisites: ER-B05-04, ER-B05-08.
- Acceptance: Exact approved tag and assets are publicly downloadable and asset hashes match locally verified artifacts.
- Sources: owner-launch, BOX-001, ER-021, ER-023, ER-024, decision-runtime, decision-numerics.
- Evidence needs: Owner publication approval received September 8, 2026. Public assets and unauthenticated download verified. Required human review in ER-B05-08 remains incomplete; this status records publication and asset verification only.
- Recorded evidence: ["https://github.com/thepianistdirector/earth-rehearsal/releases/tag/v0.1.0", "docs/evidence/public-release-verification.json", "STATUS.md#unresolved-release-gates"].

### ER-B05-05 — Observe first-run and recovery workflow

- Status: **BLOCKED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: An actual external participant obtains the public artifact, changes an input, diagnoses an invalid control and reopens/reproduces evidence; observer provenance is recorded.
- Area: External users reproduce and inspect the study; original/canonical wave: W05; publication wave: W05.
- Prerequisites: ER-B05-06.
- Acceptance: An actual external participant obtains the public artifact, changes an input, diagnoses an invalid control and reopens/reproduces evidence; observer provenance is recorded.
- Sources: owner-launch, BOX-001, ER-021, ER-023, ER-024, decision-runtime, decision-numerics.
- Evidence needs: Actual external observation and destination-specific publication authority.
- Recorded evidence: ["STATUS.md#unresolved-release-gates"].

### ER-B05-07 — Publish native Tanduna programme

- Status: **BLOCKED**; release: 0.1; basis: owner_proposed_cut; kind: delivery_outcome.
- Outcome: Public readback verifies actual wave/task counts, order, dependencies, scope and access instructions against the canonical export.
- Area: External users reproduce and inspect the study; original/canonical wave: W05; publication wave: W05.
- Prerequisites: ER-B05-06.
- Acceptance: Public readback verifies actual wave/task counts, order, dependencies, scope and access instructions against the canonical export.
- Sources: owner-launch, BOX-001, ER-021, ER-023, ER-024, decision-runtime, decision-numerics.
- Evidence needs: Actual external observation and destination-specific publication authority.
- Recorded evidence: ["STATUS.md#unresolved-release-gates"].

## W06 — Catchment scenarios have explicit boundaries

### ER-001 — Specify the first pollutant scenario

- Status: **PLANNED**; release: 0.x; basis: source_requirement; kind: historical_contract.
- Outcome: Define the synthetic catchment, particle classes, boundary conditions, analytic references and mass-accounting equation.
- Area: historical acceptance contract; original/canonical wave: 1; publication wave: W06.
- Prerequisites: ER-F03.
- Acceptance: Define the synthetic catchment, particle classes, boundary conditions, analytic references and mass-accounting equation.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P06-01 — Define catchment question and support

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Named synthetic domain, modeled question and spatial/temporal support exclude unsupported real-site interpretation.
- Area: Catchment scenarios have explicit boundaries; original/canonical wave: W06; publication wave: W06.
- Prerequisites: ER-F03.
- Acceptance: Named synthetic domain, modeled question and spatial/temporal support exclude unsupported real-site interpretation.
- Sources: owner-launch, ER-001.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P06-02 — Specify particle class contract

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Each admitted class has units, conserved quantity and evidence for included processes; unsupported classes are rejected.
- Area: Catchment scenarios have explicit boundaries; original/canonical wave: W06; publication wave: W06.
- Prerequisites: ER-P06-01.
- Acceptance: Each admitted class has units, conserved quantity and evidence for included processes; unsupported classes are rejected.
- Sources: owner-launch, ER-001.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P06-03 — Describe source and sink topology

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Every boundary edge has direction, quantity and provenance; an unconnected sink fails validation.
- Area: Catchment scenarios have explicit boundaries; original/canonical wave: W06; publication wave: W06.
- Prerequisites: ER-P06-01.
- Acceptance: Every boundary edge has direction, quantity and provenance; an unconnected sink fails validation.
- Sources: owner-launch, ER-001.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P06-04 — Declare initial conditions across cells

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Scenario specifies stock and water state per modeled compartment and rejects missing compartments.
- Area: Catchment scenarios have explicit boundaries; original/canonical wave: W06; publication wave: W06.
- Prerequisites: ER-P06-01.
- Acceptance: Scenario specifies stock and water state per modeled compartment and rejects missing compartments.
- Sources: owner-launch, ER-001.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P06-05 — Separate boundary condition families

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Closed, prescribed-inflow and prescribed-stage boundaries are distinct typed contracts with incompatible combinations rejected.
- Area: Catchment scenarios have explicit boundaries; original/canonical wave: W06; publication wave: W06.
- Prerequisites: ER-P06-01.
- Acceptance: Closed, prescribed-inflow and prescribed-stage boundaries are distinct typed contracts with incompatible combinations rejected.
- Sources: owner-launch, ER-001.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P06-06 — Record omitted catchment pathways

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Model card lists omitted groundwater, resuspension or reactions and identifies claims those omissions prohibit.
- Area: Catchment scenarios have explicit boundaries; original/canonical wave: W06; publication wave: W06.
- Prerequisites: ER-P06-01.
- Acceptance: Model card lists omitted groundwater, resuspension or reactions and identifies claims those omissions prohibit.
- Sources: owner-launch, ER-001.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P06-07 — Approve first spatial study contract

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Qualified review checks source/particle/support assumptions before any real catchment interpretation is promoted.
- Area: Catchment scenarios have explicit boundaries; original/canonical wave: W06; publication wave: W06.
- Prerequisites: ER-P06-01, ER-P06-02, ER-P06-03, ER-P06-04, ER-P06-05, ER-P06-06.
- Acceptance: Qualified review checks source/particle/support assumptions before any real catchment interpretation is promoted.
- Sources: owner-launch, ER-001.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W07 — Environmental sources have usable rights

### ER-002 — Review environmental data and rights

- Status: **PLANNED**; release: 0.x; basis: source_requirement; kind: historical_contract.
- Outcome: Record exact source licenses, resolution, date coverage and missing variables; clearly label invented scenario inputs.
- Area: historical acceptance contract; original/canonical wave: 1; publication wave: W07.
- Prerequisites: ER-001.
- Acceptance: Record exact source licenses, resolution, date coverage and missing variables; clearly label invented scenario inputs.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P07-01 — Catalog exact source releases

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Each dataset has canonical identifier, provider, retrieval date and immutable version or checksum.
- Area: Environmental sources have usable rights; original/canonical wave: W07; publication wave: W07.
- Prerequisites: ER-P06-07.
- Acceptance: Each dataset has canonical identifier, provider, retrieval date and immutable version or checksum.
- Sources: owner-launch, ER-002.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P07-02 — Resolve redistribution permissions

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: A rights table distinguishes use, derivatives and redistribution; blocked rights prevent packaging that source.
- Area: Environmental sources have usable rights; original/canonical wave: W07; publication wave: W07.
- Prerequisites: ER-P07-01.
- Acceptance: A rights table distinguishes use, derivatives and redistribution; blocked rights prevent packaging that source.
- Sources: owner-launch, ER-002.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P07-03 — Track spatial and date coverage

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Coverage records expose resolution, coordinate reference and temporal gaps before scenario binding.
- Area: Environmental sources have usable rights; original/canonical wave: W07; publication wave: W07.
- Prerequisites: ER-P07-01.
- Acceptance: Coverage records expose resolution, coordinate reference and temporal gaps before scenario binding.
- Sources: owner-launch, ER-002.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P07-04 — Expose missing variables and quality flags

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Missing values cannot become zero and quality flags survive all transformations.
- Area: Environmental sources have usable rights; original/canonical wave: W07; publication wave: W07.
- Prerequisites: ER-P07-01.
- Acceptance: Missing values cannot become zero and quality flags survive all transformations.
- Sources: owner-launch, ER-002.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P07-05 — Preserve transformation provenance

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Derived input records retain ordered transformations, parent hashes and unit changes.
- Area: Environmental sources have usable rights; original/canonical wave: W07; publication wave: W07.
- Prerequisites: ER-P07-01.
- Acceptance: Derived input records retain ordered transformations, parent hashes and unit changes.
- Sources: owner-launch, ER-002.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P07-06 — Separate synthetic and observed inputs

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Fixtures and reports visibly distinguish wholly synthetic, measured and derived quantities.
- Area: Environmental sources have usable rights; original/canonical wave: W07; publication wave: W07.
- Prerequisites: ER-P07-01.
- Acceptance: Fixtures and reports visibly distinguish wholly synthetic, measured and derived quantities.
- Sources: owner-launch, ER-002.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P07-07 — Test source replacement compatibility

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: A changed dataset version triggers support/unit/rights checks and a new scenario identity.
- Area: Environmental sources have usable rights; original/canonical wave: W07; publication wave: W07.
- Prerequisites: ER-P07-01, ER-P07-02, ER-P07-03, ER-P07-04, ER-P07-05, ER-P07-06.
- Acceptance: A changed dataset version triggers support/unit/rights checks and a new scenario identity.
- Sources: owner-launch, ER-002.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W08 — Flow and transport kernels meet references

### ER-003 — Build the experiment skeleton

- Status: **PLANNED**; release: 0.x; basis: source_requirement; kind: historical_contract.
- Outcome: A CLI validates units and source/sink definitions; a hand-computable no-removal case passes.
- Area: historical acceptance contract; original/canonical wave: 1; publication wave: W08.
- Prerequisites: ER-001, ER-002.
- Acceptance: A CLI validates units and source/sink definitions; a hand-computable no-removal case passes.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P08-01 — Verify closed-box accumulation

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Separate zero-flow model reproduces M0 plus Lt without invoking the BOX quotient expression.
- Area: Flow and transport kernels meet references; original/canonical wave: W08; publication wave: W08.
- Prerequisites: ER-P06-07, ER-P07-07.
- Acceptance: Separate zero-flow model reproduces M0 plus Lt without invoking the BOX quotient expression.
- Sources: owner-launch, ER-004.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-004 — Implement the reference flow/transport model

- Status: **PLANNED**; release: 0.x; basis: source_requirement; kind: historical_contract.
- Outcome: Pass closed-box and open-boundary analytical cases with justified residual tolerances.
- Area: historical acceptance contract; original/canonical wave: 2; publication wave: W08.
- Prerequisites: ER-001, ER-002, ER-003.
- Acceptance: Pass closed-box and open-boundary analytical cases with justified residual tolerances.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P08-02 — Verify open-boundary transport

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Reference inflow/outflow case closes mass and matches its declared analytic solution.
- Area: Flow and transport kernels meet references; original/canonical wave: W08; publication wave: W08.
- Prerequisites: ER-P08-01.
- Acceptance: Reference inflow/outflow case closes mass and matches its declared analytic solution.
- Sources: owner-launch, ER-004.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P08-03 — Preserve positivity by method

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Admitted timesteps retain nonnegative stocks; negative-stock cases fail instead of being silently clipped.
- Area: Flow and transport kernels meet references; original/canonical wave: W08; publication wave: W08.
- Prerequisites: ER-P08-01.
- Acceptance: Admitted timesteps retain nonnegative stocks; negative-stock cases fail instead of being silently clipped.
- Sources: owner-launch, ER-004.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P08-04 — Audit edge flux direction

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Reversing a test edge changes donor/receiver accounting consistently and global mass still closes.
- Area: Flow and transport kernels meet references; original/canonical wave: W08; publication wave: W08.
- Prerequisites: ER-P08-01.
- Acceptance: Reversing a test edge changes donor/receiver accounting consistently and global mass still closes.
- Sources: owner-launch, ER-004.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P08-05 — Support conservative compartment exchange

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Internal transfers cancel in whole-domain balance and remain visible in local balances.
- Area: Flow and transport kernels meet references; original/canonical wave: W08; publication wave: W08.
- Prerequisites: ER-P08-01.
- Acceptance: Internal transfers cancel in whole-domain balance and remain visible in local balances.
- Sources: owner-launch, ER-004.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P08-06 — Declare solver applicability envelope

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Model card ties accepted flow regimes and particle processes to executed references and exclusions.
- Area: Flow and transport kernels meet references; original/canonical wave: W08; publication wave: W08.
- Prerequisites: ER-P08-01.
- Acceptance: Model card ties accepted flow regimes and particle processes to executed references and exclusions.
- Sources: owner-launch, ER-004.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P08-07 — Detect internal transfer defects

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Duplicating or dropping an exchange is caught by an independently reconstructed domain ledger.
- Area: Flow and transport kernels meet references; original/canonical wave: W08; publication wave: W08.
- Prerequisites: ER-P08-01, ER-P08-02, ER-P08-03, ER-P08-04, ER-P08-05, ER-P08-06.
- Acceptance: Duplicating or dropping an exchange is caught by an independently reconstructed domain ledger.
- Sources: owner-launch, ER-004.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W09 — Intervention policies conserve material

### ER-005 — Implement source-reduction and capture policies

- Status: **PLANNED**; release: 0.x; basis: source_requirement; kind: historical_contract.
- Outcome: Track captured and residual mass separately; no efficiency parameter can silently remove unaccounted mass.
- Area: historical acceptance contract; original/canonical wave: 2; publication wave: W09.
- Prerequisites: ER-001, ER-002, ER-003.
- Acceptance: Track captured and residual mass separately; no efficiency parameter can silently remove unaccounted mass.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P09-01 — Define source-prevention boundary

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Prevented input is reported against the untreated source baseline without being counted as captured waste.
- Area: Intervention policies conserve material; original/canonical wave: W09; publication wave: W09.
- Prerequisites: ER-P08-07.
- Acceptance: Prevented input is reported against the untreated source baseline without being counted as captured waste.
- Sources: owner-launch, ER-005.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P09-02 — Represent interception location

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Interception acts on named edges and rejects placement outside the modeled topology.
- Area: Intervention policies conserve material; original/canonical wave: W09; publication wave: W09.
- Prerequisites: ER-P09-01.
- Acceptance: Interception acts on named edges and rejects placement outside the modeled topology.
- Sources: owner-launch, ER-005.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P09-03 — Bound capture policy response

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Admitted capture law has stated limits and evidence; efficiency outside those limits is rejected.
- Area: Intervention policies conserve material; original/canonical wave: W09; publication wave: W09.
- Prerequisites: ER-P09-01.
- Acceptance: Admitted capture law has stated limits and evidence; efficiency outside those limits is rejected.
- Sources: owner-launch, ER-005.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P09-04 — Model capacity exhaustion explicitly

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: A finite synthetic capacity saturates and remaining material continues to downstream fate.
- Area: Intervention policies conserve material; original/canonical wave: W09; publication wave: W09.
- Prerequisites: ER-P09-01.
- Acceptance: A finite synthetic capacity saturates and remaining material continues to downstream fate.
- Sources: owner-launch, ER-005.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P09-05 — Represent leakage as a transfer

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Leakage leaves custody and enters a named modeled destination with no lost mass.
- Area: Intervention policies conserve material; original/canonical wave: W09; publication wave: W09.
- Prerequisites: ER-P09-01.
- Acceptance: Leakage leaves custody and enters a named modeled destination with no lost mass.
- Sources: owner-launch, ER-005.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P09-06 — Compare intervention resource envelopes

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Resource differences appear alongside metrics rather than being hidden in unequal arm assumptions.
- Area: Intervention policies conserve material; original/canonical wave: W09; publication wave: W09.
- Prerequisites: ER-P09-01.
- Acceptance: Resource differences appear alongside metrics rather than being hidden in unequal arm assumptions.
- Sources: owner-launch, ER-005.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P09-07 — Audit policy composition order

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Combined policies declare order and a noncommuting test demonstrates the reported difference.
- Area: Intervention policies conserve material; original/canonical wave: W09; publication wave: W09.
- Prerequisites: ER-P09-01, ER-P09-02, ER-P09-03, ER-P09-04, ER-P09-05, ER-P09-06.
- Acceptance: Combined policies declare order and a noncommuting test demonstrates the reported difference.
- Sources: owner-launch, ER-005.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W10 — Waste custody survives the whole lifecycle

### ER-006 — Add disposal and lifecycle accounting

- Status: **PLANNED**; release: 0.x; basis: source_requirement; kind: historical_contract.
- Outcome: Report the destination and energy assumptions for captured waste; detect double counting.
- Area: historical acceptance contract; original/canonical wave: 2; publication wave: W10.
- Prerequisites: ER-001, ER-002, ER-003.
- Acceptance: Report the destination and energy assumptions for captured waste; detect double counting.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P10-01 — Define custody ownership and destinations

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Every transfer has origin, destination, timestamp and quantity; unknown destinations remain explicit.
- Area: Waste custody survives the whole lifecycle; original/canonical wave: W10; publication wave: W10.
- Prerequisites: ER-P09-07.
- Acceptance: Every transfer has origin, destination, timestamp and quantity; unknown destinations remain explicit.
- Sources: owner-launch, ER-006.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P10-02 — Model storage inventory and residence

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Storage inflows and releases reconcile to stock over each declared interval.
- Area: Waste custody survives the whole lifecycle; original/canonical wave: W10; publication wave: W10.
- Prerequisites: ER-P10-01.
- Acceptance: Storage inflows and releases reconcile to stock over each declared interval.
- Sources: owner-launch, ER-006.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P10-03 — Track waste transport losses

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Shipment quantities reconcile delivered, retained and leaked mass with destination records.
- Area: Waste custody survives the whole lifecycle; original/canonical wave: W10; publication wave: W10.
- Prerequisites: ER-P10-01.
- Acceptance: Shipment quantities reconcile delivered, retained and leaked mass with destination records.
- Sources: owner-launch, ER-006.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P10-04 — Represent sorting fractions

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Sorting outputs sum to admitted inputs and reject unsupported fraction totals.
- Area: Waste custody survives the whole lifecycle; original/canonical wave: W10; publication wave: W10.
- Prerequisites: ER-P10-01.
- Acceptance: Sorting outputs sum to admitted inputs and reject unsupported fraction totals.
- Sources: owner-launch, ER-006.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P10-05 — Separate treatment conversion products

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Treatment records specify conserved species or justified conversion boundaries and never erase residuals.
- Area: Waste custody survives the whole lifecycle; original/canonical wave: W10; publication wave: W10.
- Prerequisites: ER-P10-01.
- Acceptance: Treatment records specify conserved species or justified conversion boundaries and never erase residuals.
- Sources: owner-launch, ER-006.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P10-06 — Require disposal evidence class

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Disposal status requires named evidence and authority; a storage receipt cannot satisfy disposal completion.
- Area: Waste custody survives the whole lifecycle; original/canonical wave: W10; publication wave: W10.
- Prerequisites: ER-P10-01.
- Acceptance: Disposal status requires named evidence and authority; a storage receipt cannot satisfy disposal completion.
- Sources: owner-launch, ER-006.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P10-07 — Link custody energy assumptions

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Each modeled handling activity cites energy assumptions and uncertainty independently of pollutant reduction.
- Area: Waste custody survives the whole lifecycle; original/canonical wave: W10; publication wave: W10.
- Prerequisites: ER-P10-01, ER-P10-02, ER-P10-03, ER-P10-04, ER-P10-05, ER-P10-06.
- Acceptance: Each modeled handling activity cites energy assumptions and uncertainty independently of pollutant reduction.
- Sources: owner-launch, ER-006.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W11 — Dry and storm comparisons use paired conditions

### ER-007 — Create dry-weather and storm cases

- Status: **PLANNED**; release: 0.x; basis: source_requirement; kind: historical_contract.
- Outcome: Use documented synthetic flow profiles with paired random inputs and all boundary conditions saved.
- Area: historical acceptance contract; original/canonical wave: 3; publication wave: W11.
- Prerequisites: ER-004, ER-005, ER-006.
- Acceptance: Use documented synthetic flow profiles with paired random inputs and all boundary conditions saved.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P11-01 — Version dry-weather forcing profiles

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Dry cases retain original boundaries, units and temporal support with no undocumented interpolation.
- Area: Dry and storm comparisons use paired conditions; original/canonical wave: W11; publication wave: W11.
- Prerequisites: ER-P08-07, ER-P09-07, ER-P10-07.
- Acceptance: Dry cases retain original boundaries, units and temporal support with no undocumented interpolation.
- Sources: owner-launch, ER-007, ER-008, ER-009.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-008 — Compare three intervention strategies

- Status: **PLANNED**; release: 0.x; basis: source_requirement; kind: historical_contract.
- Outcome: Show no intervention, source reduction and capture under equal resource assumptions, including invalid runs.
- Area: historical acceptance contract; original/canonical wave: 3; publication wave: W11.
- Prerequisites: ER-004, ER-005, ER-006, ER-007.
- Acceptance: Show no intervention, source reduction and capture under equal resource assumptions, including invalid runs.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P11-02 — Version storm hydrographs

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Storm cases preserve onset, peak and recession inputs and explicitly synthetic or observed classification.
- Area: Dry and storm comparisons use paired conditions; original/canonical wave: W11; publication wave: W11.
- Prerequisites: ER-P11-01.
- Acceptance: Storm cases preserve onset, peak and recession inputs and explicitly synthetic or observed classification.
- Sources: owner-launch, ER-007, ER-008, ER-009.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P11-03 — Pair stochastic forcings across arms

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: All paired arms share recorded seeds and forcings; mismatches fail comparison eligibility.
- Area: Dry and storm comparisons use paired conditions; original/canonical wave: W11; publication wave: W11.
- Prerequisites: ER-P11-01.
- Acceptance: All paired arms share recorded seeds and forcings; mismatches fail comparison eligibility.
- Sources: owner-launch, ER-007, ER-008, ER-009.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P11-04 — Record resource equality and exceptions

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Comparison manifest declares shared budgets and explains any arm-specific resource demand.
- Area: Dry and storm comparisons use paired conditions; original/canonical wave: W11; publication wave: W11.
- Prerequisites: ER-P11-01.
- Acceptance: Comparison manifest declares shared budgets and explains any arm-specific resource demand.
- Sources: owner-launch, ER-007, ER-008, ER-009.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P11-05 — Keep all attempted arms in denominators

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Crashes and constraint failures remain in the comparison attempt table.
- Area: Dry and storm comparisons use paired conditions; original/canonical wave: W11; publication wave: W11.
- Prerequisites: ER-P11-01.
- Acceptance: Crashes and constraint failures remain in the comparison attempt table.
- Sources: owner-launch, ER-007, ER-008, ER-009.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P11-06 — Export spatial balances with provenance

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Every mapped quantity traces to retained cells/edges, units, support and source quality.
- Area: Dry and storm comparisons use paired conditions; original/canonical wave: W11; publication wave: W11.
- Prerequisites: ER-P11-01.
- Acceptance: Every mapped quantity traces to retained cells/edges, units, support and source quality.
- Sources: owner-launch, ER-007, ER-008, ER-009.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-009 — Export maps, balances and limitations

- Status: **PLANNED**; release: 0.x; basis: source_requirement; kind: historical_contract.
- Outcome: Every figure derives from retained run data and labels simulation, source quality and unknown ecological effects.
- Area: historical acceptance contract; original/canonical wave: 3; publication wave: W11.
- Prerequisites: ER-004, ER-005, ER-006, ER-008.
- Acceptance: Every figure derives from retained run data and labels simulation, source quality and unknown ecological effects.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P11-07 — Gate first catchment comparison

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Integrated dry/storm baseline/prevention/capture evidence passes conservation and limitation review.
- Area: Dry and storm comparisons use paired conditions; original/canonical wave: W11; publication wave: W11.
- Prerequisites: ER-P11-01, ER-P11-02, ER-P11-03, ER-P11-04, ER-P11-05, ER-P11-06.
- Acceptance: Integrated dry/storm baseline/prevention/capture evidence passes conservation and limitation review.
- Sources: owner-launch, ER-007, ER-008, ER-009.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W12 — Uncertainty reveals ranking reversals

### ER-010 — Test particle and flow sensitivity

- Status: **PLANNED**; release: 0.x; basis: source_requirement; kind: historical_contract.
- Outcome: Vary supported settling, fragmentation and flow parameters; identify rankings that change.
- Area: historical acceptance contract; original/canonical wave: 4; publication wave: W12.
- Prerequisites: ER-007, ER-008, ER-009.
- Acceptance: Vary supported settling, fragmentation and flow parameters; identify rankings that change.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P12-01 — Partition uncertainty sources

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Input, parameter, numerical, structural and stochastic uncertainty have separate records and no implied equivalence.
- Area: Uncertainty reveals ranking reversals; original/canonical wave: W12; publication wave: W12.
- Prerequisites: ER-P11-07.
- Acceptance: Input, parameter, numerical, structural and stochastic uncertainty have separate records and no implied equivalence.
- Sources: owner-launch, ER-010.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P12-02 — Bound supported settling sensitivity

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Only literature-supported or explicitly synthetic settling ranges are sampled and classification is visible.
- Area: Uncertainty reveals ranking reversals; original/canonical wave: W12; publication wave: W12.
- Prerequisites: ER-P12-01.
- Acceptance: Only literature-supported or explicitly synthetic settling ranges are sampled and classification is visible.
- Sources: owner-launch, ER-010.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P12-03 — Conserve fragmentation sensitivity

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Class conversion under fragmentation preserves the declared conserved quantity and tracks unsupported fate.
- Area: Uncertainty reveals ranking reversals; original/canonical wave: W12; publication wave: W12.
- Prerequisites: ER-P12-01.
- Acceptance: Class conversion under fragmentation preserves the declared conserved quantity and tracks unsupported fate.
- Sources: owner-launch, ER-010.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P12-04 — Test flow parameter sensitivity

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Paired flow perturbations retain valid boundary assumptions and report metric response.
- Area: Uncertainty reveals ranking reversals; original/canonical wave: W12; publication wave: W12.
- Prerequisites: ER-P12-01.
- Acceptance: Paired flow perturbations retain valid boundary assumptions and report metric response.
- Sources: owner-launch, ER-010.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P12-05 — Expose correlated parameter sampling

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Sampling preserves declared covariance or marks unknown dependence rather than assuming independence silently.
- Area: Uncertainty reveals ranking reversals; original/canonical wave: W12; publication wave: W12.
- Prerequisites: ER-P12-01.
- Acceptance: Sampling preserves declared covariance or marks unknown dependence rather than assuming independence silently.
- Sources: owner-launch, ER-010.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P12-06 — Report ranking reversal regions

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Output identifies parameter regions where ordering changes or evidence cannot distinguish arms.
- Area: Uncertainty reveals ranking reversals; original/canonical wave: W12; publication wave: W12.
- Prerequisites: ER-P12-01.
- Acceptance: Output identifies parameter regions where ordering changes or evidence cannot distinguish arms.
- Sources: owner-launch, ER-010.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P12-07 — Retain structural unknowns

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Unmodeled pathways remain unknown instead of receiving invented probability distributions.
- Area: Uncertainty reveals ranking reversals; original/canonical wave: W12; publication wave: W12.
- Prerequisites: ER-P12-01, ER-P12-02, ER-P12-03, ER-P12-04, ER-P12-05, ER-P12-06.
- Acceptance: Unmodeled pathways remain unknown instead of receiving invented probability distributions.
- Sources: owner-launch, ER-010.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W13 — Resolution and remapping are evidence-backed

### ER-011 — Validate resolution and numerical stability

- Status: **PLANNED**; release: 0.x; basis: source_requirement; kind: historical_contract.
- Outcome: Run timestep/grid refinement and source/sink perturbations; reject unstable or nonconservative runs.
- Area: historical acceptance contract; original/canonical wave: 4; publication wave: W13.
- Prerequisites: ER-007, ER-008, ER-009.
- Acceptance: Run timestep/grid refinement and source/sink perturbations; reject unstable or nonconservative runs.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P13-01 — Measure timestep convergence

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Accepted study reports successive refinements and checks an independently justified asymptotic error criterion.
- Area: Resolution and remapping are evidence-backed; original/canonical wave: W13; publication wave: W13.
- Prerequisites: ER-P08-07, ER-P11-07.
- Acceptance: Accepted study reports successive refinements and checks an independently justified asymptotic error criterion.
- Sources: owner-launch, ER-011.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P13-02 — Measure spatial refinement

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Grid refinement preserves boundary support and documents changes in predicted stocks and fluxes.
- Area: Resolution and remapping are evidence-backed; original/canonical wave: W13; publication wave: W13.
- Prerequisites: ER-P13-01.
- Acceptance: Grid refinement preserves boundary support and documents changes in predicted stocks and fluxes.
- Sources: owner-launch, ER-011.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P13-03 — Conserve spatial remapping

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: A coarse/fine transfer test preserves integrated mass and reveals interpolation error separately.
- Area: Resolution and remapping are evidence-backed; original/canonical wave: W13; publication wave: W13.
- Prerequisites: ER-P13-01.
- Acceptance: A coarse/fine transfer test preserves integrated mass and reveals interpolation error separately.
- Sources: owner-launch, ER-011.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P13-04 — Conserve temporal exchange

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Models exchanging unequal intervals reconcile integrated flux over shared boundaries.
- Area: Resolution and remapping are evidence-backed; original/canonical wave: W13; publication wave: W13.
- Prerequisites: ER-P13-01.
- Acceptance: Models exchanging unequal intervals reconcile integrated flux over shared boundaries.
- Sources: owner-launch, ER-011.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P13-05 — Declare coupling order error

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: A manufactured coupled case measures splitting error under reduced exchange intervals.
- Area: Resolution and remapping are evidence-backed; original/canonical wave: W13; publication wave: W13.
- Prerequisites: ER-P13-01.
- Acceptance: A manufactured coupled case measures splitting error under reduced exchange intervals.
- Sources: owner-launch, ER-011.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P13-06 — Retain unstable refinement failures

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Failed finer runs remain visible and cannot be omitted to claim convergence.
- Area: Resolution and remapping are evidence-backed; original/canonical wave: W13; publication wave: W13.
- Prerequisites: ER-P13-01.
- Acceptance: Failed finer runs remain visible and cannot be omitted to claim convergence.
- Sources: owner-launch, ER-011.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P13-07 — Gate resolution-dependent rankings

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: A reversal across admitted grids blocks an unqualified intervention ranking.
- Area: Resolution and remapping are evidence-backed; original/canonical wave: W13; publication wave: W13.
- Prerequisites: ER-P13-01, ER-P13-02, ER-P13-03, ER-P13-04, ER-P13-05, ER-P13-06.
- Acceptance: A reversal across admitted grids blocks an unqualified intervention ranking.
- Sources: owner-launch, ER-011.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W14 — Calibration does not consume confirmation

### ER-012 — Create independent holdout scenarios

- Status: **PLANNED**; release: 0.x; basis: source_requirement; kind: historical_contract.
- Outcome: Reserve public or synthetic confirmation conditions before search; state whether they validate numerics or environmental realism.
- Area: historical acceptance contract; original/canonical wave: 4; publication wave: W14.
- Prerequisites: ER-007, ER-008, ER-009.
- Acceptance: Reserve public or synthetic confirmation conditions before search; state whether they validate numerics or environmental realism.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P14-01 — Freeze development and holdout identities

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Scenario hashes and split rationale are retained before tuning begins.
- Area: Calibration does not consume confirmation; original/canonical wave: W14; publication wave: W14.
- Prerequisites: ER-P11-07, ER-P12-07, ER-P13-07.
- Acceptance: Scenario hashes and split rationale are retained before tuning begins.
- Sources: owner-launch, ER-012.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P14-02 — Prevent temporal and spatial leakage

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Neighboring samples are grouped or justified so holdout independence is not asserted from row separation.
- Area: Calibration does not consume confirmation; original/canonical wave: W14; publication wave: W14.
- Prerequisites: ER-P14-01.
- Acceptance: Neighboring samples are grouped or justified so holdout independence is not asserted from row separation.
- Sources: owner-launch, ER-012.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P14-03 — Declare identifiable parameter combinations

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Diagnostic reports distinguish fitted values from confounded combinations.
- Area: Calibration does not consume confirmation; original/canonical wave: W14; publication wave: W14.
- Prerequisites: ER-P14-01.
- Acceptance: Diagnostic reports distinguish fitted values from confounded combinations.
- Sources: owner-launch, ER-012.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P14-04 — Record calibration objective and bounds

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Fitting stores objective, allowed parameters, bounds, algorithm and consumed budget.
- Area: Calibration does not consume confirmation; original/canonical wave: W14; publication wave: W14.
- Prerequisites: ER-P14-01.
- Acceptance: Fitting stores objective, allowed parameters, bounds, algorithm and consumed budget.
- Sources: owner-launch, ER-012.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P14-05 — Evaluate frozen confirmation cases

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Holdout results use unchanged model and thresholds and retain all failed conditions.
- Area: Calibration does not consume confirmation; original/canonical wave: W14; publication wave: W14.
- Prerequisites: ER-P14-01.
- Acceptance: Holdout results use unchanged model and thresholds and retain all failed conditions.
- Sources: owner-launch, ER-012.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P14-06 — Reclassify consumed holdouts

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Any holdout used to revise a model becomes development evidence for the next version.
- Area: Calibration does not consume confirmation; original/canonical wave: W14; publication wave: W14.
- Prerequisites: ER-P14-01.
- Acceptance: Any holdout used to revise a model becomes development evidence for the next version.
- Sources: owner-launch, ER-012.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P14-07 — Label numerical versus environmental validation

- Status: **PLANNED**; release: 0.x; basis: proposal; kind: delivery_outcome.
- Outcome: Claims state which validation class the evidence supports and reject upgrades without observations/review.
- Area: Calibration does not consume confirmation; original/canonical wave: W14; publication wave: W14.
- Prerequisites: ER-P14-01, ER-P14-02, ER-P14-03, ER-P14-04, ER-P14-05, ER-P14-06.
- Acceptance: Claims state which validation class the evidence supports and reject upgrades without observations/review.
- Sources: owner-launch, ER-012.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W15 — Drainage adapters preserve their own physics

### ER-013 — Integrate drainage and water-network adapters

- Status: **PLANNED**; release: long-term; basis: source_requirement; kind: historical_contract.
- Outcome: Reproduce an official example per chosen engine; do not silently equate pipe quality with treatment performance.
- Area: historical acceptance contract; original/canonical wave: 5; publication wave: W15.
- Prerequisites: ER-010, ER-011, ER-012.
- Acceptance: Reproduce an official example per chosen engine; do not silently equate pipe quality with treatment performance.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P15-01 — Review drainage engine adoption

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Exact version, license, dependencies, resource needs and replacement path receive required approval before installation.
- Area: Drainage adapters preserve their own physics; original/canonical wave: W15; publication wave: W15.
- Prerequisites: ER-P14-07.
- Acceptance: Exact version, license, dependencies, resource needs and replacement path receive required approval before installation.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P15-02 — Reproduce official drainage example

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Selected engine output matches an official supported example within documented tolerances.
- Area: Drainage adapters preserve their own physics; original/canonical wave: W15; publication wave: W15.
- Prerequisites: ER-P15-01.
- Acceptance: Selected engine output matches an official supported example within documented tolerances.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P15-03 — Map drainage units and supports

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Adapter rejects incompatible units, datums and time support before execution.
- Area: Drainage adapters preserve their own physics; original/canonical wave: W15; publication wave: W15.
- Prerequisites: ER-P15-01.
- Acceptance: Adapter rejects incompatible units, datums and time support before execution.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P15-04 — Preserve drainage boundary semantics

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Rainfall, runoff and hydraulic boundaries retain engine meanings and cannot be substituted silently.
- Area: Drainage adapters preserve their own physics; original/canonical wave: W15; publication wave: W15.
- Prerequisites: ER-P15-01.
- Acceptance: Rainfall, runoff and hydraulic boundaries retain engine meanings and cannot be substituted silently.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P15-05 — Check surcharge and overflow accounting

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: An admitted overflow case reconciles volumes and pollutant destinations without losing excess water.
- Area: Drainage adapters preserve their own physics; original/canonical wave: W15; publication wave: W15.
- Prerequisites: ER-P15-01.
- Acceptance: An admitted overflow case reconciles volumes and pollutant destinations without losing excess water.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P15-06 — Record engine failure and warnings

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Nonconvergence and engine warnings propagate into invalidity decisions and retained attempt records.
- Area: Drainage adapters preserve their own physics; original/canonical wave: W15; publication wave: W15.
- Prerequisites: ER-P15-01.
- Acceptance: Nonconvergence and engine warnings propagate into invalidity decisions and retained attempt records.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P15-07 — Enforce adapter authority limits

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Untrusted executable access is gated on demonstrated isolation; a subprocess alone cannot pass the gate.
- Area: Drainage adapters preserve their own physics; original/canonical wave: W15; publication wave: W15.
- Prerequisites: ER-P15-01, ER-P15-02, ER-P15-03, ER-P15-04, ER-P15-05, ER-P15-06.
- Acceptance: Untrusted executable access is gated on demonstrated isolation; a subprocess alone cannot pass the gate.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W16 — Pressurized water models retain distinct claims

### ER-P16-01 — Review network solver contract

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Exact engine version, rights and applicability are admitted before network execution.
- Area: Pressurized water models retain distinct claims; original/canonical wave: W16; publication wave: W16.
- Prerequisites: ER-P14-07.
- Acceptance: Exact engine version, rights and applicability are admitted before network execution.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P16-02 — Reproduce official distribution example

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Pressure/flow/quality outputs reproduce a supported official example with versioned tolerances.
- Area: Pressurized water models retain distinct claims; original/canonical wave: W16; publication wave: W16.
- Prerequisites: ER-P16-01.
- Acceptance: Pressure/flow/quality outputs reproduce a supported official example with versioned tolerances.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P16-03 — Preserve junction and tank balances

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Network exchange and tank storage reconcile in a selected reference case.
- Area: Pressurized water models retain distinct claims; original/canonical wave: W16; publication wave: W16.
- Prerequisites: ER-P16-01.
- Acceptance: Network exchange and tank storage reconcile in a selected reference case.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P16-04 — Declare constituent quality semantics

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Transported constituent units and reaction assumptions are explicit and separate from treatment removal.
- Area: Pressurized water models retain distinct claims; original/canonical wave: W16; publication wave: W16.
- Prerequisites: ER-P16-01.
- Acceptance: Transported constituent units and reaction assumptions are explicit and separate from treatment removal.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P16-05 — Test water-age interpretation

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Water age output is labeled as an engine quantity without automatic health or safety inference.
- Area: Pressurized water models retain distinct claims; original/canonical wave: W16; publication wave: W16.
- Prerequisites: ER-P16-01.
- Acceptance: Water age output is labeled as an engine quantity without automatic health or safety inference.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P16-06 — Separate treatment-unit interface

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Treatment inputs/outputs require their own model card and cannot inherit network validation.
- Area: Pressurized water models retain distinct claims; original/canonical wave: W16; publication wave: W16.
- Prerequisites: ER-P16-01.
- Acceptance: Treatment inputs/outputs require their own model card and cannot inherit network validation.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P16-07 — Audit network-to-catchment exchange

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Cross-domain transfers conserve admitted quantities and reject mismatched spatial/temporal supports.
- Area: Pressurized water models retain distinct claims; original/canonical wave: W16; publication wave: W16.
- Prerequisites: ER-P16-01, ER-P16-02, ER-P16-03, ER-P16-04, ER-P16-05, ER-P16-06.
- Acceptance: Cross-domain transfers conserve admitted quantities and reject mismatched spatial/temporal supports.
- Sources: owner-launch, ER-013.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W17 — Restoration response has a declared domain

### ER-014 — Add a restoration or urban-cooling case

- Status: **PLANNED**; release: long-term; basis: source_requirement; kind: historical_contract.
- Outcome: Document supported spatial scale, public inputs and ecological/thermal response limitations.
- Area: historical acceptance contract; original/canonical wave: 5; publication wave: W17.
- Prerequisites: ER-010, ER-011, ER-012.
- Acceptance: Document supported spatial scale, public inputs and ecological/thermal response limitations.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P17-01 — Choose bounded restoration question

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Decision record selects a research question and excludes unsupported ecological outcome promises.
- Area: Restoration response has a declared domain; original/canonical wave: W17; publication wave: W17.
- Prerequisites: ER-P14-07.
- Acceptance: Decision record selects a research question and excludes unsupported ecological outcome promises.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P17-02 — Review restoration input rights

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Selected public inputs have exact coverage, permissions and missing-variable records.
- Area: Restoration response has a declared domain; original/canonical wave: W17; publication wave: W17.
- Prerequisites: ER-P17-01.
- Acceptance: Selected public inputs have exact coverage, permissions and missing-variable records.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P17-03 — Declare ecological response model

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Response equations cite evidence and supported scale; unsupported response constants are not invented.
- Area: Restoration response has a declared domain; original/canonical wave: W17; publication wave: W17.
- Prerequisites: ER-P17-01.
- Acceptance: Response equations cite evidence and supported scale; unsupported response constants are not invented.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P17-04 — Represent baseline habitat assumptions

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Initial habitat or land-cover state is versioned and distinguished from measured ecology.
- Area: Restoration response has a declared domain; original/canonical wave: W17; publication wave: W17.
- Prerequisites: ER-P17-01.
- Acceptance: Initial habitat or land-cover state is versioned and distinguished from measured ecology.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P17-05 — Expose restoration time horizons

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Delayed responses and evaluation horizon remain explicit with no instantaneous benefit assumption.
- Area: Restoration response has a declared domain; original/canonical wave: W17; publication wave: W17.
- Prerequisites: ER-P17-01.
- Acceptance: Delayed responses and evaluation horizon remain explicit with no instantaneous benefit assumption.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P17-06 — Evaluate restoration uncertainty

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Sensitivity exposes unsupported or controlling parameters and bounds interpretation accordingly.
- Area: Restoration response has a declared domain; original/canonical wave: W17; publication wave: W17.
- Prerequisites: ER-P17-01.
- Acceptance: Sensitivity exposes unsupported or controlling parameters and bounds interpretation accordingly.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P17-07 — Obtain qualified restoration review

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: A domain reviewer assesses applicability and contradictions before promoting ecological claims.
- Area: Restoration response has a declared domain; original/canonical wave: W17; publication wave: W17.
- Prerequisites: ER-P17-01, ER-P17-02, ER-P17-03, ER-P17-04, ER-P17-05, ER-P17-06.
- Acceptance: A domain reviewer assesses applicability and contradictions before promoting ecological claims.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W18 — Urban cooling respects energy boundaries

### ER-P18-01 — Select thermal quantity and support

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Study names modeled temperature or heat flux, averaging support and applicability limits.
- Area: Urban cooling respects energy boundaries; original/canonical wave: W18; publication wave: W18.
- Prerequisites: ER-P14-07.
- Acceptance: Study names modeled temperature or heat flux, averaging support and applicability limits.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P18-02 — Balance modeled energy exchanges

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: An analytic thermal control accounts for stored and exchanged energy with justified residuals.
- Area: Urban cooling respects energy boundaries; original/canonical wave: W18; publication wave: W18.
- Prerequisites: ER-P18-01.
- Acceptance: An analytic thermal control accounts for stored and exchanged energy with justified residuals.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P18-03 — Distinguish air and surface temperature

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Inputs and reports reject silent interchange between air and surface thermal quantities.
- Area: Urban cooling respects energy boundaries; original/canonical wave: W18; publication wave: W18.
- Prerequisites: ER-P18-01.
- Acceptance: Inputs and reports reject silent interchange between air and surface thermal quantities.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P18-04 — Track cooling water demand

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Admitted evaporative processes report water consumption and downstream boundary implications.
- Area: Urban cooling respects energy boundaries; original/canonical wave: W18; publication wave: W18.
- Prerequisites: ER-P18-01.
- Acceptance: Admitted evaporative processes report water consumption and downstream boundary implications.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P18-05 — Record shade and geometry assumptions

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Geometry, exposure and radiation inputs retain provenance and uncertainty.
- Area: Urban cooling respects energy boundaries; original/canonical wave: W18; publication wave: W18.
- Prerequisites: ER-P18-01.
- Acceptance: Geometry, exposure and radiation inputs retain provenance and uncertainty.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P18-06 — Test urban thermal resolution

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Temporal/spatial refinement identifies when thermal comparison ordering changes.
- Area: Urban cooling respects energy boundaries; original/canonical wave: W18; publication wave: W18.
- Prerequisites: ER-P18-01.
- Acceptance: Temporal/spatial refinement identifies when thermal comparison ordering changes.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P18-07 — Separate heat exposure from health

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Reports withhold health-effect claims absent the independently reviewed exposure/health model.
- Area: Urban cooling respects energy boundaries; original/canonical wave: W18; publication wave: W18.
- Prerequisites: ER-P18-01, ER-P18-02, ER-P18-03, ER-P18-04, ER-P18-05, ER-P18-06.
- Acceptance: Reports withhold health-effect claims absent the independently reviewed exposure/health model.
- Sources: owner-launch, ER-014.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W19 — Climate inputs retain their provenance

### ER-015 — Add climate and lifecycle scenarios

- Status: **PLANNED**; release: long-term; basis: source_requirement; kind: historical_contract.
- Outcome: Separate historical data, projections and intervention assumptions; account for energy and emissions without geoengineering control.
- Area: historical acceptance contract; original/canonical wave: 5; publication wave: W19.
- Prerequisites: ER-010, ER-011, ER-012.
- Acceptance: Separate historical data, projections and intervention assumptions; account for energy and emissions without geoengineering control.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P19-01 — Separate observations and projections

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Input records identify observed, projected and synthetic quantities throughout exports.
- Area: Climate inputs retain their provenance; original/canonical wave: W19; publication wave: W19.
- Prerequisites: ER-P14-07.
- Acceptance: Input records identify observed, projected and synthetic quantities throughout exports.
- Sources: owner-launch, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P19-02 — Record projection scenario and ensemble

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Scenario, model version, member and temporal support survive transformations.
- Area: Climate inputs retain their provenance; original/canonical wave: W19; publication wave: W19.
- Prerequisites: ER-P19-01.
- Acceptance: Scenario, model version, member and temporal support survive transformations.
- Sources: owner-launch, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P19-03 — Audit downscaling applicability

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Downscaling method documents supported scale and cannot imply new observational resolution.
- Area: Climate inputs retain their provenance; original/canonical wave: W19; publication wave: W19.
- Prerequisites: ER-P19-01.
- Acceptance: Downscaling method documents supported scale and cannot imply new observational resolution.
- Sources: owner-launch, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P19-04 — Preserve calendar and time conventions

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Calendar conversion handles leap and nonstandard calendars without silent time shifts.
- Area: Climate inputs retain their provenance; original/canonical wave: W19; publication wave: W19.
- Prerequisites: ER-P19-01.
- Acceptance: Calendar conversion handles leap and nonstandard calendars without silent time shifts.
- Sources: owner-launch, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P19-05 — Track bias-adjustment transformations

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Adjusted series retain raw parent identity, training window and method assumptions.
- Area: Climate inputs retain their provenance; original/canonical wave: W19; publication wave: W19.
- Prerequisites: ER-P19-01.
- Acceptance: Adjusted series retain raw parent identity, training window and method assumptions.
- Sources: owner-launch, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P19-06 — Test scenario robustness without probabilities

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Comparisons retain scenario disagreement without assigning unsupported likelihoods.
- Area: Climate inputs retain their provenance; original/canonical wave: W19; publication wave: W19.
- Prerequisites: ER-P19-01.
- Acceptance: Comparisons retain scenario disagreement without assigning unsupported likelihoods.
- Sources: owner-launch, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P19-07 — Exclude climate actuation interfaces

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Configuration and adapters have no hardware or geoengineering control path.
- Area: Climate inputs retain their provenance; original/canonical wave: W19; publication wave: W19.
- Prerequisites: ER-P19-01, ER-P19-02, ER-P19-03, ER-P19-04, ER-P19-05, ER-P19-06.
- Acceptance: Configuration and adapters have no hardware or geoengineering control path.
- Sources: owner-launch, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W20 — Lifecycle tradeoffs remain multidimensional

### ER-P20-01 — Declare lifecycle functional unit

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Comparisons share a stated functional unit, time horizon and system boundary.
- Area: Lifecycle tradeoffs remain multidimensional; original/canonical wave: W20; publication wave: W20.
- Prerequisites: ER-P10-07, ER-P19-07.
- Acceptance: Comparisons share a stated functional unit, time horizon and system boundary.
- Sources: owner-launch, ER-006, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P20-02 — Record energy and emissions factors

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Every factor has source/version/units and uncertainty; absent evidence remains missing.
- Area: Lifecycle tradeoffs remain multidimensional; original/canonical wave: W20; publication wave: W20.
- Prerequisites: ER-P20-01.
- Acceptance: Every factor has source/version/units and uncertainty; absent evidence remains missing.
- Sources: owner-launch, ER-006, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P20-03 — Track upstream material burdens

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Modeled manufacture and transport inventories remain linked to intervention quantities.
- Area: Lifecycle tradeoffs remain multidimensional; original/canonical wave: W20; publication wave: W20.
- Prerequisites: ER-P20-01.
- Acceptance: Modeled manufacture and transport inventories remain linked to intervention quantities.
- Sources: owner-launch, ER-006, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P20-04 — Expose waste and toxicity gaps

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Unsupported toxicity or waste impacts stay unassessed rather than zero.
- Area: Lifecycle tradeoffs remain multidimensional; original/canonical wave: W20; publication wave: W20.
- Prerequisites: ER-P20-01.
- Acceptance: Unsupported toxicity or waste impacts stay unassessed rather than zero.
- Sources: owner-launch, ER-006, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P20-05 — Report land and water demands

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Resource burdens are separately quantified with declared supports and provenance.
- Area: Lifecycle tradeoffs remain multidimensional; original/canonical wave: W20; publication wave: W20.
- Prerequisites: ER-P20-01.
- Acceptance: Resource burdens are separately quantified with declared supports and provenance.
- Sources: owner-launch, ER-006, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P20-06 — Present Pareto tradeoffs

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Non-dominated alternatives are shown without invented universal environmental weights.
- Area: Lifecycle tradeoffs remain multidimensional; original/canonical wave: W20; publication wave: W20.
- Prerequisites: ER-P20-01.
- Acceptance: Non-dominated alternatives are shown without invented universal environmental weights.
- Sources: owner-launch, ER-006, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P20-07 — Audit boundary displacement

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: A gain driven by excluded lifecycle burdens is labeled incomplete and cannot support whole-system benefit.
- Area: Lifecycle tradeoffs remain multidimensional; original/canonical wave: W20; publication wave: W20.
- Prerequisites: ER-P20-01, ER-P20-02, ER-P20-03, ER-P20-04, ER-P20-05, ER-P20-06.
- Acceptance: A gain driven by excluded lifecycle burdens is labeled incomplete and cannot support whole-system benefit.
- Sources: owner-launch, ER-006, ER-015.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W21 — Hypotheses declare evidence and falsifiers

### ER-016 — Build source-backed hypotheses

- Status: **PLANNED**; release: long-term; basis: source_requirement; kind: historical_contract.
- Outcome: Require evidence, a measurable outcome and a failure condition for every proposed intervention.
- Area: historical acceptance contract; original/canonical wave: 6; publication wave: W21.
- Prerequisites: ER-013, ER-014, ER-015.
- Acceptance: Require evidence, a measurable outcome and a failure condition for every proposed intervention.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P21-01 — Require source-backed hypothesis records

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Every proposal cites admitted evidence, measurable outcome and explicit failure condition.
- Area: Hypotheses declare evidence and falsifiers; original/canonical wave: W21; publication wave: W21.
- Prerequisites: ER-P15-07, ER-P16-07, ER-P17-07, ER-P18-07, ER-P19-07, ER-P20-07.
- Acceptance: Every proposal cites admitted evidence, measurable outcome and explicit failure condition.
- Sources: owner-launch, ER-016.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P21-02 — Constrain proposal parameter space

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Proposals outside model applicability or allowed parameter bounds are rejected before execution.
- Area: Hypotheses declare evidence and falsifiers; original/canonical wave: W21; publication wave: W21.
- Prerequisites: ER-P21-01.
- Acceptance: Proposals outside model applicability or allowed parameter bounds are rejected before execution.
- Sources: owner-launch, ER-016.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P21-03 — Protect evaluator from proposers

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: A permission test proves proposers cannot edit scoring rules, raw outcomes or accepted evidence.
- Area: Hypotheses declare evidence and falsifiers; original/canonical wave: W21; publication wave: W21.
- Prerequisites: ER-P21-01.
- Acceptance: A permission test proves proposers cannot edit scoring rules, raw outcomes or accepted evidence.
- Sources: owner-launch, ER-016.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P21-04 — Protect confirmation records

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Proposal tools cannot inspect held-out evidence during development search.
- Area: Hypotheses declare evidence and falsifiers; original/canonical wave: W21; publication wave: W21.
- Prerequisites: ER-P21-01.
- Acceptance: Proposal tools cannot inspect held-out evidence during development search.
- Sources: owner-launch, ER-016.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P21-05 — Retain rejected hypotheses

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Rejected proposals preserve reasons and provenance without entering valid run counts.
- Area: Hypotheses declare evidence and falsifiers; original/canonical wave: W21; publication wave: W21.
- Prerequisites: ER-P21-01.
- Acceptance: Rejected proposals preserve reasons and provenance without entering valid run counts.
- Sources: owner-launch, ER-016.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P21-06 — Require adverse pathway statements

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Every proposal names relevant harm/displacement pathways and evidence gaps.
- Area: Hypotheses declare evidence and falsifiers; original/canonical wave: W21; publication wave: W21.
- Prerequisites: ER-P21-01.
- Acceptance: Every proposal names relevant harm/displacement pathways and evidence gaps.
- Sources: owner-launch, ER-016.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P21-07 — Gate model-generated scientific claims

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Generated text cannot promote a hypothesis or simulation to verified environmental benefit.
- Area: Hypotheses declare evidence and falsifiers; original/canonical wave: W21; publication wave: W21.
- Prerequisites: ER-P21-01, ER-P21-02, ER-P21-03, ER-P21-04, ER-P21-05, ER-P21-06.
- Acceptance: Generated text cannot promote a hypothesis or simulation to verified environmental benefit.
- Sources: owner-launch, ER-016.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W22 — Search methods share constraints and budgets

### ER-017 — Compare budgeted search methods

- Status: **PLANNED**; release: long-term; basis: source_requirement; kind: historical_contract.
- Outcome: Use equal simulation budgets and the same ecological constraints; retain all proposals and failed runs.
- Area: historical acceptance contract; original/canonical wave: 6; publication wave: W22.
- Prerequisites: ER-013, ER-014, ER-015.
- Acceptance: Use equal simulation budgets and the same ecological constraints; retain all proposals and failed runs.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P22-01 — Implement fixed-policy benchmark

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: A frozen transparent policy set establishes baseline search performance.
- Area: Search methods share constraints and budgets; original/canonical wave: W22; publication wave: W22.
- Prerequisites: ER-P21-07.
- Acceptance: A frozen transparent policy set establishes baseline search performance.
- Sources: owner-launch, ER-017.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P22-02 — Implement seeded random search

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Seed, bounds, proposals and failures are retained for deterministic replay.
- Area: Search methods share constraints and budgets; original/canonical wave: W22; publication wave: W22.
- Prerequisites: ER-P22-01.
- Acceptance: Seed, bounds, proposals and failures are retained for deterministic replay.
- Sources: owner-launch, ER-017.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P22-03 — Bound agent proposal search

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Agent budget includes inference and simulation costs and stops at approved limits.
- Area: Search methods share constraints and budgets; original/canonical wave: W22; publication wave: W22.
- Prerequisites: ER-P22-01.
- Acceptance: Agent budget includes inference and simulation costs and stops at approved limits.
- Sources: owner-launch, ER-017.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P22-04 — Equalize search comparison resources

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Methods share declared compute budgets and ecological constraints with exceptions disclosed.
- Area: Search methods share constraints and budgets; original/canonical wave: W22; publication wave: W22.
- Prerequisites: ER-P22-01.
- Acceptance: Methods share declared compute budgets and ecological constraints with exceptions disclosed.
- Sources: owner-launch, ER-017.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P22-05 — Account for failed search attempts

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Invalid/crashed proposals consume recorded budget and remain in outcome denominators.
- Area: Search methods share constraints and budgets; original/canonical wave: W22; publication wave: W22.
- Prerequisites: ER-P22-01.
- Acceptance: Invalid/crashed proposals consume recorded budget and remain in outcome denominators.
- Sources: owner-launch, ER-017.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P22-06 — Prevent score-boundary manipulation

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Candidates that shift pollution outside evaluation boundaries fail protected constraints.
- Area: Search methods share constraints and budgets; original/canonical wave: W22; publication wave: W22.
- Prerequisites: ER-P22-01.
- Acceptance: Candidates that shift pollution outside evaluation boundaries fail protected constraints.
- Sources: owner-launch, ER-017.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P22-07 — Compare search uncertainty honestly

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Matched repetitions expose variability and no superiority claim is made from an unreplicated run.
- Area: Search methods share constraints and budgets; original/canonical wave: W22; publication wave: W22.
- Prerequisites: ER-P22-01, ER-P22-02, ER-P22-03, ER-P22-04, ER-P22-05, ER-P22-06.
- Acceptance: Matched repetitions expose variability and no superiority claim is made from an unreplicated run.
- Sources: owner-launch, ER-017.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W23 — Confirmation challenges intervention rankings

### ER-018 — Confirm robust intervention tradeoffs

- Status: **PLANNED**; release: long-term; basis: source_requirement; kind: historical_contract.
- Outcome: Retest shortlisted strategies on holdouts; reject gains that only displace pollution across the modeled boundary.
- Area: historical acceptance contract; original/canonical wave: 6; publication wave: W23.
- Prerequisites: ER-013, ER-014, ER-015.
- Acceptance: Retest shortlisted strategies on holdouts; reject gains that only displace pollution across the modeled boundary.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P23-01 — Freeze shortlisted interventions

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Candidate identities and selection criteria are committed before holdout access.
- Area: Confirmation challenges intervention rankings; original/canonical wave: W23; publication wave: W23.
- Prerequisites: ER-P14-07, ER-P22-07.
- Acceptance: Candidate identities and selection criteria are committed before holdout access.
- Sources: owner-launch, ER-018.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P23-02 — Retest on independent conditions

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Shortlisted strategies run all reserved cases with unchanged evaluator and limits.
- Area: Confirmation challenges intervention rankings; original/canonical wave: W23; publication wave: W23.
- Prerequisites: ER-P23-01.
- Acceptance: Shortlisted strategies run all reserved cases with unchanged evaluator and limits.
- Sources: owner-launch, ER-018.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P23-03 — Challenge displaced pollution pathways

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Confirmation includes admitted downstream/custody burdens and flags omitted controlling pathways.
- Area: Confirmation challenges intervention rankings; original/canonical wave: W23; publication wave: W23.
- Prerequisites: ER-P23-01.
- Acceptance: Confirmation includes admitted downstream/custody burdens and flags omitted controlling pathways.
- Sources: owner-launch, ER-018.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P23-04 — Report harmful and null findings

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Negative and indistinguishable outcomes remain visible alongside favorable comparisons.
- Area: Confirmation challenges intervention rankings; original/canonical wave: W23; publication wave: W23.
- Prerequisites: ER-P23-01.
- Acceptance: Negative and indistinguishable outcomes remain visible alongside favorable comparisons.
- Sources: owner-launch, ER-018.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P23-05 — Audit multiplicity and selection

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Claim table discloses tested candidates and selection effects with justified uncertainty treatment.
- Area: Confirmation challenges intervention rankings; original/canonical wave: W23; publication wave: W23.
- Prerequisites: ER-P23-01.
- Acceptance: Claim table discloses tested candidates and selection effects with justified uncertainty treatment.
- Sources: owner-launch, ER-018.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P23-06 — Replicate ranking calculations independently

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: A separate calculation from retained records reproduces or disputes reported ordering.
- Area: Confirmation challenges intervention rankings; original/canonical wave: W23; publication wave: W23.
- Prerequisites: ER-P23-01.
- Acceptance: A separate calculation from retained records reproduces or disputes reported ordering.
- Sources: owner-launch, ER-018.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P23-07 — Restrict robust tradeoff claims

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Only supported domains and holdout conditions appear in confirmed claims; failures narrow scope.
- Area: Confirmation challenges intervention rankings; original/canonical wave: W23; publication wave: W23.
- Prerequisites: ER-P23-01, ER-P23-02, ER-P23-03, ER-P23-04, ER-P23-05, ER-P23-06.
- Acceptance: Only supported domains and holdout conditions appear in confirmed claims; failures narrow scope.
- Sources: owner-launch, ER-018.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W24 — Study views communicate uncertainty accessibly

### ER-019 — Build a local watershed comparison view

- Status: **PLANNED**; release: long-term; basis: source_requirement; kind: historical_contract.
- Outcome: Accessible maps/tables expose units, waste destinations and uncertainty without implying real-world cleanup.
- Area: historical acceptance contract; original/canonical wave: 7; publication wave: W24.
- Prerequisites: ER-016, ER-017, ER-018.
- Acceptance: Accessible maps/tables expose units, waste destinations and uncertainty without implying real-world cleanup.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P24-01 — Navigate scenario and run lineage

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Users can traverse study, attempt and source identities without ambiguous overwrites.
- Area: Study views communicate uncertainty accessibly; original/canonical wave: W24; publication wave: W24.
- Prerequisites: ER-P23-07.
- Acceptance: Users can traverse study, attempt and source identities without ambiguous overwrites.
- Sources: owner-launch, ER-009, ER-019.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P24-02 — Inspect accessible spatial alternatives

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Every map has an equivalent usable table with units and explicit missingness.
- Area: Study views communicate uncertainty accessibly; original/canonical wave: W24; publication wave: W24.
- Prerequisites: ER-P24-01.
- Acceptance: Every map has an equivalent usable table with units and explicit missingness.
- Sources: owner-launch, ER-009, ER-019.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P24-03 — Expose custody destination drilldown

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: A selected captured quantity traces through transfers to terminal fate and uncertainty.
- Area: Study views communicate uncertainty accessibly; original/canonical wave: W24; publication wave: W24.
- Prerequisites: ER-P24-01.
- Acceptance: A selected captured quantity traces through transfers to terminal fate and uncertainty.
- Sources: owner-launch, ER-009, ER-019.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P24-04 — Compare aligned quantities only

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: UI rejects or labels mismatched units, supports, models and unassessed metrics.
- Area: Study views communicate uncertainty accessibly; original/canonical wave: W24; publication wave: W24.
- Prerequisites: ER-P24-01.
- Acceptance: UI rejects or labels mismatched units, supports, models and unassessed metrics.
- Sources: owner-launch, ER-009, ER-019.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P24-05 — Inspect uncertainty components

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Users can distinguish numerical, parameter and scenario ranges with textual explanations.
- Area: Study views communicate uncertainty accessibly; original/canonical wave: W24; publication wave: W24.
- Prerequisites: ER-P24-01.
- Acceptance: Users can distinguish numerical, parameter and scenario ranges with textual explanations.
- Sources: owner-launch, ER-009, ER-019.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P24-06 — Test keyboard and assistive workflow

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Recorded human checks cover navigation, focus, labels and comparison/export recovery.
- Area: Study views communicate uncertainty accessibly; original/canonical wave: W24; publication wave: W24.
- Prerequisites: ER-P24-01.
- Acceptance: Recorded human checks cover navigation, focus, labels and comparison/export recovery.
- Sources: owner-launch, ER-009, ER-019.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P24-07 — Preserve narrow-layout readability

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Zoom and narrow viewport checks retain data labels, warnings and usable controls.
- Area: Study views communicate uncertainty accessibly; original/canonical wave: W24; publication wave: W24.
- Prerequisites: ER-P24-01, ER-P24-02, ER-P24-03, ER-P24-04, ER-P24-05, ER-P24-06.
- Acceptance: Zoom and narrow viewport checks retain data labels, warnings and usable controls.
- Sources: owner-launch, ER-009, ER-019.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W25 — Batch execution is bounded and recoverable

### ER-020 — Add bounded batch workers

- Status: **PLANNED**; release: long-term; basis: source_requirement; kind: historical_contract.
- Outcome: Limit compute and storage; cancellation/recovery preserve completed evidence and mark partial studies.
- Area: historical acceptance contract; original/canonical wave: 7; publication wave: W25.
- Prerequisites: ER-016, ER-017, ER-018.
- Acceptance: Limit compute and storage; cancellation/recovery preserve completed evidence and mark partial studies.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P25-01 — Measure need before worker adoption

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Observed serial workload and approved resource envelope justify any added concurrency.
- Area: Batch execution is bounded and recoverable; original/canonical wave: W25; publication wave: W25.
- Prerequisites: ER-P23-07.
- Acceptance: Observed serial workload and approved resource envelope justify any added concurrency.
- Sources: owner-launch, ER-020.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P25-02 — Enforce per-study resource ceilings

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: CPU/time/storage limits stop an intentionally excessive study with retained diagnostics.
- Area: Batch execution is bounded and recoverable; original/canonical wave: W25; publication wave: W25.
- Prerequisites: ER-P25-01.
- Acceptance: CPU/time/storage limits stop an intentionally excessive study with retained diagnostics.
- Sources: owner-launch, ER-020.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P25-03 — Implement cancellation semantics

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Cancellation preserves completed evidence and identifies every unfinished attempt.
- Area: Batch execution is bounded and recoverable; original/canonical wave: W25; publication wave: W25.
- Prerequisites: ER-P25-01.
- Acceptance: Cancellation preserves completed evidence and identifies every unfinished attempt.
- Sources: owner-launch, ER-020.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P25-04 — Make retries duplicate-safe

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Repeating a failed dispatch cannot activate duplicate complete results for one attempt.
- Area: Batch execution is bounded and recoverable; original/canonical wave: W25; publication wave: W25.
- Prerequisites: ER-P25-01.
- Acceptance: Repeating a failed dispatch cannot activate duplicate complete results for one attempt.
- Sources: owner-launch, ER-020.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P25-05 — Recover interrupted worker ownership

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Expired ownership and restart tests prevent two workers from writing the same active bundle.
- Area: Batch execution is bounded and recoverable; original/canonical wave: W25; publication wave: W25.
- Prerequisites: ER-P25-01.
- Acceptance: Expired ownership and restart tests prevent two workers from writing the same active bundle.
- Sources: owner-launch, ER-020.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P25-06 — Bound artifact retention

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Retention policies preserve cited evidence and require explicit handling of dependent references.
- Area: Batch execution is bounded and recoverable; original/canonical wave: W25; publication wave: W25.
- Prerequisites: ER-P25-01.
- Acceptance: Retention policies preserve cited evidence and require explicit handling of dependent references.
- Sources: owner-launch, ER-020.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P25-07 — Demonstrate execution isolation

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Adversarial adapter access tests establish actual filesystem/network authority boundaries before untrusted execution.
- Area: Batch execution is bounded and recoverable; original/canonical wave: W25; publication wave: W25.
- Prerequisites: ER-P25-01, ER-P25-02, ER-P25-03, ER-P25-04, ER-P25-05, ER-P25-06.
- Acceptance: Adversarial adapter access tests establish actual filesystem/network authority boundaries before untrusted execution.
- Sources: owner-launch, ER-020.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W26 — Independent contributors reproduce new cases

### ER-021 — Package portable environmental studies

- Status: **PLANNED**; release: long-term; basis: source_requirement; kind: historical_contract.
- Outcome: Another contributor reproduces a case offline with lawful fixtures and complete metadata.
- Area: historical acceptance contract; original/canonical wave: 7; publication wave: W26.
- Prerequisites: ER-016, ER-017, ER-018.
- Acceptance: Another contributor reproduces a case offline with lawful fixtures and complete metadata.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P26-01 — Select second catchment transfer question

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: New case differs in declared support or forcing and records which conclusions are being challenged.
- Area: Independent contributors reproduce new cases; original/canonical wave: W26; publication wave: W26.
- Prerequisites: ER-P24-07, ER-P25-07.
- Acceptance: New case differs in declared support or forcing and records which conclusions are being challenged.
- Sources: owner-launch, ER-021, ER-022, ER-023.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-022 — Replicate a second catchment case

- Status: **PLANNED**; release: long-term; basis: source_requirement; kind: historical_contract.
- Outcome: An independent contributor reproduces a new scenario and documents transfer failures.
- Area: historical acceptance contract; original/canonical wave: 8; publication wave: W26.
- Prerequisites: ER-019, ER-020, ER-021.
- Acceptance: An independent contributor reproduces a new scenario and documents transfer failures.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-023 — Review environmental and usability claims

- Status: **PLANNED**; release: long-term; basis: source_requirement; kind: historical_contract.
- Outcome: A domain reviewer checks conservation and ecological interpretation; a user completes a comparison/export workflow.
- Area: historical acceptance contract; original/canonical wave: 8; publication wave: W26.
- Prerequisites: ER-019, ER-020, ER-021.
- Acceptance: A domain reviewer checks conservation and ecological interpretation; a user completes a comparison/export workflow.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P26-02 — Prepare lawful independent case package

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Fixture rights and complete study metadata support external reproduction without private inputs.
- Area: Independent contributors reproduce new cases; original/canonical wave: W26; publication wave: W26.
- Prerequisites: ER-P26-01.
- Acceptance: Fixture rights and complete study metadata support external reproduction without private inputs.
- Sources: owner-launch, ER-021, ER-022, ER-023.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P26-03 — Record independent execution environment

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Contributor records artifact version, platform and exact steps with no invented participant evidence.
- Area: Independent contributors reproduce new cases; original/canonical wave: W26; publication wave: W26.
- Prerequisites: ER-P26-01.
- Acceptance: Contributor records artifact version, platform and exact steps with no invented participant evidence.
- Sources: owner-launch, ER-021, ER-022, ER-023.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P26-04 — Retain transfer failures

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Discrepancies, unsupported inputs and failed assumptions remain published evidence.
- Area: Independent contributors reproduce new cases; original/canonical wave: W26; publication wave: W26.
- Prerequisites: ER-P26-01.
- Acceptance: Discrepancies, unsupported inputs and failed assumptions remain published evidence.
- Sources: owner-launch, ER-021, ER-022, ER-023.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P26-05 — Reconcile reproduction differences

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Independent results compare hashes, numerical tolerances and model assumptions before resolving disagreement.
- Area: Independent contributors reproduce new cases; original/canonical wave: W26; publication wave: W26.
- Prerequisites: ER-P26-01.
- Acceptance: Independent results compare hashes, numerical tolerances and model assumptions before resolving disagreement.
- Sources: owner-launch, ER-021, ER-022, ER-023.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P26-06 — Obtain conservation and interpretation review

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Qualified reviewer separately assesses accounting correctness and ecological interpretation.
- Area: Independent contributors reproduce new cases; original/canonical wave: W26; publication wave: W26.
- Prerequisites: ER-P26-01.
- Acceptance: Qualified reviewer separately assesses accounting correctness and ecological interpretation.
- Sources: owner-launch, ER-021, ER-022, ER-023.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P26-07 — Observe comparison and export usability

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: A real user completes the workflow and recorded friction drives bounded fixes.
- Area: Independent contributors reproduce new cases; original/canonical wave: W26; publication wave: W26.
- Prerequisites: ER-P26-01, ER-P26-02, ER-P26-03, ER-P26-04, ER-P26-05, ER-P26-06.
- Acceptance: A real user completes the workflow and recorded friction drives bounded fixes.
- Sources: owner-launch, ER-021, ER-022, ER-023.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## W27 — Research publication remains correctable

### ER-024 — Prepare the research preview release

- Status: **PLANNED**; release: long-term; basis: source_requirement; kind: historical_contract.
- Outcome: Include limitations, known invalid cases, source notices and maintainer approval; no field-deployment claim.
- Area: historical acceptance contract; original/canonical wave: 8; publication wave: W27.
- Prerequisites: ER-019, ER-020, ER-021.
- Acceptance: Include limitations, known invalid cases, source notices and maintainer approval; no field-deployment claim.
- Sources: foundation.
- Evidence needs: Original full acceptance is binding; mapped partial delivery cannot complete this umbrella.
- Recorded evidence: [].

### ER-P27-01 — Version portable study releases

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Study archives include original inputs, model/evaluator identity, diagnostics and exact reproduction instructions.
- Area: Research publication remains correctable; original/canonical wave: W27; publication wave: W27.
- Prerequisites: ER-P26-07.
- Acceptance: Study archives include original inputs, model/evaluator identity, diagnostics and exact reproduction instructions.
- Sources: owner-launch, ER-021, ER-024.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P27-02 — Maintain source and dependency notices

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Distributed artifacts carry applicable licenses and attribution for every included component.
- Area: Research publication remains correctable; original/canonical wave: W27; publication wave: W27.
- Prerequisites: ER-P27-01.
- Acceptance: Distributed artifacts carry applicable licenses and attribution for every included component.
- Sources: owner-launch, ER-021, ER-024.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P27-03 — Publish invalid and unsupported cases

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Release notes expose known failures and applicability limits without selective omission.
- Area: Research publication remains correctable; original/canonical wave: W27; publication wave: W27.
- Prerequisites: ER-P27-01.
- Acceptance: Release notes expose known failures and applicability limits without selective omission.
- Sources: owner-launch, ER-021, ER-024.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P27-04 — Require maintainer release decision

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Exact reviewed artifact and outstanding risks receive the required destination-specific authority.
- Area: Research publication remains correctable; original/canonical wave: W27; publication wave: W27.
- Prerequisites: ER-P27-01.
- Acceptance: Exact reviewed artifact and outstanding risks receive the required destination-specific authority.
- Sources: owner-launch, ER-021, ER-024.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P27-05 — Support corrections and retractions

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: A correction links superseded claim/artifact identity while preserving prior evidence history.
- Area: Research publication remains correctable; original/canonical wave: W27; publication wave: W27.
- Prerequisites: ER-P27-01.
- Acceptance: A correction links superseded claim/artifact identity while preserving prior evidence history.
- Sources: owner-launch, ER-021, ER-024.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P27-06 — Document support and deprecation bounds

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Users can identify supported environments, compatibility policy and migration limits.
- Area: Research publication remains correctable; original/canonical wave: W27; publication wave: W27.
- Prerequisites: ER-P27-01.
- Acceptance: Users can identify supported environments, compatibility policy and migration limits.
- Sources: owner-launch, ER-021, ER-024.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

### ER-P27-07 — Preserve no-field-action boundary

- Status: **PLANNED**; release: long-term; basis: proposal; kind: delivery_outcome.
- Outcome: Release materials and interfaces exclude physical deployment and unsupported real-world efficacy promises.
- Area: Research publication remains correctable; original/canonical wave: W27; publication wave: W27.
- Prerequisites: ER-P27-01, ER-P27-02, ER-P27-03, ER-P27-04, ER-P27-05, ER-P27-06.
- Acceptance: Release materials and interfaces exclude physical deployment and unsupported real-world efficacy promises.
- Sources: owner-launch, ER-021, ER-024.
- Evidence needs: Separate applicability, rights and qualified-review evidence before environmental interpretation.
- Recorded evidence: [].

## Source identity mapping

| Original | Treatment | Successors |
| --- | --- | --- |
| earth-rehearsal:ER-F01 | retained | ER-F01 |
| earth-rehearsal:ER-F02 | retained | ER-F02 |
| earth-rehearsal:ER-F03 | retained | ER-F03 |
| earth-rehearsal:ER-001 | expanded | ER-001, ER-B01-01, ER-B01-02, ER-B01-03, ER-B01-04, ER-B01-05, ER-B01-06, ER-B01-07, ER-B01-08, ER-P06-01, ER-P06-02, ER-P06-03, ER-P06-04, ER-P06-05, ER-P06-06, ER-P06-07 |
| earth-rehearsal:ER-002 | expanded | ER-002, ER-B01-01, ER-B01-02, ER-B01-03, ER-B01-04, ER-B01-05, ER-B01-06, ER-B01-07, ER-B01-08, ER-P07-01, ER-P07-02, ER-P07-03, ER-P07-04, ER-P07-05, ER-P07-06, ER-P07-07 |
| earth-rehearsal:ER-003 | expanded | ER-003, ER-B01-01, ER-B01-02, ER-B01-03, ER-B01-04, ER-B01-05, ER-B01-06, ER-B01-07, ER-B01-08, ER-B02-01, ER-B02-02, ER-B02-03, ER-B02-04, ER-B02-05, ER-B02-06, ER-B02-07, ER-B02-08 |
| earth-rehearsal:ER-004 | expanded | ER-004, ER-B02-01, ER-B02-02, ER-B02-03, ER-B02-04, ER-B02-05, ER-B02-06, ER-B02-07, ER-B02-08, ER-P08-01, ER-P08-02, ER-P08-03, ER-P08-04, ER-P08-05, ER-P08-06, ER-P08-07 |
| earth-rehearsal:ER-005 | expanded | ER-005, ER-B03-01, ER-B03-02, ER-B03-03, ER-B03-04, ER-B03-05, ER-B03-06, ER-B03-07, ER-B03-08, ER-P09-01, ER-P09-02, ER-P09-03, ER-P09-04, ER-P09-05, ER-P09-06, ER-P09-07 |
| earth-rehearsal:ER-006 | expanded | ER-006, ER-B03-01, ER-B03-02, ER-B03-03, ER-B03-04, ER-B03-05, ER-B03-06, ER-B03-07, ER-B03-08, ER-P10-01, ER-P10-02, ER-P10-03, ER-P10-04, ER-P10-05, ER-P10-06, ER-P10-07, ER-P20-01, ER-P20-02, ER-P20-03, ER-P20-04, ER-P20-05, ER-P20-06, ER-P20-07 |
| earth-rehearsal:ER-007 | expanded | ER-007, ER-P11-01, ER-P11-02, ER-P11-03, ER-P11-04, ER-P11-05, ER-P11-06, ER-P11-07 |
| earth-rehearsal:ER-008 | expanded | ER-008, ER-B04-01, ER-B04-02, ER-B04-03, ER-B04-04, ER-B04-05, ER-B04-06, ER-B04-07, ER-B04-08, ER-P11-01, ER-P11-02, ER-P11-03, ER-P11-04, ER-P11-05, ER-P11-06, ER-P11-07 |
| earth-rehearsal:ER-009 | expanded | ER-009, ER-B04-01, ER-B04-02, ER-B04-03, ER-B04-04, ER-B04-05, ER-B04-06, ER-B04-07, ER-B04-08, ER-P11-01, ER-P11-02, ER-P11-03, ER-P11-04, ER-P11-05, ER-P11-06, ER-P11-07, ER-P24-01, ER-P24-02, ER-P24-03, ER-P24-04, ER-P24-05, ER-P24-06, ER-P24-07 |
| earth-rehearsal:ER-010 | expanded | ER-010, ER-P12-01, ER-P12-02, ER-P12-03, ER-P12-04, ER-P12-05, ER-P12-06, ER-P12-07 |
| earth-rehearsal:ER-011 | expanded | ER-011, ER-B02-01, ER-B02-02, ER-B02-03, ER-B02-04, ER-B02-05, ER-B02-06, ER-B02-07, ER-B02-08, ER-B04-01, ER-B04-02, ER-B04-03, ER-B04-04, ER-B04-05, ER-B04-06, ER-B04-07, ER-B04-08, ER-P13-01, ER-P13-02, ER-P13-03, ER-P13-04, ER-P13-05, ER-P13-06, ER-P13-07 |
| earth-rehearsal:ER-012 | expanded | ER-012, ER-P14-01, ER-P14-02, ER-P14-03, ER-P14-04, ER-P14-05, ER-P14-06, ER-P14-07 |
| earth-rehearsal:ER-013 | expanded | ER-013, ER-P15-01, ER-P15-02, ER-P15-03, ER-P15-04, ER-P15-05, ER-P15-06, ER-P15-07, ER-P16-01, ER-P16-02, ER-P16-03, ER-P16-04, ER-P16-05, ER-P16-06, ER-P16-07 |
| earth-rehearsal:ER-014 | expanded | ER-014, ER-P17-01, ER-P17-02, ER-P17-03, ER-P17-04, ER-P17-05, ER-P17-06, ER-P17-07, ER-P18-01, ER-P18-02, ER-P18-03, ER-P18-04, ER-P18-05, ER-P18-06, ER-P18-07 |
| earth-rehearsal:ER-015 | expanded | ER-015, ER-P19-01, ER-P19-02, ER-P19-03, ER-P19-04, ER-P19-05, ER-P19-06, ER-P19-07, ER-P20-01, ER-P20-02, ER-P20-03, ER-P20-04, ER-P20-05, ER-P20-06, ER-P20-07 |
| earth-rehearsal:ER-016 | expanded | ER-016, ER-P21-01, ER-P21-02, ER-P21-03, ER-P21-04, ER-P21-05, ER-P21-06, ER-P21-07 |
| earth-rehearsal:ER-017 | expanded | ER-017, ER-P22-01, ER-P22-02, ER-P22-03, ER-P22-04, ER-P22-05, ER-P22-06, ER-P22-07 |
| earth-rehearsal:ER-018 | expanded | ER-018, ER-P23-01, ER-P23-02, ER-P23-03, ER-P23-04, ER-P23-05, ER-P23-06, ER-P23-07 |
| earth-rehearsal:ER-019 | expanded | ER-019, ER-P24-01, ER-P24-02, ER-P24-03, ER-P24-04, ER-P24-05, ER-P24-06, ER-P24-07 |
| earth-rehearsal:ER-020 | expanded | ER-020, ER-P25-01, ER-P25-02, ER-P25-03, ER-P25-04, ER-P25-05, ER-P25-06, ER-P25-07 |
| earth-rehearsal:ER-021 | expanded | ER-021, ER-B05-01, ER-B05-02, ER-B05-03, ER-B05-04, ER-B05-05, ER-B05-06, ER-B05-07, ER-B05-08, ER-P26-01, ER-P26-02, ER-P26-03, ER-P26-04, ER-P26-05, ER-P26-06, ER-P26-07, ER-P27-01, ER-P27-02, ER-P27-03, ER-P27-04, ER-P27-05, ER-P27-06, ER-P27-07 |
| earth-rehearsal:ER-022 | expanded | ER-022, ER-P26-01, ER-P26-02, ER-P26-03, ER-P26-04, ER-P26-05, ER-P26-06, ER-P26-07 |
| earth-rehearsal:ER-023 | expanded | ER-023, ER-B05-01, ER-B05-02, ER-B05-03, ER-B05-04, ER-B05-05, ER-B05-06, ER-B05-07, ER-B05-08, ER-P26-01, ER-P26-02, ER-P26-03, ER-P26-04, ER-P26-05, ER-P26-06, ER-P26-07 |
| earth-rehearsal:ER-024 | expanded | ER-024, ER-B05-01, ER-B05-02, ER-B05-03, ER-B05-04, ER-B05-05, ER-B05-06, ER-B05-07, ER-B05-08, ER-P27-01, ER-P27-02, ER-P27-03, ER-P27-04, ER-P27-05, ER-P27-06, ER-P27-07 |
