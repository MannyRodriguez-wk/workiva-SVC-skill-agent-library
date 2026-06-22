# Contributing

Thanks for adding to the Workiva Demo Consulting Skill Library. This is a
proof-of-concept shared by the Demo Consulting team and the broader Solution
Consulting org, so the bar is "useful, accurate, and safe for shared data" —
not "perfect." Keep it practical.

## Before you start

- **One skill, one folder.** Each skill lives in `skills/<skill-name>/` and the
  folder name must match the `name:` in its frontmatter (kebab-case).
- **Don't edit someone else's skill content without asking.** Trigger wording,
  board IDs, and data sources are load-bearing. Small fixes (typos, broken
  links) are fine; behavior changes get a heads-up to the owner.

## Adding a new skill

1. **Create the folder and `SKILL.md`:**

   ```bash
   mkdir -p skills/my-skill
   $EDITOR skills/my-skill/SKILL.md
   ```

2. **Write good frontmatter.** Required: `name`, `description`. The
   `description` is what makes the agent pick your skill at the right time —
   spell out *when to use it* and the natural-language triggers, plus what it
   produces. Put any extra metadata under `metadata:` so it validates cleanly.

   ```markdown
   ---
   name: my-skill
   description: >
     One or two sentences: what this does and exactly when to invoke it.
     Use when the user says "...", "...", or any <task> request.
   metadata:
     author: Your Name / Team
     version: 1.0.0
   ---

   # My Skill

   Clear, step-by-step instructions the agent follows...
   ```

3. **Bundle extras only if needed.** Longer docs go in `references/`, templates
   and sample files in `assets/`, helper scripts in `scripts/`. Keep `SKILL.md`
   the entry point.

4. **Validate:**

   ```bash
   agentskills validate skills/my-skill
   ```

   New skills should pass. Allowed frontmatter fields are `name`, `description`,
   `metadata`, `allowed-tools`, `compatibility`, `license`. If you have custom
   fields, nest them under `metadata:`.

5. **Update the index.** Add a one-line entry to [SKILL_INDEX.md](./SKILL_INDEX.md).

6. **Open a PR** (see below).

## Writing skills that touch shared data

Several skills here read or write the system of record (Monday.com boards,
quarterly trackers, leadership decks). If yours does:

- **Never invent data.** If a field is unknown, the skill should ask, not guess.
- **Confirm before overwriting** anything in a shared system.
- **Document the data source** in the skill (board IDs, sheet names, etc.) so
  reviewers can verify it.
- **Close the loop** — the skill should summarize what it changed.

## Pull requests

- Branch off the default branch; don't commit skills directly to it.
- Keep PRs focused: one skill (or one logical change) per PR.
- In the description, say what the skill does, who it's for, and paste the
  `agentskills validate` output.
- Get **at least one review** from another Demo Consulting / SC team member.
  Treat it like code review — reviewers check trigger accuracy, data sources,
  and data-safety, and are not authorized to approve their own changes.
- Squash-merge with a clear message.

## Style

- Markdown, kebab-case skill names, US English.
- Be explicit about triggers — that's how the agent knows when to fire.
- Prefer short, imperative instructions in the skill body.
- No secrets, credentials, or customer PII in any skill or asset.
