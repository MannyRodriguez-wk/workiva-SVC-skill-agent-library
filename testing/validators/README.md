# Validators

Lightweight pre-commit / CI checks that enforce the contribution contract for
this library. Schemas live in [`../schemas/`](../schemas/).

## What gets validated

| Asset | Path glob | Schema |
|-------|-----------|--------|
| Agent identities | `org/*/agents/*.yaml` | [`agent-config.schema.json`](../schemas/agent-config.schema.json) |
| Core skills | `core/skills/**/SKILL.md` (frontmatter) | [`skill-config.schema.json`](../schemas/skill-config.schema.json) |
| Org playbooks | `org/**/playbooks/**/SKILL.md` (frontmatter) | [`skill-config.schema.json`](../schemas/skill-config.schema.json) |

Agent configs **must** declare `data_boundaries`,
`required_environment_variables`, and downstream `dependencies` — the validator
fails the build if they are missing.

## Running

```bash
# whole repo
python3 testing/validators/validate.py

# specific files (handy for pre-commit / CI on changed paths)
python3 testing/validators/validate.py org/value-management/agents/roi_generator_agent.yaml

# stock Agent Skills structural check (separate tool)
for d in core/skills/*/; do echo "== $d =="; agentskills validate "$d"; done
```

### Dependencies

- **PyYAML** (required) — parses YAML/frontmatter.
- **jsonschema** (recommended) — full Draft-07 schema validation. If it is not
  installed the validator degrades to a required-fields structural check and
  prints a `WARN`. Install both with:

  ```bash
  pip install pyyaml jsonschema
  ```

## ERROR vs WARN

- **ERROR** → non-zero exit; blocks the commit/PR. Use for true contract
  violations (missing required fields, unparseable files, schema failures).
- **WARN** → does not fail the build. Used for **known, documented migration
  gaps** — chiefly the `gstack` `plan-*` / office-hours frontmatter, which is
  preserved exactly as delivered and flagged via
  `metadata.migration_status: preserved-extended-frontmatter`.

## Wiring into pre-commit (suggested)

Add a hook that runs the validator on changed asset files:

```yaml
# .pre-commit-config.yaml (illustrative — not yet enabled)
-   repo: local
    hooks:
    -   id: scvm-asset-validate
        name: SCVM asset contract validation
        entry: python3 testing/validators/validate.py
        language: system
        files: '^(org/.*/(agents|playbooks)/|core/skills/).*'
```

CI should run the same command on every PR (see
[`../../CONTRIBUTING.md`](../../CONTRIBUTING.md)).
