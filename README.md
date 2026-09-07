# Earth Rehearsal

**A software laboratory for cleaner water, less pollution and testable climate interventions.**

Let researchers simulate environmental interventions before proposing physical experiments: plastic interception, water treatment, runoff prevention, restoration and climate adaptation. Optimize the full system, including displaced pollution, waste disposal, energy use and ecological tradeoffs.

Created and maintained by **Lucas Santana** ([thepianistdirector](https://github.com/thepianistdirector)). [Tanduna project](https://tanduna.com/p/earth-rehearsal) · [Public repository](https://github.com/thepianistdirector/earth-rehearsal)

> **Starting from zero.** This repository currently contains project design, architecture and a contributor plan. No simulator, application, autonomous research system or benchmark result has been implemented here. All 24 build tasks are planned. Proposed capabilities below describe what we want to build.

## Who this is for

Environmental modelers, water researchers, climate-adaptation teams and open-science contributors.

## First useful experiment

Create a synthetic watershed with a transparent flow and particle mass-balance model. Compare no intervention, source reduction and simulated interception under dry and storm conditions. Report retained, escaped, captured and disposed mass, costs and uncertainties. No real treatment equipment or field experiment is part of the project.

Software experiments make it possible to compare ideas repeatedly, inspect failures and share reproducible evidence without operating physical systems. They remain bounded by the quality and applicability of their models. A convincing visualization or agent report is not independent validation.

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

## Architecture in one paragraph

Start with Python finite-volume or compartment transport models and a separate intervention accounting layer. A mass ledger tracks sources, sinks, transfer, captured material and disposal destinations. Add SWMM through an adapter for runoff/drainage and EPANET through a different adapter for distribution hydraulics/water-quality work. Neither tool is assumed to supply a validated microplastic or ecosystem model. Spatial climate and restoration models remain independent adapters with scale and coupling tests. Results are immutable software experiments with maps or plots generated from the recorded run.

Agents propose and interpret experiments; numerical engines and protected evaluators determine results. Every experiment retains its inputs, assumptions, source version, environment, resource budget and failure state.

## Build plan

| Wave | Outcome | Gate |
| --- | --- | --- |
| 1 | Watershed experiment contract | One bounded question, lawful inputs and conservation checks are defined. |
| 2 | Flow, transport and intervention kernels | The model conserves quantities and explains intervention effects. |
| 3 | First cleanup comparison | A complete synthetic watershed study is reproducible. |
| 4 | Validation and uncertainty | Fragile cleanup rankings are detected before expansion. |
| 5 | Water, restoration and climate extensions | New environmental domains have their own model evidence. |
| 6 | Agent-guided environmental experiments | Agents explore robust interventions with traceable assumptions. |
| 7 | Open study workbench | Contributors can inspect interventions and reproduce bundles. |
| 8 | Independent environmental preview | A release candidate makes only supported research claims. |

Read the [roadmap](ROADMAP.md), [24 contributor tasks](TASKS.md), [architecture](ARCHITECTURE.md), [experiment and evaluation contract](EXPERIMENTS.md), [sources and data policy](SOURCES.md) and [current state](STATUS.md). All waves are future work; a plan is not execution authorization.

## Scientific and operating boundaries

Conserve water and pollutant mass across explicit boundaries. Captured material cannot disappear; count disposal, leakage, fragmentation and energy use where modeled. Public data are not automatically licensed for redistribution. No hardware control, environmental release, field intervention or location targeting of sensitive habitats. Distinguish modeled proxies from verified ecological outcomes.

Stop ranking if mass does not close or results depend on unvalidated removal constants. If finer resolution reverses a ranking, report model uncertainty and collect better public evidence. Cut global-climate ambition before weakening the first watershed benchmark.

## Contribute

Start with [CONTRIBUTING.md](CONTRIBUTING.md). The next eligible work is the first benchmark/contract task. Implementation follows review of exact dependency choices and a maintainer-accepted bounded task. There are no install or runtime commands yet; do not interpret proposed paths or commands as an existing application.

## Related independent projects

- [Vital Rehearsal](https://github.com/thepianistdirector/vital-rehearsal): An open simulation laboratory for physiology, disease research and safer care workflows.
- [Grid Horizons](https://github.com/thepianistdirector/grid-horizons): Simulate better grids, transformers and energy systems before proposing physical changes.
- [Civic Safelab](https://github.com/thepianistdirector/civic-safelab): Test public-safety sensing in synthetic worlds while measuring privacy and false alarms.
- [Lean Model Lab](https://github.com/thepianistdirector/lean-model-lab): Find reproducible training and inference efficiency gains without hiding quality tradeoffs.
- [Research Continuum](https://github.com/thepianistdirector/research-continuum): A reproducible autonomous research system that turns hypotheses into independently checked experiments.

These repositories are independently buildable. Shared experiment formats are a design intention; there is no shared service or integration implemented today. Extract a common library only after two real implementations demonstrate the need.

## License

Original repository content is licensed under **AGPL-3.0-only**; see [LICENSE](LICENSE). Third-party data, models, papers and code retain their own terms and are not relicensed by this repository. No third-party dataset, model weights or upstream implementation is bundled in this initial planning release.
