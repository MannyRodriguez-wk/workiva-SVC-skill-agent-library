# Workiva SCVM Skill Library

An org-wide **AI asset library proof-of-concept** for **SCVM** — spanning
**Solutions Consulting**, **Value Management**, and **Demo Engineering**. It is a
shared, version-controlled home for the reusable AI capabilities (skills,
prompts) and domain identities (agents, playbooks) the SCVM org uses to do
repeatable, high-leverage knowledge work.

> **Status: POC / early.** This repository is an experiment in packaging SCVM's
> repeatable workflows as portable, reviewable assets. Expect rough edges.
> Nothing here is an official Workiva product, and asset behavior should be
> reviewed before it touches customer-facing or system-of-record work.

---

## Why this exists

SCVM teams do a lot of repeatable, high-value work — scoping demos, keeping
Monday.com boards clean, rolling up quarterly impact, responding to RFx, building
ROI models, and pressure-testing plans before build. Much of that lives in
people's heads or in one-off prompts.

This library captures those workflows once, as structured assets, so the org can
**standardize**, **share**, **version/review**, and **govern** them — and
evaluate whether a shared AI library is worth scaling across all of SCVM.

This is the evolution of the original *Workiva Demo Consulting Skill Library*
into an **org-wide** structure with a clean separation between **capabilities**
and **identities** (below).

---

## Architecture: capabilities vs. identities

The central design decision is a split between **what the system can do** and
**who does it**:

- **`core/` — capabilities (shared, stateless, domain-agnostic).**
  - `core/skills/` — reusable Agent Skills any domain can compose.
  - `core/prompts/` — shared prompts: governance guardrails and personas.
- **`org/<domain>/` — identities (domain-specific).**
  - `org/<domain>/agents/` — agent configs that *compose* core skills + prompts
    + domain playbooks into a named identity with declared data boundaries.
  - `org/<domain>/playbooks/` — multi-step, domain-specific workflows.
- **`testing/` — the contribution contract.** JSON schemas + a validator that
  enforce it.

Domains: `solutions-consulting`, `value-management`, `demo-engineering`.

```
workiva-scvm-skill-library/
├── README.md                 # this file
├── CONTRIBUTING.md           # PR + schema + security rules
├── ASSET_INDEX.md            # the catalog of every asset
├── NOTICE.md                 # licensing / ownership (POC — terms TBD)
├── .gitignore
├── core/
│   ├── skills/               # stateless reusable capabilities
│   │   ├── dc-tracker/
│   │   ├── monday-board-auditor/
│   │   └── monday-impact-reporter/
│   └── prompts/
│       ├── global_guardrails.md
│       └── executive_persona.txt
├── org/
│   ├── solutions-consulting/
│   │   ├── agents/rf_responder_agent.yaml
│   │   └── playbooks/        # (placeholder: README)
│   ├── value-management/
│   │   ├── agents/roi_generator_agent.yaml
│   │   └── playbooks/        # (placeholder: README)
│   └── demo-engineering/
│       ├── agents/office_hours_agent.yaml
│       └── playbooks/
│           └── workiva-demo-build-office-hours/
│               ├── SKILL.md
│               ├── plan-ceo-review/SKILL.md
│               ├── plan-eng-review/SKILL.md
│               └── plan-design-review/SKILL.md
└── testing/
    ├── schemas/
    │   ├── agent-config.schema.json
    │   └── skill-config.schema.json
    └── validators/
        ├── validate.py
        └── README.md
```

> **Structure note (demo-engineering):** the former top-level
> `workiva-demo-build-office-hours` skill and its three nested `plan-*` reviews
> are demo-build review **workflows**, so they now live as a **playbook** under
> `org/demo-engineering/playbooks/`. Their `SKILL.md` contents are **preserved
> exactly as delivered**. The owning identity is
> [`org/demo-engineering/agents/office_hours_agent.yaml`](./org/demo-engineering/agents/office_hours_agent.yaml),
> which references the playbook paths and the relevant core skills.

---

## The asset catalog

See **[ASSET_INDEX.md](./ASSET_INDEX.md)** for the full catalog, categorized by
asset type, function, target audience, owning domain, and downstream
dependencies. At a glance:

- **Core skills:** `dc-tracker`, `monday-board-auditor`, `monday-impact-reporter`.
- **Core prompts:** `global_guardrails.md`, `executive_persona.txt`.
- **Agents:** `rf-responder-agent` (SC), `roi-generator-agent` (VM),
  `office-hours-agent` (DE).
