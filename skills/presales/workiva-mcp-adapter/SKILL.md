---
name: workiva-mcp-adapter
description: "Adapter skill that receives the standard presales handoff JSON payload (per ../shared/evidence-schema.md) from a sibling skill (account-opportunity-brief, rfp-security-analysis, salesforce-draft-updates, presales-handoff, or any other presales skill whose handoff_target includes 'workiva-mcp-adapter') and enriches it by querying the internal Workiva GRC/Documents MCP — a special-access, internal-only, read-only demo environment covering controls, policies, audits, and SOX-related documentation. It resolves open_question_validation_required and inference_working_hypothesis entries into verified_workiva_internal_fact evidence with citations where a matching internal document exists, and returns the same payload shape with evidence updated/added. Not typically invoked directly by a user; invoked programmatically or explicitly when a sibling skill or operator says 'run this through the Workiva MCP adapter,' 'enrich this handoff against internal docs,' or 'check this against the internal GRC/Documents MCP.'"
metadata:
  disable-model-invocation: true
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Workiva MCP Adapter — Internal GRC/Documents Enrichment

This is an **adapter skill**, not a user-facing analysis skill
(`disable-model-invocation: true`). It is part of the presales skill family
and shares conventions with
[`../core-presales-intelligence/SKILL.md`](../core-presales-intelligence/SKILL.md)
and the shared evidence taxonomy in
[`../shared/evidence-schema.md`](../shared/evidence-schema.md).

## Purpose & Trigger Phrases

This skill's sole job is to take a handoff JSON payload produced by another
presales skill and enrich it by checking any unresolved or hypothesized
claims against Workiva's internal GRC/Documents MCP — an internal-only,
read-only demo environment covering controls, policies, audits, and
SOX-related documentation.

It is **primarily invoked by other skills**, not directly by a user typing a
request. The invocation pattern is: a sibling presales skill (e.g.
`account-opportunity-brief`, `rfp-security-analysis`,
`salesforce-draft-updates`, `presales-handoff`) finishes its own analysis,
emits its standard handoff JSON with `"handoff_target"` including
`"workiva-mcp-adapter"`, and that JSON payload is handed to this skill for
enrichment before the final output is returned to the Solution/Value
Consultant.

Because `disable-model-invocation: true` is set, this skill is not
auto-triggered by conversational phrasing alone. Explicit invocation phrases
that should route here include:

- "Run this handoff through the Workiva MCP adapter."
- "Enrich this payload against internal GRC/Documents."
- "Check these open questions against Workiva internal docs."
- "See if the internal MCP resolves any of these open items."
- A sibling skill's own instructions saying "hand off to `workiva-mcp-adapter`."

## Required Inputs

The **handoff JSON payload itself**, conforming to
[`../shared/evidence-schema.md`](../shared/evidence-schema.md). At minimum
the payload must contain:

- `account_id` (string or synthetic placeholder; may be `null` if not
  applicable to the originating skill)
- `opportunity_id` (optional; string, synthetic placeholder, or `null`)
- `evidence` — array of `{claim, classification, source}` objects
- `open_questions` — array of plain-text strings

If the incoming payload is missing `evidence` or `open_questions` entirely
(not just empty), stop and report that the payload does not conform to the
shared schema — do not attempt to guess its shape or invent evidence to fill
gaps.

## Source Retrieval — Workiva Internal GRC/Documents MCP Only

This adapter queries **exactly one system**: the **Workiva internal
GRC/Documents MCP**. It does not call Salesforce, Gong, Google Drive, or any
other connector — those are the responsibility of the sibling skill that
produced the handoff payload.

Important characteristics of this system, restated here because they govern
every decision this adapter makes:

- It is a **special-access, internal-only, read-only demo environment** —
  it is **not** part of general enterprise Claude access, and it may not be
  reachable in every environment this skill runs in.
- It exposes query/search/read tools over internal demo content, product
  documentation, controls, policies, audits, and SOX-related material — never
  write/update/create/delete tools. This adapter never calls a write-capable
  tool even if one happens to be exposed.
