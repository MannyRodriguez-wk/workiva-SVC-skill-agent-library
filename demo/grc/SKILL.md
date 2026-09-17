---
name: demo-grc
description: "Live-demos Workiva's GRC (governance/risk/compliance) MCP surface to a prospect: control environment overview, risk-and-control-matrix (RCM) review, risk-based audit planning, remediation/issue aging, and policy search. Use when the user says: '/grc', 'show me the GRC demo', 'show me the audit/compliance demo', 'demo controls and risk to this prospect', 'demo the RCM', 'demo risk-based audit planning', or 'show me the compliance heatmap'."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# GRC (Governance / Risk / Compliance) Demo

Live-demos Workiva's GRC MCP surface — control environment overview, risk-and-control-matrix (RCM) review, risk-based audit planning, remediation/issue aging, and policy search — directly against a prospect's (or a sandboxed/synthetic) workspace.

This is a **domain sub-skill of the top-level `/demo` anchor skill** (`../SKILL.md`). The anchor skill handles session-safety gating (confirming a safe demo environment before any tool is called) before routing here — **this skill does not repeat that full gate.** It does, however, restate one final safety-net rule at the point it matters most: see §11.

Shared references:
- `../shared/session-safety.md` — full session-safety gating and recovery procedures (owned by the anchor skill; also holds the workspace-entitlement recovery guidance referenced in §5 below).
- `../shared/output-standards.md` — shared formatting/palette conventions for demo output, including the **Presentation Yellow** palette used for Audit & Risk / GRC content.

## 1. Purpose & Trigger Phrases

**Purpose:** Give a prospect a credible, hands-on look at Workiva's GRC MCP tools by walking a real (or realistic synthetic) control environment through one of the workflows below, live — control breadth in one call, an RCM drill-down, risk-based audit planning, emerging-risk gap analysis, or an interactive compliance heatmap prototype.

**Trigger phrases** (non-exhaustive — use judgment for close paraphrases):
- "/grc"
- "show me the GRC demo"
- "show me the audit/compliance demo"
- "demo controls and risk to this prospect"
- "demo the RCM" / "walk me through the risk and control matrix"
- "demo risk-based audit planning"
- "show me the compliance heatmap"
- "search our policies for X"

## 2. Required / Optional Inputs

**Required (confirm before starting):**
- Which flow the prospect wants: **audit-planning**, **risk-coverage / RCM review**, **emerging-risk**, or **heatmap prototype**.
- The target workspace to demo against.

**Optional, depending on flow:**
- The target process name (e.g., "Revenue," "Procure-to-Pay") for an RCM drill-down or audit-planning flow.
- A specific external regulation/standard of interest, for the emerging-risk flow.
- Segmentation preference (status, risk owner, risk category) for the heatmap prototype.

If the prospect hasn't specified a flow or a workspace, ask — don't guess and start pulling controls.

## 3. Tool-Search Batch Loading

Before starting any workflow, batch-load the tools you'll need with `tool_search` rather than discovering them one at a time mid-demo:

- `tool_search("grc controls issues policies")` — surfaces `grc_get_governance_workspace_settings`, `grc_aggregate_controls`, `grc_get_process`, `grc_get_process_risks_by_ids`, `grc_list_analytics_views`, `grc_run_analytics_query`, `grc_list_issues`, `grc_search_policy_sections`.
- `tool_search("grc graph test forms")` — surfaces the graph-tier tools (e.g., `grc_graph_get_sox_programs`). **Load these only for awareness — do not call them.** This tier has been denied/untested in every workspace tested so far; treat it as not-yet-demo-ready (see §4).

## 4. Tool Reference & Known Gotchas