- **Playbooks:** `workiva-demo-build-office-hours` (+ `plan-ceo/eng/design-review`).

---

## Governance

Every asset inherits **[`core/prompts/global_guardrails.md`](./core/prompts/global_guardrails.md)**:
no credentials in prompts, respect declared data boundaries, cite/report sources,
never fabricate Workiva policy, and require human review for customer-facing or
legal/financial output.

| Dimension | `core/` capabilities | `org/` identities |
|-----------|----------------------|-------------------|
| Nature | what the system *can do* | *who* does it & how |
| State | stateless, reusable | domain-specific |
| Owner | SCVM core (shared) | the named domain |
| Data boundaries | declared by the calling agent | **declared in the agent config** |
| Review | code-style review | code-style review **+** data-safety **+** domain owner |

**Agent configs must declare** `data_boundaries`,
`required_environment_variables`, and downstream `dependencies` — enforced by
[`testing/schemas/agent-config.schema.json`](./testing/schemas/agent-config.schema.json).

---

## Contribution workflow

See **[CONTRIBUTING.md](./CONTRIBUTING.md)**. Short version:

1. Branch — never commit to the default branch.
2. Add the asset in the right place (`core/skills`, `core/prompts`,
   `org/<domain>/agents`, or `org/<domain>/playbooks`).
3. Make it pass validation (below).
4. Update [ASSET_INDEX.md](./ASSET_INDEX.md).
5. Open a PR with the required sections; get one review (data-safety + domain
   owner where applicable).

---

## Validation

Two layers:

```bash
# 1. Stock Agent Skills structural check (skills & playbooks)
for d in core/skills/*/; do echo "== $d =="; agentskills validate "$d"; done

# 2. SCVM contribution-contract check (agents + skill/playbook frontmatter)
python3 testing/validators/validate.py
```

Current status (POC):

| Asset | Stock `agentskills validate` |
|-------|------------------------------|
| `core/skills/dc-tracker` | ✅ pass |
| `core/skills/monday-board-auditor` | ✅ pass |
| `core/skills/monday-impact-reporter` | ✅ pass |
| `org/.../workiva-demo-build-office-hours` | ⚠️ fails — extra field `version` |
| `org/.../plan-ceo-review` | ⚠️ fails — extended `gstack` frontmatter (`benefits-from`, `gbrain`, …) |
| `org/.../plan-eng-review` | ⚠️ fails — extended `gstack` frontmatter |
| `org/.../plan-design-review` | ⚠️ fails — extra fields (`preamble-tier`, `interactive`, `triggers`, `version`) |

The four ⚠️ playbook assets originate from the external **gstack** skill
ecosystem and use extended frontmatter that the stock validator rejects. They are
**functional in their origin runtime**; the failures are schema-strictness
mismatches, not broken assets, and their content has been **preserved exactly as
delivered**. Normalizing them (moving extended fields under `metadata:` or
labeling `metadata.migration_status`) is tracked on the [rollout plan](#rollout-plan).
The SCVM validator reports these as **WARN**, not ERROR, so they do not block CI.

All three agent configs and all skill/playbook frontmatter pass the SCVM
contract check (0 errors). The SCVM validator uses `jsonschema` for full
validation when installed and falls back to a required-fields check otherwise.

---

## Rollout plan for SCVM

- **Phase 0 — POC (now):** Establish the org-wide layout
  (capabilities vs. identities), migrate existing Demo skills into `core/`, seed
  one agent per domain, and stand up the contribution contract (schemas +
  validator).
- **Phase 1 — Hardening:** Normalize the gstack playbook frontmatter to clean
  validation, flesh out the SC and VM playbooks behind their agents, and wire the
  validator into pre-commit/CI.
- **Phase 2 — Broaden contributors:** Onboard each domain's contributors, add
  asset templates, and document data sources (board IDs, KB endpoints) centrally.
- **Phase 3 — SCVM-wide rollout:** Publish install/usage guidance, run validation
  on every PR in CI, and assign maintainers/owners per domain.
- **Phase 4 — Governance at scale:** Define deprecation, versioning, and a review
  rota so the library stays trustworthy as it grows across SCVM.

---

## License / ownership

Internal Workiva proof-of-concept. Licensing terms are not yet settled — see
[NOTICE.md](./NOTICE.md). Do not redistribute outside Workiva without confirming
terms with the repository owners.
