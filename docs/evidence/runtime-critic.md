# Independent runtime critic — 2026-09-07

Review identity: own runtime turn_context verified `gpt-6-astra`, medium effort. Leaf, read-only production review; only this evidence note and project-scoped probe artifacts were written. No human or environmental validation is claimed.

Scope: owner launch instruction, frozen decisions 0001/0002, exact fixture, all runtime modules and existing tests. Fixed rubric: exact physics and independent paths; conservation/custody; strict bounded inputs; atomic recovery; evidence claims.

## Reproduced findings

1. **P2: positive subnormal duration could complete with no numerical execution.** At the reviewed initial revision, `study.py:step_counts` used `ceil(duration / step)`. Set dry duration to `5e-324`, storm duration to zero, keeping other default inputs. Validation returned counts `[0, 0]`; `bundle.run` produced `evaluation.valid == True`, nine zero-step runs and a completion marker. Original probe retained at `runs/critic-tiny-duration`. Root subsequently changed positive-duration counts and binary64 time-grid admission. Direct independent recheck now raises `InvalidStudy: dry.duration: time grid cannot advance at binary64 precision`. **Fix observed and counterexample closed.**

2. **P2: deeply nested input escapes useful error handling.** Write `'[' * 20000 + '0' + ']' * 20000` to a project-scoped JSON file (40,001 bytes, within the study input limit), then run `python3 earth.py validate-study runs/critic-nested.json`. Observed exit 1 and full `RecursionError` traceback. `study.py:read_json` caught JSONDecodeError and UnicodeError but not RecursionError; CLI likewise did not catch it. Reject excessive nesting or wrap parser recursion as InvalidStudy. No bundle was falsely completed. **Reported to root; final fix verification pending at note creation.**

## Positive evidence and limits

- Exact default matches EXPERIMENTS.md: V=1000, M0=0, dry (3600 s, 0.1 m3/s, 0.001 kg/s), storm (1800 s, 0.5 m3/s, 0.003 kg/s), controls 0.5. Analytic exponential integration is separate from Euler; evaluator independently reconstructs source/outlet/water relations and rejects unsupported benefit claims.
- No double-counting defect found in examined terminal boundary: capture is a transfer; stored throughput is distinct from terminal stock; terminal unknown destination equals capture. Root is separately adding custody identities and parent-study provenance; those additions are outside this initial review verdict.
- 80 deterministic varied admitted-input probes (random seed 233; volume, flow, source, duration and initial mass varied across several orders; capped at 2000 coarse steps) passed all nine-run evaluations. This is numerical stress evidence, not comprehensive proof across the input domain.
- Existing suite executed during review: 35 tests passed. Recovery tests include actual killed child processes before calculation and activation, and independent reopen without calling the numerical kernel. Existing-output rejection and source-matched reproduce are exercised.
- No additional material physics, custody or atomic-completion defect established. Public distribution, actual external users, browser/manual accessibility, domain review and native Tanduna publication are not established by this review.

Root remediation verification: both findings are fixed. Positive subnormal duration rejects before allocation; the 40 KB nested JSON now produces a concise ERROR diagnostic. Full post-fix suite evidence is recorded separately.
