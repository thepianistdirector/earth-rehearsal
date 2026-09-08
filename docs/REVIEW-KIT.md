# Human review and external first-run kit

Status: **NOT PERFORMED**. This is a preparation protocol, not evidence of a participant or reviewer. No outreach has been sent. GitHub v0.1.0 is public; the released source and example hashes remain unchanged. This protocol is available separately from the frozen release archive.

## Exact release for interpretation review

Open the [v0.1.0 release](https://github.com/thepianistdirector/earth-rehearsal/releases/tag/v0.1.0). Download `earth-rehearsal-box-001-example-0.1.0.zip`, verify SHA-256 `e27ca75969fe428804cd06f04ade5e1e86509c7da4e1df0aba6b5c4013889e79`, extract it and open its `report.html`. Alternatively, generate a fresh report from the public source package using the commands below. The source asset has SHA-256 `5607260a25f7defb71b646b21ea99ef30c8c2640e6f4d5687f5c3133c697415c`; runtime digest is `13288ad265c1ef23a644fe45252520683e49f6ad78c82d2701b23141f6a39a63`. The reviewer must record which exact material they inspected. This kit is separate from the frozen source archive.

The human interpretation review should establish whether:

1. The report makes clear that the reservoir, dry/storm forcings and 0.5 controls are fictional inputs, with A0_KNOWN_ANSWER applicability.
2. Analytic results are distinguished from the finest numerical approximation and its measured error. The analytic baseline final stock is about 4.789738 kg; the numerical final stock is about 4.794601 kg. Numerical agreement is not field validation.
3. Capture leaves reservoir dynamics unchanged, and captured transfer, stored throughput and terminal unknown-destination stock cannot be mistaken for three separate removal credits.
4. Disposal, lifecycle, ecology and health remain NOT_EVALUATED. Unknown fate is not described as safe disposal or net benefit. No field-action recommendation appears.
5. The exact starting study, units, bounded editing, raw records, errors, provenance and local reproduction path are understandable.
6. Any rejected or qualified interpretation is recorded with its actual review date. This review remains pending after publication; do not backdate it or infer it from owner publication approval. A real-world environmental interpretation would require a qualified domain reviewer and new evidence; this release does not introduce one.

Record the actual reviewer role and scope. Owner approval alone is not an observation of an external first run. Do not infer technical qualification from a person's name or their approval.

## External participant workflow

The participant must obtain the actual publicly downloadable release asset independently of the developer checkout. Download the [public source archive](https://github.com/thepianistdirector/earth-rehearsal/releases/download/v0.1.0/earth-rehearsal-0.1.0.tar.gz) and [SHA256SUMS](https://github.com/thepianistdirector/earth-rehearsal/releases/download/v0.1.0/SHA256SUMS). Record the actual URL used. Verify the source checksum against both the checksum file and the source hash above, extract it into a fresh directory, and use Python 3.12. Record the actual operating system and Python version. An agent's local extraction does not satisfy this participant requirement.

From the extracted source directory:

```sh
python3 --version
python3 earth.py run --out runs/first
python3 earth.py inspect runs/first
python3 earth.py run --source-factor 0.25 --out runs/changed
python3 earth.py negative-control --kind conservation --out runs/conservation.json
python3 earth.py negative-control --kind disposal --out runs/disposal.json
python3 earth.py reproduce runs/first --out runs/reproduced
python3 earth.py export runs/first --out runs/exported
python3 earth.py inspect runs/exported
python3 -m unittest discover -s tests -p test_bundle.py -v
```

Open runs/first/report.html and runs/changed/report.html. The original run has nine source kilograms in the baseline arm, split into reservoir stock and escaped mass. Source-factor 0.25 changes the source-reduction trajectory, while the other arms retain their input conditions. Ask the participant to explain where captured mass ends up and which outcomes are not evaluated. Record their actual explanation, errors and confusion; do not replace it with the expected answer.

The final command runs the packaged recovery tests, including real SIGKILL before calculation and before activation on POSIX. Record whether those specific tests executed or were skipped. This is automated recovery evidence observed by a participant, not a manual interruption observation or proof for other platforms.

To inspect incomplete-state handling separately, the participant may make a fresh exported demonstration copy and remove only that copy's completion marker:

```sh
python3 earth.py export runs/first --out runs/incomplete-demo
python3 -c "from pathlib import Path; Path('runs/incomplete-demo/complete.json').unlink()"
python3 earth.py inspect runs/incomplete-demo
python3 earth.py run --study runs/incomplete-demo/study.json --out runs/recovered-demo
python3 earth.py inspect runs/recovered-demo
python3 earth.py inspect runs/first
```

Expected: inspecting incomplete-demo reports an incomplete attempt; a fresh run from its study succeeds; the original remains inspectable. This is explicitly a **missing-marker demonstration**, not a claim that the demonstration copy was produced by an interrupted calculation. Record real failures as failures. Never delete the original participant output or overwrite a directory to make a step pass.

## Observation record template

Leave unknown or unperformed fields blank or NOT PERFORMED. Use a participant/reviewer pseudonym and role; do not publish private identifying information.

| Field | Actual observation |
| --- | --- |
| Reviewer/participant pseudonym and role | NOT PERFORMED |
| Observation date and method | NOT PERFORMED |
| Exact public release and asset URL actually used | NOT PERFORMED |
| Asset checksum actually checked | NOT PERFORMED |
| Environment / Python version | NOT PERFORMED |
| Source package obtained without developer checkout | NOT PERFORMED |
| First-run outcome and error text | NOT PERFORMED |
| Changed-input trajectory observed | NOT PERFORMED |
| Participant's explanation of captured mass | NOT PERFORMED |
| Participant's explanation of NOT_EVALUATED outcomes | NOT PERFORMED |
| Negative-control diagnosis | NOT PERFORMED |
| Offline reopen and reproduction outcome | NOT PERFORMED |
| Real process-interruption test outcome / skipped tests | NOT PERFORMED |
| Incomplete-marker demonstration and original preservation | NOT PERFORMED |
| Keyboard/narrow-layout or assistive-technology observations | NOT PERFORMED |
| Review objections, limitations and requested corrections | NOT PERFORMED |
| Human review decision and exact scope | NOT PERFORMED |
| Maintainer disposition and retained evidence location | NOT PERFORMED |

No test checkbox automatically promotes a source task to USER VALIDATED or RELEASE VERIFIED. The root must examine the actual record, its scope and contradictions, and update only the supported canonical evidence level.

## Native Tanduna publication handoff

An authenticated owner-authorized session must first read the exact project and all owner-visible tasks, including unpublished drafts, then reconcile source IDs before creating anything. The public snapshot of zero tasks is not proof that the owner has no private drafts.

Use plan/publication.json as the canonical programme, plan/tanduna-tasks.template.json as task-preparation arguments and plan/tanduna-save-draft.template.json as the graph template. Preserve the original discussion proposal and create a new expanded-programme proposal through the supported workflow. Replace every placeholder only with a returned, scoped ID. Read current revisions before updates; retain IDs after partial failure and read back before retrying.

Current main already records the verified public v0.1.0 access instructions. Read the current canonical plan rather than the candidate-status snapshot retained inside the release archive. The plan contains 221 source rows, 28 active waves and 444 dependency links; repository evidence levels are distinct from native runner completion. Resolve required review preparation honestly; no task execution, reviewer pass, vote or acceptance can be invented to pass a platform gate.

After the supported actual review and approval/publication workflow completes, verify the public roadmap and task pages without relying on the authenticated owner's private view. Compare counts, wave ordering, dependencies, original source mappings, 0.1 horizon, implementation/evidence status and real access instructions to the canonical export. A saved draft or pending submission remains incomplete.
