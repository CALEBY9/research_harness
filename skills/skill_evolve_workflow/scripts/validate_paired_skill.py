#!/usr/bin/env python3
"""Validate the paired Codex/Claude skill package without external dependencies."""

from __future__ import annotations

import argparse
import json
import re
import tempfile
from pathlib import Path


COMMON_KEYS = {"name", "description", "license", "allowed-tools", "metadata", "version"}
ALLOWED_KEYS = {
    "codex": COMMON_KEYS,
    "claude": COMMON_KEYS | {"argument-hint"},
}
REQUIRED_KEYS = {"name", "description"}
NAME_RE = re.compile(r"^[a-z0-9](?:[a-z0-9_-]{0,62}[a-z0-9])?$")
VERSION_RE = re.compile(r"^\d+\.\d+\.\d+$")
TOP_LEVEL_RE = re.compile(r"^([A-Za-z][A-Za-z0-9_-]*):(?:\s*(.*))?$")


def _scalar(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def _frontmatter(content: str) -> tuple[dict[str, str], str, list[str]]:
    normalized = content.replace("\r\n", "\n")
    errors: list[str] = []
    if not normalized.startswith("---\n"):
        return {}, normalized, ["FRONTMATTER_MISSING"]
    end = normalized.find("\n---\n", 4)
    if end < 0:
        return {}, normalized, ["FRONTMATTER_UNCLOSED"]

    values: dict[str, str] = {}
    for line_no, line in enumerate(normalized[4:end].splitlines(), start=2):
        if not line or line.lstrip().startswith("#") or line[0].isspace():
            continue
        match = TOP_LEVEL_RE.fullmatch(line)
        if not match:
            errors.append(f"FRONTMATTER_TOP_LEVEL_INVALID:{line_no}")
            continue
        key, raw = match.group(1), match.group(2) or ""
        if key in values:
            errors.append(f"FRONTMATTER_DUPLICATE_KEY:{key}")
        values[key] = _scalar(raw)
    return values, normalized[end + 5 :], errors


def _fence_errors(body: str) -> list[str]:
    marker: str | None = None
    length = 0
    language = ""
    errors: list[str] = []
    for line_no, line in enumerate(body.splitlines(), start=1):
        match = re.match(r"^[ \t]*(?:(?:[-+*]|\d+[.)])[ \t]+)?(`{3,}|~{3,})(.*)$", line)
        if match:
            token = match.group(1)
            if marker is None:
                marker, length = token[0], len(token)
                language = match.group(2).strip().lower()
            elif token[0] == marker and len(token) >= length and not match.group(2).strip():
                marker, length = None, 0
                language = ""
            elif language in {"markdown", "md"} and token[0] == marker and len(token) >= length:
                errors.append(f"MARKDOWN_TEMPLATE_FENCE_COLLISION:{line_no}")
    if marker is not None:
        errors.append("MARKDOWN_FENCE_UNCLOSED")
    return errors


def _table_errors(body: str) -> list[str]:
    """Check pipe-table header/delimiter widths, including Markdown templates."""
    errors: list[str] = []
    lines = body.splitlines()
    for index in range(len(lines) - 1):
        header, delimiter = lines[index].strip(), lines[index + 1].strip()
        if not header.startswith("|") or not re.fullmatch(r"\|(?:\s*:?-{3,}:?\s*\|)+", delimiter):
            continue
        cells = re.split(r"(?<!\\)\|", header.strip("|"))
        columns = delimiter.count("|") - 1
        if len(cells) != columns:
            errors.append(f"MARKDOWN_TABLE_COLUMNS:{index + 1}:{len(cells)}:{columns}")
    return errors


def validate(path: Path, platform: str) -> dict[str, object]:
    errors: list[str] = []
    if not path.is_file():
        return {"platform": platform, "path": str(path), "valid": False, "errors": ["SKILL_FILE_MISSING"]}
    try:
        content = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return {"platform": platform, "path": str(path), "valid": False, "errors": ["SKILL_NOT_UTF8"]}

    fields, body, parse_errors = _frontmatter(content)
    errors.extend(parse_errors)
    missing = sorted(REQUIRED_KEYS - fields.keys())
    errors.extend(f"FRONTMATTER_REQUIRED_MISSING:{key}" for key in missing)
    unexpected = sorted(fields.keys() - ALLOWED_KEYS[platform])
    errors.extend(f"FRONTMATTER_KEY_UNSUPPORTED:{key}" for key in unexpected)

    name = fields.get("name", "")
    if name and not NAME_RE.fullmatch(name):
        errors.append("SKILL_NAME_INVALID")
    if name and path.parent.name != name:
        errors.append(f"SKILL_DIRECTORY_NAME_MISMATCH:{path.parent.name}:{name}")
    description = fields.get("description", "")
    if not description:
        errors.append("SKILL_DESCRIPTION_EMPTY")
    elif len(description) > 1024:
        errors.append("SKILL_DESCRIPTION_TOO_LONG")
    version = fields.get("version", "")
    if version and not VERSION_RE.fullmatch(version):
        errors.append("SKILL_VERSION_INVALID")
    if re.search(r"(?m)^[ ]{0,3}\[TODO:[^\n]*\][ \t]*$", body):
        errors.append("SKILL_TODO_UNFINISHED")
    errors.extend(_fence_errors(body))
    errors.extend(_table_errors(body))

    return {
        "platform": platform,
        "path": str(path),
        "valid": not errors,
        "name": name,
        "description": description,
        "version": version or None,
        "legacy_underscore_name": "_" in name,
        "errors": errors,
    }


def validate_pair(codex_path: Path, claude_path: Path) -> dict[str, object]:
    codex = validate(codex_path, "codex")
    claude = validate(claude_path, "claude")
    pair_errors: list[str] = []
    for field in ("name", "description", "version"):
        if codex.get(field) != claude.get(field):
            pair_errors.append(f"PAIR_FIELD_MISMATCH:{field}")
    valid = bool(codex["valid"] and claude["valid"] and not pair_errors)
    return {
        "valid": valid, "codex": codex, "claude": claude, "pair_errors": pair_errors,
        "verification_scope": "platform metadata, directory name, supported Markdown template structure",
        "body_equivalence_checked": False,
        "behavioral_validation_performed": False,
    }


def self_test() -> int:
    base_body = "# Test\n\n```text\nok\n```\n"
    cases: list[tuple[str, bool]] = []
    with tempfile.TemporaryDirectory(prefix="paired-skill-validator-") as tmp:
        root = Path(tmp)
        codex_dir = root / "codex" / "legacy_skill"
        claude_dir = root / "claude" / "legacy_skill"
        codex_dir.mkdir(parents=True)
        claude_dir.mkdir(parents=True)
        codex_path = codex_dir / "SKILL.md"
        claude_path = claude_dir / "SKILL.md"
        codex_path.write_text(
            "---\nname: legacy_skill\ndescription: Paired test skill.\nversion: 1.2.3\n---\n\n" + base_body,
            encoding="utf-8",
        )
        claude_path.write_text(
            "---\nname: legacy_skill\ndescription: Paired test skill.\nargument-hint: [input]\nallowed-tools: Read\nversion: 1.2.3\n---\n\n" + base_body,
            encoding="utf-8",
        )
        cases.append(("valid_pair", validate_pair(codex_path, claude_path)["valid"] is True))

        bad_codex = codex_path.read_text(encoding="utf-8").replace("version: 1.2.3", "argument-hint: [bad]\nversion: 1.2.3")
        codex_path.write_text(bad_codex, encoding="utf-8")
        result = validate_pair(codex_path, claude_path)
        cases.append(("codex_rejects_claude_key", "FRONTMATTER_KEY_UNSUPPORTED:argument-hint" in result["codex"]["errors"]))

        codex_path.write_text(bad_codex.replace("argument-hint: [bad]\n", "").replace("version: 1.2.3", "version: latest"), encoding="utf-8")
        result = validate_pair(codex_path, claude_path)
        cases.append(("invalid_version", "SKILL_VERSION_INVALID" in result["codex"]["errors"]))

        codex_path.write_text(
            "---\nname: legacy_skill\ndescription: Paired test skill.\nversion: 1.2.3\n---\n\n```text\nunclosed\n",
            encoding="utf-8",
        )
        result = validate_pair(codex_path, claude_path)
        cases.append(("unclosed_fence", "MARKDOWN_FENCE_UNCLOSED" in result["codex"]["errors"]))

        codex_path.write_text(
            "---\nname: legacy_skill\ndescription: Different description.\nversion: 1.2.3\n---\n\n" + base_body,
            encoding="utf-8",
        )
        result = validate_pair(codex_path, claude_path)
        cases.append(("pair_mismatch", "PAIR_FIELD_MISMATCH:description" in result["pair_errors"]))

        cases.append(("table_columns", bool(_table_errors("| A | B | C |\n|---|---|"))))
        cases.append(("escaped_table_pipe", not _table_errors("| A \\| B | C |\n|---|---|")))
        cases.append(("nested_template_collision", any(
            error.startswith("MARKDOWN_TEMPLATE_FENCE_COLLISION")
            for error in _fence_errors("```markdown\n```bash\nrun\n```\n```\n")
        )))
        cases.append(("valid_nested_template", not _fence_errors(
            "````markdown\n```bash\nrun\n```\n````\n"
        )))
        cases.append(("assurance_scope", result["body_equivalence_checked"] is False
                      and result["behavioral_validation_performed"] is False))

    failed = [name for name, passed in cases if not passed]
    print(json.dumps({"self_test": "PASS" if not failed else "FAIL", "cases": dict(cases)}, sort_keys=True))
    return 0 if not failed else 1


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--codex", type=Path, help="Path to the Codex SKILL.md")
    parser.add_argument("--claude", type=Path, help="Path to the Claude SKILL.md")
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    if args.self_test:
        return self_test()
    if args.codex is None or args.claude is None:
        parser.error("--codex and --claude are required unless --self-test is used")
    result = validate_pair(args.codex.resolve(), args.claude.resolve())
    print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
