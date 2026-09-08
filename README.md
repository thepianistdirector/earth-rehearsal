# Earth Rehearsal

**Reproduce a fictional reservoir calculation. See where the mass goes.**

Earth Rehearsal 0.1 is a local, standard-library Python tool for BOX-001: a fixed-volume, well-mixed synthetic reservoir under dry and storm forcing. Run baseline, source reduction and outlet capture; compare independent analytic and numerical trajectories; inspect water, pollutant and custody ledgers.

**[Download v0.1.0](https://github.com/thepianistdirector/earth-rehearsal/releases/tag/v0.1.0). Native Tanduna plan publication and human validation remain pending.** This calculation is `A0_KNOWN_ANSWER` evidence. It does not establish real-world cleanup, disposal, ecological, lifecycle or health benefit. The source-reduction and capture factors are fictional inputs, not measured effectiveness.

Created and maintained by **Lucas Santana** ([thepianistdirector](https://github.com/thepianistdirector)). [Public source](https://github.com/thepianistdirector/earth-rehearsal) · [Tanduna project](https://tanduna.com/projects/earth-rehearsal) · [Evidence status](STATUS.md).

## First run

Use **Python 3.12**. The public source artifact is verified on Linux with CPython 3.12; other operating systems and Python versions are not yet verified. There is no pip install, external dataset, browser dependency, account or network requirement for the calculation.

Download `earth-rehearsal-0.1.0.tar.gz` and `SHA256SUMS` from the release, verify the archive checksum and extract it. From the source package directory:

```sh
python3 earth.py run --out runs/first
python3 earth.py inspect runs/first
```

Open `runs/first/report.html` in a browser. The same directory contains the exact `study.json`, raw `result.json`, complete finest-grid `trajectories.csv`, checksummed `manifest.json` and activation marker `complete.json`. All three arms and three refinement levels are retained. HTML works without scripts or an internet connection.

The main comparison uses the finest Euler grid; the analytic result and their differences are shown separately. With default inputs, the analytic baseline ends at about **4.789738 kg in the reservoir** and **4.210262 kg through the outlet**. Numerical output is deliberately not identical: timestep refinement measures its error.

## Change and challenge the study

```sh
python3 earth.py run --source-factor 0.25 --out runs/source-quarter
python3 earth.py run --capture-fraction 0.75 --out runs/capture-three-quarters
python3 earth.py negative-control --kind conservation --out runs/broken-conservation.json
python3 earth.py negative-control --kind disposal --out runs/false-disposal.json
```

A successful negative control prints `EXPECTED_REJECTION` and writes the evaluator's reason. It never creates a complete successful result. `--kind source` and `--kind custody` test incorrect source flux and missing custody. CLI control changes retain the parent study identity in provenance.

For volume, initial mass, flow, source or duration, copy `scenarios/box-001.json`, edit supported quantities with their explicit SI units, and validate before running:

```sh
python3 earth.py validate-study my-study.json
python3 earth.py run --study my-study.json --out runs/custom
```

Keep exactly dry then storm, positive equal inflow/outflow and a fixed volume. Unsupported fields, incompatible units, invalid signs/ranges, nonfinite numbers, nonadvancing time grids and excessive step counts fail clearly. The [frozen numerical policy](docs/decisions/0002-numerical-policy.md) defines computational bounds; these are not environmental plausibility ranges. An externally edited file is a separate study; the tool does not infer its unknown parent.

## Reopen, reproduce and recover

```sh
python3 earth.py inspect runs/first
python3 earth.py reproduce runs/first --out runs/reproduced
python3 earth.py export runs/first --out runs/exported
```

`inspect` verifies retained artifacts and recomputes evaluation without executing the numerical kernel. `reproduce` requires the matching source package and writes a separate attempt with the same frozen study. `export` copies the verified portable JSON/CSV/HTML evidence into a fresh directory.

Existing output directories are never overwritten. An interrupted attempt retains its study and any available raw evidence. An attempt without `complete.json` is incomplete, even if some report files exist. Rerun its `study.json` into a new directory. A hard-killed attempt can retain `RUNNING` in `attempt.json`; absence of the completion marker remains decisive. Hash checks detect changed bytes, not the authenticity of an untrusted author. Inspect untrusted reports as you would other downloaded HTML.

## What capture means

The reservoir boundary closes as initial mass + source = final stock + escaped + captured, within the predeclared arithmetic tolerance. Captured mass is an integrated transfer into custody, through storage and then to `destination_unknown`. Terminal stored stock is zero in this fixture. Stored throughput and unknown-destination stock are not extra removal credits to add to captured mass.

Disposal, lifecycle, ecology and health remain `NOT_EVALUATED`, including for zero-capture runs. No settling, reaction, fragmentation, evaporation, groundwater, spatial variability or real intervention performance is modeled. Read [limitations](docs/LIMITATIONS.md), [the experiment contract](EXPERIMENTS.md) and [source notices](SOURCES.md).

## Verify and contribute

```sh
python3 -m unittest discover -s tests -v
python3 tools/validate_plan.py --self-test
python3 tools/render_plan.py --check
```

The runtime tests exercise controls, independent reference agreement, corruption detection and real process interruption. Plan checks validate planning consistency only. Agent tests and reviews are not human/domain validation. See [CONTRIBUTING.md](CONTRIBUTING.md) for the contributor workflow.

The [canonical plan](plan/tasks.json) contains 221 rows: 27 preserved historical contracts and 194 delivery outcomes, including 40 bounded 0.1 outcomes across five waves. The [roadmap](ROADMAP.md) retains the wider catchment, drainage, treatment, water-distribution, restoration, climate and lifecycle programme. Those later domains require their own physics, rights and evidence; BOX-001 does not complete them. [Architecture](ARCHITECTURE.md) · [Task contracts](TASKS.md).

## License

Original source, synthetic fixture and generated project artifacts are **AGPL-3.0-only**; see [LICENSE](LICENSE) and [NOTICE](NOTICE). External papers and candidate models retain their own terms. No third-party solver, dataset, font, image, model weights or production library is bundled. No field intervention, equipment control or environmental release is part of this software.
