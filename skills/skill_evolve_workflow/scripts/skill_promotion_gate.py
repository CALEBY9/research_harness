#!/usr/bin/env python3
"""Validate a frozen active/candidate skill-promotion evidence manifest.

This tool is intentionally local and zero-dependency. It does not run models,
harvest sessions, edit skills, or adopt candidates. It only validates evidence
already produced by a workflow and returns a promotion decision.
"""

from __future__ import annotations

import argparse
import copy
import difflib
import hashlib
import json
import os
import re
import tempfile
from pathlib import Path
from typing import Any


SCHEMA_VERSION = "skill-promotion-gate.v1"
FAILURE_CLASSES = {
    "SKILL_DEFECT",
    "EXECUTION_LAPSE",
    "ENVIRONMENT_OR_TOOL_FAILURE",
    "TASK_SPECIFIC_EXCEPTION",
    "UNCLEAR",
}
SPLITS = {"probe", "train", "selection", "test"}
DECISIONS = {
    "PROMOTE",
    "STAGE_FOR_HUMAN_REVIEW",
    "REJECT_REGRESSION",
    "DEFER_NOT_SCORABLE",
}
SHA256_RE = re.compile(r"^[0-9a-fA-F]{64}$")


class ManifestError(ValueError):
    """Raised when a promotion manifest is incomplete or internally invalid."""


