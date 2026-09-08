# Sources, candidate tools and data policy

Official documentation and peer-reviewed research inspected for the architecture foundation on 2026-09-07. Each source supports only the bounded decision shown. A listing is not dependency approval, dataset-ingestion authority, benchmark evidence, endorsement or blanket scientific validation.

## Architecture source ledger

| Source | Bounded support for this plan | Limit carried into Earth Rehearsal |
| --- | --- | --- |
| US EPA, [Guidance on the Development, Evaluation, and Application of Environmental Models](https://www.epa.gov/measurements-modeling/guidance-development-evaluation-and-application-environmental-models) (2009 guidance entry point) | Model purpose, evaluation and applicability must be explicit for environmental decision use | Guidance is not validation of this platform or any chosen model |
| US EPA, [SWMM 5.2 User's Manual](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P10145M6.TXT) | SWMM separates runoff/washoff from routing and offers routing choices with different assumptions; dynamic-wave routing solves one-dimensional Saint-Venant continuity/momentum and can represent backwater, reversal and pressurization | SWMM capability does not validate microplastic fate, site parameters, ecological outcomes or a future adapter |
| US EPA, [EPANET 2.2 User Manual](https://nepis.epa.gov/Exe/ZyPURL.cgi?Dockey=P10113EM.TXT) | Candidate boundary for pressurized network hydraulics, supported constituent transport/reaction, water age and source tracing | Distribution water quality is not treatment efficacy, potability or regulatory compliance; reaction parameters still need contextual evidence |
| US EPA, [Sustainable Materials Management hierarchy](https://www.epa.gov/smm/sustainable-materials-management-non-hazardous-materials-and-waste-management-hierarchy) | Keeps prevention/source reduction, reuse/recycling, energy recovery, treatment and disposal distinct; treatment and energy recovery still leave downstream material flows | The hierarchy is a preference framework, not a lifecycle result for captured pollutant or a license to award avoided-burden credits |
| Hein et al., [Hydro-geomorphic perspectives on microplastic distribution in freshwater river systems](https://doi.org/10.1016/j.watres.2023.120567), *Water Research* 245 (2023) | Supports modeling particle density, size, shape/biofilm, settling/resuspension and sediment storage as uncertain, interacting transport processes; riverbed sediment is not automatically a terminal sink | This review exposes knowledge gaps and heterogeneous evidence; it supplies no universal parameter values for BOX-001 or a real catchment |
| Copernicus/ECMWF, [ERA5 hourly data on single levels](https://cds.climate.copernicus.eu/datasets/reanalysis-era5-single-levels?tab=documentation) | Candidate historical/reanalysis boundary with named DOI, update/version information, quality/uncertainty documentation and CC-BY terms | Reanalysis is model-observation synthesis, not a local observation or future projection; exact variables, retrieval and terms must be frozen per study |
| IPCC AR6 WGI, [Chapter 10: Linking Global to Regional Climate Change](https://www.ipcc.ch/report/ar6/wg1/chapter/chapter-10/) | Regional climate information is fitness-for-purpose; resolution alone does not fix process errors, and forcing, model response, internal variability and observational uncertainty must remain visible | An ensemble mean/spread or downscaled cell is not a site prediction, and ensemble spread is not total uncertainty |
| IPCC AR6 Synthesis Report, [Longer Report](https://www.ipcc.ch/report/ar6/syr/longer-report/) | Adaptation can shift or amplify vulnerability and has soft/hard limits; restoration and urban adaptation need trade-off and maladaptation checks | Broad assessed findings do not validate a local wetland, cooling, flood or health response model |
| Climate and Forecast community, [CF Metadata Conventions](https://cfconventions.org/cf-conventions/cf-conventions.html) | Candidate conventions for units, coordinates, calendars, bounds, grid mappings, cell methods and scientific variable names in array data | Metadata conformance does not make two spatial/temporal supports scientifically exchangeable; coupling still needs explicit remapping and tests |
| UCAR Unidata, [UDUNITS-2 documentation](https://docs.unidata.ucar.edu/udunits/current/) | Candidate reference for parsing physical units and converting compatible quantities | Listed for evaluation only; no dependency is installed, and unit conversion cannot repair a semantic mismatch such as mass versus particle count |
| Python, [subprocess documentation](https://docs.python.org/3/library/subprocess.html) | Supports explicit executable/argument-array process adapters and documents shell/security behavior | Standard process launching is not a complete sandbox; OS-level network, filesystem and resource isolation still require platform-specific proof |

## Source and data record

Before any dependency, model, dataset or paper-derived parameter enters an accepted scenario, create a `SourceRecord` with:

- provider/author, canonical URL or DOI, title and access date;
- exact release, edition, dataset version or reproducible retrieval window;
- license and terms, required attribution, access controls, redistribution and derivative permissions;
- original format/byte identity when lawful to retain, plus every transformation and tool version;
- variables and units, spatial reference/support/resolution, temporal calendar/support/coverage and missing-data semantics;
- sampling/assimilation/model method, quality flags, uncertainty, known bias and missing variables;
- permitted study/applicability scope and prohibited interpretations; and
- whether raw data may be bundled, must be fetched by the reproducer, or must be replaced by a synthetic fixture.

Public visibility, an API response and academic citation do not imply permission to redistribute data. A paper may justify a mechanism candidate without granting rights to its supplementary data or supporting transfer of its fitted parameters. Keep controlled-access data, personal information, credentials and third-party assets out of this public repository.

## Candidate adoption gate

For each runtime dependency or external solver, record the exact official source/version/license; maintenance and advisory state; runtime, native and transitive dependencies; serialization/loading behavior; network/telemetry and credential behavior; input/output limits; compute/storage cost; malformed-output, timeout and cancellation behavior; known-answer fixture; alternatives; isolation plan; and rollback. Installation or upgrade requires separate maintainer authority.

SWMM and EPANET remain later adapter candidates. ERA5 remains a possible historical climate input. UDUNITS and a Climate and Forecast compatible array format remain interoperability candidates. BOX-001 intentionally needs none of them: its inputs are wholly synthetic and a standard-library implementation should be attempted first.

## Evidence limits and research gaps

The source ledger establishes why the architecture separates domains and what a candidate tool says it can do. It does not establish applicable parameters, calibration data, independent validation, numerical tolerances, environmental benefit or operational safety for any Earth Rehearsal study.

Before plausible freshwater particle work, obtain source-backed size/shape/density classes, settling and resuspension evidence, sampling uncertainty and a qualified freshwater-transport review. Before lifecycle comparison, define material composition, geography, collection/logistics, treatment/disposal routes, leakage, allocation/substitution method and characterization factors with a qualified lifecycle/waste review. Restoration, urban cooling and climate extensions each need context-specific observations and reviewers; one domain's acceptance cannot validate another.

Original repository content is AGPL-3.0-only. Referenced code, documentation, data and papers retain their own terms and are not relicensed by this repository.

## September 7 runtime source review

Fresh official EPA [model guidance](https://www.epa.gov/measurements-modeling/guidance-development-evaluation-and-application-environmental-models) and [SWMM overview](https://www.epa.gov/water-research/storm-water-management-model-swmm) were inspected during launch. They support explicit evaluation/applicability and the separation of later runoff, routing and water-quality domains. No EPA model code, dataset or manual is bundled or used for BOX constants. The exact wholly synthetic fixture derives from this repository's EXPERIMENTS.md at a7e2fe7bc47726798ef01364f692a4ceb53f36e1 under AGPL-3.0-only. Analytic equations and Euler implementation are original project code. Python 3.12 standard library is the only runtime requirement; no third-party production dependency has been adopted.

## September 8 manufactured-network reference

Al-Mohy and Higham (2011), [Computing the Action of the Matrix Exponential](https://eprints.maths.manchester.ac.uk/1591/), supports exponential-action methods using Taylor approximation and scaling, including affine augmentation. Earth Rehearsal uses its own small, fixed-degree bounded implementation and elementary remainder bound; it does not copy or claim the full paper algorithm. The [EPA model-evaluation guidance](https://www.epa.gov/measurements-modeling/guidance-development-evaluation-and-application-environmental-models) continues to inform the distinction between numerical checks and fit-for-purpose environmental interpretation. These references supply no catchment, particle, capacity or fate parameters. All CATCHMENT-001 quantities are original synthetic controls under this repository license. No external runtime dependency, solver, dataset or model code is adopted.


## v0.5 manufactured protocols

The normalized plug-flow mass formula, donor-cell controls, overlap remapping, finite candidate-grid loss calculation and evidence protocols are original project derivations/code. They adopt no external implementation or parameters. Calibration observations are explicitly known synthetic reference outputs with the truth and generator documented in [their fixture notice](scenarios/calibration/README.md). A reserved synthetic input is not an independent field dataset. Reference certificates and review-driven numerical corrections are documented in the benchmark; the small implementation does not claim to reproduce the full Al-Mohy–Higham algorithm.

## v0.6 observed daily-discharge admission

The first actual dataset is the USGS daily API response for station USGS-01646500, parameter 00060/statistic 00003, January 1, 2021 through December 31, 2024. [The source record](scenarios/observations/potomac-2021-2024/source.json) retains exact requests, hashes, original units, access timestamps, USGS attribution and public-domain terms. The [admission contract](docs/benchmarks/observations/USGS-DAILY-001.md) documents actual response/schema differences, quality policy, civil-date support, limits and falsifiers. [USGS API terms](https://api.waterdata.usgs.gov/ogcapi/v0/?f=html), [citation instructions](https://waterdata.usgs.gov/citation/) and [provisional conditions](https://waterdata.usgs.gov/provisional-data-statement/) were checked September 8, 2026.

The original-foot conversion follows [NIST's units table](https://www.nist.gov/document/2026-hb-133-appendix-e). No upstream implementation is copied; original Python code and a separate decimal reference perform the calculations. No sensor uncertainty, pollution concentration, device performance, intervention effect, climate attribution or review is invented. This dataset is distinct from the manufactured calibration controls.