- **If the internal MCP cannot be reached, this adapter must say so plainly**
  — output the literal note **"Workiva internal MCP not available in this
  environment."** for every affected item — and must **never fabricate** a
  result, citation, or document title to fill the gap. A missing connection
  is reported, not papered over.
- This adapter never asserts that the internal MCP was queried unless a
  query call actually executed and returned (empty or otherwise).

## Step-by-Step Workflow

1. **Validate the incoming payload.** Confirm `evidence` and
   `open_questions` are present and well-formed per
   [`../shared/evidence-schema.md`](../shared/evidence-schema.md). If not,
   stop and report the malformed payload rather than guessing.
2. **Check internal MCP availability.** Attempt a lightweight query against
   the Workiva internal GRC/Documents MCP. If it is unreachable, skip
   straight to step 6 and mark every candidate item with "Workiva internal
   MCP not available in this environment." — do not attempt partial
   enrichment against any other source.
3. **Identify enrichment candidates.** Walk the `evidence[]` array and the
   `open_questions[]` array. Select every entry classified
   `open_question_validation_required` or `inference_working_hypothesis`,
   plus every plain-text item in `open_questions[]`, as a candidate for
   internal-doc lookup.
4. **Map each candidate to a specific internal-doc query.** For each
   candidate, derive a targeted query against the internal GRC/Documents
   MCP — e.g. a claim about "SOC 2 Type II scope" maps to a query for the
   current SOC 2 Type II report/scope document; a claim about "CSRD taxonomy
   tagging support" maps to a query for the relevant product/release
   documentation or control description. Do not run a single generic query
   for the whole payload — each candidate gets its own targeted lookup so
   the resulting citation is traceable to the specific claim it resolves.
