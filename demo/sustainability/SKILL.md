---
name: demo-sustainability
description: "Live-demo Workiva's MCP surface for sustainability/ESG reporting scenarios — cross-workspace CSRD/ISSB regulatory scoping, joining ESG program data with financial/subsidiary data, and producing a scoping matrix plus executive summary. Trigger phrases: '/sustainability', 'show me the ESG demo', 'show me the ESG/CSRD demo', 'demo sustainability reporting', 'demo CSRD/ISSB scoping', 'scope this prospect for CSRD/ISSB'."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Sustainability / ESG Demo (`/sustainability`)

This is a domain sub-skill of the top-level `/demo` anchor skill
(`../SKILL.md`). `/demo` performs session-safety gating (workspace
confirmation, environment checks) before routing here — this skill does
**not** repeat that full gate. It does restate one non-negotiable
safety-net rule at the end (see "Safety net," below), because this skill
must be safe to read and follow on its own if it's ever opened out of
sequence.

If you arrived here without `/demo` having already confirmed the target
demo environment and named workspaces, stop and go through `/demo` first.

## Purpose & trigger phrases

Purpose: give a Solution Consultant (SC) a live, tool-backed walkthrough of
Workiva's sustainability/ESG reporting surface — specifically cross-workspace
regulatory scoping for frameworks like CSRD or ISSB — using real Wdata MCP
queries against demo-environment data, ending in a scoping matrix and an
executive summary suitable for a prospect-facing readout or board-style
slide.

Trigger phrases (from the SC, verbatim or close paraphrase):
- `/sustainability`
- "show me the ESG demo"
- "show me the ESG/CSRD demo"
- "demo sustainability reporting"
- "demo CSRD/ISSB scoping"
- "scope this prospect for CSRD/ISSB"

## Required / optional inputs

**Required (must be explicitly provided by the SC — never inferred):**
- The two (or more) named workspace IDs to cross-reference, e.g. a
  sustainability-data workspace and a financial-reporting workspace. Per
  `../shared/session-safety.md`, this skill will not guess, default, or
  wander into a workspace the SC did not name.
- The target regulatory framework for scoping, e.g. `CSRD` or `ISSB`.

**Optional:**
- A specific country or region list to narrow the scoping matrix (if
  omitted, scope across all countries returned by the entity-structure
  query).
- A PCAF financed-emissions angle, if the demo is meant to touch financed
  emissions rather than pure entity-scoping (uses the same workflow ladder
  against `pcaf."workspaceId"."sourceProviderId"` instead of/in addition to
  `business_data`).

If either required input is missing, ask for it before running any query.
Do not proceed on an assumed workspace name.

## Tool-search batch loading note

Sustainability demos use the same Wdata tool family as every other Wdata
domain skill — there is no separate "ESG tool set." Before running any
query, batch-load the tool schemas once with:

```
tool_search("wdata query tables")
```

This loads `wdata_search_query`, `wdata_get_query`, `wdata_run_query`,
`wdata_get_query_result`, and `wdata_download_query_result` together. Do not
call `tool_search` again per query — only the FROM-clause source changes
between sustainability queries, not the tool family.

## FROM-clause grammar for this domain

| Source | FROM clause | Typical use in this demo |
|---|---|---|
| ESG program | `FROM program."workspaceId"."tableId"` (or `program_v2`) | ESG program metrics/targets |
| Program dimensions | `FROM program_dimension_v1."workspaceId"."tableId"` | Dimensional breakdowns of program data (e.g. by country, by facility) |
| PCAF datasets | `FROM pcaf."workspaceId"."sourceProviderId"` | Financed-emissions data, if in scope |
| Business data | `FROM business_data."workspaceId"."tableId"` | Subsidiary/entity structure, net sales by country |

Standard Presto rules apply throughout, same as every other Wdata domain:
SELECT-only, always an explicit `LIMIT`, bind parameters as `:ParamName`,
alias any GUID table reference, and confirm the server's echoed, normalized
SQL before treating a query as final.

## Why this domain is different: cross-workspace, not cross-query

