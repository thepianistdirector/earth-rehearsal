# Earth Rehearsal contributor tasks

The three Wave 0 architecture-foundation tasks are **DONE**. All 24 original tasks remain **PLANNED** with their original IDs, acceptance text and dependency order; ER-001 additionally waits for ER-F03. [STATUS.md](STATUS.md) is the mutable progress authority. [plan/tasks.json](plan/tasks.json) is the machine-readable task/dependency contract. Update both task descriptions together when scope changes. Tanduna publication/review and task execution are separate operations.

Before an implementation task starts, bind it to an actual repository branch/commit, inspect existing paths and dependencies, identify one primary owner and record the exact verification commands available in that checkout. Proposed directory names below are ownership boundaries to establish, not claims of existing modules. Later outcome packages may need decomposition at their wave gate; do not treat all 24 as one autonomous job.

Protected across every task: evaluator/holdouts outside the task's authority, accepted evidence, unrelated source, credentials, data rights, domain safety rules and resource ceilings. No production deploy, physical system connection, external outreach or paid compute is authorized by a task description. Do not commit, push or publish unless the specific contribution task authorizes it. The maintainer reviews source contributions and scientific claims separately.

`READY_FOR_REVIEW` means the proposed deliverable exists and its local consistency checks pass. The authorized root may accept the foundation under Lucas Santana's instruction, change those tasks to `DONE` in both task contracts, and record review evidence in `STATUS.md`. It is not a simulation, runtime or scientific-evidence status.
## Wave 0 — Architecture and research-programme foundation

## ER-F01 — Establish the architecture contract

- Wave: 0; status: **DONE**; owner: architecture-foundation workstream, accepted by the authorized root on 2026-09-07.
- Dependencies: none.
- Owned scope: `ARCHITECTURE.md`, `EXPERIMENTS.md`, `SOURCES.md`.
- Acceptance: Define domain-specific solver and applicability boundaries; units and spatial/temporal/scale coupling; mass, energy, capture, disposal and lifecycle ledgers; uncertainty, identifiability, calibration and validation; versioned study/run/result contracts; negative outcomes; evaluator authority; scheduler recovery; plugin isolation; and evidence-based local-to-distributed scale triggers.
- Evidence: The named contracts and falsifiers are present in the owned documents; repository-plan validation checks navigation and the task graph.
- Nonclaim: Architecture review does not validate a scientific model, dataset, intervention or runtime.

## ER-F02 — Establish the outcome and dependency roadmap

- Wave: 0; status: **DONE**; owner: architecture-foundation workstream, accepted by the authorized root on 2026-09-07.
- Dependencies: ER-F01.
- Owned scope: `README.md`, `ROADMAP.md`, `TASKS.md`, `STATUS.md`, `CONTRIBUTING.md`.
- Acceptance: Prepend Wave 0 without replacing Waves 1–8; connect the first analytic case to the original 24 tasks; state scientific gates, external reviewer/data/resource dependencies, scope cuts, stop conditions and evidence-driven replanning triggers.
- Evidence: The roadmap exposes the critical sequence and extension join points; the original waves and task contracts remain navigable.
- Nonclaim: The roadmap assigns no calendar, compute budget, reviewer or implementation completion.

## ER-F03 — Specify the executable next-work packet and validate the repository plan

- Wave: 0; status: **DONE**; owner: architecture-foundation workstream, accepted by the authorized root on 2026-09-07.
- Dependencies: ER-F02.
- Owned scope: `EXPERIMENTS.md`, `TASKS.md`, `plan/tasks.json`, `tools/validate_plan.py`.
- Acceptance: Specify BOX-001 with sufficient equations, synthetic values, intervention arms, invalid cases, artifacts and gates to begin ER-001 without inventing science; add a standard-library validator for unique IDs, status/wave constraints, dependencies, acyclicity, Wave 0 ordering, roadmap/task navigation and local Markdown links.
- Evidence: `python3 tools/validate_plan.py` passes on the review candidate and fails if a protected graph invariant is perturbed.
- Nonclaim: The executable packet is a work contract. No CLI, numerical kernel or benchmark output exists yet.

## Next executable packet after Wave 0 acceptance

