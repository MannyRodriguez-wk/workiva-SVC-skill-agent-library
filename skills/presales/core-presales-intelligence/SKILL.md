---
name: core-presales-intelligence
description: "Shared foundation and conventions for the Workiva presales skill family (Gong/Salesforce/RFP-analysis skills used by Solution and Value Consultants). This skill is not invoked directly by users — it documents the evidence classification taxonomy, fallback strings, read-only constraint, connector tool list, handoff payload format, and synthetic-data rule that every sibling presales skill must follow. Sibling skills reference this document and ../shared/evidence-schema.md rather than restating the rules in full."
metadata:
  disable-model-invocation: true
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Core Presales Intelligence — Shared Conventions

This skill defines the shared rules for the presales skill family: nine sibling
skills under `skills/presales/` that pull context from Gong, Salesforce, Google
Drive, and Workiva's internal GRC/Documents environment to help Solution
Consultants (SCs) and Value Consultants (VCs) prepare for calls, write briefs,
and respond to RFPs.

It is not meant to be triggered by a user directly (`disable-model-invocation:
true`). Every sibling skill's own `SKILL.md` must restate the non-negotiable
rules below (read-only constraint, evidence tagging, synthetic data) in its
own words, and link back here (`../core-presales-intelligence/SKILL.md`) and
to `../shared/evidence-schema.md` for the handoff payload shape.

## 1. Evidence classification taxonomy

Every factual claim in any presales-skill output must be tagged with exactly
one of the following classifications. Use the literal string values shown —
downstream adapters key off of them.

| Classification | Definition | Example |
|---|---|---|
| `confirmed_customer_statement` | Something the customer/prospect actually said or wrote, directly attributable to a call, email, or Gong transcript. | "Jordan Rivera (Acme Test Corp) said on the 2026-08-14 call: 'Our close process takes 11 business days.'" |
| `salesforce_operating_context` | Structured facts pulled from Salesforce records (opportunity stage, amount, close date, account owner, product line) — not a customer quote, but system-of-record data. | "Opportunity `Acme Test Corp – ESG Suite Renewal` is in stage `Negotiation/Review`, close date 2026-10-30 (source: `search_opportunities`)." |
| `verified_workiva_internal_fact` | A fact about Workiva's own products, pricing, roadmap, or internal GRC/demo environment, confirmed against an internal source (internal docs MCP, semantic model, product docs) — not inferred. | "Workiva's ESG Reporting solution supports CSRD taxonomy tagging as of the FY26 release (source: internal GRC/Documents MCP)." |
| `inference_working_hypothesis` | A reasonable conclusion the skill draws by connecting other evidence, but that has not been directly confirmed by the customer or a system of record. Must be labeled as a hypothesis, not fact. | "Given the account's stated 11-day close process and prior audit findings, Acme Test Corp likely has a manual, spreadsheet-based consolidation step (inference — not confirmed by customer)." |
| `open_question_validation_required` | A gap in available evidence that should be posed back to the SC/VC or asked of the customer before being treated as fact. | "Unclear whether Acme Test Corp's close process spans multiple ERPs — needs validation with the customer." |
| `risk_assumption_dependency` | An assumption the recommendation depends on, where being wrong would materially change the recommendation or demo approach. | "This proposed demo flow assumes Acme Test Corp uses Workday as its HRIS; if not, the integration story changes." |

Every `evidence[]` entry in the handoff payload (see §4 and
`../shared/evidence-schema.md`) must use one of these six values in its
`classification` field. Do not invent new classification values.

## 2. Fallback strings for unverifiable claims

When a claim cannot be classified into one of the six categories above because
the underlying source could not be checked, do not guess or silently omit it.
Use one of these two fixed strings as the claim text (or as the value of an
otherwise-required field):

- **`"Unknown — requires validation."`**
  Use when no data source (Gong, Salesforce, Drive, internal GRC/Documents)
  returned anything on the topic, and the skill has no basis for even a
  working hypothesis. This says "we don't know" plainly.

- **`"Requires Workiva-source validation."`**
  Use specifically when a claim is about Workiva's own product, pricing,
  security posture, roadmap, or internal capability, and the skill cannot
  confirm it against a verified Workiva-internal source. This flags "don't
  let a customer-facing rep repeat this until Workiva confirms it" — a
  narrower and higher-stakes case than generic unknowns.

Both strings must be used verbatim (exact casing and punctuation) so
downstream adapters and reviewers can pattern-match on them.

## 3. Read-only hard constraint (non-negotiable)

**Every presales skill is READ-ONLY.** None of the nine sibling skills — nor
this shared foundation — may ever write, update, create, or delete data in
Salesforce, Gong, Google Workspace, or any Workiva internal system, even when
the underlying connector technically supports write operations (e.g.
Salesforce via Workato is a read+write tier connector, but presales skills
only ever call its read/query tools).

Concretely:

