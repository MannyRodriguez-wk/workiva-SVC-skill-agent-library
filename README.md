# SVC Skill & Agent Library

`SVC-skill-agent-library` — a shared, version-controlled library of AI **skills**
and **agent configs** for the Workiva **Solution Consulting (SC)** team. The goal
is simple: any SC team member can download an agent config or a skill from here
and use it in their own agent runtime.

> **Status: POC / early.** This repository is an experiment in packaging SC's
> repeatable workflows as portable, reviewable assets. Expect rough edges.
> Nothing here is an official Workiva product, and behavior should be reviewed
> before it touches customer-facing work.

---

## Why this exists

SC teams do a lot of repeatable, high-value work — scoping demos, designing demo
packages, and pressure-testing plans before build. Much of that lives in people's
heads or in one-off prompts.

This library captures those workflows once, as structured assets, so the wider SC
team can **download**, **reuse**, and **improve** them instead of re-deriving them
each time.

---

## How it's organized

One flat library. Two top-level buckets plus the docs:

- **`skills/`** — reusable capabilities and playbooks. Each skill is a folder with
  a `SKILL.md` the agent follows. Multi-step workflows (like the demo-build
  office hours + plan reviews) live here too, nested where it makes sense.
- **`agents/`** — agent configs (`*.yaml`) that *compose* skills into a named
  role, and declare their data boundaries and required env vars.
- **`ASSET_INDEX.md`** — the catalog of everything in the library.

```
SVC-skill-agent-library/
├── README.md              # this file
├── CONTRIBUTING.md        # how to add or change an asset
├── ASSET_INDEX.md         # catalog of every asset
├── NOTICE.md              # licensing / ownership (POC — terms TBD)
├── .gitignore
├── agents/
│   └── office_hours_agent.yaml
└── skills/
    └── workiva-demo-build-office-hours/
        ├── SKILL.md
        ├── plan-ceo-review/SKILL.md
        ├── plan-eng-review/SKILL.md
        └── plan-design-review/SKILL.md
```

The mental model is simple: **skills are what the library can do; agents are the
roles that put skills to work.**

> The three `plan-*` reviews are bundled **inside**
> `skills/workiva-demo-build-office-hours/` because they're used together as one
> demo-build review flow. Their `SKILL.md` contents are preserved exactly as
> delivered.

---

## The catalog

See **[ASSET_INDEX.md](./ASSET_INDEX.md)** for the full list with descriptions.
At a glance:

- **Skills:** `workiva-demo-build-office-hours` (+ `plan-ceo-review`,
  `plan-eng-review`, `plan-design-review`).
- **Agents:** `office-hours-agent`.

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

## Downloading and using an asset

These assets target agent runtimes that support the Agent Skills format (e.g.
Claude Code / Claude apps with skills enabled).

```bash
# clone the library
git clone <repo-url> SVC-skill-agent-library

# copy a skill into your runtime's skills directory
cp -r SVC-skill-agent-library/skills/workiva-demo-build-office-hours ~/.claude/skills/
```

Once installed, invoke a skill by describing the task in natural language (the
`description` tells the agent when to fire) or by its slash name where supported
(e.g. `/plan-ceo-review`).

Agents in `agents/` are configs that name which skills a role composes; download
one into a runtime that supports agent configs, or use it as a reference for
assembling the same role by hand.

---

## Validation

Skill structure is checked with the `agentskills` CLI:

```bash
# validate one skill
agentskills validate skills/workiva-demo-build-office-hours

# validate everything
for d in skills/*/; do echo "== $d =="; agentskills validate "$d"; done
```

Current status (POC):

| Skill | `agentskills validate` |
|-------|------------------------|
| `skills/workiva-demo-build-office-hours` | ⚠️ fails — extra field `version` |
| `skills/workiva-demo-build-office-hours/plan-ceo-review` | ⚠️ fails — extended `gstack` frontmatter |
| `skills/workiva-demo-build-office-hours/plan-eng-review` | ⚠️ fails — extended `gstack` frontmatter |
| `skills/workiva-demo-build-office-hours/plan-design-review` | ⚠️ fails — extra fields (`preamble-tier`, `interactive`, `triggers`, `version`) |

These skills come from the external **gstack** ecosystem and use extended
frontmatter the stock validator rejects. They are functional in their origin
runtime; the failures are schema-strictness mismatches, not broken skills, and
their content is **preserved exactly as delivered**. Normalizing them (moving
extended fields under `metadata:`) is future cleanup, not blocking.

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Short version: branch, add your asset
under `skills/` or `agents/`, validate skills with `agentskills validate`, update
`ASSET_INDEX.md`, open a small PR, get one review. No secrets, ever.

---

## Roadmap

- **Now — POC:** Seed the library with a first skill + agent; prove the
  download → use → contribute loop works for the SC team.
- **Next — Hardening:** Bring the gstack skills to clean validation, add per-skill
  usage notes.
- **Then — Broaden:** Onboard more SC contributors; add skill templates.
- **Later — Rollout:** Publish download/usage guidance for the wider SC team and
  wire `agentskills validate` into CI on every PR.

---

## License / ownership

Internal Workiva proof-of-concept. Licensing terms are not yet settled — see
[NOTICE.md](./NOTICE.md). Do not redistribute outside Workiva without confirming
terms with the repository owners.
