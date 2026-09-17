---
name: demo-reporting
description: "Live-demos Workiva's Documents/Spreadsheets MCP surface for Financial Reporting scenarios: filing review, accounting-standard (ASC) checks, period-over-period filing comparison, feature/link audits at scale, data-lineage tracing, and the 'Auto-SOI' style raw-dataset-to-styled-document workflow. Use when the user says: '/reporting', 'show me the financial reporting demo', 'demo document review to this prospect', 'demo Auto-SOI', 'review this filing for accounting changes', or 'compare these two filing periods'."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Financial Reporting Demo

This skill drives a live demo of Workiva's Documents/Spreadsheets MCP surface against Financial Reporting use cases: filing review, ASC/accounting-standard checks, period-over-period filing comparison, feature/link audits at scale, data-lineage tracing, and the "Auto-SOI" raw-dataset-to-styled-document workflow.

This skill is a **domain sub-skill of the top-level `/demo` anchor skill** (`../SKILL.md`). The anchor skill handles session-safety gating (confirming this is a demo/sandboxed session, not live customer data) before routing here — **this skill does not repeat that gate**. It does, however, restate one final safety-net rule at the point it matters most: see §9.

Shared references:
- `../shared/session-safety.md` — full session-safety gating and recovery procedures (owned by the anchor skill).
- `../shared/output-standards.md` — shared formatting/palette conventions for demo output, including the Purple Mountain palette used for Financial Reporting content.

## 1. Purpose & Trigger Phrases

**Purpose:** Give a prospect a credible, hands-on look at Workiva's Documents and Spreadsheets MCP tools by walking a real (or realistic synthetic) filing or dataset through one of the five demo workflows below, live.

**Trigger phrases** (non-exhaustive):
- "/reporting"
- "show me the financial reporting demo"
- "demo document review to this prospect"
- "demo Auto-SOI"
- "review this filing for accounting changes"
- "compare these two filing periods"
- "audit this document for which features are actually in use"
- "trace where this number came from"

## 2. Required / Optional Inputs

**Required (varies by workflow — confirm before starting):**
- The target document and/or workspace name(s) to demo against.

**Optional, depending on which workflow is being run:**
- The two filing periods to compare, if doing period-over-period comparison (e.g., "Q2 2026" vs. "Q3 2026" filings).
- A sample/style Word document showing the desired output format, if doing the Auto-SOI workflow.
- The raw portfolio-holdings (or other) dataset to build from, if doing the Auto-SOI workflow.
- The specific accounting standard(s) of interest, if doing ASC review (e.g., lease accounting, revenue recognition, credit-loss modeling).

If the prospect hasn't specified which workflow they want, ask — don't guess and start pulling documents.

## 3. Tool-Search Batch Loading

Before starting any workflow, batch-load the tools you'll need with `tool_search` rather than discovering them one at a time mid-demo:

- `tool_search("documents list sections")` — for `documents_list_document`, `documents_list_section`, `documents_get_section`
- `tool_search("document links footnotes")` — for `documents_list_link`
- `tool_search("spreadsheets sheets cell range")` — for `spreadsheets_list_spreadsheet`, `spreadsheets_list_sheet`, `spreadsheets_get_cell_range`

Loading these up front avoids an awkward mid-demo pause while tools resolve.

## 4. Core Drill-Down Chain (applies to every workflow below)

Reading any filing content follows the same chain:

1. `documents_list_document` — find the target document.
2. `documents_list_section` — list the outline. **This returns structure only (IDs and names) — not section content.** Do not attempt to summarize or quote from a `list_section` response as if it were the text.
3. `documents_get_section` — actually fetch the text of a specific section, by `sectionId`.

### Gotcha 1 — track sections by `sectionId`, never by `index`

`index` in a `list_section` response is a **sibling position within that nesting level only** — it resets to 0 at every level of nesting. Two completely different sections at two different nesting levels can both be `index: 0`. If you track "the section I want" by its index instead of its `sectionId`, you will silently fetch the wrong section — this will not error, it will just be wrong. Always record and reference `sectionId`.

### Gotcha 2 — reuse `revision` across every paginated call for the same listing

`documents_list_section` (and document listing generally) can page. Every paginated response carries a `revision` value tied to the document's state at the moment of the first page. **That same `revision` must be passed on every subsequent page request for that listing.** Dropping it risks stitching together an outline from two different document revisions — sections from a Tuesday draft mixed with sections from a Thursday draft, silently combined into one "outline" that never existed. This is a real, verified failure mode, not a theoretical one.

Also check `incomplete` / `nextOffset` on every page. A first page is not necessarily the whole outline — if `incomplete` is true or a `nextOffset` is present, there are more sections to fetch before you can say you've seen the full structure.

