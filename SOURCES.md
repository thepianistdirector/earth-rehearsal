# Sources, candidate tools and data policy

Official entry points inspected while preparing this plan on 2026-09-07. These links support the bounded descriptions below; they do not prove an implemented integration, available benchmark data, endorsement or scientific validity for every planned scenario.

| Source | Supported planning use |
| --- | --- |
| [EPA SWMM](https://www.epa.gov/water-research/storm-water-management-model-swmm) | Official runoff/drainage model; candidate for hydrological context, not an automatic microplastic validation. |
| [EPA EPANET](https://www.epa.gov/water-research/epanet) | Official water-distribution modeling resource; keep distribution-network claims separate from treatment efficacy. |
| [Copernicus Climate Data Store](https://climate.copernicus.eu/climate-data-store) | Public climate-data entry point; select the exact dataset, terms, resolution and supported use before ingesting it. |

## Before adopting a dependency or dataset

Record the exact official release and license, maintenance/advisory state, runtime and transitive dependencies, safe loading behavior, telemetry/network use, storage/compute cost, alternatives and rollback. A source being listed here does not authorize installation or data download. Exact versions are deliberately deferred until the implementation environment and compatibility evidence exist.

For each dataset/model, document provenance, permitted use, attribution, redistribution rights, access requirements, geography/population/time coverage, uncertainty and missing variables. Link source records to all derived artifacts. Reject incompatible terms and use an honestly labeled synthetic fixture when appropriate. Keep private information, credentials, controlled-access data and third-party assets out of this public repository.

## Evidence limits

The initial model uses a small inspectable reference implementation. Evaluate EPA SWMM and EPANET for the relevant later hydraulics boundaries, and Copernicus products for climate inputs. Specialized particle, ecosystem and climate-response solvers require separate benchmark selection.

Official tool documentation establishes the tool's stated purpose; our model cards and independent benchmarks must establish applicability to our experiment. Sources are not blanket proof for results we have not measured. The project's original documents use AGPL-3.0-only; referenced material retains its own terms.
