---
name: demo-analytics
description: "Live-demos Workiva's Wdata (data/analytics) MCP surface to a prospect: dimensional/OLAP analysis, actual-vs-budget variance, revenue forecasting, and data-quality/rollup detection, run directly against platform data with no export to an external BI tool. Use when the user says: '/analytics', 'show me the Wdata demo', 'show me the OLAP demo', 'demo forecasting to this prospect', 'demo variance analysis', or 'run the analytics demo on platform data'."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Demo: Analytics (Wdata / OLAP)

Live-demos Workiva's Wdata MCP surface — dimensional/OLAP analysis, Actual-vs-Budget variance, forecasting, and data-quality/rollup detection — run directly against platform data. Nothing here gets exported to an external BI tool first; the whole point of the demo is that the analysis happens *on* the governed dataset the prospect already trusts.

This is a **domain sub-skill** of the top-level `../SKILL.md` (`/demo`) anchor skill. The anchor skill handles session-safety gating (confirming a safe demo environment, sandboxed/synthetic data posture, etc.) before routing here — this skill does not repeat that full gate. It does, however, restate one final safety-net rule at the end (Section 9), because a live prospect demo is exactly the moment a raw error or fabricated number does the most damage.

Linked shared references:
- `../shared/session-safety.md` — full session-safety gate (owned by the anchor skill; consult if anything here seems to conflict with a live safety check).
- `../shared/output-standards.md` — formatting/branding standard for demo output.

## 1. Purpose & Trigger Phrases

**Purpose:** Run a credible, narratable live demo of Workiva's Wdata query surface for a prospect, built around the one currently-tested Wave 1 scenario: OLAP analysis and forecasting directly on Income Statement data. Demonstrate two distinct value props without conflating them:

1. **Dimensional analysis without leaving the platform** — a credible alternative to exporting to an external BI tool for ad hoc / moderate-complexity questions, while staying anchored to the same governed, curated dataset the prospect already trusts.
2. **Predictive forecasting directly on platform data** — explicitly forward-looking. There is no existing demo precedent for this beyond the Wave 1 test. Present it as a capability worth validating live with this prospect, not as a proven, polished workflow. Do not oversell it.

**Trigger phrases** (non-exhaustive — use judgment for close paraphrases):
- `/analytics`
- "show me the Wdata demo"
- "show me the OLAP demo"
- "demo forecasting to this prospect"
- "demo variance analysis"
- "run the analytics demo on platform data"
- "can Workiva do dimensional analysis without exporting to [BI tool]"

## 2. Required / Optional Inputs

**Required:**
- A target Wdata table, saved query, or workspace to demo against (name, GUID, or "use the flagship saved query for [workspace]").