The anchor use case for this skill (CSRD/ISSB scoping) inherently spans two
workspaces — sustainability-program data typically lives in one workspace,
financial/subsidiary data in another. Wdata does not offer a single query
that joins across workspaces. That means:

- Run one query against the financial/subsidiary workspace
  (`business_data."workspaceId"."tableId"`) for net sales by country and
  entity structure.
- Run a separate query against the sustainability-program workspace
  (`program."workspaceId"."tableId"` or `program_dimension_v1`) for
  ESG-relevant program data.
- Reconcile the two result sets manually (in the skill's own output —
  e.g. a joined table by country/entity), not via a single cross-workspace
  SQL statement.
- Every workspace touched must be named explicitly by the SC up front, per
  `../shared/session-safety.md`'s tenant-safety rules. Never infer a second
  workspace from a hint in the first query's results.

## Step-by-step workflow: cross-workspace CSRD/ISSB scoping (anchor use case)

This is currently the only tested Wave-1 sustainability use case. Treat it
as the default workflow when the SC says `/sustainability` without further
detail.

1. **Confirm inputs.** Restate the two named workspaces (financial-reporting
   workspace, sustainability-data workspace) and the target framework
   (CSRD or ISSB) back to the SC before running anything.
2. **Batch-load Wdata tools** with `tool_search("wdata query tables")` (once).
3. **Query the financial-reporting workspace** for net sales by country and
   subsidiary/entity structure via `business_data."workspaceId"."tableId"`.
   Use `wdata_search_query` → `wdata_get_query` → `wdata_run_query` →
   `wdata_get_query_result`, with an explicit `LIMIT` and bound params.
4. **Query the sustainability-data workspace** for relevant ESG program data
   via `program."workspaceId"."tableId"` (or `program_dimension_v1` for a
   country/entity-level breakdown), following the same tool ladder.
5. **Reconcile manually**: build a country-by-entity scoping matrix that
   marks each country/entity as in-scope, out-of-scope, or needs-review for
   the named framework, based on the aggregate revenue and entity-structure
   data pulled in steps 3–4.
6. **State the data-limitation caveat as a mandatory step, not a footnote**
   (see next section) — every scoping matrix this skill produces must carry
   it, every time.
7. **Draft the executive summary** (see "Output guidance") and, if
   requested, a board-ready slide outline summarizing the scoping matrix and
   the caveat.

### Mandatory caveat — must appear next to every scoping conclusion

Real CSRD/ISSB scoping determinants are entity-level revenue, headcount, and
listing status. This workflow's underlying data is typically only available
at the legal-entity and aggregate-regional-revenue level. This is a material
gap, not a nuance, and must be stated plainly next to any scoping
conclusion — never optional, never buried in a footnote, never omitted
because "the SC already knows."

Use this exact framing (adapt names/figures, not the substance):

> "Scoping shown here is based on legal entity and aggregate regional
> revenue; entity-level revenue, headcount, and listing status — the actual
> regulatory determinants — were not available in this dataset and would
> need separate validation."

Never present a scoping matrix produced by this workflow as a definitive
regulatory determination. It is a directional, demo-purposed illustration of
what Workiva's cross-workspace query surface can assemble — not a
compliance opinion.

## Output guidance

Follow `../shared/output-standards.md` for formatting, and use the **Link
Blue** palette for any sustainability-themed visual output (slide outlines,
tables rendered with color, etc.), per that shared standard. Output should
include:
- The scoping matrix (table: country/entity × in-scope/out-of-scope/needs-review).
- The mandatory caveat, stated adjacent to the matrix, not appended
  separately at the end.
- A short executive summary paragraph suitable for a prospect readout.
- Optionally, a board-ready slide outline if requested.

## Quality checklist

Before presenting output to the SC or prospect, confirm:

- [ ] Both (or all) workspaces were explicitly named by the SC — none
      inferred.
- [ ] Every query used an explicit `LIMIT` and bound params (`:ParamName`).
- [ ] Any GUID table reference was aliased.
- [ ] The server's echoed, normalized SQL was reviewed before treating a
      result as final.
