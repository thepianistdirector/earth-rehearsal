#!/usr/bin/env python3
"""Validate Earth Rehearsal's task graph and local plan navigation."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import unquote


FOUNDATION_IDS = ("ER-F01", "ER-F02", "ER-F03")
ORIGINAL_IDS = tuple(f"ER-{number:03d}" for number in range(1, 25))
VALID_STATUSES = {
    "PLANNED",
    "IN_PROGRESS",
    "IN PROGRESS",
    "IMPLEMENTED",
    "AUTOMATED_PASS",
    "AUTOMATED PASS",
    "RUNTIME_VERIFIED",
    "RUNTIME VERIFIED",
    "USER_VALIDATED",
    "USER VALIDATED",
    "RELEASE_VERIFIED",
    "RELEASE VERIFIED",
    "READY_FOR_REVIEW",
    "DONE",
    "BLOCKED",
    "FAILED",
    "NOT_TESTED",
    "NOT TESTED",
}
PLAN_DOCUMENTS = (
    "README.md",
    "CONTRIBUTING.md",
    "ARCHITECTURE.md",
    "ROADMAP.md",
    "TASKS.md",
    "EXPERIMENTS.md",
    "SOURCES.md",
    "STATUS.md",
)


def fail(errors: list[str], message: str) -> None:
    errors.append(message)


def validate_acyclic(tasks: dict[str, dict], errors: list[str]) -> None:
    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(task_id: str, path: list[str]) -> None:
        if task_id in visiting:
            cycle_start = path.index(task_id)
            fail(errors, "dependency cycle: " + " -> ".join(path[cycle_start:] + [task_id]))
            return
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in tasks[task_id]["dependsOn"]:
            if dependency in tasks:
                visit(dependency, path + [task_id])
        visiting.remove(task_id)
        visited.add(task_id)

    for task_id in tasks:
        visit(task_id, [])


def validate_links(root: Path, errors: list[str]) -> None:
    link_pattern = re.compile(r"(?<!!)\[[^]]+\]\(([^)]+)\)")
    for relative_document in PLAN_DOCUMENTS:
        document = root / relative_document
        if not document.is_file():
            fail(errors, f"missing plan document: {relative_document}")
            continue
        for target in link_pattern.findall(document.read_text(encoding="utf-8")):
            target = target.strip().split(maxsplit=1)[0].strip("<>")
            if target.startswith(("http://", "https://", "mailto:", "#")):
                continue
            local_target = unquote(target.split("#", 1)[0])
            if local_target and not (document.parent / local_target).resolve().exists():
                fail(errors, f"broken local link in {relative_document}: {target}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--root",
        type=Path,
        default=Path(__file__).resolve().parent.parent,
        help="repository root (defaults to this script's parent repository)",
    )
    root = parser.parse_args().root.resolve()
    errors: list[str] = []

    try:
        plan = json.loads((root / "plan/tasks.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"FAIL: cannot read plan/tasks.json: {exc}", file=sys.stderr)
        return 1

    if not isinstance(plan, dict):
        print("FAIL: plan/tasks.json top level must be an object", file=sys.stderr)
        return 1

    schema_version = plan.get("schemaVersion")
    if schema_version != 2 or isinstance(schema_version, bool):
        fail(errors, "schemaVersion must be the supported version 2")
    if plan.get("project") != "earth-rehearsal":
        fail(errors, "project must be earth-rehearsal")
    if plan.get("stateAuthority") != "../STATUS.md":
        fail(errors, "stateAuthority must be ../STATUS.md")

    raw_tasks = plan.get("tasks")
    if not isinstance(raw_tasks, list):
        print("FAIL: plan.tasks must be a list", file=sys.stderr)
        return 1

    ordered_ids = [task.get("id") for task in raw_tasks if isinstance(task, dict)]
    identifiers_are_valid = len(ordered_ids) == len(raw_tasks) and all(
        isinstance(task_id, str) and bool(task_id.strip()) for task_id in ordered_ids
    )
    if not identifiers_are_valid:
        fail(errors, "every task must be an object with a string id")
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    if len(set(ordered_ids)) != len(ordered_ids):
        fail(errors, "task IDs must be unique")
    if ordered_ids[:3] != list(FOUNDATION_IDS):
        fail(errors, "Wave 0 tasks must be prepended in ER-F01 -> ER-F02 -> ER-F03 order")

    required_ids = set(FOUNDATION_IDS + ORIGINAL_IDS)
    actual_ids = set(ordered_ids)
    if not required_ids.issubset(actual_ids):
        fail(errors, f"required task IDs missing: {sorted(required_ids - actual_ids)}")

    tasks = {task["id"]: task for task in raw_tasks if isinstance(task, dict) and isinstance(task.get("id"), str)}
    positions = {task_id: index for index, task_id in enumerate(ordered_ids)}
    graph_is_well_formed = True
    for task_id, task in tasks.items():
        title = task.get("title")
        if not isinstance(title, str) or not title.strip():
            fail(errors, f"{task_id}: title must be a nonempty string")
        owned_paths = task.get("ownedPaths")
        if (
            not isinstance(owned_paths, list)
            or not owned_paths
            or any(not isinstance(path, str) or not path.strip() for path in owned_paths)
        ):
            fail(errors, f"{task_id}: ownedPaths must be a nonempty string list")
        elif len(owned_paths) != len(set(owned_paths)):
            fail(errors, f"{task_id}: ownedPaths entries must be unique")
        wave = task.get("wave")
        if not isinstance(wave, int) or isinstance(wave, bool) or wave < 0:
            fail(errors, f"{task_id}: wave must be a non-negative integer")
        status = task.get("status")
        if not isinstance(status, str) or status not in VALID_STATUSES:
            fail(errors, f"{task_id}: unknown status {status!r}")
        acceptance = task.get("acceptance")
        if not isinstance(acceptance, str) or not acceptance.strip():
            fail(errors, f"{task_id}: acceptance text is required")

        dependencies = task.get("dependsOn")
        if not isinstance(dependencies, list) or any(not isinstance(item, str) for item in dependencies):
            fail(errors, f"{task_id}: dependsOn must be a string list")
            graph_is_well_formed = False
            continue
        if len(dependencies) != len(set(dependencies)):
            fail(errors, f"{task_id}: dependencies must be unique")
            graph_is_well_formed = False
        for dependency in dependencies:
            if dependency not in tasks:
                fail(errors, f"{task_id}: unknown dependency {dependency}")
                graph_is_well_formed = False
            elif positions[dependency] >= positions[task_id]:
                fail(errors, f"{task_id}: dependency {dependency} must appear earlier in the plan")

    for task_id in FOUNDATION_IDS:
        if tasks.get(task_id, {}).get("wave") != 0:
            fail(errors, f"{task_id}: foundation task must remain in Wave 0")
        foundation_status = tasks.get(task_id, {}).get("status")
        if not isinstance(foundation_status, str) or foundation_status not in {"READY_FOR_REVIEW", "DONE"}:
            fail(errors, f"{task_id}: foundation status must be READY_FOR_REVIEW or DONE")
    if tasks.get("ER-F01", {}).get("dependsOn") != []:
        fail(errors, "ER-F01 must have no dependency")
    if tasks.get("ER-F02", {}).get("dependsOn") != ["ER-F01"]:
        fail(errors, "ER-F02 must depend on ER-F01")
    if tasks.get("ER-F03", {}).get("dependsOn") != ["ER-F02"]:
        fail(errors, "ER-F03 must depend on ER-F02")
    er_001_dependencies = tasks.get("ER-001", {}).get("dependsOn", [])
    if not isinstance(er_001_dependencies, list) or "ER-F03" not in er_001_dependencies:
        fail(errors, "ER-001 must retain the ER-F03 architecture-foundation gate")

    if not graph_is_well_formed:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1

    if len(tasks) == len(raw_tasks):
        validate_acyclic(tasks, errors)

    tasks_path = root / "TASKS.md"
    roadmap_path = root / "ROADMAP.md"
    status_path = root / "STATUS.md"
    for path in (tasks_path, roadmap_path, status_path):
        if not path.is_file():
            fail(errors, f"missing plan document: {path.relative_to(root)}")
    tasks_markdown = tasks_path.read_text(encoding="utf-8") if tasks_path.is_file() else ""
    roadmap_markdown = roadmap_path.read_text(encoding="utf-8") if roadmap_path.is_file() else ""
    status_markdown = status_path.read_text(encoding="utf-8") if status_path.is_file() else ""

    for task_id, task in tasks.items():
        title = task.get("title")
        expected_heading = rf"^## {re.escape(task_id)} — {re.escape(title)}$" if isinstance(title, str) else "(?!)"
        headings = list(re.finditer(expected_heading, tasks_markdown, re.MULTILINE))
        if len(headings) != 1:
            fail(errors, f"TASKS.md must contain exactly one matching ID/title heading for {task_id}")
            section = ""
        else:
            section_start = headings[0].end()
            next_heading = re.search(r"^## ", tasks_markdown[section_start:], re.MULTILINE)
            section_end = section_start + next_heading.start() if next_heading else len(tasks_markdown)
            section = tasks_markdown[section_start:section_end]

        wave = task.get("wave")
        status = task.get("status")
        wave_status_pattern = re.compile(
            rf"^- Wave: {re.escape(str(wave))}; status: \*\*{re.escape(str(status))}\*\*(?:;[^\n]*)?\.$",
            re.MULTILINE,
        )
        if not wave_status_pattern.search(section):
            fail(errors, f"TASKS.md wave/status must match plan/tasks.json for {task_id}")

        dependencies = task.get("dependsOn")
        expected_dependencies = ", ".join(dependencies) if isinstance(dependencies, list) and dependencies else "none"
        if f"- Dependencies: {expected_dependencies}." not in section:
            fail(errors, f"TASKS.md dependencies must match plan/tasks.json for {task_id}")

        acceptance = task.get("acceptance")
        if isinstance(acceptance, str) and f"- Acceptance: {acceptance}" not in section:
            fail(errors, f"TASKS.md acceptance must match plan/tasks.json for {task_id}")
    for wave in sorted({task.get("wave") for task in tasks.values() if isinstance(task.get("wave"), int)}):
        if len(re.findall(rf"^## Wave {wave}\b", roadmap_markdown, re.MULTILINE)) != 1:
            fail(errors, f"ROADMAP.md must contain exactly one Wave {wave} heading")
    for task_id in FOUNDATION_IDS:
        status = tasks.get(task_id, {}).get("status")
        if status and f"| {task_id} | {status} |" not in status_markdown:
            fail(errors, f"STATUS.md must record {task_id} as {status}")
        status_row = next(
            (line for line in status_markdown.splitlines() if line.startswith(f"| {task_id} |")),
            "",
        )
        if status == "DONE" and "pending" in status_row.lower():
            fail(errors, f"STATUS.md must replace pending review text with acceptance evidence for {task_id}")
    validate_links(root, errors)

    if errors:
        for error in errors:
            print(f"FAIL: {error}", file=sys.stderr)
        return 1
    waves = sorted({task["wave"] for task in tasks.values()})
    print(
        f"PASS: {len(tasks)} tasks, Waves {waves[0]}-{waves[-1]}, dependency DAG, "
        "statuses, task acceptance, navigation, and local links"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