**Optional:**
- Time range of interest (e.g., trailing 12 months, specific fiscal year).
- Dimensions of interest (account, time, channel, product, entity — whatever the prospect's own reporting structure emphasizes).
- Known prospect pain point to anchor the narrative (e.g., "they currently export to Tableau for this," or "they've been burned by a rollup double-count before").

If no target is specified, ask which workspace/table/saved query to use before running anything — do not guess a GUID.

## 3. Tool-Search Batch Loading

Batch-load the Wdata tools before starting rather than discovering them one at a time mid-demo:

- `tool_search("wdata query tables")` — surfaces `wdata_search_query`, `wdata_get_query`, `wdata_run_query`, `wdata_list_table`.
- `tool_search("query result download")` — surfaces `wdata_get_query_result`, `wdata_download_query_result`.

Confirm all five are loaded before beginning Section 4's workflow so the demo doesn't stall on a tool-search call in front of the prospect.

## 4. FROM-Clause Grammar (read this before writing any query)

Getting the `FROM` clause wrong is the single most common hard failure in this demo. Confirm the source type first, then use the matching clause exactly:

| Source | FROM clause |
|---|---|
| Wdata table (default) | `FROM "workspaceId"."tableId"` |
| Workiva spreadsheet | `FROM spreadsheets."workbookId"."sheetId"` |
| Saved query | `FROM queries."workspaceId"."queryId"` |
| External Snowflake | `FROM external."workspaceId"."tableId"` |
| Business data | `FROM business_data."workspaceId"."tableId"` |
| ESG program | `FROM program."workspaceId"."tableId"` (or `program_v2`) |
| Graph reports | `FROM graph."workspaceId"."tableId"` |
| Common Object Model | `FROM com."workspaceId"."tableId"` |
| Identity services | `FROM iam."workspaceId"."tableId"` |
| Frameworks explorer | `FROM explorer."workspaceId"."tableId"` (or `explorer_v2`) |

Additional dialect rules (Presto, SELECT-only, no writes ever):
- Tables are referenced by GUID and **must be aliased**.
- Always include an explicit `LIMIT`.
- Use `COALESCE`, `DATE 'YYYY-MM-DD'`, `SUBSTRING`, `CURRENT_DATE` per standard Presto syntax.
- Bind parameters as `:ParamName` or `IN :Param` — never string-concatenate values into the query text.
- The server echoes back the normalized SQL on every run. **Always read that echo** before trusting the result — it's the fastest way to catch a FROM-clause or parameter-binding mistake before it becomes a demo failure.

## 5. Mandatory Pre-Flight Checks

These two checks are **mandatory steps in the workflow, not optional tips**. Skipping either one is the most likely way this demo breaks in front of a prospect.

### 5.1 Row-count probe (before building any narrative around a table)

`wdata_list_table` returns `columnCount`, `status`, and timestamps — it **never returns a row count**. A table can show `status: EDITED` with a full column list while holding zero actual rows. Before building any demo narrative around a table:

1. Run a quick row-count probe: `SELECT COUNT(*) AS row_count FROM "workspaceId"."tableId" AS t LIMIT 1`.
2. Optionally pair it with a MIN/MAX probe on the primary date or amount column to sanity-check the data actually spans the expected range.
3. If `row_count` is 0 (or implausibly low), **do not proceed with that table**. Check for sibling/variant tables in the same workspace (a "Supp" or "v2" variant is a common pattern) and probe those instead.

This is not paranoia — it's a verified real failure mode: a "Supp" variant of a GL table had 0 rows while the base table had ~46,000, and the workspace's flagship saved query pointed at the empty variant, returning `rowsReturned: 0` silently with no error.

### 5.2 Choices-vs-actual-data probe (before trusting a saved query's parameter list)

`wdata_get_query` returns parameter metadata including `choices` — but `choices` describes what the query **accepts**, not what actually **exists** in the underlying data. Before presenting a saved query's parameter list as a complete picture of the prospect's data:

1. Run a `SELECT DISTINCT` probe on the dimension in question against the underlying table, not just against the saved query's declared `choices`.
2. Compare the two lists. Flag any entity in the real data that isn't in `choices` — especially consolidated/rollup entities or placeholder/junk entities, which are common and easy to miss.

Verified real case: a saved query's `choices` listed 5 entities; the underlying table actually contained 7, including an unlisted consolidated rollup entity and a junk placeholder entity. Silently ignoring this would double-count or omit real spend in the demo.

## 6. Step-by-Step Workflow (Anchor Use Case: OLAP + Variance + Forecast on Income Statement Data)

1. **Confirm target and scope.** Get workspace/table/saved-query, time range, and dimensions of interest from the user (Section 2). If a saved query is named, run `wdata_search_query` then `wdata_get_query` to retrieve `queryText` and parameter metadata.
2. **Row-count pre-flight (5.1).** Probe the target table(s) for actual row counts before doing anything else. If the primary candidate is empty, fall back to a sibling/base table and note the discrepancy for the narrative — this is itself a great "here's a real platform capability" moment: the demo caught a hidden data-quality issue.
3. **Choices-vs-actual-data pre-flight (5.2).** If a saved query with dimension parameters is in play, run the distinct-value probe and reconcile against `choices` before using either to frame the story.
4. **Sanity-check the saved query's logic** before presenting any of its numbers as trustworthy. Known real defect patterns worth actively checking for:
   - A `LEFT JOIN` silently turned `INNER` by a `WHERE` filter on the right-hand table — this hides unbudgeted spend and unspent budget in a variance report.
   - Unguarded division in a variance % calculation (divide-by-zero risk on zero-budget or zero-actual rows).
   - Redundant `GROUP BY` clauses that don't change results but signal the query wasn't cleanly authored.
   If found, either fix the query text before running it, or — if a prospect asks a probing question about a number — be ready to narrate: "here's a real production-grade complexity, not a toy example," and walk through the fix live. This is a credibility asset, not a liability, if handled transparently.
5. **Run the OLAP aggregation.** Query revenue/expense aggregated by account × time × channel × product via `wdata_run_query`, then `wdata_get_query_result` (poll until `COMPLETE`). Explicitly check for and correct double-counting from subtotal rows and org-level rollups mixed in with leaf-level detail — filter or exclude rollup rows as needed and narrate why.
6. **Compute Actual-vs-Budget variance.** Join actual and budget series (respecting the LEFT JOIN check from step 4) and compute variance and variance % per segment.
7. **Narrate value prop #1** at this point: this dimensional cut just happened against the platform's own governed dataset, with no export to an external BI tool — call this out explicitly as the ad hoc / moderate-complexity alternative.
8. **Download the result set** via `wdata_download_query_result` (CSV, byte-paginated) for anything headed into forecasting.
9. **Forecast revenue 6 months out.** Do this via code execution against the downloaded CSV — linear regression and Holt-Winters — not by trying to force windowed statistics into Presto SQL. Presto is not the right tool for this; code execution against the downloaded result is the deliberate correct choice, not a workaround. Say so explicitly if asked why the forecast didn't happen "in the query."
10. **Flag anomalous segments via z-scores** computed the same way (code execution against the downloaded result).
11. **Narrate value prop #2** distinctly from #1: predictive forecasting directly on platform data is forward-looking and has no existing demo precedent beyond this Wave 1 scenario — frame it as "worth validating live with you," not as a mature, polished capability.
12. **Run the quality checklist** (Section 8) before presenting any number to the prospect.
13. **Format output** per `../shared/output-standards.md` before presenting.

## 7. Output Guidance

Format all demo output per `../shared/output-standards.md`, using the Zesty Neue / Brand palette treatment for mixed/platform-analytics content (tables, variance summaries, and forecast charts alike). Keep the two value props visually and narratively separate — do not blend the "on-platform OLAP" result set and the "forward-looking forecast" result set into a single undifferentiated table; label which is which.

## 8. Quality Checklist

Before presenting any result to the prospect, confirm:

- [ ] Row-count pre-flight (5.1) was run against every table used, not assumed from `wdata_list_table` metadata alone.
- [ ] Choices-vs-actual-data pre-flight (5.2) was run for any saved query with dimension parameters in play.
- [ ] The server's normalized SQL echo was read and matches intent (correct `FROM` clause per Section 4, correct alias, explicit `LIMIT`).
- [ ] The saved query (if used) was checked for the known LEFT-JOIN-turned-INNER pattern, unguarded division, and redundant `GROUP BY`.
- [ ] Subtotal/rollup rows were excluded or explicitly reconciled before presenting aggregated revenue/expense figures.
- [ ] Value prop #1 (on-platform dimensional analysis) and value prop #2 (forecasting) are narrated as distinct claims — the forecasting claim is explicitly framed as forward-looking, not proven.
- [ ] No raw tool error, stack trace, or "0 rows" silent failure is shown to the prospect without being caught and resolved first.

## 9. Read-Only Note

This skill is **SELECT-only. No writes, ever.** Every Wdata query executed in this demo must be a read query with an explicit `LIMIT`. Never attempt or narrate a write, update, or delete against any Wdata source — the platform surface used here has no such capability in scope for this demo, and none should be implied to the prospect.

## 10. Final Safety-Net Rule

Never show a raw error or fabricated/placeholder data to the prospect — pause and recover per `../shared/session-safety.md` instead. If a query fails, returns an empty/implausible result, or any step in Section 5 or 6 turns up a discrepancy that can't be resolved live, stop the demo flow, do not paper over the gap with an invented number, and follow the recovery procedure in `../shared/session-safety.md`.

## 11. Worked Example — Fully Synthetic

> All workspace names, table names, GUIDs, and figures below are fabricated for illustration only.

**Setup:** Prospect ("Northwind Consolidated") asks to see dimensional variance analysis and a revenue forecast on their Income Statement data, currently staged in workspace `ws-nwc-fin-001`.

**Step 1 — Confirm target.** User requests: "run the analytics demo against Northwind's flagship IS variance query, trailing 12 months, cut by channel and product."

**Step 2 — `wdata_search_query`** returns saved query `qry-nwc-is-variance-v3`, described as "IS Actual vs Budget by Account/Channel/Product." `wdata_get_query` returns:

```
queryText: "SELECT a.account_name, a.channel, a.product, SUM(a.amount) AS actual, SUM(b.amount) AS budget
  FROM \"ws-nwc-fin-001\".\"tbl-is-actuals-supp-7f2a\" AS a
  LEFT JOIN \"ws-nwc-fin-001\".\"tbl-is-budget-9c1d\" AS b
    ON a.account_id = b.account_id AND a.period = b.period
  WHERE b.period = :Period
  GROUP BY 1,2,3,1,2,3
  LIMIT 5000"
parameters: { Period: { type: "string", mode: "required", choices: ["2025-Q1","2025-Q2","2025-Q3","2025-Q4","2026-Q1"] } }
```

**Step 3 — Row-count pre-flight (mandatory).**

```sql
SELECT COUNT(*) AS row_count FROM "ws-nwc-fin-001"."tbl-is-actuals-supp-7f2a" AS t LIMIT 1
```
→ `row_count: 0`

The flagship query points at `tbl-is-actuals-supp-7f2a` ("Supp" variant), which is empty. Probing the sibling:

```sql
SELECT COUNT(*) AS row_count FROM "ws-nwc-fin-001"."tbl-is-actuals-base-4e91" AS t LIMIT 1
```
→ `row_count: 46213`

**Caught before it became a live failure.** The demo narrative shifts to: "Your flagship saved query is actually pointed at an empty 'Supp' variant of your actuals table — the base table has ~46K rows. This is exactly the kind of silent gap this pre-flight check is designed to catch before it ever reaches a live report." The query is re-run against `tbl-is-actuals-base-4e91` for the rest of the demo.

**Step 4 — Logic sanity-check.** The `WHERE b.period = :Period` filter sits on the right-hand (budget) table of a `LEFT JOIN`, silently turning it into an effective `INNER JOIN` — any actual with no matching budget row for that period disappears entirely, hiding unbudgeted spend. Fix applied for the demo: move the period filter into the `ON` clause.

```sql
SELECT a.account_name, a.channel, a.product,
       COALESCE(SUM(a.amount), 0) AS actual,
       COALESCE(SUM(b.amount), 0) AS budget
FROM "ws-nwc-fin-001"."tbl-is-actuals-base-4e91" AS a
LEFT JOIN "ws-nwc-fin-001"."tbl-is-budget-9c1d" AS b
  ON a.account_id = b.account_id AND a.period = b.period AND b.period = :Period
WHERE a.period = :Period
GROUP BY 1, 2, 3
LIMIT 5000
```

**Step 5 — Choices-vs-actual-data pre-flight.**

```sql
SELECT DISTINCT channel FROM "ws-nwc-fin-001"."tbl-is-actuals-base-4e91" AS t LIMIT 100
```
→ returns `Retail`, `Wholesale`, `Direct`, `Consolidated-All-Channels`, `ZZ-Unassigned`

Only three channels appeared in the prospect's dashboards; `Consolidated-All-Channels` (a rollup) and `ZZ-Unassigned` (a junk placeholder) are excluded from the leaf-level aggregation with a one-line note to the prospect on why.

**Step 6 — Run OLAP + variance.** `wdata_run_query` → poll `wdata_get_query_result` until `COMPLETE`. Server echo confirms the corrected SQL and the three-channel filter ran as intended. Variance % computed as `(actual - budget) / NULLIF(budget, 0)` to guard the divide-by-zero case flagged in Section 4's dialect notes.

**Value prop #1 narrated:** "That variance cut — by account, channel, and product, reconciled against your governed actuals table — just happened without exporting anything to an external BI tool."

**Step 7 — Download and forecast.** `wdata_download_query_result` pulls the 12-month actuals series as CSV. Code execution (not SQL) runs a linear regression and Holt-Winters model to project revenue 6 months forward, and flags one segment (`Wholesale × Product-C`) as a z-score anomaly for the most recent quarter.

**Value prop #2 narrated:** "This forecast is a capability we're validating live with you today — it's not a polished, off-the-shelf report yet, but it's running directly against the same platform data you just saw the variance analysis pull from, with no separate export step."

**Output formatting:** presented per `../shared/output-standards.md`, with the OLAP/variance table and the forecast chart clearly labeled as separate sections.