| Tool | What it does | Gotcha to hold onto |
|---|---|---|
| `grc_get_governance_workspace_settings` | Reads Multi-Instance Controls (MIC) config | An **all-nulls response is valid** — it means MIC is off and every control is STANDALONE. Confirm via `dimensionalityType`; never treat nulls as an error. |
| `grc_aggregate_controls` | One-call rollup across 9 dimensions: process, sub-process, owner, frequency, significance, automated/manual, preventive/detective, dimensionality type, location, system, control test aging, assessment aging | Great **opening demo call** — shows breadth in one shot (control counts by process, test-aging distribution). |
| `grc_get_process` | Returns sub-processes, controls (with descriptions), risks (with descriptions), and the linked flowchart in one call | This call **is** the RCM for a process — no separate "RCM" tool exists. |
| `grc_get_process_risks_by_ids` | Returns a `mitigatingControls` array per risk | This is the **authoritative** risk-to-control link — not the ID naming convention (e.g., `REV.CR.001`), which is cosmetic only. An **empty `mitigatingControls` array = an uncovered risk** — a strong "here's a gap you didn't know you had" demo moment. |
| `grc_list_analytics_views` | Returns 5 views: Controls, Risks, Issues & Actions, CPM Assignments, Self Assessments | Use to orient the prospect before running `grc_run_analytics_query`. |
| `grc_run_analytics_query` | Runs a query against one of the 5 views | Segment grain and time granularity **must match** (e.g., `.current` with a current-state segment, not `.monthly` + `month` mismatched against a current-state segment). Responses include a `chartHint` — use it to pick the right visualization. |
| `grc_list_issues` | Lists issues/findings; supports `orderBy` (severity, status, targetRemediationDate, resolutionDate, createdAt) and filters on status/type/dates | `type` includes legacy `GENERAL`, plus `AUDIT_FINDING`, `CONTROL_ISSUE`, `GENERAL_ISSUE`. **Must query all four types** or risk silently missing issue history. |
| `grc_search_policy_sections` | Semantic similarity search over policy content | Not keyword match. Results are **not limited to published policies** unless a `documentStatuses` filter is passed. Every result carries a `documentStatus` (e.g., `DRAFT`) — **surface it**; never present a DRAFT policy as if it were approved. |
| Graph-tier (`grc_graph_get_sox_programs` and similar) | SOX-program graph queries | **Do not demo.** Denied/untested in every workspace tested so far — say so plainly if asked, rather than attempting a live call. |

## 5. Known Defects/Gaps — Guard Against These Every Time

1. **GRC entitlement is per-workspace, not per-user or global.** Real testers hit "Access denied" on GRC calls in one workspace while the identical call succeeded in another. **Do a lightweight probe call before promising a live GRC flow** — e.g., `grc_get_governance_workspace_settings` or `grc_list_analytics_views` against the target workspace. If denied, **never show the raw error to the prospect.** Smoothly pivot ("let me pull that from a different view") or fall back to a workspace known to work, per `../shared/session-safety.md`'s recovery guidance. This probe is a **mandatory step**, not a nice-to-have, in the audit-planning flow specifically (§7 step 1).
2. **Risk scoring is absent in every workspace tested.** Likelihood, impact, inherent/residual risk, and criticality all come back empty (`customFieldDataById` is empty). **Never invent or imply a risk score/rating exists.** If asked, state plainly: "risk scoring isn't populated in this environment" — do not fabricate a number.
3. **Nested `description` fields are unreliable.** A risk object's embedded `process`/`subProcess.description` can echo the wrong parent's description. Always fetch a process's own description via a **direct `grc_get_process` call** — never trust a nested field.
4. **GRC deep links (`linkCatalog`) are broken.** Every returned URL uses a non-routable `http://localhost:8080` base. **Never click through or promise a live link** during a demo — reference the destination by name instead.
5. **Owner fields may contain personal emails.** Use display names in any demo-facing output; only surface an email if the prospect specifically needs a contact.

## 6. Workflow: Control Environment Overview (Opening / Breadth Demo)

1. Confirm the target workspace.
2. Entitlement probe (§5.1): `grc_get_governance_workspace_settings`. An all-nulls response is fine — note MIC is off, every control is STANDALONE, and move on. A denial means pivot per §5.1.
3. `grc_aggregate_controls` — present the rollup across the 9 dimensions (process, sub-process, owner, frequency, significance, automated/manual, preventive/detective, dimensionality type, location, system, control test aging, assessment aging). This is the single best "here's the breadth of what you have" opening shot.
4. Optionally drill from here into §7 (RCM) for a specific process the prospect calls out.

## 7. Workflow: RCM Review (Risk-and-Control-Matrix Drill-Down)

1. Confirm the target process name and workspace.
2. `grc_get_process` for that process — this **is** the RCM: sub-processes, controls (with descriptions), risks (with descriptions), and the linked flowchart, in one call. Use this call's own `description` field for the process — never a nested `description` echoed from elsewhere (§5.3).
3. Pull the risk IDs from the process response and call `grc_get_process_risks_by_ids` to get each risk's authoritative `mitigatingControls` array.
4. **Flag any risk with an empty `mitigatingControls` array** as an uncovered risk — this is a strong, concrete demo moment ("here's a gap you didn't know you had"), not a cosmetic ID-naming observation.
5. Present the process, its controls, its risks, and coverage status (covered vs. uncovered) together as the RCM view.

## 8. Workflow: Risk-Based Audit Planning