- Only call query/search/read/get-style tools (see §4 for the approved list).
- Never call a tool that creates, updates, or deletes a Salesforce record, a
  Google Drive file, a Gong entity, or a Workiva internal document — with the
  narrow exception of `add_gtmasst_log`, which each sibling skill may use
  only to append its own audit/activity log entry, never to alter
  opportunity, account, or contact data.
- All output is a **draft or recommendation for a human to review and
  manually apply.** No skill in this family autonomously executes an action
  on behalf of the SC/VC.
- Every sibling skill's own `SKILL.md` must restate this constraint
  explicitly, in its own words, near the top of the file. Do not assume the
  reader has read this shared document.

## 4. Available connector tools

These are the actual MCP tools presales skills may reference or call in this
environment. Sibling skills should only call tools from this list, and only
in their read capacity per §3.

**Gong MCP (read-only)**
- `Ask Account`
- `Ask Deal`
- `Generate Brief`

**Salesforce (via Workato — connector is read+write tier; presales skills only ever READ)**
- `search_accounts`
- `search_opportunities`
- `search_contacts`
- `search_leads`
- `search_products`
- `search_tasks`
- `execute_soql_query`
- `get_current_user_id`
- `get_inside_sales_opp_audit_data`
- `retrieve_semantic_model`
- `view_report`
- `add_gtmasst_log` (write-of-own-audit-log only — see §3 exception)

**Google Drive (read-only usage only)**
- search files
- read file content
- download file content
- get file metadata

**Workiva internal GRC/Documents MCP (internal-only demo environment, read-only)**
- query/search/read tools exposed by that server for internal demo content,
  product documentation, and GRC reference material

## 5. Handoff payload convention

Every presales skill ends its output with a single machine-readable JSON
block, so two downstream adapter skills can consume it without re-parsing
prose:

- **`workiva-mcp-adapter`** — maps the payload into a Workiva internal
  GRC/Documents query format.
- **`demo-framework-adapter`** — maps the payload into a Workiva
  demo-environment setup payload.

The full schema lives in `../shared/evidence-schema.md`. The minimal common
shape is:

```json
{
  "skill": "gong-call-brief",
  "account_id": "acme-test-corp-001",
  "opportunity_id": "0061-acme-esg-renewal",
  "summary": "One paragraph, human-readable summary of the skill's output.",
  "evidence": [
    {
      "claim": "Acme Test Corp's close process takes 11 business days.",
      "classification": "confirmed_customer_statement",
      "source": "Gong call 2026-08-14, Jordan Rivera"
    }
  ],
  "open_questions": [
    "Does Acme Test Corp's close process span multiple ERPs?"
  ],
  "handoff_target": ["workiva-mcp-adapter", "demo-framework-adapter"]
}
```

Fields:

- `skill` — the sibling skill's kebab-case name (e.g. `gong-call-brief`,
  `rfp-gap-analysis`).
- `account_id` / `opportunity_id` — Salesforce IDs (or synthetic
  placeholders in examples), null if not applicable to that skill's output.
- `summary` — short human-readable synopsis.
- `evidence` — array of `{claim, classification, source}` objects. Every
  `classification` value must be one of the six taxonomy values from §1.
  Unverifiable claims use one of the §2 fallback strings as the `claim` text.
  `source` should be traceable (transcript date + speaker, Salesforce object
  + tool name, document title, etc.) — never blank.
- `open_questions` — array of plain-text strings, one per unresolved
  question requiring human/customer validation.
- `handoff_target` — array containing one or both of
  `"workiva-mcp-adapter"`, `"demo-framework-adapter"`, indicating which
  downstream adapter(s) should consume this payload.

See `../shared/evidence-schema.md` for the full JSON Schema definition,
field types, and validation rules.

## 6. Synthetic data rule

All examples in every presales skill's `SKILL.md` — including this one — must
use obviously fake, synthetic account and person names. Never use real
customer, prospect, or Workiva-internal-only names or data in example text.

Approved-style examples: `Acme Test Corp`, `Globex Test Industries`,
`Northwind Test Holdings`, `Jordan Rivera`, `Sam Okafor`, `Priya Chandran`.

Do not reuse real Salesforce account IDs, opportunity IDs, or Gong call IDs in
example text — use clearly synthetic placeholders (e.g.
`acme-test-corp-001`, `0061-acme-esg-renewal`).

## 7. Checklist for sibling skills

Each of the nine sibling `SKILL.md` files should:

1. Restate the read-only constraint (§3) explicitly, in its own words.
2. Tag every claim in its output with one of the six evidence classifications
   (§1), using the exact fallback strings (§2) where evidence is missing.
3. Only call connector tools from the approved list (§4), and only in
   read capacity.
4. End its output with the handoff JSON block conforming to
   `../shared/evidence-schema.md` (§5).
5. Use only synthetic account/person names in its own examples (§6).
6. Link back to `../core-presales-intelligence/SKILL.md` and
   `../shared/evidence-schema.md` rather than duplicating this document in
   full.