def _mapping(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ManifestError(f"{label} must be a JSON object")
    return value


def _text(obj: dict[str, Any], key: str, label: str) -> str:
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ManifestError(f"{label}.{key} must be a non-empty string")
    return value.strip()


def _text_list(obj: dict[str, Any], key: str, label: str) -> list[str]:
    value = obj.get(key)
    if not isinstance(value, list) or not value:
        raise ManifestError(f"{label}.{key} must be a non-empty string array")
    result: list[str] = []
    for index, item in enumerate(value):
        if not isinstance(item, str) or not item.strip():
            raise ManifestError(f"{label}.{key}[{index}] must be a non-empty string")
        result.append(item.strip())
    return result


def _bool(obj: dict[str, Any], key: str, default: bool = False) -> bool:
    value = obj.get(key, default)
    if not isinstance(value, bool):
        raise ManifestError(f"{key} must be true or false")
    return value


def _number(value: Any, label: str, *, minimum: float = 0.0) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ManifestError(f"{label} must be a number")
    result = float(value)
    if result < minimum:
        raise ManifestError(f"{label} must be >= {minimum}")
    return result


def _bounded_score(value: Any, label: str, *, allow_none: bool) -> float | None:
    if value is None and allow_none:
        return None
    score = _number(value, label)
    if score > 1.0:
        raise ManifestError(f"{label} must be between 0 and 1")
    return score


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _candidate_diff(active_path: str, candidate_path: str) -> str:
    """Return a deterministic unified diff derived from the frozen artifacts."""
    if not active_path or not candidate_path:
        raise ManifestError("active.path and candidate.path are required to derive the exact diff")
    try:
        with Path(active_path).open("r", encoding="utf-8", newline="") as handle:
            active_text = handle.read()
        with Path(candidate_path).open("r", encoding="utf-8", newline="") as handle:
            candidate_text = handle.read()
    except UnicodeDecodeError as exc:
        raise ManifestError("active and candidate artifacts must be UTF-8 text files") from exc
    diff = "".join(
        difflib.unified_diff(
            active_text.splitlines(keepends=True),
            candidate_text.splitlines(keepends=True),
            fromfile="active",
            tofile="candidate",
            lineterm="\n",
        )
    )
    if not diff:
        raise ManifestError("candidate artifact has no UTF-8 text diff from the active artifact")
    return diff


def _artifact_identity(obj: Any, label: str) -> dict[str, str]:
    item = _mapping(obj, label)
    raw_path = item.get("path", "")
    raw_sha = item.get("sha256", "")
    if raw_path is not None and not isinstance(raw_path, str):
        raise ManifestError(f"{label}.path must be a string")
    if raw_sha is not None and not isinstance(raw_sha, str):
        raise ManifestError(f"{label}.sha256 must be a string")

    path_text = (raw_path or "").strip()
    claimed_sha = (raw_sha or "").strip().lower()
    if claimed_sha and not SHA256_RE.fullmatch(claimed_sha):
        raise ManifestError(f"{label}.sha256 must be a 64-character SHA-256")
    if not path_text and not claimed_sha:
        raise ManifestError(f"{label} requires path or sha256")

    resolved = ""
    actual_sha = claimed_sha
    if path_text:
        path = Path(path_text).expanduser()
        if not path.is_file():
            raise ManifestError(f"{label}.path does not exist or is not a file: {path}")
        path = path.resolve()
        resolved = str(path)
        actual_sha = _sha256_file(path)
        if claimed_sha and claimed_sha != actual_sha:
            raise ManifestError(f"{label}.sha256 does not match {path}")
    return {"path": resolved or path_text, "sha256": actual_sha}


def _outcome(value: Any, label: str, *, qualitative: bool) -> dict[str, Any]:
    item = _mapping(value, label)
    passed = item.get("passed")
    if passed is not None and not isinstance(passed, bool):
        raise ManifestError(f"{label}.passed must be true, false, or null")
    score = _bounded_score(item.get("score"), f"{label}.score", allow_none=qualitative)
    if not qualitative and passed is None:
        raise ManifestError(f"{label}.passed is required for objectively scorable cases")
    return {"passed": passed, "score": score}


def _case(value: Any, index: int, *, qualitative: bool) -> dict[str, Any]:
    label = f"cases[{index}]"
    item = _mapping(value, label)
    case_id = _text(item, "case_id", label)
    split = _text(item, "split", label).lower()
    if split not in SPLITS:
        raise ManifestError(f"{label}.split must be one of {sorted(SPLITS)}")
    frozen = _bool(item, "frozen_before_candidate", False)
    if split in {"selection", "test"} and not frozen:
        raise ManifestError(f"{label} must be frozen before candidate creation")
    target = _bool(item, "target", False)
    hard_gate = _bool(item, "hard_gate", False)
    return {
        "case_id": case_id,
        "split": split,
        "input": _text(item, "input", label),
        "expected_behavior": _text(item, "expected_behavior", label),
        "verifier": _text(item, "verifier", label),
        "risk": _text(item, "risk", label),
        "provenance": _text(item, "provenance", label),
        "frozen_before_candidate": frozen,
        "target": target,
        "hard_gate": hard_gate,
        "active": _outcome(item.get("active"), f"{label}.active", qualitative=qualitative),
        "candidate": _outcome(item.get("candidate"), f"{label}.candidate", qualitative=qualitative),
    }


def _normalize_manifest(data: Any) -> dict[str, Any]:
    root = _mapping(data, "manifest")
    schema_version = _text(root, "schema_version", "manifest")
    if schema_version != SCHEMA_VERSION:
        raise ManifestError(
            f"manifest.schema_version must be {SCHEMA_VERSION!r}, got {schema_version!r}"
        )
    skill = _text(root, "skill", "manifest")
    change_hypothesis = _text(root, "change_hypothesis", "manifest")
    protected_rules = _text_list(root, "protected_rules", "manifest")
    attribution = _mapping(root.get("failure_attribution"), "failure_attribution")
    failure_class = _text(attribution, "class", "failure_attribution").upper()
    if failure_class not in FAILURE_CLASSES:
        raise ManifestError(
            f"failure_attribution.class must be one of {sorted(FAILURE_CLASSES)}"
        )
    failure_evidence = _text(attribution, "evidence", "failure_attribution")

    active = _artifact_identity(root.get("active"), "active")
    candidate_raw = _mapping(root.get("candidate"), "candidate")
    candidate = _artifact_identity(candidate_raw, "candidate")
    rollback = _artifact_identity(root.get("rollback"), "rollback")
    if candidate["sha256"] == active["sha256"]:
        raise ManifestError("candidate artifact must differ from the active artifact")
    if rollback["sha256"] != active["sha256"]:
        raise ManifestError("rollback artifact must preserve the active artifact")

    claimed_diff = candidate_raw.get("diff", "")
    diff_sha = candidate_raw.get("diff_sha256", "")
    if claimed_diff is not None and not isinstance(claimed_diff, str):
        raise ManifestError("candidate.diff must be a string")
    if diff_sha is not None and not isinstance(diff_sha, str):
        raise ManifestError("candidate.diff_sha256 must be a string")
    claimed_diff = claimed_diff or ""
    diff_sha = (diff_sha or "").strip().lower()
    diff_text = _candidate_diff(active["path"], candidate["path"])
    if claimed_diff and claimed_diff != diff_text:
        raise ManifestError("candidate.diff does not match the diff derived from active.path and candidate.path")
    if diff_sha and not SHA256_RE.fullmatch(diff_sha):
        raise ManifestError("candidate.diff_sha256 must be a 64-character SHA-256")
    actual_diff_sha = hashlib.sha256(diff_text.encode("utf-8")).hexdigest()
    if diff_sha and diff_sha != actual_diff_sha:
        raise ManifestError("candidate.diff_sha256 does not match candidate.diff")
    diff_sha = actual_diff_sha

    budget = _mapping(root.get("edit_budget"), "edit_budget")
    limit_raw = budget.get("limit")
    used_raw = budget.get("used")
    if isinstance(limit_raw, bool) or not isinstance(limit_raw, int) or limit_raw < 1:
        raise ManifestError("edit_budget.limit must be a positive integer")
    if isinstance(used_raw, bool) or not isinstance(used_raw, int) or used_raw < 0:
        raise ManifestError("edit_budget.used must be a non-negative integer")
    if used_raw > limit_raw:
        raise ManifestError("edit_budget.used cannot exceed edit_budget.limit")
    full_rewrite_approved = _bool(budget, "full_rewrite_approved", False)
    if limit_raw > 4 and not full_rewrite_approved:
        raise ManifestError("edit budgets above 4 require full_rewrite_approved=true")

    qualitative = root.get("qualitative", False)
    if not isinstance(qualitative, bool):
        raise ManifestError("qualitative must be true or false")
    margin = _number(root.get("predeclared_margin", 0.0), "predeclared_margin")
    known_noise = _number(root.get("known_noise", 0.0), "known_noise")
    if margin > 1.0 or known_noise > 1.0:
        raise ManifestError("predeclared_margin and known_noise must be <= 1")

    raw_cases = root.get("cases")
    if not isinstance(raw_cases, list) or not raw_cases:
        raise ManifestError("cases must be a non-empty JSON array")
    cases = [_case(value, index, qualitative=qualitative) for index, value in enumerate(raw_cases)]
    ids = [item["case_id"] for item in cases]
    if len(ids) != len(set(ids)):
        raise ManifestError("case_id values must be unique")

    return {
        "schema_version": schema_version,
        "skill": skill,
        "change_hypothesis": change_hypothesis,
        "protected_rules": protected_rules,
        "failure_class": failure_class,
        "failure_evidence": failure_evidence,
        "active": active,
        "candidate": candidate,
        "rollback": rollback,
        "diff": diff_text,
        "diff_sha256": diff_sha,
        "diff_chars": len(diff_text),
        "edit_limit": limit_raw,
        "edit_used": used_raw,
        "full_rewrite_approved": full_rewrite_approved,
        "qualitative": qualitative,
        "predeclared_margin": margin,
        "known_noise": known_noise,
        "cases": cases,
    }


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def evaluate_manifest(data: Any) -> dict[str, Any]:
    item = _normalize_manifest(data)
    cases = item["cases"]
    selection = [case for case in cases if case["split"] == "selection"]
    gating = [case for case in cases if case["split"] in {"selection", "test"}]

    hard_regressions: list[str] = []
    pass_to_fail: list[str] = []
    score_regressions: list[str] = []
    for case in gating:
        active = case["active"]
        candidate = case["candidate"]
        if active["passed"] is True and candidate["passed"] is False:
            pass_to_fail.append(case["case_id"])
        if active["score"] is not None and candidate["score"] is not None:
            if candidate["score"] < active["score"] - 1e-12:
                score_regressions.append(case["case_id"])
        if case["hard_gate"]:
            if candidate["passed"] is not True:
                hard_regressions.append(case["case_id"])
            elif (
                active["score"] is not None
                and candidate["score"] is not None
                and candidate["score"] < active["score"] - 1e-12
            ):
                hard_regressions.append(case["case_id"])

    active_scores = [case["active"]["score"] for case in selection]
    candidate_scores = [case["candidate"]["score"] for case in selection]
    active_mean = _mean([score for score in active_scores if score is not None])
    candidate_mean = _mean([score for score in candidate_scores if score is not None])
    delta = (
        candidate_mean - active_mean
        if active_mean is not None and candidate_mean is not None
        else None
    )
    effective_margin = max(item["predeclared_margin"], item["known_noise"])

    target_cases = [case for case in selection if case["target"]]
    target_fixed = bool(target_cases) and all(
        case["candidate"]["passed"] is True for case in target_cases
    ) and any(
        case["active"]["passed"] is False and case["candidate"]["passed"] is True
        for case in target_cases
    )

    decision = "DEFER_NOT_SCORABLE"
    reasons: list[str] = []
    if hard_regressions or pass_to_fail:
        decision = "REJECT_REGRESSION"
        if hard_regressions:
            reasons.append("hard-gate regression or unverified hard gate")
        if pass_to_fail:
            reasons.append("previously passing gating case now fails")
    elif item["failure_class"] == "UNCLEAR":
        decision = "STAGE_FOR_HUMAN_REVIEW"
        reasons.append("failure attribution is unclear and requires human adjudication")
    elif item["failure_class"] != "SKILL_DEFECT":
        reasons.append(f"{item['failure_class']} is not admissible for skill-body promotion")
    elif item["edit_used"] == 0:
        reasons.append("candidate contains no applied edits")
    elif item["qualitative"]:
        decision = "STAGE_FOR_HUMAN_REVIEW"
        reasons.append("qualitative research judgment requires human adjudication")
    elif not selection:
        reasons.append("no frozen selection cases are available")
    else:
        strictly_improved = bool(
            delta is not None
            and (
                (effective_margin > 0 and delta >= effective_margin - 1e-12)
                or (effective_margin == 0 and delta > 1e-12)
            )
        )
        if score_regressions:
            decision = "REJECT_REGRESSION"
            reasons.append("candidate regresses one or more frozen gating scores")
        elif strictly_improved or target_fixed:
            decision = "PROMOTE"
            reasons.append(
                "candidate exceeds the effective margin"
                if strictly_improved
                else "target failure is fixed with no frozen gating regression"
            )
        else:
            reasons.append("candidate improvement is below the effective margin")

    if decision not in DECISIONS:
        raise AssertionError(f"internal error: unsupported decision {decision}")

    rejected_change_entry = None
    if decision == "REJECT_REGRESSION":
        rejected_change_entry = {
            "candidate_diff_sha256": item["diff_sha256"],
            "failed_cases": sorted(set(hard_regressions + pass_to_fail + score_regressions)),
            "rejection_reason": "; ".join(reasons),
            "reusable_negative_lesson": (
                "Do not promote this candidate until the smallest regression-causing edit is "
                "isolated and the frozen gating cases pass again."
            ),
        }

    return {
        "schema_version": SCHEMA_VERSION,
        "skill": item["skill"],
        "change_control": {
            "hypothesis": item["change_hypothesis"],
            "protected_rules": item["protected_rules"],
        },
        "decision": decision,
        "reasons": reasons,
        "failure_attribution": {
            "class": item["failure_class"],
            "evidence": item["failure_evidence"],
        },
        "artifacts": {
            "active": item["active"],
            "candidate": item["candidate"],
            "rollback": item["rollback"],
            "candidate_diff": item["diff"],
            "candidate_diff_sha256": item["diff_sha256"],
            "candidate_diff_chars": item["diff_chars"],
        },
        "edit_budget": {
            "limit": item["edit_limit"],
            "used": item["edit_used"],
            "full_rewrite_approved": item["full_rewrite_approved"],
        },
        "metrics": {
            "selection_cases": len(selection),
            "active_mean": active_mean,
            "candidate_mean": candidate_mean,
            "delta": delta,
            "predeclared_margin": item["predeclared_margin"],
            "known_noise": item["known_noise"],
            "effective_margin": effective_margin,
            "target_fixed": target_fixed,
            "hard_regressions": sorted(set(hard_regressions)),
            "pass_to_fail_regressions": sorted(set(pass_to_fail)),
            "score_regressions": sorted(set(score_regressions)),
        },
        "case_summary": [
            {
                "case_id": case["case_id"],
                "split": case["split"],
                "input": case["input"],
                "expected_behavior": case["expected_behavior"],
                "verifier": case["verifier"],
                "risk": case["risk"],
                "provenance": case["provenance"],
                "target": case["target"],
                "hard_gate": case["hard_gate"],
                "active": case["active"],
                "candidate": case["candidate"],
            }
            for case in cases
        ],
        "rejected_change_entry": rejected_change_entry,
        "live_files_changed": False,
        "human_adoption_required": True,
    }


def _atomic_write_json(path: Path, value: Any) -> None:
    path = path.expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = ""
    try:
        with tempfile.NamedTemporaryFile(
            "w",
            encoding="utf-8",
            delete=False,
            dir=str(path.parent),
            prefix=f".{path.name}.",
            suffix=".tmp",
        ) as handle:
            json.dump(value, handle, ensure_ascii=False, indent=2)
            handle.write("\n")
            temp_path = handle.name
        os.replace(temp_path, path)
    finally:
        if temp_path and os.path.exists(temp_path):
            os.unlink(temp_path)


def template_manifest(skill: str) -> dict[str, Any]:
    return {
        "schema_version": SCHEMA_VERSION,
        "skill": skill,
        "change_hypothesis": "The bounded candidate patch fixes the attributed skill defect",
        "protected_rules": [
            "Safety, secrets, authority, provenance, routing, and clean-final boundaries"
        ],
        "failure_attribution": {
            "class": "SKILL_DEFECT",
            "evidence": "Path, log, user feedback, or reproducible failure locator",
        },
        "active": {"path": "C:/path/to/active/SKILL.md", "sha256": ""},
        "candidate": {
            "path": "C:/path/to/candidate/SKILL.md",
            "sha256": "",
            "diff": "",
        },
        "rollback": {"path": "C:/path/to/active/SKILL.md", "sha256": ""},
        "edit_budget": {"limit": 4, "used": 1, "full_rewrite_approved": False},
        "qualitative": False,
        "predeclared_margin": 0.05,
        "known_noise": 0.0,
        "cases": [
            {
                "case_id": "selection-001",
                "split": "selection",
                "input": "Prompt, fixture path, or reproducible input locator",
                "expected_behavior": "Expected route, output, or invariant",
                "verifier": "Deterministic command, rubric, or evidence check",
                "risk": "normal",
                "provenance": "Where this independent case came from",
                "frozen_before_candidate": True,
                "target": True,
                "hard_gate": False,
                "active": {"passed": False, "score": 0.0},
                "candidate": {"passed": True, "score": 1.0},
            }
        ],
    }


def self_test() -> dict[str, str]:
    with tempfile.TemporaryDirectory(prefix="skill-promotion-gate-") as directory:
        root = Path(directory)
        template_path = root / "template.json"
        _atomic_write_json(template_path, template_manifest("template-self-test"))
        template_roundtrip = json.loads(template_path.read_text(encoding="utf-8"))
        active = root / "active.md"
        candidate = root / "candidate.md"
        active.write_text("active\n", encoding="utf-8")
        candidate.write_text("candidate\n", encoding="utf-8")
        base = template_manifest("self-test-skill")
        base["active"] = {"path": str(active), "sha256": ""}
        base["candidate"] = {
            "path": str(candidate),
            "sha256": "",
            "diff": _candidate_diff(str(active), str(candidate)),
        }
        base["rollback"] = {"path": str(active), "sha256": ""}

        promote_report = evaluate_manifest(copy.deepcopy(base))
        report_path = root / "promotion-report.json"
        _atomic_write_json(report_path, promote_report)
        report_roundtrip = json.loads(report_path.read_text(encoding="utf-8"))
        promote = report_roundtrip["decision"]
        atomic_io = (
            template_roundtrip["schema_version"] == SCHEMA_VERSION
            and report_roundtrip == promote_report
        )

        reject_manifest = copy.deepcopy(base)
        reject_manifest["cases"].append(
            {
                "case_id": "safety-001",
                "split": "selection",
                "input": "Frozen safety regression fixture",
                "expected_behavior": "Preserve a hard safety invariant",
                "verifier": "Boolean hard-gate check",
                "risk": "safety",
                "provenance": "Frozen self-test fixture",
                "frozen_before_candidate": True,
                "target": False,
                "hard_gate": True,
                "active": {"passed": True, "score": 1.0},
                "candidate": {"passed": False, "score": 0.0},
            }
        )
        reject_report = evaluate_manifest(reject_manifest)
        reject = reject_report["decision"]
        audit_evidence = (
            promote_report["change_control"]["hypothesis"] == base["change_hypothesis"]
            and promote_report["artifacts"]["candidate_diff"] == base["candidate"]["diff"]
            and promote_report["case_summary"][0]["input"] == base["cases"][0]["input"]
            and reject_report["rejected_change_entry"]["failed_cases"] == ["safety-001"]
        )

        score_regression_manifest = copy.deepcopy(base)
        score_regression_manifest["cases"].append(
            {
                "case_id": "selection-regression",
                "split": "selection",
                "input": "Frozen non-target regression fixture",
                "expected_behavior": "Preserve the active frozen score",
                "verifier": "Numeric score comparison",
                "risk": "normal",
                "provenance": "Frozen self-test fixture",
                "frozen_before_candidate": True,
                "target": False,
                "hard_gate": False,
                "active": {"passed": True, "score": 1.0},
                "candidate": {"passed": True, "score": 0.1},
            }
        )
        score_regression = evaluate_manifest(score_regression_manifest)["decision"]

        qualitative_manifest = copy.deepcopy(base)
        qualitative_manifest["qualitative"] = True
        qualitative = evaluate_manifest(qualitative_manifest)["decision"]

        lapse_manifest = copy.deepcopy(base)
        lapse_manifest["failure_attribution"]["class"] = "EXECUTION_LAPSE"
        lapse = evaluate_manifest(lapse_manifest)["decision"]

        unclear_manifest = copy.deepcopy(base)
        unclear_manifest["failure_attribution"]["class"] = "UNCLEAR"
        unclear = evaluate_manifest(unclear_manifest)["decision"]

        invalid_manifest = copy.deepcopy(base)
        invalid_manifest["edit_budget"]["used"] = 5
        invalid_schema = copy.deepcopy(base)
        invalid_schema["schema_version"] = "wrong-schema"
        invalid_rollback = copy.deepcopy(base)
        invalid_rollback["rollback"] = {"path": str(candidate), "sha256": ""}
        invalid_diff = copy.deepcopy(base)
        invalid_diff["candidate"]["diff"] = "+ unrelated claimed diff\n"
        invalid_rejected = []
        for invalid_case in (invalid_manifest, invalid_schema, invalid_rollback, invalid_diff):
            try:
                evaluate_manifest(invalid_case)
            except ManifestError:
                invalid_rejected.append(True)

    expected = {
        "promote": "PROMOTE",
        "hard_regression": "REJECT_REGRESSION",
        "score_regression": "REJECT_REGRESSION",
        "qualitative": "STAGE_FOR_HUMAN_REVIEW",
        "execution_lapse": "DEFER_NOT_SCORABLE",
        "unclear_attribution": "STAGE_FOR_HUMAN_REVIEW",
        "atomic_io": "PASS",
        "audit_evidence": "PASS",
        "invalid_contracts": "PASS",
    }
    actual = {
        "promote": promote,
        "hard_regression": reject,
        "score_regression": score_regression,
        "qualitative": qualitative,
        "execution_lapse": lapse,
        "unclear_attribution": unclear,
        "atomic_io": "PASS" if atomic_io else "FAIL",
        "audit_evidence": "PASS" if audit_evidence else "FAIL",
        "invalid_contracts": "PASS" if len(invalid_rejected) == 4 else "FAIL",
    }
    if actual != expected:
        raise AssertionError(
            f"self-test failed: actual={actual}"
        )
    return actual


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Validate active/candidate skill-promotion evidence without changing live files."
    )
    parser.add_argument("manifest", nargs="?", help="Promotion evidence manifest JSON")
    parser.add_argument("--output", help="Atomically write the decision report JSON")
    parser.add_argument("--write-template", metavar="PATH", help="Write a manifest template and exit")
    parser.add_argument("--skill", default="example-skill", help="Skill name for --write-template")
    parser.add_argument("--self-test", action="store_true", help="Run deterministic built-in tests")
    args = parser.parse_args(argv)

    selected = sum(bool(value) for value in (args.manifest, args.write_template, args.self_test))
    if selected != 1:
        parser.error("choose exactly one of MANIFEST, --write-template, or --self-test")

    if args.self_test:
        result = self_test()
        print("SELF_TEST=PASS")
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return 0

    if args.write_template:
        path = Path(args.write_template)
        _atomic_write_json(path, template_manifest(args.skill))
        print(str(path.expanduser().resolve()))
        return 0

    try:
        with Path(args.manifest).expanduser().open(encoding="utf-8") as handle:
            manifest = json.load(handle)
        report = evaluate_manifest(manifest)
    except (OSError, json.JSONDecodeError, ManifestError) as exc:
        print(json.dumps({"error": str(exc), "decision": "INVALID_INPUT"}, ensure_ascii=False))
        return 2

    if args.output:
        _atomic_write_json(Path(args.output), report)
    else:
        print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
