# Session Safety Gate — Shared Pre-Flight Checklist

This is the full safety gate that `demo/SKILL.md` runs, in order, **every
single time** `/demo` is invoked, before any MCP tool touches live data. The
four domain sub-skills (`demo/grc/`, `demo/reporting/`, `demo/analytics/`,
`demo/sustainability/`) assume this gate has already run for the current
session and do not re-run it themselves. They link here instead of restating
it, and each restates only the final safety-net rule (never show placeholder
data, never show a raw error) as a closing reminder.

This document exists because Wave 1 testing of the Workiva MCP connector
produced real incidents, not hypothetical ones. The connector itself is
**entirely read-only** — every exposed tool is list/get/search/run in shape,
nothing writes — but read-only does not mean risk-free in a live,
prospect-facing setting. The risk is exposure and confusion, not data
corruption. Treat every rule below as load-bearing, not procedural theater.

## Why this gate exists — the incidents

1. **Cross-session memory leak (highest severity).** A tester ran a demo for
   a fake "Company A," opened a fresh chat, and asked about Company A —
   Claude returned the company name, audience context, and demo script from
   the prior session. Root cause: Settings → Capabilities → "Generate Memory
   from Chat History" was auto-enabled because the user also belonged to a
   corporate Claude org; disabling it disables memory across **all** of that
   user's Claude workspaces, not just the demo one. This is
   configuration-dependent — it does not fail every time. Testers who saw no
   leak got lucky, they were not operating safely.
2. **Wrong-tenant risk.** A tester connected to a workspace outside the
   intended demo organization (landed under "Workiva - Office of the CFO"
   instead of "Workiva - Sales") mid-session. They caught it before pulling
   any data and switched back — but the org list is not static and its
   ordering is not stable. A workspace can appear or shift position mid-session,
   so "I picked the right one last time" is not evidence it will be right
   this time.
3. **GRC entitlement inconsistency.** Multiple testers independently got
   "Access denied" on GRC calls (processes, risks, issues, analytics) in one
   workspace (e.g. "GRC-Risk Management") while the identical call succeeded
   in another (e.g. "GRC-All"). Entitlements are per-workspace, not per-user,
   and are not visible in advance — you cannot tell from the workspace name
   alone whether a given GRC call will succeed.
4. **No external network access.** The connector cannot fetch external
   files, templates, or regulator sites. A tester failed trying to get Claude
   to convert data into a NAIC standard import template because Claude had
   no way to reach the internet to find that template. Do not promise
   external-fetch capability live.
5. **Placeholder data shown as real.** One tester's session displayed a
   chart with placeholder numbers that did not reflect actual query results,
   then self-corrected mid-demo. This must never happen. A prospect who sees
   a number, however briefly, treats it as real regardless of a later
   correction.

## The gate — run in this order, every time

### Step 1 — Confirm memory is OFF

Before anything else: confirm Settings → Capabilities → "Generate Memory
from Chat History" is disabled for this session. If you are not certain of
its current state, **ask the SC to confirm it directly** before proceeding —
do not assume it is off because it was off last time, and do not proceed on
"probably fine." Remember this setting is workspace-wide for the user, not
demo-scoped: a corporate-org membership can silently re-enable it.

If memory cannot be confirmed OFF, stop and resolve this before any MCP tool
is called. A live cross-session leak in front of a prospect is the single
worst outcome this gate exists to prevent.

### Step 2 — Confirm organization, workspace, and purpose match — explicitly, out loud

Run or instruct `list_workspaces` (loaded via the batch tool-search pattern
in `demo/SKILL.md` Part 2). Before the first data read of the session,
confirm **three things explicitly with the SC** — not silently, not
inferred:

- **Organization** — is this a demo/sales tenant, and specifically *not* any
  tenant that could contain real corporate data?
- **Workspace** — the SC must name the workspace explicitly. Never infer or
  guess which workspace is "probably" the right one from naming similarity
  or from what was used last time. The list order is not stable and a
  workspace can appear mid-session that wasn't visible before.
- **Purpose match** — does this tenant's type/configuration actually match
  what is about to be demoed (e.g. a GRC-focused ask should land in a
  workspace actually provisioned for GRC, not just any sales tenant)?

If any of the three is ambiguous, **ask the SC**. Never proceed on an
inferred answer to any of these three questions.

### Step 3 — Proactively probe GRC entitlement before promising a GRC flow

If GRC is the target domain for this session (routed to `demo/grc/SKILL.md`),
run one lightweight test call against the confirmed workspace *before*
telling the prospect what you're about to show them. Entitlements are
per-workspace and invisible in advance — do not discover "Access denied" live
on stage after already narrating what the prospect is about to see. If the
probe fails, tell the SC privately and adjust the plan (different workspace,
different domain, or a caveat to the prospect) before continuing.

### Step 4 — Live correction protocol

State this plainly to whoever is operating the session: if at any point data
appears that looks like it belongs to a prior session, a different customer,
or an unexpected workspace, **stop the demo narrative immediately**, say so
to the SC (not silently to the prospect — the SC needs to know in real
time), and clear the session before continuing. Do not try to quietly
paper over a suspected leak and keep going.

### Step 5 — Never expose raw errors or fabricated data

- Never display a raw error message, stack trace, or internal identifier
  (vertex ID, GUID, internal tool name) to the prospect. Translate failures
  into plain, calm language for the SC to relay, or handle silently if it's
  a retryable/expected condition.
- Never render a chart, table, or number that was not actually returned by a
  tool call. No illustrative data, no "this is roughly what it would look
  like," no placeholder filled in while waiting on a real result. If a query
  returns nothing, say that plainly — do not fill the gap with anything that
  looks like real output.

## One-line summary for domain skills to restate

Every domain sub-skill (`demo/grc/`, `demo/reporting/`, `demo/analytics/`,
`demo/sustainability/`) must restate, at minimum: *"This gate
(`../shared/session-safety.md`) has already run for this session. As a final
safety net: never show placeholder/illustrative data, never show a raw error
or internal identifier to the prospect, and stop immediately if
prior-session or wrong-tenant data appears."*
