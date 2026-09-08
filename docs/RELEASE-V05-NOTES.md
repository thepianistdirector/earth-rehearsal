# Earth Rehearsal v0.5.0

Earth Rehearsal v0.5 adds a local synthetic-study workbench to the original BOX-001 benchmark: source-bound compartment networks, finite capture and storage, explicit sensitivity campaigns, spatial/time/remapping controls and frozen calibration/confirmation with portable evidence.

All bundled inputs and observation files are original **A0_KNOWN_ANSWER manufactured controls**. They establish computational behavior within declared limits. Disposal, lifecycle, ecological, health and field-transport benefit remain **NOT_EVALUATED**. Human/qualified review and native Tanduna acceptance remain separately tracked requirements.

- Network reports retain every numerical/reference trajectory, class, water flux, capture event, stored stock and unknown destination.
- Campaigns retain failed, invalid and unrun samples; the example shows a prevention/capture ordering reversal.
- Resolution controls separate timestep error from spatial approximation and report profile loss alongside conserved remapping.
- Calibration retains equivalent candidate vectors and the full denominator. Holdout exposure is recorded before reading observations and prevents refitting against that cohort.
- New network/protocol inspection checks raw physics, conclusions, CSV and HTML consistency. Portable reproduction preserves frozen selection and labels replay explicitly.

Download the source archive and `SHA256SUMS`, verify the checksum and extract the source. Use Python 3.12; there is no pip install, external dataset or runtime network requirement.

```sh
python3 earth.py catchment run --out runs/first
python3 earth.py catchment inspect runs/first
python3 earth.py campaign run --out runs/campaign
python3 earth.py resolution run --out runs/resolution
python3 earth.py calibration freeze --out runs/cohort
python3 earth.py calibration fit runs/cohort --out runs/fit
python3 earth.py calibration confirm runs/cohort --fit runs/fit --out runs/confirmation
```

Open each generated `report.html`. The example ZIP contains an `index.html` linking all five verified collections. See the source's `docs/STUDIES.md` for export, reproduction, explicit replay, holdout consumption, bounds and recovery. Existing evidence directories are preserved; choose a fresh output path.

The exact source candidate passed **47 isolated packaged command outcomes and 83 tests** on Linux x86_64 with CPython 3.12.14 and independent macOS arm64 with CPython 3.12.13. The Mac run had zero skipped tests. Candidate verification records, browser observations and the distributed example ZIP verification are attached. The Mac candidate was transferred privately; it is not represented as a public download or human observation. Public-artifact verification will be recorded separately after publication.

Original source, manufactured fixtures and generated examples are AGPL-3.0-only, Lucas Santana / Earth Rehearsal. No third-party solver, dataset, model weights or browser library is bundled. The historical v0.1.0 release remains unchanged; use its matching source to reproduce old bundles.

## Post-publication evidence

The exact approved release is public. All six assets plus SHA256SUMS were downloaded without authentication and matched their approved hashes. The downloaded source passed 47 expected isolated command outcomes and 83 tests on Linux x86_64 / CPython 3.12.14 with zero skips. [Retained public-download and execution evidence](https://github.com/thepianistdirector/earth-rehearsal/blob/main/docs/evidence/v05-public-release-verification.json) preserves the full output and its scope. Fresh independent public Mac execution also passed 47 expected outcomes and 83 tests with zero skips on macOS 26.6.2 arm64 / CPython 3.12.13. [The public Mac record](https://github.com/thepianistdirector/earth-rehearsal/blob/main/docs/evidence/v05-macos-public-release-verification.json) retains its separate unauthenticated download provenance and full verifier output. Required human/qualified review, external participant evidence and native Tanduna publication remain open.