**Packet:** first ER-001 subpacket / BOX-001 scenario and analytic reference specification.

- Objective: establish a reviewable scenario/model contract and hand-verifiable expected values for the two-interval synthetic reservoir in [EXPERIMENTS.md](EXPERIMENTS.md).
- Owned paths: create `docs/benchmarks/box-001.md` and, if useful, fixtures beneath `docs/benchmarks/box-001/`; leave runtime scenarios for ER-003 and change no solver, evaluator, dependency or unrelated plan file.
- Inputs: the equations, exact fixture values, three intervention arms, conservation/custody rules and invalid cases in BOX-001; the applicability and contract rules in [ARCHITECTURE.md](ARCHITECTURE.md).
- Required output: a versioned human-readable scenario; analytic end-stock and integrated flux values for both intervals and all arms; dimension/sign table; explicit exclusions; expected ledger; applicability `A0_KNOWN_ANSWER`; and source classification `wholly_synthetic`.
- Acceptance: two independent hand calculations agree; all quantities balance algebraically; reducing the source changes only source input; capture changes only the escaped/captured split and custody; `destination_unknown` blocks disposal/net-benefit claims; and the deliberately perturbed ledger is rejected by the written acceptance rule.
- Verification available now: `python3 tools/validate_plan.py`; add no runtime command until an actual CLI exists. Record the exact source revision and review result in `STATUS.md` when executed.
- Stop/escalate: stop if a value, equation or state cannot be interpreted without a hidden unit or boundary; if an implementation dependency appears necessary; or if acceptance would require choosing real-world particle/fate parameters. Lucas approves dependencies and scope changes. A qualified freshwater-pollutant reviewer is required before ER-001 expands from this accounting case to plausible particle classes.
- Budget: documentation and hand calculation only; no network data ingestion, paid inference, cloud compute or physical action.
- Completion boundary: this subpacket establishes BOX-001 but does **not** complete ER-001. ER-001 remains open until its preserved acceptance also defines the synthetic catchment, particle classes, boundary conditions, analytic references and mass-accounting equation.

## ER-001 — Specify the first pollutant scenario

- Wave: 1; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-F03.
- Owned scope: `docs/benchmarks/`.
- Acceptance: Define the synthetic catchment, particle classes, boundary conditions, analytic references and mass-accounting equation.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-002 — Review environmental data and rights

- Wave: 1; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-001.
- Owned scope: `docs/data/`.
- Acceptance: Record exact source licenses, resolution, date coverage and missing variables; clearly label invented scenario inputs.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-003 — Build the experiment skeleton

- Wave: 1; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-001, ER-002.
- Owned scope: `src/`, `tests/`, `scenarios/`.
- Acceptance: A CLI validates units and source/sink definitions; a hand-computable no-removal case passes.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-004 — Implement the reference flow/transport model

- Wave: 2; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-001, ER-002, ER-003.
- Owned scope: `adapters/transport/`.
- Acceptance: Pass closed-box and open-boundary analytical cases with justified residual tolerances.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-005 — Implement source-reduction and capture policies

- Wave: 2; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-001, ER-002, ER-003.
- Owned scope: `src/interventions/`.
- Acceptance: Track captured and residual mass separately; no efficiency parameter can silently remove unaccounted mass.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-006 — Add disposal and lifecycle accounting

- Wave: 2; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-001, ER-002, ER-003.
- Owned scope: `src/accounting/`.
- Acceptance: Report the destination and energy assumptions for captured waste; detect double counting.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-007 — Create dry-weather and storm cases

- Wave: 3; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-004, ER-005, ER-006.
- Owned scope: `scenarios/watershed/`.
- Acceptance: Use documented synthetic flow profiles with paired random inputs and all boundary conditions saved.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-008 — Compare three intervention strategies

- Wave: 3; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-004, ER-005, ER-006, ER-007.
- Owned scope: `src/evaluation/`.
- Acceptance: Show no intervention, source reduction and capture under equal resource assumptions, including invalid runs.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-009 — Export maps, balances and limitations

- Wave: 3; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-004, ER-005, ER-006, ER-008.
- Owned scope: `src/reports/`.
- Acceptance: Every figure derives from retained run data and labels simulation, source quality and unknown ecological effects.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-010 — Test particle and flow sensitivity

