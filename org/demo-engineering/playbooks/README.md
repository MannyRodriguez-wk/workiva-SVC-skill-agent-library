# Demo Engineering — Playbooks

Multi-step, domain-specific demo-build workflows owned by **Demo Engineering**.

## Migrated playbooks

### `workiva-demo-build-office-hours/`

The demo-build review workflow (formerly a top-level skill). It runs a YC-style
forcing-question "office hours" session to produce a Demo Build Design Doc, and
bundles three nested plan-review steps:

- `plan-ceo-review/` — CEO/founder-mode plan review (strategy, scope, ambition).
- `plan-eng-review/` — engineering-manager-mode review (architecture, data flow,
  edge cases, tests, performance).
- `plan-design-review/` — designer's-eye review (rates design dimensions 0–10).

These `SKILL.md` assets are **preserved exactly as delivered**. They originate
from the external "gstack" skill ecosystem and use extended frontmatter fields
(`preamble-tier`, `interactive`, `benefits-from`, `version`, `triggers`,
`gbrain`) that do not pass the stock `agentskills validate` schema. That is a
known, documented migration gap — see [`ASSET_INDEX.md`](../../../ASSET_INDEX.md)
and the root [`README.md`](../../../README.md#validation).

The owning identity is
[`org/demo-engineering/agents/office_hours_agent.yaml`](../agents/office_hours_agent.yaml),
which references this playbook and its nested reviews.
