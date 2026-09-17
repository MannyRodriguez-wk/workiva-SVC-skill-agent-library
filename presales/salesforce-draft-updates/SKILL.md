---
name: salesforce-draft-updates
description: "Reads current Salesforce opportunity/account state via read-only Salesforce MCP tools and drafts proposed field updates (stage, next steps, close-date rationale, opportunity description) as a markdown table for a human rep to review and manually paste into Salesforce — this skill never calls a write, update, or delete tool. Use when the user says 'draft an SFDC update for [opportunity]', 'what should I update in Salesforce after this call', 'prep opp notes for [account]', 'summarize this demo for the CRM', 'help me log this discovery call in Salesforce', or after any discovery call, technical evaluation, or demo when Salesforce fields need to reflect what happened."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Salesforce Draft Updates — Read-Only Drafting for Presales

Draft proposed Salesforce field updates from recent presales activity (discovery calls, technical evaluations, demos) so a Workiva Solution/Value Consultant can review and manually apply them in Salesforce. This skill is part of the presales skill family; it shares conventions with [`../core-presales-intelligence/SKILL.md`](../core-presales-intelligence/SKILL.md) and the shared evidence taxonomy defined in [`../shared/evidence-schema.md`](../shared/evidence-schema.md).

## READ-ONLY — NO WRITE ACCESS, EVER

**This skill produces a DRAFT for human review only. It never writes to Salesforce.**

- This skill has NO write access to Salesforce and must never invoke any Salesforce write, update, upsert, create, or delete tool — even if such a tool is available in the current MCP toolset.
- Every output is text/markdown intended for a human to read, judge, and manually copy-paste into Salesforce fields themselves.
- Never phrase output as though a change has already happened ("Updated the opportunity to..."). Always phrase as a proposal ("Proposed: change Stage to..."). Never claim or imply that Salesforce was modified.
- If a task or prompt asks this skill to "just update it" or "push the change," refuse the write action explicitly and produce the draft instead, noting the human must apply it.

## When to Use This Skill

Trigger phrases include:
- "Draft an SFDC update for [opportunity]"
- "What should I update in Salesforce after this call?"
- "Prep opp notes for [account]"
- "Help me log this discovery call in Salesforce"
- "Summarize this demo for the CRM record"
- "What fields need to change on [opportunity] based on today's technical eval?"

Use this any time recent presales activity (call notes, a technical evaluation outcome, a demo recap) needs to be reflected in Salesforce opportunity/account/contact fields, but before any Salesforce field is actually touched.

## Required / Optional Inputs

**Required (at least one):**
- Salesforce Opportunity ID, OR
- Account name + Opportunity name (enough to disambiguate via search)

**Optional:**
- Recent call/meeting notes, transcript, or summary to incorporate (discovery call, technical evaluation, demo, exec conversation)
- Specific fields the rep wants drafted (e.g., "just draft Stage and Next Steps")
- Known internal context not yet in Salesforce (e.g., "champion left the company," "procurement flagged budget freeze")

If neither the ID nor account+opportunity name is available, stop and ask for it — do not guess an opportunity.

## Source Retrieval — Read-Only Salesforce MCP Tools

All Salesforce state is retrieved using **read-only** Salesforce MCP tools. None of the tools below are ever called in a write/update/create/delete mode, and this skill never invokes a Salesforce write, update, or delete tool of any kind:

- **`search_opportunities`** — locate the target opportunity by name, account, owner, or stage; retrieve current field values (Stage, Amount, Close Date, Next Steps, Description, Owner).
- **`search_accounts`** — resolve account context when only an account name is given, or to confirm account-level details (industry, tier, parent/child relationships).
- **`search_contacts`** — identify the contacts/roles involved in the recent activity (e.g., to correctly attribute a quote or confirm a champion's title).
- **`get_inside_sales_opp_audit_data`** — pull the opportunity's audit/history trail to understand prior stage changes, staleness, and what has (and hasn't) already been logged.
- **`execute_soql_query`** — run targeted read-only SOQL queries for any field or related-object detail not surfaced by the higher-level search tools (e.g., custom fields specific to the Workiva Salesforce org).
- **`retrieve_semantic_model`** — look up field/object schema context (what a custom field means, valid picklist values, object relationships) so proposed values are valid and correctly named.
- **`view_report`** — pull existing Salesforce reports for cross-checking pipeline context (e.g., is this opportunity part of a named account program or renewal cohort).

