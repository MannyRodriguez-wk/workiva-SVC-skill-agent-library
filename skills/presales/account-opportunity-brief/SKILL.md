---
name: account-opportunity-brief
description: "Produces a one-page Account & Opportunity Brief for Workiva Solution/Value Consultants prepping for a presales engagement — pulls Salesforce account, opportunity, contact, and reporting context into a single read-before-your-call document covering account overview, opportunity stage/size/timeline, buying committee, product fit, and known risks. Use when the user says things like 'brief me on [account]', 'give me the account/opp overview before my call', 'prep me for [opportunity]', 'what do I need to know about [account] before I talk to them', or 'kick off presales on [opportunity]'. This is the entry-point skill for a presales engagement; other presales skills (gong-discovery-analysis, technical-discovery-planner, etc.) assume this brief has already been produced."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Account & Opportunity Brief

The entry-point skill for a presales engagement kickoff. Given an account or
opportunity name, this skill assembles a single one-page brief a Solution/Value
Consultant (SVC) reads before their first call: account overview, opportunity
stage/size/timeline, key stakeholders/buying committee, product fit context, and
known risks. Every other presales skill in this library (e.g.
`gong-discovery-analysis`, `technical-discovery-planner`) assumes this brief
already exists and builds on top of it.

This skill shares conventions with every other skill in `skills/presales/`.
See:

- [../core-presales-intelligence/SKILL.md](../core-presales-intelligence/SKILL.md)
  for the shared presales operating model, tone, and cross-skill handoff
  conventions.
- [../shared/evidence-schema.md](../shared/evidence-schema.md) for the full
  evidence classification taxonomy and the canonical handoff JSON schema
  referenced in this document.

## 1. Purpose & Trigger Phrases

**Purpose:** Give an SVC everything they need to walk into a first call
informed, without spending 30+ minutes cross-referencing Salesforce tabs.

**Trigger phrases** (non-exhaustive; match on intent, not exact wording):

- "Brief me on [account]"
- "Give me the account/opp overview before my call"
- "Prep me for [opportunity]"
- "What do I need to know about [account] before I talk to them?"
- "Kick off presales on [opportunity]"
- "Pull the account and opportunity context for [account/opp]"

## 2. Required / Optional Inputs

**Required (one of):**

- Account name or Salesforce Account ID
- Opportunity name or Salesforce Opportunity ID

**Optional:**

- Specific contact name (to prioritize in the stakeholder section)
- Specific product line or module (to focus the product fit notes, e.g.
  "focus on Wdesk / financial close")