- [ ] The financial/subsidiary query and the ESG-program query were run as
      separate queries per workspace, then reconciled manually — not
      presented as a single federated query.
- [ ] The entity-level-vs-aggregate-revenue caveat appears directly next to
      the scoping matrix, using the exact framing above (or a close,
      faithful paraphrase) — not as a trailing footnote.
- [ ] The output is explicitly framed as illustrative/demo scoping, not a
      regulatory determination.
- [ ] Output formatting and color palette follow `../shared/output-standards.md`.

## Read-only, explicitly

This skill is **read-only, always**. It only ever calls `wdata_search_query`,
`wdata_get_query`, `wdata_run_query`, `wdata_get_query_result`, and
`wdata_download_query_result` — all SELECT-only against Presto. It never
writes, updates, or deletes ESG program data, business data, or PCAF data,
and never modifies workspace configuration. If a workflow ever seems to
require a write, stop and hand it back to the SC rather than attempting it.

## Safety net (restated from `/demo` and `../shared/session-safety.md`)

Even though `/demo` handles session-safety gating before routing here: if
anything goes wrong mid-demo — a query errors, returns nothing, returns data
that looks wrong, or a workspace turns out not to be what was expected —
**never show a raw error or fabricated/placeholder data to the prospect.**
Pause, and recover per `../shared/session-safety.md` instead. This applies
even if it means pausing live in front of the prospect.

## Worked example (fully synthetic)

The following uses invented workspace names, invented country/revenue
figures, and no real Workiva or customer data. Do not reuse these
placeholders as if they were real workspace IDs.

**SC input:** "Run the CSRD scoping demo. Sustainability workspace is
`ws-esg-northlake-demo`, financial workspace is `ws-fin-northlake-demo`.
Framework: CSRD."

**Step 3 — query financial-reporting workspace (`ws-fin-northlake-demo`):**

```sql
SELECT entity_name, country, net_sales_local, currency
FROM business_data."ws-fin-northlake-demo"."subsidiary_net_sales"
WHERE fiscal_year = :FiscalYear
LIMIT 500
```

Synthetic result (excerpt):

| entity_name | country | net_sales_local | currency |
|---|---|---|---|
| Northlake Test Gmbh | Germany | 62,400,000 | EUR |
| Northlake Test SAS | France | 41,100,000 | EUR |
| Northlake Test Ltd | Ireland | 9,800,000 | EUR |

**Step 4 — query sustainability-data workspace (`ws-esg-northlake-demo`):**

```sql
SELECT country, esg_program_status, reporting_year
FROM program_dimension_v1."ws-esg-northlake-demo"."country_program_status"
WHERE reporting_year = :ReportingYear
LIMIT 500
```

Synthetic result (excerpt):

| country | esg_program_status | reporting_year |
|---|---|---|
| Germany | active_reporting | 2026 |
| France | active_reporting | 2026 |
| Ireland | not_yet_onboarded | 2026 |

**Step 5 — reconciled scoping matrix (built manually from the two result
sets above):**

| Country | Aggregate net sales (local) | ESG program status | CSRD scoping (illustrative) |
|---|---|---|---|
| Germany | €62.4M | active_reporting | Likely in-scope |
| France | €41.1M | active_reporting | Likely in-scope |
| Ireland | €9.8M | not_yet_onboarded | Needs review |

**Step 6 — mandatory caveat (stated directly beneath the matrix):**

> Scoping shown here is based on legal entity and aggregate regional
> revenue; entity-level revenue, headcount, and listing status — the actual
> CSRD regulatory determinants — were not available in this dataset and
> would need separate validation.

**Step 7 — executive summary:**

"Based on aggregate net sales and entity structure pulled from the
financial-reporting workspace, and ESG program onboarding status pulled from
the sustainability-data workspace, Germany and France appear likely in-scope
for CSRD reporting, while Ireland's ESG program onboarding status needs
follow-up before a scoping call can be made. This is a directional,
demo-purposed illustration, not a regulatory determination — entity-level
revenue, headcount, and listing status were not available in this dataset
and must be validated separately before any compliance decision is made."
