# SVC Skill Library

A shared **AI skill library** for the Workiva **Solution Consulting (SC)** team.
Drop skills and agent configs in the repo; copy them into your own Claude app.

> **POC / early.** Not an official Workiva product. Review before customer-facing use.

---

## Start here

| You want to… | Go to… |
|--------------|--------|
| **Use** skills in Claude | [SC_USAGE_GUIDE.md](./SC_USAGE_GUIDE.md) |
| **Add** a skill or agent | [CONTRIBUTING.md](./CONTRIBUTING.md) — two steps, copy-paste templates |
| **Browse** what's available | [ASSET_INDEX.md](./ASSET_INDEX.md) |

---

## What's in the library

| Skill | Purpose |
|-------|---------|
| [`internal-apps-template-beta`](./skills/internal-apps-template-beta/SKILL.md) | Deploy internal Apps Script tools + Confluence embed |
| [`stop-slop`](./skills/stop-slop/SKILL.md) | De-AI prose editing |
| [`tufte-charts`](./skills/tufte-charts/SKILL.md) | Tufte-style charts and tables |
| [`grillme`](./skills/grillme/grillme.md) | Plan/design pressure test (`/grilling`) |

**Agents:** none yet — [`agents/`](./agents/) is ready for YAML configs.

---

## Repo layout

```
SVC-skill-library/
├── SC_USAGE_GUIDE.md      # using skills in Claude
├── CONTRIBUTING.md        # adding skills/agents (start here to contribute)
├── ASSET_INDEX.md         # catalog (maintainers keep this updated)
├── skills/                # ← drop skill folders here
│   └── README.md          # copy-paste SKILL.md starter
└── agents/                # ← drop agent YAML here (empty for now)
    └── README.md          # copy-paste agent starter
```

---

## Install a skill

```bash
git clone <repo-url> SVC-skill-library
cp -r SVC-skill-library/skills/stop-slop ~/.claude/skills/
```

Details: [SC_USAGE_GUIDE.md](./SC_USAGE_GUIDE.md)

---

## License

Internal Workiva POC — see [NOTICE.md](./NOTICE.md).
