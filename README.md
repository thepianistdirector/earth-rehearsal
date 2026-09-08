# Earth Rehearsal

**Run a synthetic environmental study. Follow every mass transfer. Reopen the evidence.**

The v0.5 workbench adds prescribed-flow compartment networks, finite capture and storage, sensitivity campaigns, spatial/time controls and frozen synthetic calibration to the original BOX-001 reservoir benchmark. It runs locally with the Python standard library and produces offline HTML, JSON and CSV evidence.

**[Version 0.5.0 is public](https://github.com/thepianistdirector/earth-rehearsal/releases/tag/v0.5.0). Its unauthenticated public download passes 47 packaged command outcomes and 83 tests on Linux. Independent public Mac verification, human review and native Tanduna status are tracked separately in [STATUS.md](STATUS.md).** The historical [v0.1.0 release](https://github.com/thepianistdirector/earth-rehearsal/releases/tag/v0.1.0) is preserved. Every bundled scenario is an `A0_KNOWN_ANSWER` manufactured control. No cleanup, disposal, lifecycle, ecological or health benefit is established.

Created and maintained by **Lucas Santana** ([thepianistdirector](https://github.com/thepianistdirector)). [Public source](https://github.com/thepianistdirector/earth-rehearsal) · [Tanduna project](https://tanduna.com/projects/earth-rehearsal).

## First network study

Use **Python 3.12 on Linux or macOS**. Version-specific verification is in [STATUS.md](STATUS.md); the earlier Mac v0.1 result does not verify v0.5. No pip install, external dataset, account or network connection is needed for a study. From this source directory:

```sh
python3 earth.py catchment run --out runs/catchment
python3 earth.py catchment inspect runs/catchment
```

Open `runs/catchment/report.html`. It shows the fictional network, paired strategies, water and class balances, storage and unknown fate, reference differences, source declarations and links to every retained raw run. Charts share their scale. CSV retains every time, refinement and state from both methods.

The default finest numerical baseline ends with **8.566290453 kg in compartments** and **0.433709547 kg outside the boundary**. Finite capture ends with **0.342126993 kg stored** and **0.048227506 kg released to an unknown destination**. These are different stocks. Capture changes transport and custody; it does not establish safe disposal.

```sh
python3 earth.py catchment run --source-factor 0.25 --out runs/quarter-source
python3 earth.py catchment run --capture-capacity 0.1 --out runs/small-capture
python3 earth.py catchment negative-control --kind custody --out runs/broken-custody.json
python3 earth.py catchment reproduce runs/catchment --out runs/reproduced
python3 earth.py catchment export runs/catchment --out runs/exported
```

Successful negative controls print `EXPECTED_REJECTION`. Each new run uses a fresh directory. Source-bound edits retain the parent study and declared transformation chain. The [CATCHMENT-001 contract](docs/benchmarks/CATCHMENT-001.md) defines the admitted model and computational bounds.

## Sensitivity and resolution

```sh
python3 earth.py campaign run --out runs/campaign
python3 earth.py campaign inspect runs/campaign
python3 earth.py resolution run --out runs/resolution
python3 earth.py resolution inspect runs/resolution
```

Open each `report.html`. The campaign retains all six scheduled samples, including one intentionally invalid source factor. Its valid samples demonstrate an ordering reversal between prevention and capture. Chosen samples are not a probability distribution or a global search.

The resolution control keeps total volume, initial mass and domain fixed across 1, 2, 4 and 8 cells. It separates Euler timestep error from the compartment approximation to continuous plug flow. A conservative overlap remap separately reports its mass residual and profile error. Arbitrarily changing a graph is not counted as spatial convergence.

Both commands support `reproduce BUNDLE --out NEW_DIRECTORY` and `export BUNDLE --out NEW_DIRECTORY`. Detailed schemas, budgets and failure behavior are in [the study guide](docs/STUDIES.md).

## Freeze, fit and confirm

```sh
python3 earth.py calibration freeze --out runs/cohort
python3 earth.py calibration fit runs/cohort --out runs/fit
python3 earth.py calibration confirm runs/cohort --fit runs/fit --out runs/confirmation
python3 earth.py calibration inspect runs/confirmation
python3 earth.py calibration reproduce runs/confirmation --out runs/confirmation-replay
```

Fitting reads development observations only. The example retains an invalid candidate and two equivalent valid capacity settings, so its identifiability remains unresolved. Confirmation keeps the selected parameters and threshold frozen. An exposure record is durably written before reading holdout observations; fitting against that cohort is then refused, including after interruption. Reproduction is labelled a frozen-selection replay and supplies no fresh holdout evidence.

The data author and freezer necessarily see these **known synthetic controls**. This workflow does not claim blinded human review, statistical independence, field calibration or environmental validation. [Fixture provenance](scenarios/calibration/README.md) states the manufactured truth. [Explicit holdout consumption](docs/STUDIES.md#consume-an-exposed-holdout) preserves old evidence when preparing a distinct new cohort.

## Preserve and challenge evidence

`inspect` verifies hashes, reconstructs physics and conclusions, and checks that CSV and HTML agree with the retained evidence. It calls neither trajectory generator. `reproduce` requires the exact matching runtime source and preserves the original evidence. `export` makes a self-contained verified copy.

An attempt without its valid completion marker is incomplete. Interrupted raw trajectories, scheduled cases and exposure records remain visible. A hard-killed process can leave `RUNNING` metadata; inspect uses the completion marker. Choose a fresh output directory for recovery. A completed campaign protocol can still contain invalid or failed samples; read its counts and scientific status.

Hashes bind retained bytes, not the authenticity of an author who controls all files. Declared rights and transformation hashes do not prove external provenance. The application has no runtime plugins, field controls or external model workers.

## Original BOX-001 benchmark

The original single-reservoir commands remain available:

```sh
python3 earth.py run --out runs/box
python3 earth.py inspect runs/box
python3 earth.py negative-control --kind conservation --out runs/box-invalid.json
```

The exact published v0.1 archive and assets remain unchanged. Use that matching source package to reproduce old v0.1 bundles; the v0.5 runtime has a different source identity. Its benchmark contract remains in [EXPERIMENTS.md](EXPERIMENTS.md).

## Verify and contribute

```sh
python3 -I -m unittest discover -s tests -v
python3 tools/validate_plan.py --self-test
python3 tools/render_plan.py --check
```

Tests cover independent closed forms, long transfer paths, local and whole-domain conservation, source rights, finite capacity, custody, rounding, forged evidence, ordering, interruption, frozen selection and holdout exposure. Agent review and automated verification do not replace human or qualified review.

The [canonical plan](plan/tasks.json) preserves 221 tasks and all 27 historical contracts. [Milestones](plan/milestones.json) track the v0.5 implementation without rewriting that history or declaring the wider environmental programme complete. [Architecture](ARCHITECTURE.md) · [Limitations](docs/LIMITATIONS.md) · [Contributing](CONTRIBUTING.md) · [v0.5 human/external review kit](docs/V05-REVIEW-KIT.md).

## License

Original source, manufactured fixtures and project-generated artifacts are **AGPL-3.0-only**; see [LICENSE](LICENSE), [NOTICE](NOTICE) and [SOURCES.md](SOURCES.md). External references retain their own terms. No third-party solver, dataset, font, model weights or production library is bundled.