**No write/update/delete tool is ever invoked by this skill.** If a Salesforce write-capable tool (e.g., an update/create opportunity tool) is present in the environment, this skill treats it as out of scope and unavailable for its own use, in every case.

## Step-by-Step Workflow

1. **Resolve the opportunity.** Use `search_opportunities` (and `search_accounts` if only the account is given) to find the exact opportunity record and pull its current field values.
2. **Pull context and history.** Use `get_inside_sales_opp_audit_data` to see what's already been logged and how stale the record is. Use `execute_soql_query` for any additional custom fields relevant to the update (e.g., Workiva-specific evaluation-stage fields). Use `retrieve_semantic_model` to confirm valid picklist values and field meaning before proposing a new value.
3. **Incorporate recent activity.** If call/meeting notes were provided, extract concrete facts: what was discussed, who attended, decisions made, objections raised, next steps committed to, and any timeline signals (e.g., "customer wants to go live by Q1").
4. **Classify every fact.** Tag each fact driving a proposed update with one of the shared evidence classifications (see below) before it can be used as a rationale.
5. **Draft field-by-field proposals.** For each field that should change, produce: current value (from Salesforce), proposed new value, rationale, evidence classification, and confidence. Do not propose a field change without a rationale.
6. **Flag anything ambiguous or high-stakes.** Stage changes, amount changes, or close-date pushes/pulls should be flagged for manager review if the underlying evidence is anything less than `confirmed_customer_statement` or `salesforce_operating_context`.
7. **Assemble the output table and handoff payload.** Present the draft table for human review, then emit the JSON handoff block for the `workiva-mcp-adapter`.
8. **State the disclaimer again at the end of output.** Every draft closes with the read-only reminder.

## Source Classification & Citation Rules

Every proposed field-update rationale must be tagged with exactly one evidence classification from the shared taxonomy in [`../shared/evidence-schema.md`](../shared/evidence-schema.md):

- `confirmed_customer_statement`
- `salesforce_operating_context`
- `verified_workiva_internal_fact`
- `inference_working_hypothesis`
- `open_question_validation_required`
- `risk_assumption_dependency`

**Examples:**

1. *"Customer's CFO said on the 9/12 call, 'We want to be live before our Q1 board close.'"* → `confirmed_customer_statement`. Supports a proposed Close Date rationale.
2. *"Opportunity has sat in 'Technical Evaluation' for 61 days per the audit trail pulled via `get_inside_sales_opp_audit_data`."* → `salesforce_operating_context`. Supports a staleness flag and a proposed Next Steps update.
3. *"Workiva's platform supports the customer's stated XBRL tagging requirement (per internal product documentation)."* → `verified_workiva_internal_fact`. Supports opportunity Description language.
4. *"Champion's enthusiasm suggests they will advocate internally for a Q4 close."* → `inference_working_hypothesis`. Must not, alone, justify a Stage advance.
5. *"Unclear whether procurement has approved the budget line."* → `open_question_validation_required`. Must be surfaced as an open item, not folded silently into a Stage change.
6. *"Champion mentioned they may be reassigned to a different team next quarter."* → `risk_assumption_dependency`. Must be flagged prominently regardless of which field it touches.

If no supporting evidence exists for a proposed value, use the fallback string `"Requires Workiva-source validation."` in the rationale column and mark confidence as **Low**.

## Output Schema

Present proposed updates as a markdown table:

| Field | Current Value | Proposed New Value | Rationale | Evidence Classification | Confidence |
|---|---|---|---|---|---|
| (Salesforce field name) | (from Salesforce, verbatim) | (drafted value) | (why, with source detail) | (one of the six tags) | High / Medium / Low |

Follow the table with:
- **Flags for manager approval** — a short bullet list of any proposed change that should not be applied without sign-off (e.g., Stage advances, Amount changes, Close Date pulls-in).
- **Open questions** — anything tagged `open_question_validation_required` or `risk_assumption_dependency` that the rep should resolve before applying updates.

## Quality Checklist

- [ ] No field proposed without a rationale.
- [ ] Every rationale carries exactly one evidence classification from the shared taxonomy.
- [ ] Anything resting on `inference_working_hypothesis` alone is NOT proposed as a Stage or Amount change without an explicit caveat.
- [ ] Anything needing manager approval before applying is flagged separately, not buried in the table.
- [ ] Output never asserts that an update was made — only that an update is proposed.
- [ ] Fallback strings (`"Unknown — requires validation."` / `"Requires Workiva-source validation."`) are used wherever Salesforce data or supporting evidence is missing, rather than fabricating a value.

