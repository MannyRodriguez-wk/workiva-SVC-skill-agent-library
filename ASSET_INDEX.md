# Asset Index — Workiva SCVM Skill Library

The single catalog of every reusable AI asset in this library, categorized by
**asset type**, **function**, **target audience**, **owning domain**, and
**downstream dependencies**. This replaces the old `SKILL_INDEX.md`, which only
listed skills.

**Asset types**
- **skill** — a stateless, reusable capability (`core/skills/`). Domain-agnostic.
- **playbook** — a multi-step, domain-specific workflow (`org/<domain>/playbooks/`).
- **prompt** — a shared system prompt / persona / guardrail (`core/prompts/`).
- **agent** — an identity that composes skills, playbooks, and prompts
  (`org/<domain>/agents/`).
- **schema / validator** — the contribution contract and its checks (`testing/`).

**Validation legend:** ✅ passes stock `agentskills validate` · ⚠️ functional but
uses extended (`gstack`) frontmatter the stock validator rejects — content
preserved as delivered; see [README → Validation](./README.md#validation).

---

## Core capabilities (`core/`) — stateless, reusable, domain-agnostic

### Skills

| Asset | Type | Function | Target audience | Owning domain | Downstream dependencies | Validates |
|-------|------|----------|-----------------|---------------|-------------------------|-----------|
| [`dc-tracker`](./core/skills/dc-tracker/SKILL.md) | skill | Rolling, quarter-indexed project ledger + branded PPTX recap deck generator. Triggers: "log a project", "update the tracker", "Q1 recap", "generate the deck". | Demo Consulting / SC team | core | External `slide-deck-generator-beta`, `workiva-guidelines-beta` skills (deck gen) | ✅ |
| [`monday-board-auditor`](./core/skills/monday-board-auditor/SKILL.md) | skill | Audits the four Demo Engineering Monday.com boards for data-quality issues before reporting. Triggers: "audit our boards", "what's stale", "board health check". | Demo Engineering / Presales SC | core | Monday.com boards (Demo Ops, Events, Slack DM, Consensus) | ✅ |
| [`monday-impact-reporter`](./core/skills/monday-impact-reporter/SKILL.md) | skill | Turns delivered Monday.com work into a QBR-ready leadership impact narrative. Foundational stateless capability. Triggers: "prep my QBR", "impact report", "leadership report". | Leadership / Presales SC | core | Monday.com boards; pairs with `monday-board-auditor` | ✅ |

### Prompts

| Asset | Type | Function | Target audience | Owning domain | Downstream dependencies |
|-------|------|----------|-----------------|---------------|-------------------------|
| [`global_guardrails.md`](./core/prompts/global_guardrails.md) | prompt | Org-wide AI governance guardrails (secrets, data boundaries, sourcing, no fabricated Workiva policy, human-review gates). Inherited by every asset. | All SCVM agents & contributors | core | — (referenced by all agents) |
| [`executive_persona.txt`](./core/prompts/executive_persona.txt) | prompt | Concise executive-ready persona for demos and stakeholder summaries. | Execs, economic buyers, leadership | core | Composes with `global_guardrails.md` |

---

## Org assets (`org/`) — domain-specific identities & workflows

### Solutions Consulting

| Asset | Type | Function | Target audience | Owning domain | Downstream dependencies | Validates |
|-------|------|----------|-----------------|---------------|-------------------------|-----------|
| [`rf_responder_agent.yaml`](./org/solutions-consulting/agents/rf_responder_agent.yaml) | agent | Drafts first-pass RFP/RFI/security-questionnaire responses for human review. Status: planned. | Solutions Consulting | solutions-consulting | prompts: guardrails, exec persona; playbooks: SC playbooks (TBD); env: `RFX_KB_API_TOKEN` | ✅ |
| [`playbooks/`](./org/solutions-consulting/playbooks/README.md) | playbook | Placeholder for SC engagement workflows (first: RFx response). | Solutions Consulting | solutions-consulting | core skills + prompts | — |

### Value Management

| Asset | Type | Function | Target audience | Owning domain | Downstream dependencies | Validates |
|-------|------|----------|-----------------|---------------|-------------------------|-----------|
| [`roi_generator_agent.yaml`](./org/value-management/agents/roi_generator_agent.yaml) | agent | Builds defensible ROI / value models with every figure sourced and assumptions labeled. Status: planned. | Value Management; customer economic buyers | value-management | skills: `monday-impact-reporter`; prompts: guardrails, exec persona; env: `VALUE_MODEL_CONFIG_PATH` | ✅ |
| [`playbooks/`](./org/value-management/playbooks/README.md) | playbook | Placeholder for VM value-modeling workflows. | Value Management | value-management | core skills + prompts | — |

### Demo Engineering

| Asset | Type | Function | Target audience | Owning domain | Downstream dependencies | Validates |
|-------|------|----------|-----------------|---------------|-------------------------|-----------|
| [`office_hours_agent.yaml`](./org/demo-engineering/agents/office_hours_agent.yaml) | agent | Runs demo-build "office hours" + plan reviews to produce a vetted Demo Build Design Doc. Status: poc. | Demo Engineering / Presales SC | demo-engineering | playbooks: office-hours + 3 plan reviews; skills: `dc-tracker`; prompts: guardrails, exec persona | ✅ |
| [`workiva-demo-build-office-hours`](./org/demo-engineering/playbooks/workiva-demo-build-office-hours/SKILL.md) | playbook | YC-style forcing-question session producing a Demo Build Design Doc. Triggers: "help me build a demo", "demo build office hours". | Demo Engineering / Presales SC | demo-engineering | Bundles the three `plan-*` reviews below | ⚠️ |
| [`plan-ceo-review`](./org/demo-engineering/playbooks/workiva-demo-build-office-hours/plan-ceo-review/SKILL.md) | playbook | CEO/founder-mode plan review — challenge premises, find the 10-star product, expand/strip scope. Triggers: "think bigger", "strategy review". | Demo Engineering / Presales SC | demo-engineering | Nested under office-hours playbook | ⚠️ |
| [`plan-eng-review`](./org/demo-engineering/playbooks/workiva-demo-build-office-hours/plan-eng-review/SKILL.md) | playbook | Eng-manager-mode plan review — architecture, data flow, edge cases, tests, performance. Triggers: "review the architecture", "lock in the plan". | Demo Engineering / Presales SC | demo-engineering | Nested under office-hours playbook | ⚠️ |
| [`plan-design-review`](./org/demo-engineering/playbooks/workiva-demo-build-office-hours/plan-design-review/SKILL.md) | playbook | Designer's-eye plan review — rates design dimensions 0–10 and fixes the plan to reach 10. Triggers: "review the design plan", "design critique". | Demo Engineering / Presales SC | demo-engineering | Nested under office-hours playbook | ⚠️ |

---

## Testing & contribution contract (`testing/`)

| Asset | Type | Function | Target audience | Owning domain | Downstream dependencies |
|-------|------|----------|-----------------|---------------|-------------------------|
| [`agent-config.schema.json`](./testing/schemas/agent-config.schema.json) | schema | Enforces the agent contract: requires `data_boundaries`, `required_environment_variables`, and `dependencies`. | Contributors / CI | core | Validates `org/*/agents/*.yaml` |
| [`skill-config.schema.json`](./testing/schemas/skill-config.schema.json) | schema | Skill/playbook frontmatter contract; stock-compatible with a `migration_status` escape hatch. | Contributors / CI | core | Validates `core/skills/**` & `org/**/playbooks/**` SKILL.md |
| [`validators/validate.py`](./testing/validators/validate.py) | validator | Lightweight repo-wide contract check (jsonschema when available, structural fallback otherwise). | Contributors / CI | core | Uses both schemas |

---

## Governance matrix (capabilities vs. identities)

| Dimension | Core skills/prompts (`core/`) | Org agents/playbooks (`org/`) |
|-----------|------------------------------|-------------------------------|
| Nature | **Capabilities** — what the system *can do* | **Identities** — *who* does it & how |
| State | Stateless, reusable, domain-agnostic | Domain-specific process & sequencing |
| Owner | SCVM core (shared) | The named domain (SC / VM / DE) |
| Reuse | Composed by many agents | Composes core capabilities |
| Data boundaries | Declared at point of use by the calling agent | **Declared explicitly** in the agent config |
| Review gate | Code-style review | Code-style review **+** data-safety + domain owner |

Every agent inherits [`core/prompts/global_guardrails.md`](./core/prompts/global_guardrails.md)
and must declare its data boundaries, environment variables, and downstream
dependencies (enforced by the agent schema).
