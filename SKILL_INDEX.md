# Skill Index

All skills in this library, with short descriptions drawn from each
`SKILL.md`. Run `agentskills validate skills/<name>` to check structure.

| Skill | Description | Validates |
|-------|-------------|-----------|
| [`dc-tracker`](./skills/dc-tracker/SKILL.md) | Rolling, quarter-indexed project ledger and quarterly recap engine for the Workiva Demo Consulting team. Captures projects via interview, keeps live by-alignment and impact rollups, and generates branded PPTX recap decks. Triggers: "log a project", "update the tracker", "Q1 recap", "generate the deck". | ✅ |
| [`monday-board-auditor`](./skills/monday-board-auditor/SKILL.md) | Audits all four Demo Engineering Monday.com boards (Demo Ops, Events, Slack DM, Consensus) for data-quality issues — missing fields, stale items, unlinked deliverables — so impact reports are trustworthy. Triggers: "audit our boards", "what's stale", "board health check". | ✅ |
| [`monday-impact-reporter`](./skills/monday-impact-reporter/SKILL.md) | Generates a QBR-ready impact narrative for Demo Engineering / Presales SC by pulling delivered work from all four Monday.com boards and translating it into business value. Triggers: "prep my QBR", "impact report", "leadership report". | ✅ |
| [`workiva-demo-build-office-hours`](./skills/workiva-demo-build-office-hours/SKILL.md) | YC-style forcing-question session for designing polished, in-platform Workiva demo packages. Produces a Demo Build Design Doc (use case, audience, dataset, assets, narrative, wow moments, setup). Triggers: "help me build a demo", "demo build office hours". | ⚠️ |
| [`plan-ceo-review`](./skills/plan-ceo-review/SKILL.md) | CEO/founder-mode plan review. Rethinks the problem, hunts for the 10-star product, challenges premises, and expands or strips scope across four modes. Triggers: "think bigger", "expand scope", "strategy review", "is this ambitious enough". | ⚠️ |
| [`plan-eng-review`](./skills/plan-eng-review/SKILL.md) | Eng-manager-mode plan review. Locks in the execution plan — architecture, data flow, diagrams, edge cases, test coverage, performance — interactively with opinionated recommendations. Triggers: "review the architecture", "engineering review", "lock in the plan". | ⚠️ |
| [`plan-design-review`](./skills/plan-design-review/SKILL.md) | Designer's-eye plan review. Rates each design dimension 0–10, explains what would make it a 10, then fixes the plan to get there. Triggers: "review the design plan", "design critique". | ⚠️ |

**Legend:** ✅ passes stock `agentskills validate` · ⚠️ functional but uses
extended (`gstack`) frontmatter the stock validator rejects — content preserved
as delivered; see [README → Validation](./README.md#validation).