- A specific upcoming meeting or call context (to tailor "what to walk in
  knowing")

If only an account name is given and multiple open opportunities exist, list
them and ask the user which opportunity to brief on, or produce a
multi-opportunity summary if the user asks for "all open opportunities."

## 3. Source Retrieval Guidance (Read-Only)

This skill is **read-only**. It never creates, updates, or deletes Salesforce
records. Use the following Salesforce MCP tools, in roughly this priority
order:

- `search_accounts` — resolve the account name/ID, pull account-level fields
  (industry, segment, ARR/employee band, parent/child org structure, owner).
- `search_opportunities` — resolve the opportunity name/ID, pull stage,
  amount, close date, opportunity type, product/line-item detail, and stage
  history if available.
- `search_contacts` — pull contacts associated with the account/opportunity:
  name, title, role, last activity date, and any Salesforce-noted buying
  role (economic buyer, champion, influencer, etc.).
- `retrieve_semantic_model` — use to understand custom fields, picklist
  values, or object relationships specific to this Salesforce org before
  interpreting raw field values (e.g. what a custom "Deal Health" picklist
  value means).
- `view_report` — pull any existing Salesforce report relevant to the
  account/opportunity (e.g. a pipeline or account-health report) rather than
  re-deriving aggregate metrics by hand.

If a tool returns no result, do not guess — surface that gap explicitly in
the output using the fallback strings in Section 9. Never fabricate a
Salesforce ID, contact, or figure to fill a gap.

## 4. Step-by-Step Workflow

1. **Resolve the target.** Use `search_accounts` and/or `search_opportunities`
   to unambiguously identify the account and opportunity in scope. If
   ambiguous (multiple matches), ask the user to disambiguate before
   proceeding.
2. **Pull account context.** Retrieve account overview fields via
   `search_accounts`. Use `retrieve_semantic_model` if any field's meaning is
   unclear (custom picklists, scoring fields, etc.).
3. **Pull opportunity context.** Retrieve stage, amount, close date, product
   line items, and opportunity type via `search_opportunities`. Note stage
   history or time-in-stage if the tool surfaces it.
4. **Pull stakeholder context.** Retrieve all contacts tied to the account/
   opportunity via `search_contacts`. Classify each by apparent buying role
   where Salesforce data supports it; otherwise mark role as unknown.
5. **Pull supplementary reporting.** Use `view_report` for any standing
   account-health, pipeline, or renewal report relevant to this account.
6. **Assemble product fit notes.** Cross-reference the opportunity's
   product/line-item data against the account's industry/segment to note
   likely fit angles. Mark anything not directly evidenced in Salesforce as
   an inference (see Section 5).
7. **Identify risks and open questions.** Note anything that reads as a risk
   signal (stalled stage, missing close date, no identified economic buyer,
   long time-in-stage, no recent activity) and anything unresolved that the
   SVC should validate on the call.
8. **Classify every claim.** Tag each factual statement in the brief with its
   evidence classification per Section 5.
9. **Assemble the one-page brief** per the schema in Section 6.
10. **Run the quality checklist** (Section 7) before returning the brief.
11. **Emit the handoff payload** (Section 10) alongside the human-readable
    brief so downstream presales skills can consume it directly.

## 5. Source Classification & Citation Rules

Use the shared evidence taxonomy defined in
[../shared/evidence-schema.md](../shared/evidence-schema.md). Every factual
claim in the output must be tagged with exactly one of the following
classifications:

- `confirmed_customer_statement` — something the customer has directly said
  or written (email, call transcript, submitted RFP text), attributed to a
  named person where possible.
- `salesforce_operating_context` — a value pulled directly from a Salesforce
  field or report (stage, amount, close date, contact title, etc.).
- `verified_workiva_internal_fact` — a fact confirmed via internal Workiva
  systems/process outside Salesforce (e.g. a signed order form detail, a
  product-team confirmation of a feature's availability).
- `inference_working_hypothesis` — a reasonable inference the skill drew from
  available data but that is not itself directly sourced (e.g. "likely
  champion based on meeting frequency").
- `open_question_validation_required` — something explicitly unknown that
  the SVC should validate on the call.
- `risk_assumption_dependency` — a risk, assumption, or dependency that
  could affect deal progress if untrue or unresolved.

**Examples:**

1. *"Opportunity is in Stage 3 (Solution Validation), Amount $180,000,
   Close Date 2026-11-30."* → `salesforce_operating_context` (direct
   Salesforce fields, cite `search_opportunities`).
2. *"Maria Chen (VP Finance) appears to be the economic buyer based on
   title and meeting attendance, but this is not confirmed in Salesforce."*
   → `inference_working_hypothesis`.
3. *"No economic buyer is currently identified on the opportunity — confirm
   on first call."* → `open_question_validation_required`.
4. *"Deal has been in current stage for 94 days with no logged activity in
   the last 21 days."* → `risk_assumption_dependency` (derived from
   Salesforce activity timestamps, flagged as a risk signal).

## 6. Output Schema

Produce a single one-page brief with these sections, in order. Every bullet
must end with an inline evidence tag in brackets, e.g. `[salesforce_operating_context]`.

```
# Account & Opportunity Brief: <Account Name> — <Opportunity Name>

## Account Overview
- Industry / segment / size [tag]
- Ownership (AE, CSM, SVC assigned) [tag]
- Relationship history summary [tag]

## Opportunity Snapshot
- Stage: <stage> [tag]
- Amount: <amount> [tag]
- Close Date: <date> [tag]
- Product / line items in scope [tag]
- Time in current stage / stage velocity notes [tag]

## Stakeholders / Buying Committee
- Name — Title — Apparent role (economic buyer / champion / influencer /
  unknown) [tag]
  (repeat per contact)

## Product Fit Notes
- Likely fit angle(s) given industry/segment/product scope [tag]

## Known Risks / Open Questions
- Risk or open item [tag]
  (repeat)
```

Any field with no available data must use the fallback strings in Section 9
rather than being omitted or guessed.

## 7. Quality Checklist

Before returning the brief, confirm:

- [ ] Every bullet has exactly one evidence classification tag.
- [ ] No claim is stated more confidently than its source supports.
- [ ] All five output sections are present, even if some contain only
      fallback strings.
- [ ] At least one open question or risk is surfaced, or it is explicitly
      stated that none were found.
- [ ] All Salesforce tool calls used were read-only (no create/update/delete
      calls were made).
- [ ] The handoff JSON payload (Section 10) is included and validates against
      `../shared/evidence-schema.md`.

## 8. Read-Only Disclaimer

**This skill is strictly read-only.** It queries Salesforce via
`search_accounts`, `search_opportunities`, `search_contacts`,
`retrieve_semantic_model`, and `view_report` only. It never creates,
modifies, or deletes any Salesforce record, field, or report. If a user asks
this skill to update Salesforce data, decline and point them to the
`salesforce-draft-updates` skill instead.

## 9. Fallback Strings

Use these exact strings whenever information is unavailable or unconfirmed —
never fabricate a substitute:

- `"Unknown — requires validation."` — for missing factual fields (e.g. no
  close date set, no identified economic buyer).
- `"Requires Workiva-source validation."` — for claims that would need
  confirmation from an internal Workiva source not accessible to this skill.

## 10. MCP / Demo-Adapter Handoff Payload

This brief is the seed document for two downstream flows: the live
`workiva-mcp-adapter` (which other presales skills query for account/opp
context in-session) and the `demo-framework-adapter` (which uses account and
product-fit context to configure a tailored demo environment) — both need
this exact structured payload, so it is emitted once here rather than
re-derived by each downstream skill.

```json
{
  "schema_ref": "../shared/evidence-schema.md",
  "handoff_target": ["workiva-mcp-adapter", "demo-framework-adapter"],
  "source_skill": "account-opportunity-brief",
  "account": {
    "name": "<Account Name>",
    "salesforce_id": "<Account ID or Unknown — requires validation.>"
  },
  "opportunity": {
    "name": "<Opportunity Name>",
    "salesforce_id": "<Opportunity ID or Unknown — requires validation.>",
    "stage": "<value>",
    "amount": "<value>",
    "close_date": "<value>"
  },
  "claims": [
    {
      "field": "<e.g. opportunity.stage>",
      "value": "<value>",
      "evidence_classification": "salesforce_operating_context",
      "source_tool": "search_opportunities"
    }
  ],
  "open_questions": [
    {
      "question": "<text>",
      "evidence_classification": "open_question_validation_required"
    }
  ],
  "risks": [
    {
      "risk": "<text>",
      "evidence_classification": "risk_assumption_dependency"
    }
  ]
}
```

## 11. Worked Example (Fully Synthetic)

All names, IDs, and figures below are fabricated for illustration. No real
account, contact, or deal data is represented.

### Input

> "Brief me on Acme Test Corp — Enterprise Expansion FY26."

### Output

```
# Account & Opportunity Brief: Acme Test Corp — Acme Test Corp — Enterprise Expansion FY26

## Account Overview
- Industry: Manufacturing; Segment: Enterprise; ~4,200 employees [salesforce_operating_context]
- Account owner: AE Jordan Blake; SVC assigned: this engagement [salesforce_operating_context]
- Existing Workiva customer since 2022 (SEC reporting module) [salesforce_operating_context]

## Opportunity Snapshot
- Stage: Stage 3 — Solution Validation [salesforce_operating_context]
- Amount: $210,000 ARR [salesforce_operating_context]
- Close Date: 2026-12-15 [salesforce_operating_context]
- Product/line items in scope: ESG reporting expansion, audit management add-on [salesforce_operating_context]
- 61 days in current stage; last logged activity 9 days ago [salesforce_operating_context]

## Stakeholders / Buying Committee
- Dana Whitfield — VP Controller — likely economic buyer based on title and deal size [inference_working_hypothesis]
- Sam Ortega — Director of ESG Reporting — likely champion, most frequent meeting attendee [inference_working_hypothesis]
- IT/Security reviewer — not yet identified [open_question_validation_required]

## Product Fit Notes
- Existing SEC reporting footprint suggests strong platform familiarity, likely shortens technical onboarding for ESG module [inference_working_hypothesis]
- Audit management add-on fit unconfirmed against Acme Test Corp's current audit workflow — requires Workiva-source validation. [open_question_validation_required]

## Known Risks / Open Questions
- No economic buyer confirmed in Salesforce; Dana Whitfield's role is inferred, not verified — confirm on first call [risk_assumption_dependency]
- Deal has been in current stage 61 days, longer than typical for this stage/segment — investigate stall cause [risk_assumption_dependency]
- Security/IT stakeholder not yet identified for a deal of this size — Unknown — requires validation. [open_question_validation_required]
```

```json
{
  "schema_ref": "../shared/evidence-schema.md",
  "handoff_target": ["workiva-mcp-adapter", "demo-framework-adapter"],
  "source_skill": "account-opportunity-brief",
  "account": {
    "name": "Acme Test Corp",
    "salesforce_id": "001TEST0000ACME"
  },
  "opportunity": {
    "name": "Acme Test Corp — Enterprise Expansion FY26",
    "salesforce_id": "006TEST0000ACME",
    "stage": "Stage 3 — Solution Validation",
    "amount": "210000",
    "close_date": "2026-12-15"
  },
  "claims": [
    {
      "field": "opportunity.stage",
      "value": "Stage 3 — Solution Validation",
      "evidence_classification": "salesforce_operating_context",
      "source_tool": "search_opportunities"
    },
    {
      "field": "stakeholder.dana_whitfield.role",
      "value": "likely economic buyer",
      "evidence_classification": "inference_working_hypothesis",
      "source_tool": "search_contacts"
    }
  ],
  "open_questions": [
    {
      "question": "Who is the security/IT reviewer for this opportunity?",
      "evidence_classification": "open_question_validation_required"
    }
  ],
  "risks": [
    {
      "risk": "61 days in current stage with declining activity cadence.",
      "evidence_classification": "risk_assumption_dependency"
    }
  ]
}
```
