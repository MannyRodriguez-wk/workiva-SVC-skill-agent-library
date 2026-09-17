---
name: demo
description: "Anchor/router skill for live-demoing the Workiva internal MCP (Model Context Protocol) connector to a prospect on a real call. Enforces a hard pre-flight safety gate (memory state, tenant/workspace confirmation, GRC entitlement probing, live wrong-data correction protocol) before any MCP tool touches live data, then routes the SC to the correct domain sub-skill (/grc, /reporting, /analytics, /sustainability) based on what the prospect wants to see. Trigger phrases: '/demo', 'let's demo the MCP', 'I have a live Workiva MCP demo', 'demo the connector for [prospect]', 'walk the prospect through GRC/reporting/analytics/sustainability live', 'start the live MCP session'. Distinct from presales/demo-framework-adapter, which plans the demo narrative/script offline before the call — this skill is about safely executing a live, MCP-powered demo during the call itself."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# /demo — Live Workiva MCP Demo Anchor & Router

This is the anchor skill for the `demo/` family. It is invoked as `/demo` at
the start of any live, prospect-facing session that will use the Workiva
internal MCP connector. Its job has exactly two parts, run in strict order:

1. **Run the hard safety gate** (Part 1) before any MCP tool is called.
2. **Route** (Part 3) to the correct domain sub-skill once the gate passes.

This skill does not itself pull GRC controls, financial reporting data,
Wdata analytics, or sustainability data — it hands off to
`demo/grc/SKILL.md`, `demo/reporting/SKILL.md`, `demo/analytics/SKILL.md`,
or `demo/sustainability/SKILL.md` for that. Do not skip straight to a domain
skill without running this gate first, even if the SC seems to be in a
hurry to get on with the demo — the gate is what this skill exists to
enforce.

**Read-only disclaimer, stated up front:** the Workiva MCP connector
exposed to this skill family is **entirely read-only**. Every tool it
provides is a list/get/search/run in shape — there is no create, update, or
delete capability anywhere in this connector. Nothing this skill or any of
its sub-skills does can modify a Workiva tenant, a Salesforce record, or any
other live system. The risk this gate guards against is exposure and
confusion in front of a prospect, not data corruption.

## Part 1 — Hard Safety Gate (run every time, before any MCP tool call)

**This is the most important part of this skill. Do not soften, shorten, or
skip any step of it, even under time pressure.**

The full gate — why it exists, the real Wave 1 incidents behind each rule,
and the exact steps to run — lives in
[shared/session-safety.md](shared/session-safety.md). Read it before running
your first live session if you have not already. Restated here in brief,
run **in this order**, every single time `/demo` is invoked:

1. **Confirm memory is OFF.** Settings → Capabilities → "Generate Memory
   from Chat History" must be disabled. If you are not certain of its
   current state, ask the SC to confirm before proceeding — never assume.
   This setting is not demo-scoped: for a user who also belongs to a
   corporate Claude org, disabling it disables memory across *all* of that
   user's Claude workspaces, and leaving it on risks a cross-session leak of
   a prior prospect's name, context, or script into this session.
2. **Run/instruct `list_workspaces` and confirm three things explicitly with
   the SC before the first data read:**
   - **Organization** — a demo/sales tenant, never a tenant that could hold
     real corporate data.
   - **Workspace** — named explicitly by the SC. Never inferred or guessed.
     The workspace list is not static and its ordering is not stable; a
     workspace can appear mid-session that wasn't visible before.
   - **Purpose match** — does this tenant actually match what's about to be
     demoed?
   Any ambiguity on any of the three → **ask, never infer.**
3. **If GRC is the target domain, proactively probe entitlement** with a
   lightweight test call before promising a GRC flow to the prospect live.
   Entitlements are per-workspace and invisible in advance — do not discover
   "Access denied" on stage after already narrating what you're about to
   show.
4. **State plainly, before continuing:** if data from a prior session, a
   different customer, or an unexpected workspace appears at any point,
   **stop the demo narrative immediately**, say so to the SC (not silently
   to the prospect), and clear the session before continuing.
5. **Never display a raw error, stack trace, or internal identifier to the
   prospect.** Never render a chart or number that was not actually
   returned by a tool call — no illustrative or placeholder data, ever,
   under any circumstance.

Do not proceed to Part 3 (routing) until steps 1 and 2 have been explicitly
confirmed with the SC for this session. Step 3 gates GRC routing
specifically; steps 4 and 5 are standing rules for the entire session, not
one-time checks.

## Part 2 — Tool-Loading Pattern

All ~55 underlying MCP tools this connector exposes are deferred behind
`tool_search` and must be loaded **in batches by domain**, never one tool at
a time. This skill and every domain sub-skill should reuse these exact
search terms so tool discovery stays consistent across the family:

| Domain | Batch search terms |
|---|---|
| WData / Analytics | `"wdata query tables"`, `"query result download"` |
| Documents / Reporting | `"documents list sections"`, `"document links footnotes"` |
| Reporting (spreadsheets) | `"spreadsheets sheets cell range"` |
| GRC | `"grc controls issues policies"`, `"grc graph test forms"` |

Use these as the literal `tool_search` query text (or close paraphrases of
them) when a domain skill needs to load its tool batch. Do not search for
individual tool names one at a time — load the relevant domain's batch
together so the full set of related tools is available before starting that
part of the demo.

