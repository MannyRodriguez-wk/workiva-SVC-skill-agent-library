# Asset Index — Workiva SCVM Skill Library

The unified catalog of every asset in this library. One org, one library.

**Asset types**
- **skill** — a reusable capability or workflow (`skills/<name>/SKILL.md`).
- **agent** — an identity that composes skills + prompts (`agents/<name>_agent.yaml`).
- **prompt** — a shared system prompt / persona / guardrail (`prompts/`).

**Validation legend:** ✅ passes stock `agentskills validate` · ⚠️ functional but
uses extended (`gstack`) frontmatter the stock validator rejects — content
preserved as delivered; see [README → Validation](./README.md#validation).

---

## Skills

| Asset | Function | Target audience | Used by | Validates |
|-------|----------|-----------------|---------|-----------|
| [`dc-tracker`](./skills/dc-tracker/SKILL.md) | Rolling, quarter-indexed project ledger + branded PPTX recap deck generator. Triggers: "log a project", "update the tracker", "Q1 recap", "generate the deck". | Demo Consulting / SC team | `office-hours-agent`; external `slide-deck-generator-beta`, `workiva-guidelines-beta` | ✅ |
| [`monday-board-auditor`](./skills/monday-board-auditor/SKILL.md) | Audits the four Demo Engineering Monday.com boards for data-quality issues before reporting. Triggers: "audit our boards", "what's stale", "board health check". | Demo Engineering / Presales SC | Pairs with `monday-impact-reporter` | ✅ |
| [`monday-impact-reporter`](./skills/monday-impact-reporter/SKILL.md) | Turns delivered Monday.com work into a QBR-ready leadership impact narrative. Triggers: "prep my QBR", "impact report", "leadership report". | Leadership / Presales SC | `roi-generator-agent` | ✅ |
| [`workiva-demo-build-office-hours`](./skills/workiva-demo-build-office-hours/SKILL.md) | YC-style forcing-question session producing a Demo Build Design Doc. Triggers: "help me build a demo", "demo build office hours". | Demo Engineering / Presales SC | `office-hours-agent`; bundles the three `plan-*` reviews below | ⚠️ |
| [`plan-ceo-review`](./skills/workiva-demo-build-office-hours/plan-ceo-review/SKILL.md) | CEO/founder-mode plan review — challenge premises, find the 10-star product, expand/strip scope. Triggers: "think bigger", "strategy review". | Demo Engineering / Presales SC | Nested under office-hours | ⚠️ |
| [`plan-eng-review`](./skills/workiva-demo-build-office-hours/plan-eng-review/SKILL.md) | Eng-manager-mode plan review — architecture, data flow, edge cases, tests, performance. Triggers: "review the architecture", "lock in the plan". | Demo Engineering / Presales SC | Nested under office-hours | ⚠️ |
| [`plan-design-review`](./skills/workiva-demo-build-office-hours/plan-design-review/SKILL.md) | Designer's-eye plan review — rates design dimensions 0–10 and fixes the plan to reach 10. Triggers: "review the design plan", "design critique". | Demo Engineering / Presales SC | Nested under office-hours | ⚠️ |

---

## Agents

| Asset | Function | Target audience | Composes | Status |
|-------|----------|-----------------|----------|--------|
| [`office_hours_agent.yaml`](./agents/office_hours_agent.yaml) | Runs demo-build "office hours" + plan reviews to produce a vetted Demo Build Design Doc. | Demo Engineering / Presales SC | skills: `workiva-demo-build-office-hours` (+ 3 plan reviews), `dc-tracker`; prompts: guardrails, exec persona | poc |
| [`rf_responder_agent.yaml`](./agents/rf_responder_agent.yaml) | Drafts first-pass RFP/RFI/security-questionnaire responses for human review. | Solutions Consulting | prompts: guardrails, exec persona; env: `RFX_KB_API_TOKEN` | planned |
| [`roi_generator_agent.yaml`](./agents/roi_generator_agent.yaml) | Builds defensible ROI / value models with every figure sourced and assumptions labeled. | Value Management; customer economic buyers | skills: `monday-impact-reporter`; prompts: guardrails, exec persona; env: `VALUE_MODEL_CONFIG_PATH` | planned |

---

## Prompts

| Asset | Function | Target audience |
|-------|----------|-----------------|
| [`global_guardrails.md`](./prompts/global_guardrails.md) | Org-wide AI guardrails (secrets, data boundaries, sourcing, no fabricated Workiva policy, human-review gates). Inherited by every agent. | All SCVM agents & contributors |
| [`executive_persona.txt`](./prompts/executive_persona.txt) | Concise executive-ready persona for demos and stakeholder summaries. | Execs, economic buyers, leadership |

---

Every agent inherits [`prompts/global_guardrails.md`](./prompts/global_guardrails.md):
no credentials in prompts, respect declared data boundaries, cite sources, never
fabricate Workiva policy, and require human review for customer-facing or
legal/financial output.