5. **Evaluate each query result:**
   - If a **specific, matching internal document** is found: reclassify
     that entry as `verified_workiva_internal_fact`, rewrite the `claim`
     text to state the now-confirmed fact, and set `source` to the specific
     document/control/policy title and location returned by the MCP (never a
     vague "internal docs" citation).
   - If the query runs successfully but **returns no matching document**:
     leave the entry's classification as-is (or set to
     `open_question_validation_required` if it was an `open_questions[]`
     plain-text item being promoted into `evidence[]`), and set `claim` to
     `"Requires Workiva-source validation."`, with `source` stating exactly
     what was queried and that no match was found (e.g. "Workiva internal
     GRC/Documents MCP queried for 'SOC 2 Type II scope — Acme Test Corp
     modules', 2026-09-16, no matching document.").
   - If the MCP is **unreachable**: set `claim` to "Workiva internal MCP not
     available in this environment." and `source` to a note that the
     connection attempt failed, with the timestamp.
6. **Reassemble open_questions.** Remove from `open_questions[]` any item
   that was fully resolved into a `verified_workiva_internal_fact` evidence
   entry in step 5. Leave unresolved items in `open_questions[]` unchanged.
7. **Never touch unrelated evidence.** Entries already classified
   `confirmed_customer_statement`, `salesforce_operating_context`, or
   `risk_assumption_dependency` are passed through untouched — this adapter
   only ever acts on `open_question_validation_required` and
   `inference_working_hypothesis` entries (and raw `open_questions[]`
   strings). It never re-evaluates or downgrades anything else.
8. **Return the enriched payload**, preserving every field the shared schema
   requires, plus this adapter's own annotations (see Output Schema below).

## Source Classification & Citation Rules

This adapter reiterates the shared six-value taxonomy from
[`../core-presales-intelligence/SKILL.md`](../core-presales-intelligence/SKILL.md)
§1: `confirmed_customer_statement`, `salesforce_operating_context`,
`verified_workiva_internal_fact`, `inference_working_hypothesis`,
`open_question_validation_required`, `risk_assumption_dependency`.

This adapter's entire job is **upgrading** classifications — moving an
`open_question_validation_required` or `inference_working_hypothesis` entry
to `verified_workiva_internal_fact` once a specific internal document
confirms it, with a precise citation.

- **Never downgrade** an existing classification silently. If this adapter
  cannot confirm something, it leaves the original classification alone (or
  uses the fallback string as the claim text) — it does not invent a lower
  or higher confidence level without cause.
- **Never invent a citation.** Every `verified_workiva_internal_fact` this
  adapter produces must cite a specific document/control/policy title and
  location actually returned by the internal MCP query. If the MCP returns
  something vague or partial, cite exactly what was returned — do not
  embellish it into a more specific-sounding citation.
- **Never assert the internal MCP was queried if it wasn't reachable.** The
  `source` field must accurately reflect whether a query executed.

## Output Schema

The adapter returns the **same handoff JSON shape it received** — per
[`../shared/evidence-schema.md`](../shared/evidence-schema.md) — with:

- `evidence[]` entries updated in place where enrichment occurred (upgraded
  classification, rewritten `claim`, specific `source`), and unchanged
  otherwise.
- Any `open_questions[]` item that was fully resolved moved into `evidence[]`
  as a new `verified_workiva_internal_fact` entry (with citation) and removed
  from `open_questions[]`.
- `open_questions[]` otherwise left intact for anything unresolved.
- All original fields (`skill`, `account_id`, `opportunity_id`, `summary`,
  `handoff_target`) preserved as received, with `summary` optionally amended
  to reflect what this adapter added (e.g. "... internal GRC/Documents MCP
  confirmed 1 of 2 open items; 1 remains unresolved.").
- An additional `adapter_run` object appended, since `additionalProperties:
  true` is permitted at the top level, recording what this adapter actually
  did:

```json
{
  "adapter_run": {
    "adapter": "workiva-mcp-adapter",
    "internal_mcp_reachable": true,
    "candidates_checked": 2,
    "candidates_resolved": 1,
    "run_timestamp": "2026-09-16"
  }
}
```

## Quality Checklist

- [ ] Never invents a control/policy/document citation — every
      `verified_workiva_internal_fact` this adapter adds cites a specific,
      actually-returned internal document.
- [ ] Never asserts the internal MCP was queried if it wasn't reachable; uses
      "Workiva internal MCP not available in this environment." verbatim
      when the connection fails.
- [ ] Never silently downgrades an existing evidence classification from the
      incoming payload.
- [ ] Only acts on `open_question_validation_required` and
      `inference_working_hypothesis` entries (and raw `open_questions[]`
      strings) — passes all other evidence through untouched.
- [ ] Uses the exact fallback strings verbatim where the internal MCP has no
      matching document.
- [ ] Every returned payload still conforms to
      [`../shared/evidence-schema.md`](../shared/evidence-schema.md) —
      required fields intact, one classification value per entry, `source`
      never blank.

## READ-ONLY — NO WRITE ACCESS, EVER

**This adapter is strictly read-only.** It only ever calls query/search/read
tools exposed by the Workiva internal GRC/Documents MCP. It never calls a
write, update, create, or delete tool against that MCP or any other system,
even if such a tool happens to be exposed in the environment. It produces an
enriched JSON payload for downstream consumption — it never modifies
Salesforce, Gong, Google Drive, or any Workiva internal record, and it never
claims to have done so.

## Fallback Strings

- **`"Unknown — requires validation."`** — used verbatim when a claim cannot
  be resolved and has no basis for even a working hypothesis (rare for this
  adapter, since incoming candidates already carry some prior context, but
  used if the internal MCP query itself errors ambiguously rather than
  cleanly returning "no match").
- **`"Requires Workiva-source validation."`** — used verbatim as the `claim`
  text whenever the internal GRC/Documents MCP is reachable, a targeted
  query executes, and no matching internal document is found for a claim
  about Workiva's own product, controls, policy, or security posture.

Both strings are used exactly as written — no paraphrasing — so downstream
consumers (including a human reviewer) can pattern-match on them reliably.

## Handoff Payload

Because this skill **is** the adapter, it does not hand off to a further
adapter. Its output is the **enriched version of the input payload**
described in Output Schema above, returned directly to whichever process or
skill invoked it (the calling sibling skill, an orchestrator, or the
operator who explicitly invoked this adapter). No further `handoff_target`
processing occurs downstream of this skill within the presales family.

## Fully Synthetic Worked Example

**Incoming payload** (from `rfp-security-analysis`, synthetic):

```json
{
  "skill": "rfp-security-analysis",
  "account_id": "acme-test-corp-001",
  "opportunity_id": "0061-acme-esg-renewal",
  "summary": "Acme Test Corp's RFP raises two open items: SOC 2 Type II module scope, and whether audit logs are retained for 7 years.",
  "evidence": [
    {
      "claim": "Acme Test Corp's RFP question 22 asks whether the current SOC 2 Type II report covers the ESG Reporting and Audit Management modules specifically.",
      "classification": "open_question_validation_required",
      "source": "RFP document 'Acme_Test_Corp_RFP_2026.pdf', question 22 (Google Drive)"
    },
    {
      "claim": "Acme Test Corp's RFP question 23 asks whether audit logs are retained for a minimum of 7 years.",
      "classification": "open_question_validation_required",
      "source": "RFP document 'Acme_Test_Corp_RFP_2026.pdf', question 23 (Google Drive)"
    }
  ],
  "open_questions": [
    "Does the current SOC 2 Type II report cover the ESG Reporting and Audit Management modules Acme Test Corp asked about in question 22?",
    "Does Workiva retain audit logs for a minimum of 7 years, as asked in question 23?"
  ],
  "handoff_target": ["workiva-mcp-adapter"]
}
```

**Adapter workflow (synthetic):**

1. Payload validated — `evidence` and `open_questions` both present and
   well-formed.
2. Internal MCP availability check succeeds — Workiva internal GRC/Documents
   MCP is reachable in this run.
3. Two candidates identified: the SOC 2 Type II scope question and the
   audit-log-retention question.
4. Targeted query 1: "SOC 2 Type II report scope — ESG Reporting, Audit
   Management modules" → internal MCP returns a matching document:
   "SOC 2 Type II Report FY26, Section 3.2 — Scope of Covered Services,"
   confirming both modules are in scope.
5. Targeted query 2: "audit log retention period policy" → internal MCP
   query executes successfully but returns no matching document (retention
   period is not documented in the internal demo environment's current
   corpus).

**Enriched output payload (synthetic):**

```json
{
  "skill": "rfp-security-analysis",
  "account_id": "acme-test-corp-001",
  "opportunity_id": "0061-acme-esg-renewal",
  "summary": "Acme Test Corp's RFP raised two open items. Internal GRC/Documents MCP confirmed SOC 2 Type II scope covers both modules asked about; audit-log retention period remains unresolved and requires Workiva-source validation.",
  "evidence": [
    {
      "claim": "Workiva's current SOC 2 Type II report (FY26) covers both the ESG Reporting and Audit Management modules Acme Test Corp asked about in RFP question 22.",
      "classification": "verified_workiva_internal_fact",
      "source": "Workiva internal GRC/Documents MCP — 'SOC 2 Type II Report FY26,' Section 3.2 (Scope of Covered Services), queried 2026-09-16"
    },
    {
      "claim": "Requires Workiva-source validation.",
      "classification": "open_question_validation_required",
      "source": "Workiva internal GRC/Documents MCP queried for 'audit log retention period policy,' 2026-09-16 — no matching document found in current corpus."
    }
  ],
  "open_questions": [
    "Does Workiva retain audit logs for a minimum of 7 years, as asked in question 23?"
  ],
  "handoff_target": ["workiva-mcp-adapter"],
  "adapter_run": {
    "adapter": "workiva-mcp-adapter",
    "internal_mcp_reachable": true,
    "candidates_checked": 2,
    "candidates_resolved": 1,
    "run_timestamp": "2026-09-16"
  }
}
```

Note: question 22's entry was resolved and moved out of `open_questions[]`
into `evidence[]` as a `verified_workiva_internal_fact` with a precise
citation; question 23 remains in `open_questions[]` unchanged, with its
corresponding `evidence[]` entry using the fallback string
`"Requires Workiva-source validation."` rather than a fabricated answer.
