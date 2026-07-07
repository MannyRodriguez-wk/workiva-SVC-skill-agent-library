# SVC Skill Library

A shared, version-controlled **AI skill library proof-of-concept** for the
Workiva **Solution Consulting (SC)** team — portable skills SCs can install in
their own Claude app.

> **Status: POC / early.** Internal experiment — not an official Workiva product.
> Review behavior before customer-facing or system-of-record work.

---

## Start here (SCs)

**[SC_USAGE_GUIDE.md](./SC_USAGE_GUIDE.md)** — how to install skills in Claude,
permissions, navigation, per-skill usage, and **security risks**. Read this
before copying skills into `~/.claude/skills/`.

---

## What's in the library

| Skill | Purpose |
|-------|---------|
| [`internal-apps-template-beta`](./skills/internal-apps-template-beta/SKILL.md) | Deploy internal Apps Script tools + Confluence embed |
| [`stop-slop`](./skills/stop-slop/SKILL.md) | De-AI prose editing |
| [`tufte-charts`](./skills/tufte-charts/SKILL.md) | Tufte-style charts and tables |
| [`grillme`](./skills/grillme/grillme.md) | Plan/design pressure test (`/grilling`) |

Full catalog: **[ASSET_INDEX.md](./ASSET_INDEX.md)**

---

## Repository layout

```
SVC-skill-library/
├── SC_USAGE_GUIDE.md      # SC install + permissions + security (start here)
├── README.md              # this file
├── ASSET_INDEX.md         # skill catalog
├── CONTRIBUTING.md        # how to add or change a skill
├── NOTICE.md
├── .gitignore
└── skills/
    ├── internal-apps-template-beta/
    ├── stop-slop/
    ├── tufte-charts/
    └── grillme/
        └── grillme.md
```

Each skill is a folder with its instruction file (`SKILL.md`, or `grillme.md`
for the grill skill) and optional `references/`, `assets/`, or `scripts/`.

---

## Expected skill structure

```
skills/<skill-name>/
├── SKILL.md            # required: frontmatter + instructions
├── references/         # optional
├── assets/             # optional
└── scripts/            # optional
```

`SKILL.md` frontmatter (minimum):

```markdown
---
name: my-skill
description: >
  When to use this skill — triggers and outcomes in one or two sentences.
metadata:                       # optional — put custom fields here
  author: Your Name
  version: 1.0.0
---

# My Skill
...
```

Stock validator fields: `name`, `description`, `metadata`, `allowed-tools`,
`compatibility`, `license`.

---

## Installing a skill

```bash
git clone <repo-url> SVC-skill-library
cp -r SVC-skill-library/skills/stop-slop ~/.claude/skills/
```

See [SC_USAGE_GUIDE.md](./SC_USAGE_GUIDE.md) for full install options and
permission guidance.

---

## Validation

```bash
agentskills validate skills/stop-slop

for d in skills/*/; do echo "== $d =="; agentskills validate "$d"; done
```

| Skill | Expected |
|-------|----------|
| `internal-apps-template-beta` | ✅ |
| `stop-slop` | ✅ |
| `tufte-charts` | ✅ |
| `grillme` | ✅ |

---

## Contributing

See [CONTRIBUTING.md](./CONTRIBUTING.md). Branch, add under `skills/`, validate,
update `ASSET_INDEX.md`, open a PR. No secrets, ever.

---

## License / ownership

Internal Workiva proof-of-concept. See [NOTICE.md](./NOTICE.md). Do not
redistribute outside Workiva without confirming terms with repository owners.
