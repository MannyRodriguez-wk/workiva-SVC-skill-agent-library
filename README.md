# Workiva SCVM Skill Library

A shared, version-controlled **AI skill library proof-of-concept** for the
**Workiva SCVM** org — Solutions Consulting, Value Management, and Demo
Engineering. We're one org sharing one library: reusable skills, the agents that
compose them, and a few shared prompt primitives.

> **Status: POC / early.** This repository is an experiment in packaging SCVM's
> repeatable workflows as portable, reviewable assets. Expect rough edges.
> Nothing here is an official Workiva product, and behavior should be reviewed
> before it touches customer-facing or system-of-record work.

---

## Why this exists

SCVM teams do a lot of repeatable, high-value work — scoping demos, keeping
Monday.com boards clean, rolling up quarterly impact, responding to RFx, building
ROI models, and pressure-testing plans before build. Much of that lives in
people's heads or in one-off prompts.

This library captures those workflows once, as structured assets, so the org can
**standardize**, **share**, **version/review**, and reuse them — and evaluate
whether a shared AI library is worth scaling across all of SCVM. It grew out of
the original *Workiva Demo Consulting Skill Library*.

---

## How it's organized

One org, one flat library. Three top-level buckets plus the docs:

- **`skills/`** — reusable capabilities and playbooks. Each skill is a folder with
  a `SKILL.md` the agent follows. Multi-step workflows (like the demo-build
  office hours + plan reviews) live here too, nested where it makes sense.
- **`agents/`** — agent identities (`*.yaml`) that *compose* skills and prompts
  into a named role, and declare their data boundaries and required env vars.
- **`prompts/`** — shared prompt primitives every agent inherits (governance
  guardrails, executive persona).
- **`ASSET_INDEX.md`** — the unified catalog of everything in the library.

```
workiva-scvm-skill-library/
├── README.md              # this file
├── CONTRIBUTING.md        # how to add or change an asset
├── ASSET_INDEX.md         # unified catalog of every asset
├── NOTICE.md              # licensing / ownership (POC — terms TBD)
├── .gitignore
├── agents/
│   ├── office_hours_agent.yaml
│   ├── rf_responder_agent.yaml
│   └── roi_generator_agent.yaml
├── prompts/
│   ├── global_guardrails.md
│   └── executive_persona.txt
└── skills/
    ├── dc-tracker/SKILL.md
    ├── monday-board-auditor/SKILL.md
    ├── monday-impact-reporter/SKILL.md
    └── workiva-demo-build-office-hours/
        ├── SKILL.md
        ├── plan-ceo-review/SKILL.md
        ├── plan-eng-review/SKILL.md
        └── plan-design-review/SKILL.md
```

The mental model is simple: **skills are what the library can do; agents are the
roles that put skills to work; prompts are the shared rules they all follow.**

> The three `plan-*` reviews are bundled **inside**
> `skills/workiva-demo-build-office-hours/` because they're used together as one
> demo-build review flow. Their `SKILL.md` contents are preserved exactly as
> delivered.

---

## The catalog

See **[ASSET_INDEX.md](./ASSET_INDEX.md)** for the full list with descriptions.
At a glance:

- **Skills:** `dc-tracker`, `monday-board-auditor`, `monday-impact-reporter`,
  `workiva-demo-build-office-hours` (+ `plan-ceo-review`, `plan-eng-review`,
  `plan-design-review`).
- **Agents:** `office-hours-agent`, `rf-responder-agent`, `roi-generator-agent`.
- **Prompts:** `global_guardrails.md`, `executive_persona.txt`.

---

## Expected skill structure

Each skill lives in its own folder under `skills/`; the folder name matches the
skill's `name`. At minimum a skill is a single `SKILL.md`:

```
skills/<skill-name>/
├── SKILL.md            # required: frontmatter + instructions
├── references/         # optional: longer docs pulled in on demand
├── assets/             # optional: templates, samples
└── scripts/            # optional: helper scripts
```

`SKILL.md` starts with YAML frontmatter, then the instruction body:

```markdown
---
name: my-skill                 # kebab-case, matches the folder name
description: >                  # when to use it + what it produces + triggers
  One or two sentences telling the agent exactly when to invoke this skill.
metadata:                       # optional free-form metadata
  author: Your Name / Team
  version: 1.0.0
---

# My Skill

Instructions the agent follows when the skill is invoked...
```

The stock validator accepts these frontmatter fields: `name`, `description`,
`metadata`, `allowed-tools`, `compatibility`, `license`. Keep custom fields under
`metadata:` so they validate cleanly.

---

## Installing and using a skill

These skills target agent runtimes that support the Agent Skills format (e.g.
Claude Code / Claude apps with skills enabled).

```bash
# copy a skill into your runtime's skills directory
cp -r skills/dc-tracker ~/.claude/skills/

# or clone the repo and point your runtime's skill search path at skills/
git clone <repo-url> workiva-scvm-skill-library
```

Once installed, invoke a skill by describing the task in natural language (the
`description` tells the agent when to fire) or by its slash name where supported
(e.g. `/plan-ceo-review`).

Agents in `agents/` are config that names which skills + prompts a role composes;
load them into a runtime that supports agent configs, or use them as a reference
for assembling the same role by hand.

---

## Validation

Skill structure is checked with the `agentskills` CLI:

```bash
# validate one skill
agentskills validate skills/dc-tracker

# validate everything
for d in skills/*/; do echo "== $d =="; agentskills validate "$d"; done
```

Current status (POC):

| Skill | `agentskills validate` |
|-------|------------------------|
| `skills/dc-tracker` | ✅ pass |
| `skills/monday-board-auditor` | ✅ pass |
| `skills/monday-impact-reporter` | ✅ pass |
| `skills/workiva-demo-build-office-hours` | ⚠️ fails — extra field `version` |
| `skills/workiva-demo-build-office-hours/plan-ceo-review` | ⚠️ fails — extended `gstack` frontmatter |
| `skills/workiva-demo-build-office-hours/plan-eng-review` | ⚠️ fails — extended `gstack` frontmatter |
| `skills/workiva-demo-build-office-hours/plan-design-review` | ⚠️ fails — extra fields (`preamble-tier`, `interactive`, `triggers`, `version`) |

The four ⚠️ skills come from the external **gstack** ecosystem and use extended
frontmatter the stock validator rejects. They are functional in their origin
runtime; the failures are schema-strictness mismatches, not broken skills, and
their content is **preserved exactly as delivered**. Normalizing them (moving
extended fields under `metadata:`) is future cleanup, not blocking.

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Short version: branch, add your asset
under `skills/`, `agents/`, or `prompts/`, validate skills with
`agentskills validate`, update `ASSET_INDEX.md`, open a small PR, get one review.
No secrets, ever.

---

## Roadmap

- **Now — POC:** Seed the library with the team's existing skills and agents;
  prove the add → validate → review loop works.
- **Next — Hardening:** Bring the gstack skills to clean validation, add per-skill
  usage notes, document data sources (board IDs, etc.).
- **Then — Broaden:** Onboard more SCVM contributors; add skill templates.
- **Later — Rollout:** Publish install/usage guidance for all of SCVM and wire
  `agentskills validate` into CI on every PR.

---

## License / ownership

Internal Workiva proof-of-concept. Licensing terms are not yet settled — see
[NOTICE.md](./NOTICE.md). Do not redistribute outside Workiva without confirming
terms with the repository owners.