1. **Entitlement probe first — this is mandatory for this flow specifically.** Run a lightweight probe (`grc_get_governance_workspace_settings` or `grc_list_analytics_views`) against the target workspace before promising this flow live. This exact use case has hit the entitlement-denial issue in one workspace and worked cleanly in another (§5.1) — do not skip this step or assume it will work because it worked last time in a different workspace.
2. If the probe succeeds, proceed. If denied, pivot per §5.1/`../shared/session-safety.md` — do not show the raw error and do not silently switch workspaces without narrating the pivot.
3. `grc_aggregate_controls` — pull control-test-aging and assessment-aging distributions to identify processes with stale testing.
4. For each candidate process, `grc_get_process` + `grc_get_process_risks_by_ids` (per §7) to identify coverage gaps (uncovered risks) and untested controls.
5. `grc_list_issues` across **all four** `type` values (`GENERAL`, `AUDIT_FINDING`, `CONTROL_ISSUE`, `GENERAL_ISSUE`) — ordered by severity and targetRemediationDate — to layer in existing findings and remediation status. Querying fewer than all four types risks missing issue history.
6. Synthesize: coverage gaps + untested/stale controls + open issue severity/aging → a prioritized list of processes/engagements for the audit plan.
7. Present as an executive summary: prioritized engagements, the specific gap or staleness driving each priority, and any SOX-relevant deficiency implied by an uncovered risk or a control past its test-aging window.
8. **Never attach a risk score or criticality rating to the prioritization** — risk scoring is absent in every tested workspace (§5.2). Prioritize on coverage gaps, test/assessment aging, and issue severity/aging instead, and say so if asked how prioritization was derived.

## 9. Workflow: Emerging-Risk Identification

1. Confirm the external regulation/standard of interest (if the prospect names one) and the target workspace/process scope.
2. `grc_get_process` + `grc_get_process_risks_by_ids` (per §7) across the relevant process(es) to build the current, logged risk inventory.
3. Compare the external/emerging regulation or risk theme against the logged risk inventory to identify: risks already logged and covered, risks logged but uncovered (empty `mitigatingControls`), and risk themes with **no corresponding logged risk at all**.
4. Present the gap explicitly: "here's what you already have eyes on, here's a coverage gap in what you have, and here's a theme you don't appear to have logged yet." Frame this as "staying ahead of regulatory change," not as a compliance certification.

## 10. Workflow: Compliance Heatmap Prototype

1. Confirm segmentation preference: by status, risk owner, and/or risk category (4x4 grid).
2. `grc_list_analytics_views` to confirm the Risks (and, if relevant, Issues & Actions) view is available; `grc_run_analytics_query` against it — matching segment grain and time granularity (e.g., `.current` paired with a current-state segment, not mismatched with `.monthly` + `month`) — to pull the counts needed for each quadrant.
3. Build an interactive on-screen 4x4 heatmap artifact with click-into-quadrant detail (e.g., clicking a quadrant surfaces the underlying risks/issues from the query result for that cell).
4. **Frame this explicitly as "here's what's possible," not as an official product commitment.** This directly addresses a known customer complaint about the native heatmap UX (configuration/display/clickability) — do not imply this prototype is already shipping or roadmapped; it's a live demonstration of a possibility.
5. Do not attach a risk score/rating axis to the heatmap (§5.2) — segment by status, owner, or category, not by an inherent/residual score that doesn't exist in this environment.

## 11. Output Guidance

Format all demo output per `../shared/output-standards.md`, using the **Presentation Yellow** palette for Audit & Risk / GRC content. Reference destinations by name only — never render or click through a `linkCatalog` URL (§5.4), since every one of them points at a non-routable `http://localhost:8080` base.

## 12. Read-Only / No-Write Disclaimer

This skill is **strictly read-only** against the GRC MCP surface: `list` / `get` / `search` / `run` (analytics query) operations only. It never creates, edits, deletes, or writes to any control, risk, process, issue, or policy. The heatmap prototype in §10 is an on-screen visualization artifact built from read-only query results — it is not written back into any GRC object.

## 13. Quality Checklist

Before presenting any output live:

- [ ] An entitlement probe was run against the target workspace before promising a live flow — especially for the audit-planning flow (§8, mandatory).
- [ ] An all-nulls `grc_get_governance_workspace_settings` response was treated as valid (MIC off, STANDALONE), never as an error.
- [ ] Risk coverage was assessed via `mitigatingControls` from `grc_get_process_risks_by_ids` — never inferred from ID naming convention alone.
- [ ] No risk score, rating, likelihood/impact value, or criticality figure was stated or implied anywhere in the output.
- [ ] Any process description shown came from a direct `grc_get_process` call, not a nested `process`/`subProcess.description` field.
- [ ] No `linkCatalog` URL was rendered as clickable or promised as a live link.
- [ ] Owner names shown are display names, not raw emails, unless the prospect specifically needed a contact.
- [ ] `grc_list_issues` was queried across all four `type` values, not a subset.
- [ ] Any policy search result's `documentStatus` was surfaced, and no DRAFT policy was presented as approved.
- [ ] Graph-tier tools were not called during the live demo.
- [ ] The heatmap prototype (if run) was framed as "here's what's possible," not as a committed product feature.
- [ ] Only read (`list`/`get`/`search`/`run`) tools were used — no write/create/update/delete call was made against the GRC MCP.
- [ ] Output uses the Presentation Yellow palette per `../shared/output-standards.md`.

