#!/usr/bin/env python3
"""Lightweight contribution-contract validator for the Workiva SCVM Skill Library.

Validates:
  * Agent identity YAMLs under org/<domain>/agents/*.yaml against
    testing/schemas/agent-config.schema.json
  * SKILL.md frontmatter under core/skills/ and org/**/playbooks/ against
    testing/schemas/skill-config.schema.json

Design goals: practical, dependency-light, CI-friendly.
  * Uses `jsonschema` if installed (full schema validation).
  * Falls back to structural checks of the required-fields contract if not.
  * Always validates that JSON schema files and YAML/frontmatter parse.

Exit code is non-zero if any ERROR is found. WARN does not fail the build
(used for known, documented migration gaps such as gstack frontmatter).

Usage:
    python3 testing/validators/validate.py            # validate whole repo
    python3 testing/validators/validate.py PATH ...   # validate specific files
"""
from __future__ import annotations

import glob
import json
import os
import sys

try:
    import yaml
except ImportError:  # pragma: no cover
    print("ERROR: PyYAML is required (pip install pyyaml).", file=sys.stderr)
    sys.exit(2)

try:
    import jsonschema  # type: ignore
    HAVE_JSONSCHEMA = True
except ImportError:
    HAVE_JSONSCHEMA = False

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCHEMA_DIR = os.path.join(REPO_ROOT, "testing", "schemas")
AGENT_SCHEMA = os.path.join(SCHEMA_DIR, "agent-config.schema.json")
SKILL_SCHEMA = os.path.join(SCHEMA_DIR, "skill-config.schema.json")

errors: list[str] = []
warnings: list[str] = []


def err(msg: str) -> None:
    errors.append(msg)
    print(f"ERROR: {msg}")


def warn(msg: str) -> None:
    warnings.append(msg)
    print(f"WARN:  {msg}")


def ok(msg: str) -> None:
    print(f"OK:    {msg}")


def load_json(path: str):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def load_frontmatter(path: str):
    """Return parsed YAML frontmatter from a SKILL.md, or None."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    return yaml.safe_load(parts[1])


def validate_against(schema, data, label):
    if HAVE_JSONSCHEMA:
        validator = jsonschema.Draft7Validator(schema)
        found = False
        for e in sorted(validator.iter_errors(data), key=lambda x: list(x.path)):
            loc = "/".join(str(p) for p in e.path) or "<root>"
            err(f"{label}: {loc}: {e.message}")
            found = True
        return not found
    # Fallback: check top-level required fields only.
    missing = [f for f in schema.get("required", []) if f not in (data or {})]
    if missing:
        err(f"{label}: missing required fields: {', '.join(missing)}")
        return False
    return True


def main(argv: list[str]) -> int:
    # 1. JSON schema files must themselves parse.
    for sp in (AGENT_SCHEMA, SKILL_SCHEMA):
        try:
            load_json(sp)
            ok(f"schema parses: {os.path.relpath(sp, REPO_ROOT)}")
        except Exception as exc:  # noqa: BLE001
            err(f"schema does not parse: {sp}: {exc}")
            return 1

    agent_schema = load_json(AGENT_SCHEMA)
    skill_schema = load_json(SKILL_SCHEMA)

    if not HAVE_JSONSCHEMA:
        warn("jsonschema not installed — running required-fields fallback only. "
             "Install with: pip install jsonschema")

    # Resolve targets.
    if argv:
        agent_files = [f for f in argv if f.endswith((".yaml", ".yml"))]
        skill_files = [f for f in argv if f.endswith("SKILL.md")]
    else:
        agent_files = glob.glob(os.path.join(REPO_ROOT, "org", "*", "agents", "*.y*ml"))
        skill_files = (
            glob.glob(os.path.join(REPO_ROOT, "core", "skills", "**", "SKILL.md"), recursive=True)
            + glob.glob(os.path.join(REPO_ROOT, "org", "**", "playbooks", "**", "SKILL.md"), recursive=True)
        )

    # 2. Agent configs.
    for path in sorted(agent_files):
        rel = os.path.relpath(path, REPO_ROOT)
        try:
            data = yaml.safe_load(open(path, encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            err(f"{rel}: YAML parse error: {exc}")
            continue
        if validate_against(agent_schema, data, rel):
            ok(f"agent valid: {rel}")
        # folder/id sanity
        if isinstance(data, dict):
            domain = rel.split(os.sep)[1] if rel.startswith("org") else None
            if domain and data.get("owner_domain") not in (domain, "core"):
                warn(f"{rel}: owner_domain '{data.get('owner_domain')}' "
                     f"does not match folder domain '{domain}'")

    # 3. Skill / playbook frontmatter.
    for path in sorted(skill_files):
        rel = os.path.relpath(path, REPO_ROOT)
        fm = load_frontmatter(path)
        if fm is None:
            err(f"{rel}: no YAML frontmatter found")
            continue
        folder = os.path.basename(os.path.dirname(path))
        if fm.get("name") != folder:
            warn(f"{rel}: name '{fm.get('name')}' != folder '{folder}'")
        mig = (fm.get("metadata") or {}).get("migration_status")
        extended = {"preamble-tier", "interactive", "benefits-from", "triggers", "gbrain"}
        if extended & set(fm.keys()):
            warn(f"{rel}: uses extended (non-stock) frontmatter "
                 f"{sorted(extended & set(fm.keys()))} — preserved as delivered "
                 f"(migration_status={mig or 'unset'})")
        if validate_against(skill_schema, fm, rel):
            ok(f"skill valid: {rel}")

    print()
    print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