## 5. Workflow: ASC / Accounting-Standard Review

1. Confirm the target filing (document/workspace) and, if the prospect named one, the accounting standard(s) of interest (lease accounting, revenue recognition, credit-loss modeling, etc.).
2. `documents_list_document` to locate the filing.
3. `documents_list_section` (respecting pagination/`revision` rules in §4) to build the outline, focusing on notes/footnote sections likely to discuss accounting policy (e.g., "Summary of Significant Accounting Policies," "Leases," "Revenue Recognition," "Allowance for Credit Losses").
4. `documents_get_section` (by `sectionId`) on each candidate section to read the actual policy language.
5. Compare the language against the standard in question for staleness or inconsistency — e.g., references to a superseded lease-accounting standard, revenue-recognition disclosure language that doesn't match the standard the entity claims to follow elsewhere, credit-loss modeling language that doesn't match current expected-credit-loss guidance.
6. **Never assert a compliance conclusion.** Output must flag specific sections/notes with the standard in question and state that this requires human/audit review — this skill surfaces candidates for review, it does not certify compliance.

## 6. Workflow: Period-over-Period Filing Comparison

1. Confirm both filing periods (e.g., Q2 vs. Q3) and, if named, the specific footnote/topic to diff (e.g., revenue recognition).
2. `documents_list_document` for each period's filing.
3. `documents_list_section` on each (respecting §4 pagination rules) to locate the matching footnote/section in both periods — match by section name/topic, since `sectionId` values will generally differ across separate document instances.
4. `documents_get_section` (by `sectionId`) on the matching section in each period.
5. Diff the language for material changes — new language, removed language, changed figures, changed hedging/qualifying language.
6. Frame the output for whichever lens the prospect cares about: investor-relevance ("what would an analyst flag") or audit-concern relevance ("what would an auditor want explained"). Ask which lens matters if it isn't obvious.

## 7. Workflow: Feature / Link Audit at Scale

1. Confirm the target document (or, if the prospect wants a workspace-wide sweep, the workspace and the list of documents in scope — see caveat below).
2. `documents_list_link` against the document to enumerate range links, destination links, and rich-text anchors in use.
3. Cross-reference against the outline from `documents_list_section` to identify "phantom" helper sections (sections that exist only to feed a chart or calculation elsewhere, not to be read directly) and structured tables.
4. Summarize what's actually configured and in active use (range links, destination links, phantom helper sections, structured tables, shared style guides) versus what looks like legacy/unused structure.
5. **Workspace-wide sweep caveat:** there is no confirmed single bulk tool that fetches every link across many documents/workspaces at once. If a prospect asks for a workspace-wide sweep, say so explicitly — the real mechanism is iterating `documents_list_link` once per document in scope, not one bulk call. Set that expectation before starting, especially if the workspace is large (this affects how long the live demo will take).

## 8. Workflow: Auto-SOI (Raw Dataset → Styled Output Document)

1. Confirm the raw portfolio-holdings dataset (or other raw dataset) and the sample/style Word document showing the desired output.
2. Read the raw dataset directly (e.g., via the relevant Wdata spreadsheet surface — `spreadsheets_list_spreadsheet` → `spreadsheets_list_sheet` → `spreadsheets_get_cell_range`). This crosses into analytics/Wdata territory; coordinate with whichever skill/process owns that surface rather than duplicating it here — this skill's job is reading the dataset directly for this workflow, not re-implementing Wdata analytics.
3. Recall the **cell-range gotcha**: `spreadsheets_get_cell_range` uses sheet-local A1 notation and is **sparse** — a cell with nothing in it is simply absent from the response. Do not read an absent cell as a zero or blank value; absence means "no data returned for that cell," not "confirmed zero."
4. Use the sample Word document to infer the desired structure, styling, and footnote-legend convention for the output.
5. Generate a styled Statement of Investments (SOI) Word document with a footnote legend, matching the sample's structure.
6. **State two things explicitly in the demo narrative, every time:**
   - Workiva Development is independently building a **native Auto-SOI builder** on the product roadmap. Always frame this capability as an **analysis aid / accelerator** you can demo today — never as a replacement for, competitor to, or preview of that roadmap feature.
   - The generated Word document is **not automatically inside Workiva.** It must be manually imported back into the platform if it's meant to become part of a larger filing. Never imply the work is "done" in the sense of already being part of a filing — state the manual-import step plainly.

## 9. Naming Heuristic (Tip, Not a Platform Guarantee)

When exploring Wdata tables/queries during a demo, it's often — not always — true that:
- A numeric prefix ties a Wdata table to a saved query (e.g., `"1_GL Data Table"` ↔ `"1_GL Detail Drill Through"`).
- A leading underscore typically marks a staging file (e.g., `"_staging_import"`).

