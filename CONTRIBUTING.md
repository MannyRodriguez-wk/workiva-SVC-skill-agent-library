# Contributing

Low-friction drops. No CLI, no build step, no index editing required from you.

---

## Add a skill

1. Create **`skills/<your-skill-name>/SKILL.md`**
2. Open a **PR**

Use the starter in [`skills/README.md`](./skills/README.md) — copy, paste, edit.

**Rules:** no secrets, no customer PII, kebab-case folder name, `name:` in frontmatter matches the folder.

Maintainers update [ASSET_INDEX.md](./ASSET_INDEX.md) when your PR merges.

---

## Add an agent

1. Create **`agents/<your-agent>_agent.yaml`**
2. Open a **PR**

Use the starter in [`agents/README.md`](./agents/README.md) — copy, paste, edit.

**Rules:** reference real skill paths under `skills/`, no credentials, declare what data the agent may read/write.

The `agents/` folder is intentionally empty until someone contributes one.

---

## Before you open the PR

- [ ] No API keys, tokens, or passwords anywhere
- [ ] Triggers in `description` are clear (how the agent knows when to use it)
- [ ] Customer-facing output still needs a human review — say so in the skill/agent if relevant

---

## Review

One teammate review, then merge. Small PRs win — one skill or one agent per PR when you can.

Questions? Ping the repo owners listed in [NOTICE.md](./NOTICE.md).
