# Workiva Demo Consulting Skill Library

A **proof-of-concept** library of [Agent Skills](https://docs.claude.com/en/docs/agents-and-tools/agent-skills) built by and for the **Workiva Demo Consulting** team, with an eye toward adoption across the broader **Solution Consulting (SC)** organization.

> **Status: POC / early.** This repository is an experiment in packaging the team's repeatable workflows — portfolio tracking, board hygiene, impact reporting, demo design, and plan review — as portable, version-controlled skills. Expect rough edges. Nothing here is an official Workiva product, and skill behavior should be reviewed before it touches customer-facing or system-of-record work.

---

## Why this exists

Demo Consulting and Solution Consulting do a lot of high-leverage, repeatable knowledge work: scoping demos, keeping Monday.com boards clean, rolling up quarterly impact, and pressure-testing plans before build. Much of that lives in people's heads or in one-off prompts.

**Agent Skills** let us capture those workflows once, as structured Markdown, and reuse them consistently across the team. This library is the shared home for them so we can:

- **Standardize** how common SC tasks get done.
- **Share** proven workflows instead of re-deriving them per person.
- **Version** and review changes the same way we review code.
- **Evaluate** whether a skill library is worth scaling to the whole SC org.

## Who this is for

- **Primary:** Workiva Demo Consulting team (Manny Rodriguez, Bryan Kowal, Richie Warmkessel) and Demo Engineering / Presales SC.
- **Secondary:** The broader Workiva Solution Consulting org evaluating Agent Skills for their own workflows.
- **Contributors:** Anyone on the SC org who wants to package a repeatable workflow as a skill (see [CONTRIBUTING.md](./CONTRIBUTING.md)).

---

## Included skills

See [SKILL_INDEX.md](./SKILL_INDEX.md) for the full list with descriptions. At a glance:

| Skill | What it does |
|-------|--------------|
| [`dc-tracker`](./skills/dc-tracker/) | Rolling, quarter-indexed project ledger + branded PPTX recap deck generator for the Demo Consulting team. |
| [`monday-board-auditor`](./skills/monday-board-auditor/) | Audits the four Demo Engineering Monday.com boards for data-quality issues before reporting. |
| [`monday-impact-reporter`](./skills/monday-impact-reporter/) | Turns delivered Monday.com work into a QBR-ready leadership impact narrative. |
| [`workiva-demo-build-office-hours`](./skills/workiva-demo-build-office-hours/) | YC-style forcing-question session that produces a Demo Build Design Doc for in-platform Workiva demos. |
| [`plan-ceo-review`](./skills/plan-ceo-review/) | CEO/founder-mode plan review — challenge premises, find the 10-star product, expand or strip scope. |
| [`plan-eng-review`](./skills/plan-eng-review/) | Eng-manager-mode plan review — architecture, data flow, edge cases, tests, performance. |
| [`plan-design-review`](./skills/plan-design-review/) | Designer's-eye plan review — rates design dimensions 0–10 and fixes the plan to reach 10. |

> **Note on the `plan-*` and `office-hours` skills:** these originate from the "gstack" skill ecosystem and use extended frontmatter fields (e.g. `preamble-tier`, `interactive`, `benefits-from`, `version`). They work in that runtime but do **not** pass the stock `agentskills validate` schema. See [Validation](#validation) below. Their content has been preserved exactly as delivered.

---

## Repository layout

```
workiva-demo-consulting-skill-library/
├── README.md              # this file
├── CONTRIBUTING.md        # how to add or change a skill
├── SKILL_INDEX.md         # one-line index of every skill
├── NOTICE.md              # licensing / ownership notice (POC — terms TBD)
├── .gitignore
└── skills/
    ├── dc-tracker/
    │   └── SKILL.md
    ├── monday-board-auditor/
    │   └── SKILL.md
    ├── monday-impact-reporter/
    │   └── SKILL.md
    ├── workiva-demo-build-office-hours/
    │   └── SKILL.md
    ├── plan-ceo-review/
    │   └── SKILL.md
    ├── plan-eng-review/
    │   └── SKILL.md
    └── plan-design-review/
        └── SKILL.md
```

---

## Expected Agent Skill structure

Each skill lives in its own folder under `skills/`. The folder name is the skill's `name`. At minimum a skill is a single `SKILL.md`:

```
skills/<skill-name>/
├── SKILL.md            # required: frontmatter + instructions
├── references/         # optional: longer docs the skill can pull in on demand
├── assets/             # optional: templates, images, sample files
└── scripts/            # optional: helper scripts the skill can run
```

`SKILL.md` starts with YAML frontmatter, then the instruction body in Markdown:

```markdown
---
name: my-skill                 # kebab-case, must match the folder name
description: >                 # when to use this skill + what it does
  One or two sentences that tell the agent exactly when to invoke this
  skill and what it produces. Include the natural-language triggers.
metadata:                      # optional free-form metadata
  author: Your Name / Team
  version: 1.0.0
---

# My Skill

Instruction body the agent follows when the skill is invoked...
```

The stock validator (`agentskills validate`) accepts these frontmatter fields:
`name`, `description`, `metadata`, `allowed-tools`, `compatibility`, `license`.
Keep custom fields under `metadata:` if you want them to validate cleanly.

---

## Installing and using a skill

These skills target agent runtimes that support the Agent Skills format (e.g. Claude Code / Claude apps with skills enabled). Exact install steps depend on your runtime; the common patterns:

**Option A — copy into your skills directory**

```bash
# Claude Code user-level skills live in ~/.claude/skills/
cp -r skills/dc-tracker ~/.claude/skills/
```

**Option B — clone and point your runtime at this repo**

```bash
git clone <repo-url> workiva-demo-consulting-skill-library
# then add skills/ to your runtime's skill search path
```

Once installed, invoke a skill by describing the task in natural language (the
`description` field tells the agent when to fire), or by its slash name where the
runtime supports it (e.g. `/plan-ceo-review`).

**Validate before you rely on a skill:**

```bash
agentskills validate skills/dc-tracker
```

---

## Validation

We use the `agentskills` CLI to sanity-check skill structure:

```bash
# validate a single skill
agentskills validate skills/<skill-name>

# validate everything
for d in skills/*/; do echo "== $d =="; agentskills validate "$d"; done
```

Current status (POC):

| Skill | `agentskills validate` |
|-------|------------------------|
| `dc-tracker` | ✅ pass |
| `monday-board-auditor` | ✅ pass |
| `monday-impact-reporter` | ✅ pass |
| `workiva-demo-build-office-hours` | ⚠️ fails — extra frontmatter field `version` |
| `plan-ceo-review` | ⚠️ fails — extended `gstack` frontmatter (`benefits-from`, etc.) |
| `plan-eng-review` | ⚠️ fails — extended `gstack` frontmatter (`benefits-from`, etc.) |
| `plan-design-review` | ⚠️ fails — extra fields (`preamble-tier`, `interactive`, `version`, `triggers`) |

The four ⚠️ skills are functional in their origin runtime; the failures are
schema-strictness mismatches, not broken skills. We have intentionally **not**
edited their content. Bringing them into stock-validator compliance (e.g. moving
extended fields under `metadata:`) is tracked on the [roadmap](#roadmap).

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Short version: branch, add your skill
under `skills/<name>/`, make it pass `agentskills validate`, update
`SKILL_INDEX.md`, open a PR, get one review.

---

## Governance / review workflow

Because some of these skills touch the system of record (Monday.com boards,
quarterly impact, recap decks shown to leadership), changes get a lightweight
review:

1. **Propose** — open a PR. Never commit a new or changed skill straight to the
   default branch.
2. **Validate** — `agentskills validate` must pass for new skills (or the PR must
   explain why it can't, as with the `gstack` skills).
3. **Review** — at least one other Demo Consulting / SC team member reviews for
   accuracy of triggers, correctness of any board IDs or data sources, and that
   the skill won't silently mutate shared data without confirmation.
4. **Data-safety check** — any skill that writes to a shared system (boards,
   decks, trackers) must confirm before overwriting and must never invent data.
5. **Merge** — squash-merge with a clear message; update `SKILL_INDEX.md` in the
   same PR.

Reviewers are **not** authorized to rubber-stamp; treat skill review like code
review.

---

## Roadmap

Toward Solution Consulting adoption:

- **Phase 0 — POC (now):** Seed the library with the team's existing skills,
  prove the packaging + validation + review loop works.
- **Phase 1 — Hardening:** Bring all skills to clean `agentskills validate`
  status (normalize frontmatter), add per-skill README/usage notes, document
  data sources (board IDs, etc.) centrally.
- **Phase 2 — Broaden contributors:** Onboard the wider Demo Engineering /
  Presales SC group; add skill templates and a `scripts/` for local validation.
- **Phase 3 — SC-org rollout:** Publish install/usage guidance for the full
  Solution Consulting org, add CI to run `agentskills validate` on every PR, and
  establish ownership/maintainers per skill domain.
- **Phase 4 — Governance at scale:** Define deprecation policy, versioning
  conventions, and a review rota so the library stays trustworthy as it grows.

---

## License / ownership

This is an internal Workiva proof-of-concept. Licensing terms are not yet
settled — see [NOTICE.md](./NOTICE.md). Do not redistribute outside Workiva
without confirming terms with the repository owners.
