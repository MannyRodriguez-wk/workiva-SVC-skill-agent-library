# SVC Skill Library

Shared Claude skills for Workiva **SVC** — **Solution Consultants** and **Value Consultants**.

Upload here. Download from here. Not an official Workiva product.

---

## Upload a skill (do this on GitHub — no git, no PR)

Pick the right folder for what you built:

- **[→ Upload to `/demo`](https://github.com/MannyRodriguez-wk/workiva-SVC-skill-agent-library/upload/main/demo)** — live-demo-the-MCP-connector skills (routed by `/demo`)
- **[→ Upload to `/presales`](https://github.com/MannyRodriguez-wk/workiva-SVC-skill-agent-library/upload/main/presales)** — Gong/Salesforce/RFP presales-lifecycle skills
- **[→ Upload to `/skills`](https://github.com/MannyRodriguez-wk/workiva-SVC-skill-agent-library/upload/main/skills)** — everything else (general-purpose skills)

1. Click the right link above (log in with GitHub if asked)
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

Or [download everything as a ZIP](https://github.com/MannyRodriguez-wk/workiva-SVC-skill-agent-library/archive/refs/heads/main.zip), unzip, and open the **`demo`**, **`presales`**, or **`skills`** folder.

First time adding a skill to Claude on your machine? Ask in SVC Slack — 2-minute walkthrough, once.

---

## What's in here now

Three top-level sections. `/demo` and `/presales` are **anchor/router skills** — invoke the top-level skill (`/demo` or the relevant presales skill) and it routes you to the right sub-skill. `skills/` holds general-purpose, standalone skills.

| Section | Invoke as | Good for | What it does |
|---------|-----------|----------|----------------|
| `demo/*` | `/demo` → `/grc`, `/reporting`, `/analytics`, `/sustainability` | Solution & Value | Safely live-demos the Workiva internal MCP connector to a prospect — see below |
| `presales/*` | direct per-skill invocation | Solution & Value | Gong/Salesforce/RFP presales-lifecycle skills — see below |
| `skills/stop-slop` | direct | Solution & Value | Cleans up AI-sounding writing |
| `skills/tufte-charts` | direct | Value (and anyone presenting data) | Makes clean, exec-style charts |
| `skills/internal-apps-template-beta` | direct | Solution | Host small internal tools |
| `skills/grillme` | `/grilling` | Solution & Value | Pressure-tests a plan |

---

## Live MCP demo family (`/demo`)

`/demo` is the entry point — it enforces a hard safety gate (memory-off check, tenant/workspace confirmation, GRC entitlement pre-probe, live wrong-data recovery protocol) **before any MCP tool touches live data**, then routes to the domain that matches what the prospect wants to see:

| Skill | Invoke as | What it does |
|-------|-----------|--------------|
| `demo` | `/demo` | Anchor/router — safety gate + routing. Always run first. |
| `demo/grc` | `/grc` | Controls, RCM review, risk-based audit planning, remediation aging, policy search |
| `demo/reporting` | `/reporting` | Filing review, ASC/accounting-standard checks, period-over-period comparison, feature/link audits, Auto-SOI |
| `demo/analytics` | `/analytics` | Wdata OLAP/variance/forecasting on platform data |
| `demo/sustainability` | `/sustainability` | Cross-workspace CSRD/ISSB scoping (ESG + financial data) |

Shared session-safety rules and output/brand standards live in `demo/shared/`. This family exists because Wave 1 MCP Gateway testing surfaced real incidents — a cross-session memory leak that surfaced a prior demo's company name in a fresh chat, wrong-tenant connections, inconsistent GRC entitlements across workspaces, and a placeholder-data-shown-as-real chart — every sub-skill guards against these explicitly. All tools are read-only (list/get/search/run — nothing writes).

---

## Presales skill family (`/presales`)

Nine skills covering the presales lifecycle end-to-end (account brief → discovery → eval planning → demo narrative planning → handoff), plus a shared foundation folder. All are **read-only** — none of them write to Salesforce, Gong, Google Workspace, or Workiva systems. They draft output for a human to review and apply manually.

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
| `demo-framework-adapter` | Fills out the "SC Demo Planning Document" (CoM Mantra narrative/script) from the skills above — plans the demo offline, before the call. For live MCP execution during the call, see `/demo` above. |

Shared conventions and the handoff JSON schema live in `presales/shared/`. Every skill in this family tags claims with an evidence classification (`confirmed_customer_statement`, `salesforce_operating_context`, `verified_workiva_internal_fact`, `inference_working_hypothesis`, `open_question_validation_required`, `risk_assumption_dependency`) and uses `"Unknown — requires validation."` / `"Requires Workiva-source validation."` for anything unverifiable. All worked examples use fabricated accounts (e.g. "Acme Test Corp") — no real customer data.

---

## Marketplace readiness (in progress)

This repo is being brought toward Workiva's internal AI Marketplace plugin format. Self-publish into the Marketplace isn't documented yet (as of this writing it's listed as "coming soon"), so for now every skill here follows a best-effort convention — consistent frontmatter (`name`, `description`, `metadata.author/version/license`) — that will be adjusted once Workiva publishes the official manifest spec. Nothing here is blocked on that spec; skills are usable today via direct download/clone.

---

Questions → [NOTICE.md](./NOTICE.md)