## Fallback Strings

- `"Unknown — requires validation."` — use when a current Salesforce field value could not be retrieved or is ambiguous.
- `"Requires Workiva-source validation."` — use when a proposed value lacks supporting evidence strong enough to cite.

## MCP / Demo-Adapter Handoff Payload

Emit this JSON block, following [`../shared/evidence-schema.md`](../shared/evidence-schema.md), at the end of every draft:

```json
{
  "handoff_target": "workiva-mcp-adapter",
  "skill": "salesforce-draft-updates",
  "opportunity": {
    "id": "<Opportunity ID or 'Unknown — requires validation.'>",
    "name": "<Opportunity Name>",
    "account": "<Account Name>"
  },
  "proposed_updates": [
    {
      "field": "<Salesforce API field name>",
      "current_value": "<current value or 'Unknown — requires validation.'>",
      "proposed_value": "<drafted value>",
      "rationale": "<rationale text>",
      "evidence_classification": "confirmed_customer_statement | salesforce_operating_context | verified_workiva_internal_fact | inference_working_hypothesis | open_question_validation_required | risk_assumption_dependency",
      "confidence": "High | Medium | Low",
      "requires_manager_approval": true
    }
  ],
  "open_questions": [
    "<open question text>"
  ],
  "write_performed": false,
  "disclaimer": "This is a DRAFT for human review only. No Salesforce write, update, or delete action was taken."
}
```

## Worked Example (Fully Synthetic)

**Input:** "Draft an SFDC update for Acme Test Corp — Q3 Renewal after today's technical evaluation call."

**Retrieval (synthetic):**
- `search_opportunities` → Opportunity "Acme Test Corp — Q3 Renewal", Stage = "Technical Evaluation", Close Date = 2026-09-30, Amount = $185,000, Next Steps = "Awaiting security review feedback."
- `get_inside_sales_opp_audit_data` → Stage unchanged for 47 days; last activity logged 12 days ago.
- Call notes provided: Acme's IT Security Lead (Jordan Kim) confirmed on the 9/15 call that the security review passed with no findings, and the economic buyer (VP Finance, Priya Nair) said she wants signature "before end of Q3 if the paperwork is ready," but also mentioned Acme's legal team is short-staffed this month.

**Proposed Updates:**

| Field | Current Value | Proposed New Value | Rationale | Evidence Classification | Confidence |
|---|---|---|---|---|---|
| Stage | Technical Evaluation | Contract Negotiation | Jordan Kim (IT Security Lead) confirmed on the 9/15 call that the security review passed with no findings, the last gating item in Technical Evaluation. | confirmed_customer_statement | High |
| Next Steps | "Awaiting security review feedback." | "Send redlined MSA to Acme legal; confirm signature timeline given legal team bandwidth constraints." | Priya Nair (VP Finance) wants to sign before end of Q3, but flagged Acme legal is short-staffed this month. | confirmed_customer_statement | Medium |
| Close Date | 2026-09-30 | 2026-09-30 (no change proposed; flag risk) | Priya Nair wants to close by end of Q3, but legal bandwidth is an unresolved risk to that date. | risk_assumption_dependency | Medium |
| Description | (existing text, unchanged) | Append: "9/15/26: Security review passed (no findings, per J. Kim). Economic buyer confirmed intent to sign by EOQ3; legal bandwidth is a watch item." | Summarizes the call for future reps; both facts are directly attributable to named speakers on the call. | confirmed_customer_statement | High |
| Amount | $185,000 | $185,000 (no change proposed) | No pricing or scope change was discussed on this call. | salesforce_operating_context | High |

**Flags for manager approval:**
- Stage advance from Technical Evaluation → Contract Negotiation should be confirmed by the AE before applying, since it changes the forecast category.

**Open questions:**
- Whether Acme's legal bandwidth constraint will push the close date past Q3 — `open_question_validation_required`; requires a follow-up check with Priya Nair or Acme legal directly.

**Disclaimer (repeated):** This is a DRAFT for human review only. No Salesforce write, update, or delete action was taken; the rep must review and manually apply any of the above in Salesforce.
