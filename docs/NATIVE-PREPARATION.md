# Corrected native plan preparation

Updated September 8, 2026. The first expanded proposal received an actual **CHANGES_REQUESTED** review. Its frozen tasks and acceptance history are preserved. The supported corrected-draft action created [the current successor proposal](https://tanduna.com/p/earth-rehearsal/proposals/prp_2dd555b565fdf25a2e24a62f5f709717/tasks), observed at plan revision 1 with 221 successor tasks at revision 3. This is not a published roadmap.

The owner reconciled every successor task ID, all 28 ordered waves and all 444 dependencies from the authenticated Mac receipt against the canonical source graph. `plan/tasks.json` retains the current mappings and observations; [the review record](evidence/tanduna-review-2026-09-08.json) retains predecessor/successor identity history and the actual review limitations. Read the current provider revisions before any update.

## Apply preparation to existing successors

[plan/tanduna-preparation.json](../plan/tanduna-preparation.json) is an owner-defined, tool-neutral preparation overlay. It describes scopes, deliverables, unchanged acceptance, prerequisites, automated commands where implemented, and a specific positive procedure and failure case for every task. It must be mapped to the freshly inspected supported native schema. It is neither a task/create request nor a completed review.

BOX-001 scopes use exact current files documented in the execution record. Later delivery scopes inherit the paths of their named historical source contracts. Future paths describe intended ownership; they do not claim an implementation already exists at the observed release commit. A future task cannot start before its scientific, adoption, resource or human prerequisites. Missing implementation or reproduction instructions is an incomplete check, not permission to substitute another outcome. Any necessary future scope extension requires a new explicit owner decision at that time.

Verification cases are authored in [verification-cases.tsv](../plan/verification-cases.tsv); the six detailed corrections returned by the Mac helper are retained in [verification-procedures.json](../plan/verification-procedures.json). No observation task permits unbounded implementation fixes. The native manual-evidence field must describe the records a verifier will collect: exact artifact and environment, actual positive/rejection results, output or section references, failures/skips, performer role and scope. These records remain NOT PERFORMED until actually observed. A request to describe future evidence does not justify fabricating evidence or withholding the description.

Use the existing corrected proposal and successor IDs. Update only supported fields after readback, preserve unrelated fields and the historical/frozen predecessors, and read back exact saved values. Preserve native wave IDs when saving the graph. Update local mappings from returned revisions before resubmission. Do not import another copy of the programme.

## Platform gates

Lucas explicitly requires GPT-6 Astra only, with **no fallback and no mandatory skills**. The actual review requested explicit-none declarations where applicable. The observed completeness validator nevertheless reports `models.fallback` and `requiredSkills` missing for all 221 successor tasks. This is a platform compatibility gate to resolve through its owner and supported controls. No different model, artificial mandatory skill, fabricated review or direct database/application change is authorized by this document.

The first review was textual screening, not executed QA or scientific validation. Its UI requested Astra low, but the provider's observed model was not reported. The Mac helper's own actual model was separately verified as Astra. These evidence types remain separate.

After preparation, inspect actual completeness for every saved task. Obtain an actual new review only once known preparation gaps are resolved. Any separate required human poll action remains necessary. Finally read the public roadmap and task pages without relying on an owner's private draft view. A passing review alone is not proof of public publication.

## Local validation

```sh
python3 tools/render_plan.py --check
python3 tools/validate_plan.py --self-test
python3 tools/prepare_tanduna.py --check
```

Twenty existing negative plan probes pass. Six additional preparation probes rejected missing mappings, duplicate task IDs, swapped/unobserved successor identity, a Boolean revision, missing wave coverage and duplicate wave identity. All 221 acceptance strings and the Astra-only/no-mandatory-skills decisions were checked unchanged. These checks establish preparation consistency only; they do not claim the prospective tasks have executed or the native validator has accepted them.
