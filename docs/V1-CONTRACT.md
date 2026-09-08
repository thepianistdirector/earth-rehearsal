# v1.0 product and evidence contract

Frozen initial scope: September 8, 2026, before downloading the observed case. Owner: Lucas Santana. Product: an offline environmental study workbench for technical contributors and reviewers. The v1.0 user can obtain a package, examine a real flow record, create a bounded comparison, challenge its quality, explore a controlled intervention and export/reproduce the evidence without developer credentials or an installed solver.

## Concrete publication outputs

1. **Observed river-flow notebook and study:** USGS station 01646500, daily mean discharge, calendar 2021–2024. Descriptive question: how do flow distributions and seasonal coverage differ between the preselected 2021–2022 and 2023–2024 periods? Show each year/month, the full denominator, missing/provisional/estimated/invalid days and exclusions. No trend significance, causal attribution, local flood prediction or cleanup efficacy is claimed. Keep an inspectable notebook, frozen raw API responses, provenance, HTML report and CSV tables.
2. **Controlled intervention and custody experiment:** a predeclared finite-capacity example exposes saturation, intermittent servicing, downstream custody and leakage. Temporal aggregation/refinement and every compartment/transfer conserve quantities. Show an unfavorable or ambiguous intervention result when that is the actual result. This control remains synthetic even when a separate observed-flow study exists.
3. **Usable local workbench:** a clear entry page, command or guided local workflow, source/data-quality inspection, comparison views, errors with recovery instructions, portable bundles, export and reproducible outputs. Works offline after data acquisition; no user account or remote runtime resource is required.
4. **Public advance record:** exact input/code/output identities, original contribution, how platform tasks/agents assisted, actual test/review evidence, limitations, negative results and reproduction instructions. No invented scientific novelty, participant endorsement or native-platform completion.

## Delivery increments

| Increment | Required outcome | Existing roadmap mapping | Acceptance |
| --- | --- | --- | --- |
| 0.6 | Real observed-data source/quality/import/summary/reproduction | W07, W13, W24 | Raw-byte provenance, explicit units and daily support, retained missing/quality values, no silent fills or joins, reference arithmetic and malformed-data falsifiers, actual public-data output |
| 0.7 | Temporal coupling and complete custody control | W09, W10, W13, W20 | Independent local/global ledgers, transfers and unprocessed terminal stocks, time-boundary/step/impulse/refinement controls, no invented disposal credit |
| 0.8 | Guided offline study creation and exploration | W24, W26 | Fresh-user task flow executable without editing Python, responsive keyboard-accessible results, clear source versus assumption labels, inspect/export/reopen/reproduce |
| 0.9 | Bounded robust execution and publishable case package | W21, W23, W25, W27 | Resource ceilings, retained failures, interruption-safe new attempts, frozen case comparison, source/schema compatibility and exact packaged Linux/Mac verification |
| 1.0 | Usable supported public release | W26, W27 and inherited W05 | Actual independent public artifact run, required human/qualified and participant evidence, exact release and meaningful artifacts, accepted native public roadmap/tasks/access readback |

Version labels do not close historical tasks automatically. Partial W06–W14 and longer-term domain contracts retain their own acceptance. SWMM/EPANET, treatment efficacy, restoration, urban cooling and climate prediction are outside this narrow v1.0 release unless a separately accepted contract and dependency decision makes them necessary.

## Data and claim gates

- Ingest only documented public USGS measurements with exact retrieval request, access time, raw bytes, source identifiers, original units, approval/qualifier fields and explicit permission/attribution. Any upstream changes create a new snapshot.
- Parameter 00060 and statistic 00003 must match the requested site and one time-series identity. Reject conflicting duplicates, mixed units/sites/statistics, malformed dates, nonfinite values, unexpected pagination and unsupported quality semantics. Preserve nulls and absent days as distinct reasons.
- The analysis is descriptive, with no fitting or holdout claim. Both periods were chosen before retrieval; inspecting them consumes no claim of blinded confirmation. Site selection is a demonstration choice and does not imply representativeness.
- Daily means are not instantaneous flow. A point station is not a whole-catchment spatial field. Do not infer particle concentration, pollutant mass, treatment effect, flood peaks or real intervention efficacy from discharge alone.
- Reports expose coverage before comparisons. Do not silently rescale partial totals or fill gaps. Record provisional and estimated observations separately; show included/excluded denominators.
- Original program, scientific, external-participant and native-publication gates remain binding. Continue independent implementation while people or platform semantics are unavailable. Never fake a review or close a goal just to replace its metadata.

## Test and release floor

Reference computations must be independently expressed, with hand-checkable constant, ramp, duplicate, gap, outlier and boundary cases. Include mutated raw data, forged summaries, changed units/series/site, CSV/HTML mismatch, path traversal, output collision, interrupted write and resource-limit probes. Preserve exact v0.1 and v0.5 archives and use their matching runtimes. Future source has a development version until its full increment passes; a v1.0 label requires this contract's actual end-state evidence.
