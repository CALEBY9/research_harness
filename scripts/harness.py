"""Local research-harness maintenance. Standard library only; no model/API calls."""
from __future__ import annotations

import argparse
import ast
import json
from pathlib import Path
import re
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
IGNORE = {".git", ".agent", "local_state", "__pycache__", ".venv", "node_modules"}
TEXT = {".md", ".py", ".json", ".yaml", ".yml", ".toml", ".txt", ".sh", ".mjs",
        ".tsv", ".tex", ".bib", ".ris", ".nbib"}
SECRET_PATTERNS = [
    re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{30,}|github_pat_[A-Za-z0-9_]{40,})\b"),
    re.compile(r"\bsk-(?:proj-|ant-api\d+-)?[A-Za-z0-9_-]{32,}\b"),
    re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    re.compile(r"https?://[^\s/@:]+:[^\s/@]+@"),
]


def source_files(root=ROOT):
    return [p for p in root.rglob("*") if p.is_file()
            and not any(part in IGNORE for part in p.relative_to(root).parts)]


def validate(root=ROOT):
    errors = []
    skills = sorted((root / "skills").glob("*/SKILL.md"))
    names = set()
    for skill in skills:
        text = skill.read_text(encoding="utf-8-sig")
        parts = text.split("---", 2)
        if len(parts) != 3 or parts[0].strip():
            errors.append(f"Invalid frontmatter: {skill.relative_to(root)}")
            continue
        for key in ("name", "description"):
            if not re.search(rf"^{key}:\s*\S", parts[1], re.M):
                errors.append(f"Missing {key}: {skill.relative_to(root)}")
        match = re.search(r"^name:\s*['\"]?([^\s'\"]+)", parts[1], re.M)
        if match:
            name = match.group(1)
            if name in names:
                errors.append(f"Duplicate skill name: {name}")
            names.add(name)
            if name != skill.parent.name and (skill.parent.name, name) != ("humanizer", "humanizer:humanizer"):
                errors.append(f"Undeclared folder/name mismatch: {skill.parent.name} / {name}")
    if not skills:
        errors.append("No installed source snapshot under skills/.")
    py_count = 0
    for path in source_files(root):
        rel = path.relative_to(root)
        if path.name in {"auth.json", "credentials.json"} or path.name == ".env" or (
                path.name.startswith(".env.") and path.name != ".env.example") or path.suffix in {".pem", ".key"}:
            errors.append(f"Forbidden sensitive filename: {rel}")
        if path.suffix not in TEXT:
            continue
        try:
            content = path.read_text(encoding="utf-8-sig")
        except UnicodeError:
            errors.append(f"Non-UTF8 text: {rel}")
            continue
        for index, line in enumerate(content.splitlines(), 1):
            if any(pattern.search(line) for pattern in SECRET_PATTERNS):
                errors.append(f"Potential credential, inspect locally without printing value: {rel}:{index}")
        if path.suffix == ".py":
            try:
                ast.parse(content, filename=str(rel))
                py_count += 1
            except SyntaxError as error:
                errors.append(f"Python syntax: {rel}:{error.lineno}")
        if path.suffix == ".json":
            try:
                json.loads(content)
            except json.JSONDecodeError as error:
                errors.append(f"JSON syntax: {rel}:{error.lineno}")
    pack = root / "skills/research-agent/references/copilot-regression.json"
    cases = []
    private_cases = []
    if pack.is_file():
        try:
            payload = json.loads(pack.read_text(encoding="utf-8-sig"))
        except json.JSONDecodeError:
            payload = {}
            # The JSON check above already records the exact failure locator.
        cases = payload.get("cases", []) if isinstance(payload, dict) else []
        if not isinstance(cases, list) or any(not isinstance(c, dict) or "case_id" not in c for c in cases):
            errors.append("Invalid regression cases: expected objects with case_id")
            cases = []
        if not cases:
            errors.append("Regression cases missing or empty")
        ids = [case["case_id"] for case in cases]
        if len(ids) != len(set(ids)):
            errors.append("Duplicate regression case IDs")
        for case in cases:
            owner = case.get("expected_owner")
            if owner and owner not in names:
                errors.append(f"Missing route owner: {case['case_id']} -> {owner}")
            if "fixture" in case:
                private_cases.append(case["case_id"])
    else:
        errors.append("Research Agent regression pack missing")
    return {"status": "FAIL" if errors else "PASS", "skills": len(skills),
            "python_parsed": py_count, "regression_definitions": len(cases),
            "private_fixture_cases_not_executed": private_cases,
            "behavioral_evaluations_executed": 0, "errors": errors,
            "limits": "Structural/known-pattern credential scan only; not full secret detection or scientific QA."}


def doctor(root=ROOT):
    paths = []
    for path in source_files(root / "skills"):
        if path.suffix not in TEXT:
            continue
        content = path.read_text(encoding="utf-8-sig")
        for index, line in enumerate(content.splitlines(), 1):
            if re.search(r"[A-Z]:[/\\]|/(?:Users|home)/[^/\s]+/", line):
                paths.append({"file": path.relative_to(root).as_posix(), "line": index})
    return {"status": "LOCAL_DEPENDENCIES_PRESENT" if paths else "NO_ABSOLUTE_PATHS_FOUND",
            "absolute_path_locations": paths,
            "note": "Locators only; no source text or secret values. Paths may include examples. Review before migration."}


def stage(target, selected, root=ROOT):
    """Copy exact source into a fresh, non-discoverable staging directory."""
    target = target.resolve()
    if target.exists():
        raise ValueError("Staging target exists. Select a fresh directory; existing files are never overwritten.")
    if target == root or root.is_relative_to(target) or target.is_relative_to(root / "skills"):
        raise ValueError("Staging target overlaps source.")
    if any(part in {".codex", ".agents", ".claude"} for part in target.parts):
        raise ValueError("Use a staging directory outside live CLI configuration/skill discovery.")
    available = {p.name: p for p in (root / "skills").iterdir() if p.is_dir() and (p / "SKILL.md").exists()}
    requested = selected or sorted(available)
    missing = sorted(set(requested) - available.keys())
    if missing:
        raise ValueError("Unknown skills: " + ", ".join(missing))
    result = validate(root)
    if result["errors"]:
        raise ValueError("Source validation failed; run validate to inspect locators.")
    target.mkdir(parents=True)
    for name in requested:
        shutil.copytree(available[name], target / name,
                        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    return {"status": "STAGED", "skills": len(requested), "live_installation_changed": False,
            "note": "Exact source snapshot; absolute paths and external dependencies are not relocated."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("validate", help="Check source structure, Python/JSON and known secret patterns")
    commands.add_parser("doctor", help="Report files with machine-specific path dependencies")
    staging = commands.add_parser("stage", help="Copy source to a fresh directory; never activate skills")
    staging.add_argument("--target", required=True, type=Path)
    staging.add_argument("--skill", action="append", dest="selected")
    args = parser.parse_args()
    try:
        if args.command == "validate":
            result = validate()
        elif args.command == "doctor":
            result = doctor()
        else:
            result = stage(args.target, args.selected)
    except (OSError, ValueError) as error:
        parser.exit(2, f"{error}\n")
    print(json.dumps(result, ensure_ascii=True, indent=2))
    return 1 if result.get("status") == "FAIL" else 0


if __name__ == "__main__":
    sys.exit(main())