## 14. Safety Net (Restated From `/demo` Gate)

The top-level `/demo` skill already gated this session for safety before routing here. As a final safety net during execution: **never show a raw error or fabricated data to the prospect.** If a tool call fails, returns an entitlement denial, produces unexpected/incomplete data, or produces something that doesn't look right — pause and recover per `../shared/session-safety.md` instead of improvising a plausible-looking answer live.

## 15. Worked Example — Risk-Based Audit Planning, Northwind Assurance Group (Fully Synthetic)

> All names, workspace names, process names, risk/control IDs, and figures below are fabricated for illustration only. None refer to a real workspace or a real Workiva customer.

**Scenario:** The prospect's internal audit director asks to see how Workiva could help build next quarter's risk-based audit plan from data already sitting in the platform.

1. **Confirm scope.** Flow: audit-planning. Target workspace: `"Northwind-Assurance-Sandbox"`.
2. **Batch-load tools** per §3: `grc_get_governance_workspace_settings`, `grc_aggregate_controls`, `grc_get_process`, `grc_get_process_risks_by_ids`, `grc_list_analytics_views`, `grc_run_analytics_query`, `grc_list_issues`, `grc_search_policy_sections`.
3. **Mandatory entitlement probe (§8 step 1):** `grc_get_governance_workspace_settings("Northwind-Assurance-Sandbox")` → returns all nulls. Confirmed via `dimensionalityType: null` that this means MIC is off, not a failure — every control is STANDALONE. Probe **passed**; proceeding.
4. `grc_aggregate_controls` → rollup shows the "Procure-to-Pay" process with the oldest control-test-aging bucket in the workspace (avg. 412 days since last test) and "Revenue Recognition" with two controls flagged `assessment aging: overdue`.
5. `grc_get_process("Procure-to-Pay")` → returns sub-processes, controls (e.g., `control: "PTP.CR.014 — Three-way match review"`), and risks (e.g., `risk: "Unauthorized vendor payment"`). Process description pulled from this direct call, not from any nested field on a risk object.
6. `grc_get_process_risks_by_ids([...])` for the Procure-to-Pay risk set → risk `"Unauthorized vendor payment"` returns `mitigatingControls: []` — an **empty array**. Flagged live: "this risk currently has zero mitigating controls linked to it in the system — that's a gap, not a naming-convention issue."
7. `grc_list_issues` queried across all four types (`GENERAL`, `AUDIT_FINDING`, `CONTROL_ISSUE`, `GENERAL_ISSUE`), ordered by `severity` then `targetRemediationDate` → surfaces one open `AUDIT_FINDING` on Procure-to-Pay from a prior internal audit, still unresolved at 96 days past target remediation date.
8. **Synthesize:** Procure-to-Pay is prioritized #1 for next quarter's plan — driven by (a) the oldest control-test-aging in the workspace, (b) an uncovered risk (empty `mitigatingControls`), and (c) an overdue open finding. Revenue Recognition is prioritized #2 on overdue assessment aging alone, with controls otherwise still linked to risks.
9. **Explicitly stated:** no risk score, likelihood/impact rating, or criticality figure is attached to either priority — "risk scoring isn't populated in this environment; this prioritization is built entirely from coverage gaps, test/assessment aging, and issue severity and aging."
10. **Output presented to the prospect:**

    | Priority | Process | Driver(s) | Detail |
    |---|---|---|---|
    | 1 | Procure-to-Pay | Uncovered risk + stale control testing + overdue finding | Risk "Unauthorized vendor payment" has 0 mitigating controls; avg. control-test-aging 412 days; 1 open AUDIT_FINDING, 96 days past target remediation |
    | 2 | Revenue Recognition | Overdue assessment aging | 2 controls flagged assessment-aging overdue; no uncovered risks identified |

11. **Narrative close (per §14 safety net):** if `grc_get_process_risks_by_ids` had returned malformed or partial data for Procure-to-Pay, the correct move would have been to pause and recover per `../shared/session-safety.md` — not to narrate a plausible-sounding coverage picture the tool never actually returned. Similarly, had step 3's probe come back as a genuine "Access denied" rather than an all-nulls valid response, the demo would have pivoted to a known-working workspace rather than showing the denial to the prospect.
