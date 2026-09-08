# Local 0.1 verification

Observer: GPT-6 Astra root plus independent Astra numerical, runtime and visual critics. Automated/agent evidence only. Date: September 7, 2026. Environment: CPython 3.12.14, Linux x86_64. No GPU, paid compute, external solver or production dependency was used.

## Runtime and controls

`python3 -m unittest discover -s tests -v` executes 36 test methods with many invalid subcases. It includes equilibrium, half-life and zero-stock/source controls; tiny-time analytic flux; fixed fixture endpoint checks; true three-grid refinement; cap-bound refinement; nine-run and interval completeness; conservation-preserving wrong physics; strict units/ranges/nonfinite and nested JSON; missing/false custody and disposal; byte corruption; exact reproduction; parent-controlled edits; HTML injection escaping; complete CSV; and real SIGKILL before calculation and activation. Previous complete evidence survives interruptions, failed evaluation retains raw output and interrupted attempts cannot inspect as complete.

Independent runtime criticism found and reproduced two defects: subnormal positive duration produced zero steps, and nested JSON raised an uncaught recursion traceback. Both were fixed and their exact counterexamples now reject. Eighty deterministic varied-input probes also passed; these do not exhaust the support domain.

Default analytic baseline final reservoir stock is 4.789738373964693 kg; integrated outlet is 4.210261626035308 kg. The finest Euler baseline ends at 4.794600524617288 kg (report retains its exact computed binary64 value). Numerical difference is reported, not replaced by the analytic answer. Capture preserves reservoir dynamics and splits the accepted outlet transfer. Water in/out totals are each 1260 m3. These are synthetic software calculations only.

## Packaged first run

`python3 tools/package_release.py --out dist/NAME.tar.gz` creates an exclusive deterministic archive with per-source SHA-256 manifest. `python3 tools/verify_package.py dist/NAME.tar.gz --out runs/NEW_CHECK` extracts that actual archive into a fresh directory and invokes Python with `-I` and a minimal environment. Thirteen commands cover default and changed runs, inspect, reproduce, export and exported inspect, four negative controls, the actual runtime/recovery suite, plan self-tests and generated-view checks. Raw runs and evaluation reproduce identically; a changed control has a distinct study and trajectory and retains its parent hash.

The first pilot archive exposed an isolated-Python helper import failure in the plan validator. That defect was fixed, not bypassed. A later package also excludes downloaded third-party page text in favor of an original linked capability summary. Final release candidate verification is retained as a detached record beside the exact archive to avoid self-referential archive hashes. Archive verification is local on this same host; publicly obtained artifacts, another operating system and actual human reproduction remain pending.

## Report and browser

Chromium 140.0.7339.186 was an existing dev executable; missing AlmaLinux libraries were extracted only inside the project's ignored cache, without RPM installation, scriptlets or shared-host settings. Their source/license inventory is local QA evidence and they are excluded from the product. The browser remained sandboxed and used a loopback-only ephemeral debugging endpoint. No public server was exposed.

Four viewport checks: desktop 1440x1000; phone 390x844; narrow 320x780; 720x900 with CSS zoom 2 as an approximation of magnification. All have zero page-level horizontal overflow, no report scripts/remote resources, three labeled charts, semantic table headers/captions and visible keyboard focus. Horizontal tables scroll with arrow keys on narrow views. A reduced-motion preference is honored by the static no-animation report. Separate screenshots cover numerical tables, trajectories and custody. Root inspected these actual images. Screen-reader behavior and a participant's manual accessibility observation remain NOT TESTED.

A fresh critic compared neutral matched-resolution copies without metadata or the provenance mapping: the compact layout scored 19/20 versus the earlier layout's 13/20 under a fixed readability/evidence rubric. This influenced layout only and is not numerical or human validation.

## Plan integrity and scope

`python3 tools/validate_plan.py --self-test` passes twenty negative probes and verifies 221 rows, 28 active waves, 444 links, full original lineage, mappings, acyclicity, scope and generated views. `python3 tools/render_plan.py --check` detects projection drift. See plan/VALIDATION.md for the frozen original planning evidence.

Progress from launch: the checkout originally had only the accepted 27-row documentation/plan baseline and no runtime. This first active-work interval produced a running BOX-001, independent evaluator, atomic portable evidence, original long-term expansion, falsifiers and extracted-package proof. No public release, actual participant, domain review or native plan publication is claimed.
