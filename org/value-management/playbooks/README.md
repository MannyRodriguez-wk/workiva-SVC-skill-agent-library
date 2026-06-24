# Value Management — Playbooks

Multi-step, domain-specific workflows owned by **Value Management**.

Playbooks compose the reusable, stateless capabilities in
[`core/skills/`](../../../core/skills/) and the shared prompts in
[`core/prompts/`](../../../core/prompts/) into a repeatable value-engineering
workflow, encoding VM-specific process, assumptions, and review gates.

> Status: placeholder. No VM playbooks have been migrated yet. The first
> candidate is the ROI / value-modeling workflow used by the
> [`roi-generator-agent`](../agents/roi_generator_agent.yaml).

## Adding a playbook

1. Create `org/value-management/playbooks/<playbook-name>/SKILL.md`.
2. Follow the skill frontmatter contract (see
   [`testing/schemas/skill-config.schema.json`](../../../testing/schemas/skill-config.schema.json)).
3. Reference any core skills/prompts it depends on, and note the owning agent.
4. Register it in [`ASSET_INDEX.md`](../../../ASSET_INDEX.md).