- Wave: 4; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-007, ER-008, ER-009.
- Owned scope: `src/analysis/`.
- Acceptance: Vary supported settling, fragmentation and flow parameters; identify rankings that change.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-011 — Validate resolution and numerical stability

- Wave: 4; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-007, ER-008, ER-009.
- Owned scope: `tests/validation/`.
- Acceptance: Run timestep/grid refinement and source/sink perturbations; reject unstable or nonconservative runs.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-012 — Create independent holdout scenarios

- Wave: 4; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-007, ER-008, ER-009.
- Owned scope: `benchmarks/`.
- Acceptance: Reserve public or synthetic confirmation conditions before search; state whether they validate numerics or environmental realism.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-013 — Integrate drainage and water-network adapters

- Wave: 5; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-010, ER-011, ER-012.
- Owned scope: `adapters/hydraulics/`.
- Acceptance: Reproduce an official example per chosen engine; do not silently equate pipe quality with treatment performance.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-014 — Add a restoration or urban-cooling case

- Wave: 5; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-010, ER-011, ER-012.
- Owned scope: `adapters/restoration/`.
- Acceptance: Document supported spatial scale, public inputs and ecological/thermal response limitations.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-015 — Add climate and lifecycle scenarios

- Wave: 5; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-010, ER-011, ER-012.
- Owned scope: `adapters/climate/`, `src/lifecycle/`.
- Acceptance: Separate historical data, projections and intervention assumptions; account for energy and emissions without geoengineering control.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-016 — Build source-backed hypotheses

- Wave: 6; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-013, ER-014, ER-015.
- Owned scope: `src/agents/`.
- Acceptance: Require evidence, a measurable outcome and a failure condition for every proposed intervention.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-017 — Compare budgeted search methods

- Wave: 6; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-013, ER-014, ER-015.
- Owned scope: `src/search/`.
- Acceptance: Use equal simulation budgets and the same ecological constraints; retain all proposals and failed runs.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-018 — Confirm robust intervention tradeoffs

- Wave: 6; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-013, ER-014, ER-015.
- Owned scope: `src/evaluation/`.
- Acceptance: Retest shortlisted strategies on holdouts; reject gains that only displace pollution across the modeled boundary.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-019 — Build a local watershed comparison view

- Wave: 7; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-016, ER-017, ER-018.
- Owned scope: `apps/workbench/`.
- Acceptance: Accessible maps/tables expose units, waste destinations and uncertainty without implying real-world cleanup.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-020 — Add bounded batch workers

- Wave: 7; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-016, ER-017, ER-018.
- Owned scope: `src/workers/`.
- Acceptance: Limit compute and storage; cancellation/recovery preserve completed evidence and mark partial studies.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-021 — Package portable environmental studies

- Wave: 7; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-016, ER-017, ER-018.
- Owned scope: `src/export/`.
- Acceptance: Another contributor reproduces a case offline with lawful fixtures and complete metadata.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-022 — Replicate a second catchment case

- Wave: 8; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-019, ER-020, ER-021.
- Owned scope: `benchmarks/replication/`.
- Acceptance: An independent contributor reproduces a new scenario and documents transfer failures.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-023 — Review environmental and usability claims

- Wave: 8; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-019, ER-020, ER-021.
- Owned scope: `docs/review/`.
- Acceptance: A domain reviewer checks conservation and ecological interpretation; a user completes a comparison/export workflow.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
## ER-024 — Prepare the research preview release

- Wave: 8; status: **PLANNED**; owner: unassigned until accepted by Lucas Santana.
- Dependencies: ER-019, ER-020, ER-021.
- Owned scope: `docs/releases/`.
- Acceptance: Include limitations, known invalid cases, source notices and maintainer approval; no field-deployment claim.
- Verification: reproduce the stated observable outcome; include one representative invalid/failure case when implementing behavior. Record exact commands and source revision after the harness exists; this plan makes no claim that those commands or tests currently exist.
- Delivery: focused diff, result/diagnostics, known limitations and a concise reproduction note. Preserve unrelated work.