Mention this as a helpful pattern to look for, not as a rule the platform enforces — don't assert it as fact if the naming in a specific workspace doesn't follow it.

## 10. Read-Only / No-Write Disclaimer

This skill is **strictly read-only** against the Documents/Spreadsheets MCP surface: `list`/`get`/`search`/`run` (read) operations only. It never creates, edits, deletes, or writes to any document, section, spreadsheet, or workspace. The one exception is the Auto-SOI workflow's *generated output artifact* (§8) — that new Word document is produced as a demo deliverable, not written back into any existing filing, workspace, or document via a write call.

## 11. Output Guidance

Format all demo output per `../shared/output-standards.md`, using the **Purple Mountain palette** for Financial Reporting content. Keep section/citation references anchored to `sectionId` (never `index`) so the prospect (or a teammate reviewing the transcript later) can re-locate exactly what was shown.

## 12. Quality Checklist

Before presenting any output live:

- [ ] Every section reference is tracked/cited by `sectionId`, never by `index`.
- [ ] Every paginated `list_section` (or similar) call reused the same `revision` as prior pages for that listing; `incomplete`/`nextOffset` was checked before declaring the outline complete.
- [ ] No `list_section` response was treated as if it contained section content — content only comes from `get_section`.
- [ ] Absent cells from `spreadsheets_get_cell_range` were treated as "no data returned," never as zero.
- [ ] ASC-review output flags sections/standards for review — it does not assert a compliance conclusion.
- [ ] Auto-SOI output explicitly states (a) this is an accelerator, not a replacement for the native roadmap feature, and (b) the generated doc requires manual import to become part of a filing.
- [ ] Any "workspace-wide" link-audit ask was scoped honestly as iterative per-document calls, not a single bulk call.
- [ ] Only read (`list`/`get`/`search`/`run`) tools were used — no write/create/update/delete call was made against the Documents/Spreadsheets MCP.
- [ ] Output uses the Purple Mountain palette per `../shared/output-standards.md`.

## 13. Safety Net (Restated From `/demo` Gate)

The top-level `/demo` skill already gated this session for safety before routing here. As a final safety net during execution: **never show a raw error or fabricated data to the prospect.** If a tool call fails, returns unexpected/incomplete data, or produces something that doesn't look right — pause and recover per `../shared/session-safety.md` instead of improvising a plausible-looking answer live.

## 14. Worked Example — ASC Review, Northwind Test Holdings (Fully Synthetic)

> All names, workspace names, document names, section names, and figures below are fabricated for illustration only. None refer to a real filing or a real Workiva customer.

**Scenario:** The prospect asks to see how Workiva could help their audit team review a recent 10-K-style annual filing for outdated lease-accounting language, ahead of an internal review cycle.

1. **Confirm scope.** Target document: `"Northwind Test Holdings — FY2026 Annual Filing"`, workspace `"NWTH-FinRep-Sandbox"`. Standard of interest: lease accounting.
2. **Batch-load tools** per §3: `documents_list_document`, `documents_list_section`, `documents_get_section`, `documents_list_link`.
3. `documents_list_document` → locates `"Northwind Test Holdings — FY2026 Annual Filing"` (`documentId: doc-nwth-fy26-001`).
4. `documents_list_section` (page 1, `revision: rev-8842`) → returns an outline including `sectionId: sec-4471 ("Note 8 — Leases")` at `index: 3` under the "Notes to Financial Statements" node. Page 2 is fetched with the **same `revision: rev-8842`**; `incomplete: false` confirms the outline is complete. `sec-4471` is recorded by ID — its `index` of 3 is not used for anything past this step.
5. `documents_get_section(sectionId: sec-4471)` → returns the actual note text: *"The Company accounts for leases in accordance with ASC 840..."*
6. **Flag, don't conclude:** ASC 840 was superseded by ASC 842 for most reporting entities. The note's language is flagged as referencing a standard that may be outdated relative to current guidance — **this is surfaced as a candidate for audit/human review, not asserted as a compliance finding.**
7. **Output presented to the prospect:**

   | Section | sectionId | Standard Referenced | Flag | Disposition |
   |---|---|---|---|---|
   | Note 8 — Leases | sec-4471 | ASC 840 (as written in note text) | Possibly outdated — ASC 840 was superseded by ASC 842 | Flagged for human/audit review — not a compliance conclusion |

8. **Narrative close (per §13 safety net):** if, mid-demo, `documents_get_section` had returned an error or truncated text for `sec-4471`, the correct move would have been to pause and recover per `../shared/session-safety.md` — not to narrate a plausible-sounding note the tool never actually returned.
