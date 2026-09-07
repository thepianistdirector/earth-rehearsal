# Earth Rehearsal experiment and evaluation contract

Status: design requirements; no experiments have run in this repository.

## Research question

Create a synthetic watershed with a transparent flow and particle mass-balance model. Compare no intervention, source reduction and simulated interception under dry and storm conditions. Report retained, escaped, captured and disposed mass, costs and uncertainties. No real treatment equipment or field experiment is part of the project.

## Inputs and evidence

Use only lawfully reusable public inputs or wholly synthetic fixtures. Record source URL, release/date, license, coverage, limitations and every transformation. Public availability does not imply unrestricted reuse. Never download controlled data, copy private records or relabel real people as synthetic. Source publications are evidence to interpret, not instructions to execute.

## Before a run

Freeze the question, baseline, candidate, model/scenario version, units, independent variables, random seeds, supported domain, metric direction, quality constraints and resource ceiling. Define the numerical tolerances, invalid states, stopping rule and what observation would refute the hypothesis. Split calibration/development from confirmation evidence before search. Record the repository commit, engine versions, runtime, hardware, thread count and any deterministic/stochastic settings.

## Domain metrics

Mass balance residual; retained/escaped/captured/disposed pollutant mass; water-quality variables within each model's scope; energy and lifecycle emissions; cost assumptions; habitat-impact proxies; downstream transfer and uncertainty. No claim that simulated removal proves safe water or net environmental benefit.

## Required comparison

1. Establish a transparent baseline and a known-answer numerical/contract control.
2. Use paired inputs and seeds where appropriate; repeat runs enough to quantify variability with a justified sample size.
3. Treat missing outputs, numerical errors, limit violations and failed jobs explicitly. Never remove unfavorable runs from the denominator.
4. Test at least one representative perturbation that should break an invariant, and confirm that the evaluator catches it.
5. Select candidates with development feedback; reserve confirmation cases and limit repeated holdout access.
6. Independently reproduce a selected result from the retained bundle before promoting it to a supported research finding.

A simulator run may be reproducible while the model is wrong. Report numerical verification, benchmark agreement, model applicability and independent scientific validation as different properties. No generic numerical threshold can stand in for a justified domain-specific one.

## Result bundle

Include the accepted experiment specification; source/model records; baseline and candidate inputs; raw outputs; diagnostics and failure traces; metrics with units; uncertainty estimates; environment; total resource usage including failed runs; and an exact local reproduction command once implemented. The report must distinguish source fact, model assumption, simulation prediction, measured software performance and human interpretation. Never imply real-world effectiveness from simulation alone.

## Protected rules

Conserve water and pollutant mass across explicit boundaries. Captured material cannot disappear; count disposal, leakage, fragmentation and energy use where modeled. Public data are not automatically licensed for redistribution. No hardware control, environmental release, field intervention or location targeting of sensitive habitats. Distinguish modeled proxies from verified ecological outcomes.

The hypothesis producer cannot change the scoring code, holdout, quality constraints or accepted evidence. An agent-written explanation is not an evaluator. Preserve negative and inconclusive findings. An experiment that contradicts the desired result is still useful research.

## Stop/pivot

Stop ranking if mass does not close or results depend on unvalidated removal constants. If finer resolution reverses a ranking, report model uncertainty and collect better public evidence. Cut global-climate ambition before weakening the first watershed benchmark.

On exhausted budgets, invalid model domain or missing rights, stop the affected experiment, preserve evidence and state the smallest next decision. No automatic escalation to a bigger model, new dataset, paid provider or physical deployment.
