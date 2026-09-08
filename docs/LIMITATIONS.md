# Scope and limitations

## Current observed-data increment

The pinned USGS record contains actual daily mean discharge at one point station. `OBSERVED_DESCRIPTIVE` supports summaries of that retained record only. It does not establish calibration, independent predictive confirmation, particle loads, flood peaks, climate attribution or the effects of an intervention. The two windows and station are a preselected demonstration, not a representative regional sample.

Primary statistics exclude estimated, provisional, null, absent and negative values according to the explicit [observed-data contract](benchmarks/observations/USGS-DAILY-001.md). Approved estimates are shown in a separate sensitivity. Exclusion changes the denominator; coverage is shown beside values. No missing day is filled. A daily mean is not an instantaneous observation, and no exact water-volume integral is inferred from civil date labels. Original strings, quality flags and revision metadata remain available. USGS publication approval is not review of this software or its conclusions.

Data comes from the public USGS API under its stated public-domain terms; raw bytes, source attribution and retrieval metadata are retained. A later retrieval can differ after upstream revision. A forged local manifest cannot authenticate the provider. All ordinary study commands run offline; the explicit fetch command is a bounded public HTTPS client. No third-party solver or runtime dependency is installed.

## v0.5 synthetic workbench

The implemented catchment is a prescribed-flow compartment network. It does not solve rainfall/runoff, channel momentum or hydraulic depth. Synthetic mobility/conversion classes have no asserted relationship to real particle size, density, settling, fragmentation or toxicity. Capture capacity and release/leakage rates are manufactured controls. Handling energy is an assumption, not a lifecycle result.

Water and mass accounting, independent reference certificates, normalized grid convergence, source declarations and frozen synthetic confirmation verify software behavior within their contracts. None establishes environmental applicability. No ecological, health, disposal or lifecycle benefit is evaluated. The wider hydraulic, restoration, climate and treatment domains remain planned.

Source records preserve declared permissions, current variable identity and transformation linkage. They do not independently establish external rights, original ancestry or truth. The v0.5 numerical workbench adopts no third-party production solver or dataset; the separate observed-data increment below admits a specific public USGS response. Known synthetic observation files are authored from the independent reference; the freezer and data author see them. The fitter's exclusion of holdout observation bytes is a software property, not blinded scientific validation.

The calibration grid can be incomplete or contain equivalent candidate vectors. Its reported selection is reproducible but cannot establish global parameter identifiability. Distinct holdout inputs are not proof of statistical independence. Exposure is conservatively recorded before reading the holdout, and an interrupted exposure remains consumed. Replay never becomes fresh holdout evidence.

All numerical, artifact and checkpoint budgets are defined in [STUDIES.md](STUDIES.md) and [CATCHMENT-001](benchmarks/CATCHMENT-001.md). They bound admitted work and retained artifacts, not OS-level memory, CPU or filesystem quotas. POSIX cohort locking targets Linux/macOS with Python 3.12. Version-specific package tests, browser checks and independent-machine observations must be read in [STATUS.md](../STATUS.md); earlier v0.1 evidence does not verify v0.5.

Offline reports are regenerated during inspection to check consistency with retained evidence. Hashes and self-contained receipts cannot authenticate an author who controls all files. A valid completion marker proves protocol completion only after inspection; a completed protocol can still report failed scientific thresholds or invalid samples.

## Preserved v0.1 BOX-001 scope

BOX-001 tests an accounting calculation for one fictional fixed-volume mixed reservoir. The exact study has a dry segment and a storm segment, conservative pollutant, equal inflow/outflow and three paired arms. The first-order numerical method approximates its closed-form solution; numerical error is reported and refinement is checked. Neither method establishes environmental realism.

The source and capture factors are arbitrary synthetic controls. Outlet capture changes only the escaped/captured split, not reservoir dynamics or water flow. Captured material goes through an accounting storage state to an unknown destination. No device, disposal facility, leakage probability, treatment constant or ecological response is modeled. Unknown fate is not safe disposal. No environmental, ecological, health or net lifecycle benefit is evaluated.

Supported bounds and rejected assumptions are defined in [the frozen policy](decisions/0002-numerical-policy.md). Requests within numeric bounds can still exceed the timestep budget or floating-point time resolution and are rejected. One run uses a single local process, at most 100000 numerical steps per arm across all refinement levels, and at most 256 MB per artifact file. No batch workers, untrusted plugins, downloads, remote calls, hardware control or field interventions execute. A local Python process is not a sandbox.

Verified runtime environment: Linux x86_64, CPython 3.12.14. Other Python versions, operating systems, filesystem durability behavior and assistive technologies are not claimed verified. Atomic file replacement and directory fsync are used on this Linux filesystem. Power-loss durability on other filesystems is untested. Existing evidence is never overwritten by the CLI. Hard-killed attempts can retain RUNNING metadata; only a verified complete.json marker means complete.

The finest numerical result and analytic reference can differ. Refinement agreement establishes the behavior of this discretization for this synthetic study. It does not quantify model-form, parameter, input, measurement or ecological uncertainty. Ties are explicit; a change in metric ordering across refinement levels invalidates comparison. No universal sustainability score is produced.

Portable bundles retain raw records and hashes. Hashes detect accidental changes relative to their manifest, not a malicious author who replaces the manifest and its activation record. Use the exact corresponding source package to reproduce a bundle. Reports contain no active scripts or remote resources, but arbitrary externally supplied HTML has no authenticity guarantee.

Automated tests, agent critic review, extracted-package runs and browser observations are separately recorded in [STATUS.md](../STATUS.md). A real external participant's workflow and required human review remain pending until recorded with provenance. No public product release or native Tanduna publication is implied by a local candidate.
