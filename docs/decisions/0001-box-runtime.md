# Decision 0001 — bounded BOX-001 runtime

Date: 2026-09-07. Decision owner: active GPT-6 Astra root under Lucas's launch instruction.

## Observed facts

Clean main at a7e2fe7bc47726798ef01364f692a4ceb53f36e1 at startup; origin is thepianistdirector/earth-rehearsal. No competing Earth Rehearsal task appeared in available task inventory. Active native Goal is keyed to task 01a07e1c-fa9c-7a91-9e37-3107e0cce52c, created and read back ACTIVE. Runtime turn_context records gpt-6-astra, high effort. Python 3.12.14 is installed. Startup load 3.09; 172 GiB memory available; 1.6 TiB disk available. No GPU or account quota is claimed. Work is sequential, CPU only and project scoped. No dependency installation is needed.

Tanduna public inspection: zero tasks, no published plan, one proposal prp_fe895b39cfcb4edf458ef951c2234dab at revision 1 in discussion. Live project identity prj_3bacba68d40085fafb027f6409b7cfdc was read from the exact public campaign page; it is not inferred from the slug. See the original [public capability summary](../evidence/platform-capabilities.md); raw page snapshots remain local inspection evidence. Git author is not configured locally; do not invent an identity.

## Source requirements

EXPERIMENTS.md at the source revision specifies BOX-001, exact two segments, three arms and whole-boundary custody accounting. The larger 24 original scientific tasks retain their acceptance; this release does not close their catchment, particle, lifecycle or human-review obligations.

## Selected implementation

Use Python 3.12 standard library, local CLI and filesystem evidence. Support is initially verified only on the available Linux/Python 3.12 runtime; other environments remain untested until observed. Modules separate strict study parsing, analytic solution, conservative explicit Euler kernel, independent raw-ledger evaluator, bundle activation and static HTML/CSV reporting. No third-party engine, service or untrusted plugin executes. Runtime has no network operation.

A versioned built-in synthetic study is serialized with explicit SI units. Exactly two dry/storm segments share fixed volume and equal inflow/outflow. Supported controls are bounded computational inputs, not plausible environmental ranges. Study changes produce a different content identity. Known schema fields only; unknown fields, booleans as quantities, inconsistent units, nonfinite numbers and unsupported forcing reject clearly.

Analytic reference uses the exponential solution, independently of explicit Euler stock/flux advancement. Evaluator reconstructs per-step and whole-run water, source, stock, outlet split and custody balances. Captured transfer enters stored and is transferred to destination_unknown: storage throughput is reported separately from terminal stock, never added twice to the boundary equation. All disposal/lifecycle/ecological/health fields remain NOT_EVALUATED.

Bundle manifest freezes study, model/evaluator version, policy, runtime and raw-data identities. New attempt directories preserve interrupted output; complete.json activates a bundle last through atomic filesystem replacement. Existing output paths are never overwritten. Inspect verifies completion, hashes and invariants without rerunning numerical execution; reproduce reads the frozen study into a new output directory. Failed attempts cannot appear complete. Original evidence remains intact.

## Alternatives and consequences

Exact-only calculation would provide no independent discretization check. Numerical-only calculation would lose a known answer. Generic unit libraries, dataframes and plotting dependencies add installation burden without helping this small fixture. A spatial or multi-domain engine expands unvalidated physics. SQLite and workers have no demonstrated need. Static accessible HTML and CSV suffice; no public server runs on this host.

Costs: bounded one-process local calculations and artifact storage. Step budget and numerical stability guards reject excessive requests before allocation. Files are retained per attempt; users explicitly manage their own evidence. Rollback removes adoption of this new version without rewriting prior manifests or historical task contracts. Future schema changes require an explicit version, never implicit migration.

## Unresolved gates

Concrete public release candidate approval remains necessary under launch sections 8–9, after local verification. Public destination recommendation: repository GitHub release v0.1.0, full source archive and example report; no hosting spend. Native Tanduna publication requires authenticated supported workflow plus concrete plan approval; public docs expose an MCP endpoint but no authenticated Tanduna connector is available in this task. A genuine external user's run and any required human/domain review remain pending. No agent review can fill those evidence fields.
