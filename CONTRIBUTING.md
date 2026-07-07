# Contributing

Thanks for adding to the **Workiva SCVM Skill Library**. We're one org sharing
one library, so keep it simple and practical. The bar is "useful, accurate, and
safe for shared data."

## Where things go

| You are adding… | Path |
|-----------------|------|
| A reusable skill or workflow | `skills/<name>/SKILL.md` |

- **One skill, one folder.** The folder name must match the `name:` in the
  skill's frontmatter (kebab-case).
- **Don't edit someone else's skill content without asking.** Trigger wording,
  board IDs, and data sources are load-bearing. Typos and broken links are fine;
  behavior changes get a heads-up to the owner.
- **Preserve packaging.** When a skill bundles `references/`, `assets/`, or
  `scripts/`, keep them with the skill. Imported skills (e.g. gstack) keep their
  original `SKILL.md` content — don't silently rewrite it.

## Adding a skill

1. Create `skills/my-skill/SKILL.md` with frontmatter (`name`, `description`) and
   the instruction body. Put any custom fields under `metadata:`.
2. Validate it:
   ```bash
   agentskills validate skills/my-skill
   ```
3. Add a one-line entry to [ASSET_INDEX.md](./ASSET_INDEX.md).
4. Open a PR.

## Don't commit secrets

- No API keys, tokens, passwords, connection strings, or cookies — anywhere.
  Secrets are runtime env vars referenced by name.
- No customer PII or confidential data in any asset or sample file.
- Never fabricate data, metrics, or Workiva policy. Unknowns are `UNKNOWN`.
- Confirm before writing to a system of record; never silently overwrite.

## Pull requests

- Branch off the default branch; keep PRs small and focused (one asset or one
  logical change).
- Say what the asset does and paste the `agentskills validate` output for skills.
- Get **one review** from another SCVM team member. Treat it like code review —
  check triggers, data sources, and that no secrets slipped in.
- Squash-merge with a clear message.

## Style

- Markdown, kebab-case skill names, US English.
- Be explicit about triggers — that's how the agent knows when to fire.
- Short, imperative instructions in skill bodies.
