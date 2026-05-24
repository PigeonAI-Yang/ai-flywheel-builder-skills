from __future__ import annotations

import argparse
import sys
import uuid
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

REQUIRED_FILES = {
    "templates/learning-closure.md": [
        "# 经验收口",
        "closure_uuid",
        "run_uuid",
        "经验收口记录",
        "触发条件",
        "写入位置",
    ],
    "templates/learning-index.md": ["# 经验索引", "closure_uuid", "run_uuid"],
    "templates/memory-rules.md": ["经验收口中", "问题重复出现", "平台或工具限制"],
    "skills/ai-flywheel-builder/SKILL.md": [
        "Learning Closure Rule",
        "Do not finish a module run without performing learning closure",
    ],
    "docs/01_ARCHITECTURE.md": ["## Learning Closure", "Every module run"],
    "README.md": ["## 经验收口规则", "每个模块完成前"],
}

MODULES_REQUIRING_CLOSURE = [
    "skills/flywheel-initializer/SKILL.md",
    "skills/practice-designer/SKILL.md",
    "skills/practice-capture/SKILL.md",
    "skills/practice-reviewer/SKILL.md",
    "skills/content-decomposer/SKILL.md",
    "skills/feedback-attributor/SKILL.md",
]

MODULE_MARKERS = [
    "已完成经验收口",
    "不要在未做经验收口时结束本模块",
]

RUN_REQUIRED_FILES = [
    "run.md",
    "learning-closure.md",
]

RUN_CLOSURE_MARKERS = [
    "## run_id",
    "## run_uuid",
    "## 经验收口记录",
    "closure_uuid",
]


def read_text(relative_path: str) -> str:
    path = ROOT / relative_path
    if not path.exists():
        raise AssertionError(f"missing required file: {path}")
    return path.read_text(encoding="utf-8")


def require_markers(relative_path: str, markers: list[str]) -> list[str]:
    text = read_text(relative_path)
    missing = [marker for marker in markers if marker not in text]
    if missing:
        return [f"{relative_path}: missing marker: {marker}" for marker in missing]
    return []

def extract_section_value(text: str, heading: str) -> str:
    lines = text.splitlines()
    for index, line in enumerate(lines):
        if line.strip() == heading:
            values: list[str] = []
            for next_line in lines[index + 1 :]:
                if next_line.startswith("## "):
                    break
                stripped = next_line.strip()
                if stripped:
                    values.append(stripped)
            return "\n".join(values).strip()
    return ""


def extract_table_values(text: str, column_name: str) -> list[str]:
    lines = [line.strip() for line in text.splitlines()]
    for index, line in enumerate(lines):
        if not (line.startswith("|") and column_name in line):
            continue
        headers = [part.strip() for part in line.strip("|").split("|")]
        try:
            column_index = headers.index(column_name)
        except ValueError:
            continue

        values: list[str] = []
        for row in lines[index + 2 :]:
            if not row.startswith("|"):
                break
            cells = [part.strip() for part in row.strip("|").split("|")]
            if len(cells) <= column_index:
                continue
            value = cells[column_index]
            if value and not set(value) <= {"-"}:
                values.append(value)
        return values
    return []


def find_workspace_root(run_dir: Path) -> Path | None:
    resolved = run_dir.resolve()
    if resolved.parent.name != "runs":
        return None
    return resolved.parent.parent


def verify_learning_index(
    run_dir: Path, run_id: str, run_uuid: str, closure_uuids: list[str]
) -> list[str]:
    errors: list[str] = []
    workspace_root = find_workspace_root(run_dir)
    if workspace_root is None:
        return [
            f"{run_dir}: cannot infer workspace root; expected workspace/{{user}}/runs/{{run_id}}"
        ]

    index_path = workspace_root / "indexes" / "learning-index.md"
    if not index_path.exists():
        return [f"{index_path}: missing learning index for run closure sync"]

    index_text = index_path.read_text(encoding="utf-8")
    index_closure_uuids = set(extract_table_values(index_text, "closure_uuid"))
    index_run_ids = set(extract_table_values(index_text, "run_id"))
    index_run_uuids = set(extract_table_values(index_text, "run_uuid"))

    for closure_uuid in closure_uuids:
        if closure_uuid not in index_closure_uuids:
            errors.append(
                f"{index_path}: missing closure_uuid from run learning-closure.md: {closure_uuid}"
            )

    if run_id and run_id not in index_run_ids:
        errors.append(f"{index_path}: missing run_id from run learning-closure.md: {run_id}")

    if run_uuid and run_uuid not in index_run_uuids:
        errors.append(
            f"{index_path}: missing run_uuid from run learning-closure.md: {run_uuid}"
        )

    return errors


def verify_run_dir(run_dir: Path) -> list[str]:
    errors: list[str] = []

    if not run_dir.exists():
        return [f"run dir does not exist: {run_dir}"]
    if not run_dir.is_dir():
        return [f"run dir is not a directory: {run_dir}"]

    for file_name in RUN_REQUIRED_FILES:
        path = run_dir / file_name
        if not path.exists():
            errors.append(f"{run_dir}: missing required run file: {file_name}")

    closure_path = run_dir / "learning-closure.md"
    if not closure_path.exists():
        return errors

    text = closure_path.read_text(encoding="utf-8")
    for marker in RUN_CLOSURE_MARKERS:
        if marker not in text:
            errors.append(f"{closure_path}: missing marker: {marker}")

    run_uuid = extract_section_value(text, "## run_uuid")
    if not run_uuid:
        errors.append(f"{closure_path}: run_uuid is empty")
    else:
        try:
            uuid.UUID(run_uuid)
        except ValueError:
            errors.append(f"{closure_path}: invalid run_uuid: {run_uuid}")

    closure_uuids = extract_table_values(text, "closure_uuid")
    if not closure_uuids:
        errors.append(f"{closure_path}: no closure_uuid rows found")
    for closure_uuid in closure_uuids:
        try:
            uuid.UUID(closure_uuid)
        except ValueError:
            errors.append(f"{closure_path}: invalid closure_uuid: {closure_uuid}")

    run_id = extract_section_value(text, "## run_id")
    if not run_id:
        errors.append(f"{closure_path}: run_id is empty")

    if run_id and run_uuid and closure_uuids:
        errors.extend(verify_learning_index(run_dir, run_id, run_uuid, closure_uuids))

    return errors


def verify_project_rules() -> list[str]:
    errors: list[str] = []

    for relative_path, markers in REQUIRED_FILES.items():
        errors.extend(require_markers(relative_path, markers))

    for relative_path in MODULES_REQUIRING_CLOSURE:
        errors.extend(require_markers(relative_path, MODULE_MARKERS))

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Verify AI Flywheel Builder learning closure rules."
    )
    parser.add_argument(
        "--run-dir",
        type=Path,
        help="Optional run directory to verify for learning-closure.md and closure_uuid.",
    )
    args = parser.parse_args()

    errors = verify_project_rules()

    if args.run_dir:
        errors.extend(verify_run_dir(args.run_dir))

    if errors:
        print("Learning closure verification failed:")
        for error in errors:
            print(f"- {error}")
        return 1

    if args.run_dir:
        print("Learning closure verification passed for project rules and run dir.")
    else:
        print("Learning closure verification passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
