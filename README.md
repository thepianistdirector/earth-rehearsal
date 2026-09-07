# Earth Rehearsal

**A software laboratory for cleaner water, less pollution and testable climate interventions.**

Let researchers simulate environmental interventions before proposing physical experiments: plastic interception, water treatment, runoff prevention, restoration and climate adaptation. Optimize the full system, including displaced pollution, waste disposal, energy use and ecological tradeoffs.

Created and maintained by **Lucas Santana** ([thepianistdirector](https://github.com/thepianistdirector)). [Tanduna project](https://tanduna.com/p/earth-rehearsal) · [Public repository](https://github.com/thepianistdirector/earth-rehearsal)

> **Architecture foundation completed.** The three Wave 0 tasks are **DONE**: the architecture contract, outcome/dependency roadmap, and executable next-work packet with a standard-library plan validator. The original 24 scientific/build tasks remain **PLANNED**. No simulator, model integration, application, autonomous research runtime or scientific result is implemented. Acceptance and reproduced checks are recorded in [STATUS.md](STATUS.md).

## Who this is for

Environmental modelers, water researchers, climate-adaptation teams and open-science contributors.

## First useful experiment

Start with BOX-001, a hand-computable well-mixed reservoir under dry and storm forcing. Compare no intervention, synthetic source reduction and synthetic outlet capture. It must conserve water and pollutant mass, keep captured material in a custody ledger, reject a deliberately broken balance and label disposal and net benefit `NOT_EVALUATED`. Then grow the same contract into a synthetic watershed with spatial transport.

Software experiments make it possible to compare ideas repeatedly, inspect failures and share reproducible evidence without operating physical systems. They remain bounded by the quality and applicability of their models. A convincing visualization or agent report is not independent validation.

```mermaid
flowchart LR
  Q[Question and applicability] --> S[Versioned scenario]
  S --> N[Isolated numerical solver]
  N --> E[Protected evaluator]
  E --> L[Mass, custody, energy and uncertainty ledgers]
  L --> R[Reproducible study version]
  R --> H[Qualified human review]
```

## What we want to build

### Watershed and plastic transport

Catchment runoff, particle transport, size classes, settling/resuspension and interception; progress from an analytically testable box model to a validated spatial model.

### Clean-water process studio

Compare treatment chains and pipe-network scenarios with explicit residuals and waste destinations; do not infer potability from a simulation.

### Restoration and urban cooling

Explore wetlands, vegetation, runoff retention and heat adaptation using declared climate and ecosystem assumptions.

### Climate and lifecycle comparison

Study mitigation/adaptation scenarios with bounded public models, lifecycle boundaries and uncertainty; no geoengineering actuation.

### Experiment selection agents

Search robust interventions while accounting for cost, energy, uncertainty and ecological side effects.

Each domain keeps its own governing representation and evidence. Drainage hydraulics, particle fate, pressurized distribution, treatment units, restoration response, urban energy balance, climate inputs and lifecycle inventories do not become scientifically interchangeable because they share a scenario format.

## Architecture in one paragraph

Build a small, local study kernel around versioned scenarios, model cards, exchange contracts, run attempts, protected evaluation and immutable result bundles. Start with analytic compartments, then conservative finite-volume transport. Add SWMM through a runoff/drainage adapter and EPANET through a distinct pressurized-distribution adapter only after official examples and project-specific applicability tests pass. Climate, restoration, treatment and lifecycle models remain separate. Coupling must declare units, coordinates, time support, remapping, uncertainty and out-of-domain behavior.

Agents propose and interpret experiments; numerical engines and protected evaluators determine results. Every experiment retains inputs, assumptions, source/model/study versions, environment, resource use, negative outcomes and failure state. Execution stays local and sequential until measured workload plus replay, cancellation, recovery and isolation evidence justify another scale.

## Build plan

| Wave | Outcome | Gate |
| --- | --- | --- |
| 0 | Architecture and research-programme foundation | Maintainer reviews the contracts, dependency logic, BOX-001 packet and plan validation. |
| 1 | Watershed experiment contract | One bounded question, lawful inputs and conservation checks are defined. |
| 2 | Flow, transport and intervention kernels | The model conserves quantities and explains intervention effects. |
| 3 | First cleanup comparison | A complete synthetic watershed study is reproducible. |
| 4 | Validation and uncertainty | Fragile cleanup rankings are detected before expansion. |
| 5 | Water, restoration and climate extensions | New environmental domains have their own model evidence. |
| 6 | Agent-guided environmental experiments | Agents explore robust interventions with traceable assumptions. |
| 7 | Open study workbench | Contributors can inspect interventions and reproduce bundles. |
| 8 | Independent environmental preview | A release candidate makes only supported research claims. |

Read the [roadmap](ROADMAP.md), [27 contributor tasks](TASKS.md), [architecture](ARCHITECTURE.md), [experiment and evaluation contract](EXPERIMENTS.md), [sources and data policy](SOURCES.md) and [current state](STATUS.md). Review status is not implementation evidence; a plan is not execution authorization.

## Evidence ladder

| Scope | What it can support | What it cannot support by itself |
| --- | --- | --- |
| Known answer | Algebra, units, conservation and solver implementation | Environmental realism |
| Synthetic study | Behavior inside a declared invented scenario | Field transfer or effectiveness |
| Calibrated context | Fit to named development observations | Independent prediction |
| Independently confirmed context | Performance on frozen, withheld evidence | A different site, time, scale or intervention |
| Decision-context review | A bounded recommendation with trade-offs and qualified review | Authority for physical action or universal benefit |

## Scientific and operating boundaries

Conserve water and pollutant mass across explicit boundaries. Captured material cannot disappear; count disposal, leakage, fragmentation and energy use where modeled. Public data are not automatically licensed for redistribution. No hardware control, environmental release, field intervention or location targeting of sensitive habitats. Distinguish modeled proxies from verified ecological outcomes.

Stop ranking if mass does not close or results depend on unvalidated removal constants. If finer resolution reverses a ranking, report model uncertainty and collect better public evidence. Cut global-climate ambition before weakening the first watershed benchmark.

## Contribute

Start with [CONTRIBUTING.md](CONTRIBUTING.md). The immediate gate is maintainer review of ER-F01 through ER-F03. After acceptance, the next packet is the first ER-001 subpacket: BOX-001 scenario and analytic reference specification, fully bounded in [TASKS.md](TASKS.md). That accounting subpacket does not complete ER-001's synthetic-catchment and particle-class acceptance. There are no install or simulation commands yet; `python3 tools/validate_plan.py` checks only the repository plan.

## Related independent projects

- [Vital Rehearsal](https://github.com/thepianistdirector/vital-rehearsal): An open simulation laboratory for physiology, disease research and safer care workflows.
- [Grid Horizons](https://github.com/thepianistdirector/grid-horizons): Simulate better grids, transformers and energy systems before proposing physical changes.
- [Civic Safelab](https://github.com/thepianistdirector/civic-safelab): Test public-safety sensing in synthetic worlds while measuring privacy and false alarms.
- [Lean Model Lab](https://github.com/thepianistdirector/lean-model-lab): Find reproducible training and inference efficiency gains without hiding quality tradeoffs.
- [Research Continuum](https://github.com/thepianistdirector/research-continuum): A reproducible autonomous research system that turns hypotheses into independently checked experiments.

These repositories are independently buildable. Shared experiment formats are a design intention; there is no shared service or integration implemented today. Extract a common library only after two real implementations demonstrate the need.

## License

Original repository content is licensed under **AGPL-3.0-only**; see [LICENSE](LICENSE). Third-party data, models, papers and code retain their own terms and are not relicensed by this repository. No third-party dataset, model weights or upstream implementation is bundled in this initial planning release.
