# Contributing

Thanks for adding to the **Workiva SCVM Skill Library** — the org-wide AI asset
library shared by Solutions Consulting, Value Management, and Demo Engineering.
This is a proof-of-concept, so the bar is "useful, accurate, governed, and safe
for shared data." Contributions are reviewed like code. **PRs that don't meet the
rules below will be sent back.**

## Where things go (capabilities vs. identities)

Put your asset in the right place — this is the core of the architecture:

| You are adding… | Path | Type |
|-----------------|------|------|
| A reusable, stateless capability | `core/skills/<name>/SKILL.md` | skill |
| A shared prompt / persona / guardrail | `core/prompts/<name>.{md,txt}` | prompt |
| A domain agent identity | `org/<domain>/agents/<name>_agent.yaml` | agent |
| A domain-specific multi-step workflow | `org/<domain>/playbooks/<name>/SKILL.md` | playbook |

Domains: `solutions-consulting`, `value-management`, `demo-engineering`.

- **Capabilities (`core/`)** must be stateless and domain-agnostic — anything
  domain-specific belongs in `org/`.
- **Identities (`org/`)** compose capabilities; they don't re-implement them.
- **One asset, one folder/file.** Skill/playbook folder names must match the
  `name:` in frontmatter (kebab-case).
- **Don't edit someone else's asset content without asking.** Trigger wording,
  board IDs, prompts, and data sources are load-bearing. Typos/links are fine;
  behavior changes get a heads-up to the owning domain.

## Schema rules (the contribution contract)

Schemas live in [`testing/schemas/`](./testing/schemas/). Both layers must pass
before merge.

### Agents — [`agent-config.schema.json`](./testing/schemas/agent-config.schema.json)

Every agent YAML **must** include all of:

`id`, `name`, `owner_domain`, `purpose`, `status`, `prompts`, `dependencies`
(with `skills` + `playbooks`), `data_boundaries` (with `reads`, `writes`, and at
least one `prohibited`), `required_environment_variables`, `outputs`,
`review_requirements`.

Hard requirements:

- **`data_boundaries`** — declare what the agent reads, writes, and must never
  touch. At least one explicit `prohibited` entry.
- **`required_environment_variables`** — every secret/config by **NAME ONLY**
  (`^[A-Z][A-Z0-9_]*$`). **Never** put a value in the file.
- **`dependencies`** — list downstream `core/skills/...` and `org/...` paths the
  agent composes.
- `prompts` should include `core/prompts/global_guardrails.md`.

### Skills & playbooks — [`skill-config.schema.json`](./testing/schemas/skill-config.schema.json)

- Required frontmatter: `name` (kebab-case, matches folder) and `description`
  (when to invoke + what it produces + triggers).
- Stock-compatible fields: `name`, `description`, `metadata`, `allowed-tools`,
  `compatibility`, `license`. **Put custom fields under `metadata:`.**
- For imported assets with extended frontmatter (e.g. gstack), set
  `metadata.migration_status` to one of `native` /
  `preserved-extended-frontmatter` / `needs-normalization` and **do not silently
  rewrite the original content** — preserve it and document the gap.

### Run validation before you push

```bash
# stock structural check
agentskills validate core/skills/<name>          # or the playbook folder

# SCVM contract check (agents + skill/playbook frontmatter)
python3 testing/validators/validate.py           # whole repo
python3 testing/validators/validate.py <path>    # just your file(s)
```

`ERROR` blocks merge. `WARN` is allowed only for **documented** migration gaps
(the gstack playbooks). New assets should produce **no** new warnings.

## Security expectations

Non-negotiable:

- **No secrets, ever.** No API keys, tokens, passwords, connection strings, or
  cookies in any prompt, skill, agent, asset, or commit. Secrets are runtime env
  vars referenced by name only.
- **No customer PII or confidential data** in assets or sample files.
- **Respect data boundaries.** Don't add reads/writes an agent shouldn't have.
- **Never fabricate** data, metrics, customer facts, or Workiva policy. Unknowns
  are `UNKNOWN`, not guesses.
- **Confirm before writing** to any system of record; never silently overwrite.
- If you spot a committed secret, treat it as an incident: rotate and report.

These mirror [`core/prompts/global_guardrails.md`](./core/prompts/global_guardrails.md),
which every agent inherits.

## Pull requests

Branch off the default branch — **never** commit assets directly to it. Keep PRs
focused: one asset (or one logical change) per PR.

**Required PR sections:**

1. **What & where** — the asset, its type, and which `core/`/`org/<domain>/`
   path it lives in.
2. **Audience & owner** — target audience and owning domain.
3. **Dependencies** — core skills/prompts/playbooks it composes (for agents:
   confirm `dependencies` + `data_boundaries` + `required_environment_variables`
   are declared).
4. **Validation output** — paste both `agentskills validate` and
   `python3 testing/validators/validate.py` results.
5. **Data-safety statement** — what it reads/writes, and that it confirms before
   touching a system of record.
6. **Index update** — confirm [`ASSET_INDEX.md`](./ASSET_INDEX.md) is updated in
   the same PR.

**Review:** at least one reviewer; for `org/` assets that touch shared data, also
the owning domain. Treat it like code review — reviewers check trigger accuracy,
data sources, data-safety, and schema compliance. **Reviewers are not authorized
to approve their own changes or to rubber-stamp.** Squash-merge with a clear
message.

## Style

- Markdown, kebab-case asset names, US English.
- Be explicit about triggers — that's how the agent knows when to fire.
- Short, imperative instructions in skill/playbook bodies.
- No secrets, credentials, or customer PII — anywhere.
