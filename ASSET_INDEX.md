# Asset Index — SVC Skill & Agent Library

The catalog of every asset in this library.

**Asset types**
- **skill** — a reusable capability or workflow (`skills/<name>/SKILL.md`).
- **agent** — a config that composes skills (`agents/<name>_agent.yaml`).

**Validation legend:** ✅ passes stock `agentskills validate` · ⚠️ functional but
uses extended (`gstack`) frontmatter the stock validator rejects — content
preserved as delivered; see [README → Validation](./README.md#validation).

---

## Skills

| Asset | Function | Target audience | Used by | Validates |
|-------|----------|-----------------|---------|-----------|
| [`workiva-demo-build-office-hours`](./skills/workiva-demo-build-office-hours/SKILL.md) | YC-style forcing-question session producing a Demo Build Design Doc. Triggers: "help me build a demo", "demo build office hours". | Solution Consulting | `office-hours-agent`; bundles the three `plan-*` reviews below | ⚠️ |
| [`plan-ceo-review`](./skills/workiva-demo-build-office-hours/plan-ceo-review/SKILL.md) | CEO/founder-mode plan review — challenge premises, find the 10-star product, expand/strip scope. Triggers: "think bigger", "strategy review". | Solution Consulting | Nested under office-hours | ⚠️ |
| [`plan-eng-review`](./skills/workiva-demo-build-office-hours/plan-eng-review/SKILL.md) | Eng-manager-mode plan review — architecture, data flow, edge cases, tests, performance. Triggers: "review the architecture", "lock in the plan". | Solution Consulting | Nested under office-hours | ⚠️ |
| [`plan-design-review`](./skills/workiva-demo-build-office-hours/plan-design-review/SKILL.md) | Designer's-eye plan review — rates design dimensions 0–10 and fixes the plan to reach 10. Triggers: "review the design plan", "design critique". | Solution Consulting | Nested under office-hours | ⚠️ |

---

## Agents

| Asset | Function | Target audience | Composes | Status |
|-------|----------|-----------------|----------|--------|
| [`office_hours_agent.yaml`](./agents/office_hours_agent.yaml) | Runs demo-build "office hours" + plan reviews to produce a vetted Demo Build Design Doc. | Solution Consulting | skills: `workiva-demo-build-office-hours` (+ 3 plan reviews) | poc |

---

Agents must not embed credentials, must respect their declared data boundaries,
cite sources, never fabricate Workiva policy, and require human review for
customer-facing output. See [CONTRIBUTING.md](./CONTRIBUTING.md).
