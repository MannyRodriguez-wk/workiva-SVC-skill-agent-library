# Solutions Consulting — Playbooks

Multi-step, domain-specific workflows owned by **Solutions Consulting**.

Playbooks compose the reusable, stateless capabilities in
[`core/skills/`](../../../core/skills/) and the shared prompts in
[`core/prompts/`](../../../core/prompts/) into a repeatable engagement workflow.
Unlike a core skill, a playbook may encode SC-specific process, sequencing, and
review gates.

> Status: placeholder. No SC playbooks have been migrated yet. The first
> candidate is the RFx response workflow used by the
> [`rf-responder-agent`](../agents/rf_responder_agent.yaml).

## Adding a playbook

1. Create `org/solutions-consulting/playbooks/<playbook-name>/SKILL.md`.
2. Follow the skill frontmatter contract (see
   [`testing/schemas/skill-config.schema.json`](../../../testing/schemas/skill-config.schema.json)).
3. Reference any core skills/prompts it depends on, and note the owning agent.
4. Register it in [`ASSET_INDEX.md`](../../../ASSET_INDEX.md).
