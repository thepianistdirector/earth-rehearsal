# Plan verification evidence

The September 7, 2026 expansion was validated before implementation status updates: 221 task rows, 28 active/public waves and 444 dependency links. Of the rows, 27 are preserved historical umbrella contracts and 194 are distinct delivery outcomes; 40 delivery outcomes are the bounded 0.1 route. The original nine waves remain in immutable lineage and `historicalWaves`; numeric original task waves are unchanged. Publication wave assignment is an explicit separate field.

Executed successfully:

- `python3 tools/validate_plan.py --self-test`: baseline graph, lineage hashes, original identities/acceptance/dependencies/owned paths, source-successor coverage, outcome keys, distinct delivery titles and acceptance, wave membership/order, release scope, prerequisite outcome references, status evidence and generated views.
- Twenty negative probes: missing original identity; changed frozen acceptance; missing source mapping; dangling prerequisite; dependency cycle; wrong project; duplicate outcome key; orphan assignment; later-scope dependency on 0.1; missing prerequisite outcome coverage; task ordering; wave ordering; evidence-free completion; duplicate delivery acceptance; malformed dependency; count drift; lost successor; tampered immutable history; generated-view drift; non-object root.
- `python3 tools/render_plan.py --check`: exact generated view agreement.
- `git diff --check`: no whitespace errors.

The duplicate checks detect identical normalized delivery outcomes and keys; they do not claim to solve semantic equivalence. The authored outcomes were reviewed for substantive distinctions across model contracts, custody, numerical methods, domain applicability, external evidence and publication. Original umbrella rows are explicitly historical contracts, not an extra implementation counted for each successor.

The native template fits the observed 32-wave platform limit. `${TASK_ID:...}` values are unresolved references, not server IDs. The saved draft revision, option key, created task IDs, wave IDs on update, authority and public readback remain required. This evidence does not claim any native plan was saved, accepted or published.

After any canonical status or publication change, rerender the views and rerun validation. These checks establish planning integrity, not numerical correctness, scientific validity, human review or release completion.
