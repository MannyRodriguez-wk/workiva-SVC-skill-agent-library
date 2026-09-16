# SVC Skill Library

Shared Claude skills for Workiva **SVC** — **Solution Consultants** and **Value Consultants**.

Upload here. Download from here. Not an official Workiva product.

---

## Upload a skill (do this on GitHub — no git, no PR)

**[→ Upload directly to skills folder](https://github.com/MannyRodriguez-wk/workiva-SVC-skill-agent-library/upload/main/skills)**

1. Click the link above (log in with GitHub if asked)
2. Drag your skill **folder** into the page  
   *(folder must contain a `SKILL.md` file — ask Claude to help you make one)*
3. Scroll down → click **Commit changes**  
   *(leave the default “Commit directly to the main branch” selected)*

You're done. Every SVC consultant can download it immediately.

**Upload an agent config instead?**  
**[→ Upload directly to agents folder](https://github.com/MannyRodriguez-wk/workiva-SVC-skill-agent-library/upload/main/agents)** — drag a `.yaml` file.

### First time? You need GitHub access once

If the upload link says you don’t have permission, message **Manny Rodriguez** (or Bryan Kowal / Richie Warmkessel) — they’ll add you to the repo. After that, you upload yourself anytime.

### Three rules

- No passwords or API keys  
- No customer private info  
- You checked anything customer-facing before it goes out the door  

Optional safety notes: [SAFETY.md](./SAFETY.md)

---

## Download a skill

**[Browse all skills →](https://github.com/MannyRodriguez-wk/workiva-SVC-skill-agent-library/tree/main/skills)**

Or [download everything as a ZIP](https://github.com/MannyRodriguez-wk/workiva-SVC-skill-agent-library/archive/refs/heads/main.zip), unzip, open the **`skills`** folder.

First time adding a skill to Claude on your machine? Ask in SVC Slack — 2-minute walkthrough, once.

---

## What’s in here now

| Folder | Good for | What it does |
|--------|----------|----------------|
| `stop-slop` | Solution & Value | Cleans up AI-sounding writing |
| `tufte-charts` | Value (and anyone presenting data) | Makes clean, exec-style charts |
| `internal-apps-template-beta` | Solution | Host small internal tools |
| `grillme` | Solution & Value | Pressure-tests a plan (`/grilling`) |
| `presales/*` | Solution & Value | Gong/Salesforce/RFP presales workflow skills — see below |

---

## Presales skill family (`skills/presales/`)

Nine skills covering the presales lifecycle end-to-end, plus a shared foundation folder. All are **read-only** — none of them write to Salesforce, Gong, Google Workspace, or Workiva systems. They draft output for a human to review and apply manually.

| Skill | What it does |
|-------|--------------|
| `core-presales-intelligence` | Reference-only: shared evidence taxonomy, fallback strings, connector list, handoff schema. Not directly invoked. |
| `account-opportunity-brief` | One-page account/opportunity kickoff brief from Salesforce context |
| `gong-discovery-analysis` | Discovery-call intelligence (themes, pain points, objections) from Gong |
| `technical-discovery-planner` | Builds a technical-discovery call agenda from prior context |
| `evaluation-validation-planner` | POC/eval success criteria, timeline, and risk plan |
| `salesforce-draft-updates` | Drafts (never submits) Salesforce field updates for manual review |
| `rfp-security-analysis` | Drafts RFP/security-questionnaire answers against Workiva's documented posture |
| `presales-handoff` | Consolidates the above into a handoff packet for Implementation/CS |
| `workiva-mcp-adapter` | Adapter: enriches handoff payloads against internal Workiva GRC/Documents MCP |
| `demo-framework-adapter` | Adapter: turns handoff payloads into a demo-environment plan |

Shared conventions and the handoff JSON schema live in `skills/presales/shared/`. Every skill in this family tags claims with an evidence classification (`confirmed_customer_statement`, `salesforce_operating_context`, `verified_workiva_internal_fact`, `inference_working_hypothesis`, `open_question_validation_required`, `risk_assumption_dependency`) and uses `"Unknown — requires validation."` / `"Requires Workiva-source validation."` for anything unverifiable. All worked examples use fabricated accounts (e.g. "Acme Test Corp") — no real customer data.

---

## Marketplace readiness (in progress)

This repo is being brought toward Workiva's internal AI Marketplace plugin format. Self-publish into the Marketplace isn't documented yet (as of this writing it's listed as "coming soon"), so for now every skill here follows a best-effort convention — consistent frontmatter (`name`, `description`, `metadata.author/version/license`) — that will be adjusted once Workiva publishes the official manifest spec. Nothing here is blocked on that spec; skills are usable today via direct download/clone.

---

Questions → [NOTICE.md](./NOTICE.md)