Also load `list_workspaces` (and any workspace/session-related tool) as part
of Part 1's gate, independent of which domain batch gets loaded next.

## Part 3 — Routing Table

Once the gate in Part 1 has passed, route based on what the SC says the
prospect wants to see:

| SC says / prospect wants to see | Route to |
|---|---|
| Controls, risks, audit planning, SOX, compliance heatmaps, policy search | [`demo/grc/SKILL.md`](grc/SKILL.md) (invoke as `/grc`) |
| Financial reporting, filings, SEC accounting standard checks (ASC/10-Q), document/link/feature audits, Auto-SOI style output | [`demo/reporting/SKILL.md`](reporting/SKILL.md) (invoke as `/reporting`) |
| Data analytics, OLAP, variance, forecasting, dimensional analysis on Wdata | [`demo/analytics/SKILL.md`](analytics/SKILL.md) (invoke as `/analytics`) |
| ESG/CSRD/ISSB scoping, sustainability program data, PCAF | [`demo/sustainability/SKILL.md`](sustainability/SKILL.md) (invoke as `/sustainability`) |

If the SC wants to show more than one domain in the same session (a common
live-demo pattern — e.g. GRC then reporting), the gate in Part 1 runs once
per session, not once per domain switch — but re-confirm workspace/purpose
match if the domain switch changes what tenant/workspace should be in use,
and re-run the GRC entitlement probe (Part 1, step 3) specifically if GRC
becomes the target partway through a session that didn't originally include
it.

**All four domain skills assume this gate has already run.** They do not
re-run Part 1 in full — re-running the entire gate inside every domain skill
would be redundant and would slow down live domain-switching mid-call. Each
domain skill does, however, restate the final safety-net rule as its own
closing reminder: never show placeholder/illustrative data, never show a
raw error or internal identifier to the prospect, and stop immediately if
prior-session or wrong-tenant data appears.

## Part 4 — Output Standards

Anything rendered on-screen during the live session — tables, charts,
summaries, generated documents — must follow the shared output/brand
contract in [shared/output-standards.md](shared/output-standards.md):
one palette per artifact chosen by domain (Purple Mountain for Financial
Reporting, Presentation Yellow for Audit & Risk/GRC, Link Blue for
Sustainability, Zesty Neue/Brand green for mixed/platform content), no red
anywhere in the system (favorable/unfavorable shown via green vs. orange
*plus* a `▲`/`▼` or `(F)`/`(U)` marker, never color alone), exact-precision
numbers with stated currency and right-aligned columns, no raw GUIDs/vertex
IDs on screen, a BLUF-then-scope-then-data-then-caveats-then-next-steps
structure, no empty chart frames or illustrative data ever, and an explicit
manual-import disclaimer on any generated artifact (Word/Excel/HTML) since
none of it writes back into Workiva automatically.

## Quality Checklist

Before the SC starts pulling any live data, confirm:

- [ ] Memory (Generate Memory from Chat History) has been explicitly
      confirmed OFF for this session.
- [ ] Organization, workspace, and purpose match have all been explicitly
      confirmed with the SC — none inferred or assumed from a prior
      session.
- [ ] If GRC is in scope, entitlement has been probed before promising the
      flow to the prospect.
- [ ] The SC has been told, out loud, what to do if prior-session or
      wrong-tenant data appears mid-demo.
- [ ] The correct domain sub-skill has been identified from Part 3's
      routing table — not guessed or defaulted.
- [ ] The relevant tool batch (Part 2) has been loaded via `tool_search`
      before any individual tool call, using the documented search terms.
- [ ] Every on-screen output follows
      [shared/output-standards.md](shared/output-standards.md) — correct
      palette, no color-only favorable/unfavorable signaling, exact
      numbers, no raw identifiers, BLUF-first structure, no
      illustrative/placeholder data, manual-import disclaimer on generated
      artifacts.

## Read-Only / No-Write Disclaimer

The Workiva MCP connector this skill family operates against is entirely
read-only — list, get, search, and run tools only. Neither this anchor
skill nor any of its four domain sub-skills can create, update, or delete
data in any connected system, in a Salesforce record, or in a Workiva
tenant of any kind. Every output produced during a `/demo` session is
something displayed live to a prospect or, at most, a generated
stand-alone artifact (see Part 4(e)) that still requires a separate manual
step to bring into Workiva — never an automatic write.

## Relationship to `presales/demo-framework-adapter`

This `/demo` family is entirely separate in purpose from
[`presales/demo-framework-adapter/SKILL.md`](../presales/demo-framework-adapter/SKILL.md).
That skill plans the demo **narrative/script offline**, before the call —
mapping discovery evidence to demo moments and product modules, with no live
connector access at all. This skill (`/demo` and its four domain
sub-skills) is about safely **executing** a live, MCP-powered demo *during*
the call, against real (but demo-tenant) connector access. If an SC asks
this skill to help plan what to say or which pain points to cover before the
call, redirect them to `presales/demo-framework-adapter`; if they ask this
skill to help write a discovery brief or eval plan, redirect them to the
relevant `presales/` skill. This skill only starts once the SC is live on
the call and ready to touch the connector.
