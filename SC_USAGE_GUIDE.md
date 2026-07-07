# SC Usage Guide — Workiva SCVM Skill Library

A practical guide for Solutions Consultants (SCs), Value Management, and Demo Engineering teammates who want to use these skills in **their own Claude app** (Claude desktop, Claude Code, or another Agent Skills–compatible runtime).

> **POC status.** This library is an internal experiment. Skills are not an official Workiva product. Review outputs before customer-facing, legal, or financial use.

---

## What you get

Four portable skills in `skills/`:

| Skill | What it does | Typical use |
|-------|----------------|-------------|
| [`internal-apps-template-beta`](./skills/internal-apps-template-beta/SKILL.md) | Step-by-step deploy guide for Workiva internal web apps (Google Apps Script + clasp + Confluence embed) | Host a small internal dashboard, form, or prototype safely inside Workiva |
| [`stop-slop`](./skills/stop-slop/SKILL.md) | Removes predictable AI writing patterns from prose | Edit emails, narratives, QBR copy, customer-facing drafts |
| [`tufte-charts`](./skills/tufte-charts/SKILL.md) | Edward Tufte–style chart and table design methodology | Executive-grade visuals, dense comparison tables, minimal chartjunk |
| [`grillme`](./skills/grillme/grillme.md) | Relentless interview to pressure-test a plan or design | Run `/grilling` before you commit to a build or customer story |

Each skill is a folder with its instruction file (`SKILL.md`, or `grillme.md` for the grill skill) plus optional `references/` docs the agent loads on demand.

---

## Before you start — permissions

### Claude app / runtime permissions

When you install skills, Claude may ask to:

| Permission | Why it matters | Guidance |
|------------|----------------|----------|
| **Read skill files** | Claude loads `SKILL.md` and references when a task matches the skill | Allow for the skills directory you install. Only install skills from this trusted internal repo. |
| **Terminal / shell** | Some workflows (especially `internal-apps-template-beta`) use `clasp`, `npm`, and deploy commands | Grant only when you are actively deploying. Review every command Claude proposes before approving. |
| **File read/write** | Editing project files, HTML, Apps Script code | Scope to the project folder you opened. Do not point Claude at your entire home directory. |
| **Network / browser** | `clasp login`, opening deploy URLs, Confluence | Expected for internal-apps deploys. Use your **Workiva Google account** only. |
| **MCP or other connectors** | Not required by these four skills | If you add connectors yourself, treat them as separate permission surfaces — see Security risks below. |

**Rule of thumb:** approve tool use **per task**, not blanket “always allow.” If Claude asks to run something you do not understand, stop and ask in `#cop-ai-internal-apps` (for internal apps) or your team channel.

### Workiva / Google permissions (internal-apps skill)

The internal-apps pattern relies on:

| System | Who can do what |
|--------|------------------|
| **Google Apps Script web app** | Deployed as “Execute as Me” + “Only people in Workiva” — org-only access via Okta-backed Google |
| **Linked Google Sheet** | Anyone who can open the app can **read** rows; **writes** need edit access to the Sheet or membership in `APP_ADMINS` (Script property) |
| **Confluence embed** | Page viewers need access to the Confluence space; the iframe loads your `/exec` URL |
| **`clasp` / Apps Script editor** | Uses **your** Google identity; you own what gets pushed |

You do **not** need GitHub or a server. You **do** need a Workiva Google account, Node.js (for clasp), and Chrome for login.

### Data you may put in Claude

| OK in chat | Do not put in chat |
|------------|---------------------|
| Generic structure of an internal tool, public Workiva product concepts | Customer PII, credentials, API keys, board tokens |
| Your own draft prose for editing (`stop-slop`) | Confidential customer metrics unless approved |
| Aggregated or synthetic chart specs (`tufte-charts`) | Unredacted RFP/security questionnaire answers with customer secrets |
| Plan summaries for review (`grillme`) | Production spreadsheet IDs tied to sensitive HR/finance data without need |

If a skill needs a Sheet URL, paste only what is required (ID or URL). Remove access later if the project ends.

---

## How to navigate this repository

```
SVC-skill-library/
├── SC_USAGE_GUIDE.md          ← you are here (using skills)
├── CONTRIBUTING.md            ← adding a skill or agent (2-step drop-in)
├── ASSET_INDEX.md             ← catalog
├── skills/                    ← skill folders + README starter template
└── agents/                    ← agent YAML (empty for now) + README starter
```

- **Using skills?** Stay in this guide.
- **Contributing?** [CONTRIBUTING.md](./CONTRIBUTING.md) — copy-paste a template, open a PR. No CLI.
- **Inside a skill,** open its `SKILL.md` for triggers and instructions.

---

## Install skills in your Claude app

These steps work for Claude Code / Claude desktop with Agent Skills support. Exact UI labels may vary slightly by version.

### Option A — Copy one skill (recommended to try first)

```bash
git clone <this-repo-url> SVC-skill-library
cd SVC-skill-library

# copy one skill (skip skills/README.md — that's the contributor template)
cp -r skills/stop-slop ~/.claude/skills/
```

Repeat for each skill you want. Do not copy `skills/README.md` — that file is only for contributors.

```bash
cp -r skills/internal-apps-template-beta skills/tufte-charts skills/grillme skills/stop-slop ~/.claude/skills/
```

Restart Claude or start a new session so it picks up new skills.

### Option B — Point your runtime at the repo

