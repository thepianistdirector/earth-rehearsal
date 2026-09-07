# Contributing to Earth Rehearsal

Read [README.md](README.md), [STATUS.md](STATUS.md), the relevant [task](TASKS.md), [architecture](ARCHITECTURE.md) and [experiment contract](EXPERIMENTS.md). Project artifacts are in English. Lucas Santana is the maintainer and decides scope and source integration.

Choose one bounded task whose prerequisites are accepted. Before implementation, agree the actual base branch/commit, owned files, acceptance evidence, available commands and resource/permission limits. One primary owner handles a coherent change. Preserve other contributors' files and avoid speculative shared infrastructure.

The repository-plan validator already runs with `python3 tools/validate_plan.py`; it checks the task graph, plan consistency, navigation and local links only. There is no simulation runtime or simulator dependency to install or run. ER-003 creates that runnable skeleton and documents its real setup/test commands. Referenced engines are candidates; do not install dependencies, download model weights or datasets, or start paid experiments without the corresponding task authority and exact dependency/data review.

A contribution should contain a focused change, why it addresses the task, actual checks and failures, reproduction inputs, source/license notices and honest limitations. Unit checks prove local behavior; benchmark agreement and independent scientific interpretation require their own evidence. Never weaken a metric, tolerance, holdout or privacy boundary to make a result pass.

Conserve water and pollutant mass across explicit boundaries. Captured material cannot disappear; count disposal, leakage, fragmentation and energy use where modeled. Public data are not automatically licensed for redistribution. No hardware control, environmental release, field intervention or location targeting of sensitive habitats. Distinguish modeled proxies from verified ecological outcomes.

Use ordinary GitHub changes for code and documentation, and the [Tanduna project](https://tanduna.com/p/earth-rehearsal) for project discussion and task coordination. Submitting a contribution does not authorize automatic merge, release, deployment or real-world action. Do not post sensitive vulnerabilities, personal data or credentials publicly; contact the maintainer through an appropriate private route if needed.

Contributions of original material must be compatible with [AGPL-3.0-only](LICENSE). Keep third-party licensing and attribution intact. Cite research precisely and avoid copying paper text or datasets into the repository without the applicable rights.
