# Contributing to Earth Rehearsal

Read [README.md](README.md), [STATUS.md](STATUS.md), the relevant [task](TASKS.md), [architecture](ARCHITECTURE.md) and [experiment contract](EXPERIMENTS.md). Artifacts are in English. Lucas Santana maintains scope and source integration.

Choose one bounded outcome and inspect its source history, prerequisites, current branch/HEAD and existing writers. Record owned files, actual checks, falsifiers and exit evidence before editing. Preserve unrelated changes. The canonical task/status ledger is `plan/tasks.json`; after changes run `python3 tools/render_plan.py`. Historical contracts and frozen source documents remain in lineage.

Use Python 3.12 and the standard library. Run:

```sh
python3 -m unittest discover -s tests -v
python3 tools/validate_plan.py --self-test
python3 tools/render_plan.py --check
python3 earth.py run --out runs/contribution
python3 earth.py inspect runs/contribution
```

Test discovery must find real assertions. Numerical tests must be able to falsify representative defects, including conservation-preserving wrong physics. Do not tune tolerances to make results pass, discard failed evidence, change a frozen study in place or treat a planning validator as a scientific result. A source change intentionally changes the runtime digest; reproduce old bundles with their matching source package.

Document behavior, relevant checks, failures and limitations in a focused contribution. New production dependencies require exact source/version/license, transitive, security, network/resource and replacement review plus missing maintainer approval before installation. No shared-host configuration, paid compute, external outreach or publication is implied by a code contribution.

Original contributions must be compatible with [AGPL-3.0-only](LICENSE). Preserve source rights and attribution. Public data are not automatically licensed for redistribution. No field intervention, equipment control, environmental release or sensitive-habitat targeting. A qualified reviewer must assess any real environmental interpretation; BOX-001's known-answer evidence cannot substitute.

Use [GitHub](https://github.com/thepianistdirector/earth-rehearsal) for source review and [Tanduna](https://tanduna.com/p/earth-rehearsal) for project coordination. Only actual supported native publication/review creates platform completion; do not assert a runner-reviewed state for externally completed work. Maintainer authorization is required for the exact release or platform update.