Some setups let you add the repo’s `skills/` path as a skill search directory. Prefer Option A if you are unsure — fewer moving parts.

### Verify installation

Start a new chat and describe a task that matches a skill’s `description` (see [ASSET_INDEX.md](./ASSET_INDEX.md)). Claude should load the skill automatically when the task fits.

For **`grillme`**, invoke explicitly: type **`/grilling`** (or ask to “run a grilling session”). This skill sets `disable-model-invocation: true` so it only runs when you ask — it will not auto-fire on every message.

---

## How to use each skill

### `internal-apps-template-beta`

**When:** “Deploy my HTML prototype internally,” “set up clasp,” “embed app in Confluence.”

**You need:** `workiva-apps-template.zip` from internal Google Drive, Cursor (recommended), Node.js, Chrome, a blank Google Sheet.

**Flow:**

1. Ask Claude to walk through the skill step by step — it is designed for copy-paste “Ask Cursor” prompts.
2. Complete `clasp login` yourself in Chrome with your Workiva account.
3. Set `SPREADSHEET_ID` and optional `APP_ADMINS` in Apps Script script properties.
4. Deploy as web app: **Execute as Me**, **Only people in Workiva**.
5. Optional: duplicate the ENG Confluence template page and paste `Confluence.html` into the HTML macro.

**Support:** `#cop-ai-internal-apps` on Slack.

### `stop-slop`

**When:** Drafting or editing prose — emails, exec summaries, customer narratives, blog posts.

**How:** Paste your draft and ask to “apply stop-slop” or “remove AI writing patterns.” Claude uses the phrase/structure checklists in `references/`.

**You review:** Tone and factual accuracy. The skill improves *voice*; it does not verify facts.

### `tufte-charts`

**When:** “Tufte-style chart,” “maximize data-ink,” “executive-grade graphic,” dense comparison tables.

**How:** Provide data (CSV, table, or description) and the comparison you need. Claude applies design rules tool-agnostically (matplotlib, Excel, etc.).

**You review:** Numbers, baselines, and lie factor — the skill enforces design integrity rules but cannot validate your source data.

### `grillme`

**When:** Before locking a demo plan, customer story, or internal tool design.

**How:** Run **`/grilling`** and answer follow-up questions until the plan holds up.

**You review:** Whether the grilled plan still matches customer reality and Workiva policy.

---

## Security risks — read this

### 1. Prompt injection via skill content

Skills are instructions Claude trusts. **Only install skills from this internal repo** (or PRs your team reviewed). Do not drop random `.skill` files from the internet into `~/.claude/skills/`.

### 2. Secrets in chat or in code

Never paste API keys, Monday tokens, customer passwords, or `clasp` credentials into chat. Use Script Properties and env vars by **name** only. If Claude generates code with a hardcoded secret, remove it before push.

### 3. Over-trusting AI-generated deploy steps

For internal apps, Claude may suggest `clasp push`, redeploy, or Sheet changes. **You** are accountable for what runs under your Google account. Read terminal output; confirm deployment audience is still org-only.

### 4. Customer and confidential data

These skills are for **internal** and **approved** workflows. Do not feed restricted customer documents into Claude unless your role and Workiva AI policy allow it. `stop-slop` and `tufte-charts` do not redact data for you.

### 5. Internal app access model

A deployed Apps Script web app is **readable by anyone in Workiva who has the URL** (subject to deploy settings). Do not store sensitive HR, compensation, unreleased financial, or customer secrets in the linked Sheet unless access is intentionally restricted and approved.

Writes are gated by Sheet edit access / `APP_ADMINS`, but **read** is broader — design accordingly.

### 6. Confluence iframe and browser extensions

Embedded apps can break with strict privacy extensions or third-party cookie blocking. The skill documents fixes; they are usability issues, not authorization bypasses.

### 7. Fabricated Workiva policy or metrics

Claude can sound confident and be wrong. **Human review** is required for customer-facing claims, security answers, ROI numbers, and product behavior.

### 8. `grillme` is adversarial by design

It will challenge your plan aggressively. That is the point — do not treat its objections as official Workiva guidance without verifying.

---

## Quick troubleshooting

| Problem | What to try |
|---------|-------------|
| Skill never activates | New session after install; use trigger phrases from `ASSET_INDEX.md`; for `grillme`, use `/grilling` |
| Claude asks for broad file access | Narrow to one project folder; decline and restate scope |
| `clasp` / deploy errors | Re-run `clasp login`; confirm Workiva Google account; see skill Troubleshooting table |
| Output still sounds “AI” | Ask for another pass with stop-slop scoring dimensions |
| Chart looks polished but wrong | Re-check data and baselines; Tufte rules do not validate arithmetic |

---

## Getting help

| Topic | Channel / doc |
|-------|----------------|
| Internal Apps deploy | `#cop-ai-internal-apps` |
| Skill bugs or additions | Open a PR — see [CONTRIBUTING.md](./CONTRIBUTING.md) |
| Repo structure | [README.md](./README.md) |
| Catalog | [ASSET_INDEX.md](./ASSET_INDEX.md) |

---

## Checklist before customer-facing use

- [ ] Output reviewed by a human subject-matter expert  
- [ ] No secrets or customer PII in prompts, code, or Sheet data  
- [ ] Facts and metrics sourced; assumptions labeled  
- [ ] Internal apps deployed with **Only people in Workiva** (not public)  
- [ ] Sheet and Confluence space access matches data sensitivity  
