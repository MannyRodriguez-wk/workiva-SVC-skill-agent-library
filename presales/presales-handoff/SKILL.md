---
name: presales-handoff
description: "Consolidates outputs from the other Workiva presales skills (account-opportunity-brief, gong-discovery-analysis, technical-discovery-planner, evaluation-validation-planner, rfp-security-analysis) into a single clean Presales-to-Post-Sales Handoff Packet at deal-stage transition — closed-won or eval-to-implementation. Captures what was promised, what was validated, open commitments, known risks, and key stakeholder contacts for the Implementation/Customer Success team taking over the account. Use when a Solution/Value Consultant asks things like 'build the handoff packet for Acme Corp', 'prep this deal for implementation handoff', 'summarize everything for CS on this opportunity', 'what did we promise this customer during the sales cycle', or 'consolidate our presales work before CS takes over'. Read-only — never writes back to Salesforce or any other system; only optionally confirms deal stage/close date via Salesforce read tools."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Presales-to-Post-Sales Handoff Packet

Turn the scattered outputs of the presales process — account/opportunity brief, Gong discovery analysis, technical discovery agenda, evaluation/validation plan, RFP/security analysis — into a single, clean handoff document the Implementation/Customer Success (CS) team can actually use on day one, without re-reading five separate reports or re-interviewing the SC/VC.

This skill is one of nine sibling presales skills. It shares conventions with, and assumes familiarity with:

- [`../core-presales-intelligence/SKILL.md`](../core-presales-intelligence/SKILL.md) — the evidence classification taxonomy and general presales-intelligence conventions used across all skills in this library.
- [`../shared/evidence-schema.md`](../shared/evidence-schema.md) — the shared handoff JSON schema used to pass structured output to downstream MCP/demo-building adapters.

If those files are not yet present in your checkout, treat the classification and handoff format below as the authoritative interim spec — they are written to match those documents exactly once they land.

## 1. Purpose & Trigger Phrases

Invoke this skill at deal-stage transition — closed-won, or moving from evaluation into implementation — when an SC/VC needs to package everything learned and promised during the sales cycle into one document for the team taking over the account. Typical trigger phrases:

- "Build the handoff packet for [account]"
- "Prep this deal for implementation handoff"
- "Summarize everything for CS on [opportunity]"
- "What did we promise [account] during the sales cycle?"
- "Consolidate our presales work before CS takes over"
- "Package up the discovery/eval work for the transition team"
- "Create a closed-won handoff for [account]"

Do not invoke this skill for: mid-cycle status updates, single-source summaries (use the individual sibling skill instead — e.g. gong-discovery-analysis for just Gong), or any workflow that requires updating Salesforce fields, creating tasks, or notifying the CS team through a system (flag those as follow-up actions for a human, not something this skill performs).

## 2. Inputs

**Required:**
- Account name or Salesforce Opportunity name/ID for the deal being handed off.

**Optional** (the more of these pasted in, the more complete the packet — but the skill must run and produce a partial packet even if only the account name is given):
- Pasted output from `account-opportunity-brief` (deal background, buying committee, business context)
- Pasted output from `gong-discovery-analysis` (call themes, pain points, objections, competitive mentions)
- Pasted output from `technical-discovery-planner` (technical requirements, discovery agenda findings)
- Pasted output from `evaluation-validation-planner` (what was validated in the eval/POC, success criteria met/unmet)
- Pasted output from `rfp-security-analysis` (RFP commitments, security/compliance answers given)
- Final deal stage and close date, if already known and not requiring Salesforce lookup

If none of the optional inputs are pasted, say so explicitly in the output rather than fabricating source material — produce a packet consisting mostly of `"Unknown — requires validation."` entries and a clear note that no upstream skill outputs were provided.

## 3. Source Retrieval Guidance

This skill is a **consolidator, not a primary retriever.** It does not call Gong, Google Drive, or the Workiva internal GRC/Documents MCP directly — it works from whatever pasted sibling-skill outputs the user provides.

The one exception: this skill **may optionally** call Salesforce's `search_opportunities` (read-only) to confirm the final opportunity stage and close date if the user did not already supply them or paste an `account-opportunity-brief` output containing that data. Use it narrowly:

- Call `search_opportunities` only to confirm stage/close date/amount — not to re-derive discovery content, stakeholders, or technical findings (those come from the pasted sibling outputs).
- If `search_opportunities` returns no match or an ambiguous match, do not guess — record `"Unknown — requires validation."` for deal stage/close date and note the lookup attempt in the output.
- Never call any Salesforce write tool. This skill has no legitimate reason to update an opportunity, account, or contact record.

## 4. Step-by-Step Workflow

1. **Identify the deal.** Confirm account name and, if given, opportunity name/ID.
2. **Inventory the pasted inputs.** For each of the five possible sibling outputs (brief, Gong analysis, discovery agenda, eval plan, RFP analysis), note whether it was provided. List missing inputs explicitly — do not silently treat a missing input as "nothing to report" versus "not checked."
3. **Confirm deal stage/close date if missing.** If not present in any pasted input and not stated by the user, optionally call Salesforce `search_opportunities` (§3) to fill this in; otherwise use the fallback string.
4. **Extract candidate facts from each pasted input**, tagging each with: the originating skill, the evidence classification it already carried (if the pasted output included one), and which handoff-packet section it belongs to (Deal Summary / What Was Promised / What Was Validated / Open Commitments & Risks / Key Stakeholders).
5. **Reconcile duplicate or conflicting facts across inputs.** This is the core value of this skill — do it explicitly, not silently:
   - If the same fact appears in two or more pasted inputs with the **same** evidence classification, merge into one line and cite all originating skills.
   - If the same fact appears with **different** classifications across inputs (e.g. `gong-discovery-analysis` tagged a claim `confirmed_customer_statement` but `account-opportunity-brief` tagged the same claim `inference_working_hypothesis`), **always keep the strongest/most-verified classification** using this precedence order (strongest first): `confirmed_customer_statement` > `salesforce_operating_context` > `verified_workiva_internal_fact` > `inference_working_hypothesis` > `risk_assumption_dependency` > `open_question_validation_required`.
   - When classifications conflict, **flag the conflict explicitly** in the output (a "Conflicting Source Classifications" note under the relevant section) — do not just quietly pick the stronger tag and move on. Name both source skills and both classifications so the CS reader knows this fact was disputed upstream.
   - If two inputs state facts that are substantively **contradictory** (not just differently classified — e.g. one says the eval passed a requirement, another says it didn't), do not resolve this by guesswork. Surface both statements side by side under Open Commitments/Risks with `open_question_validation_required` and a note to confirm with the account team.
6. **Populate the six output sections** (§6), carrying every claim's evidence classification and originating skill forward.
7. **Run the quality checklist** (§7).
8. **Emit the handoff JSON** (§10).
9. **Never write anything back.** This skill only reads pasted text and, optionally, Salesforce, and returns a document (§8).

## 5. Source Classification & Citation Rules

Every claim in the packet **must** carry exactly one evidence classification, using the taxonomy defined in [`../core-presales-intelligence/SKILL.md`](../core-presales-intelligence/SKILL.md):

- `confirmed_customer_statement` — something a prospect/customer stakeholder said directly, as reported by an upstream skill (e.g. a quote surfaced in `gong-discovery-analysis`).
- `salesforce_operating_context` — factual metadata pulled from Salesforce (stage, amount, close date), whether from a pasted `account-opportunity-brief` or this skill's own optional `search_opportunities` lookup.
- `verified_workiva_internal_fact` — a Workiva-side fact (product capability, roadmap, pricing) that an upstream skill independently confirmed against a Workiva-internal source.
- `inference_working_hypothesis` — a conclusion an upstream skill (or this one, when reconciling) drew by connecting signals, not something anyone stated outright.
- `open_question_validation_required` — something no pasted input clearly answers, including unresolved conflicts between inputs (§4 step 5).
- `risk_assumption_dependency` — a stated or implied condition that, if false, would undermine the account relationship or an open commitment (e.g. "assumes the Q1 integration timeline holds").

When reconciling (§4 step 5), this skill additionally applies the precedence rule above and must preserve — never discard — the originating skill name for every claim, even after merging duplicates.

A claim with no classification tag, or with a classification silently changed without noting the conflict, is not valid output.

## 6. Output Schema

Return the packet as a markdown document with the following structure. Every claim carries an evidence classification and an originating-skill citation.

### 6.1 Handoff Packet

1. **Deal Summary** — account name, opportunity name/ID, final stage, close date, deal amount if known, one-paragraph narrative of the sales cycle.
2. **What Was Promised** — commitments made to the customer during the sales cycle (features, timelines, integrations, pricing terms, roadmap items) drawn primarily from `account-opportunity-brief`, `gong-discovery-analysis`, and `rfp-security-analysis`.
3. **What Was Validated** — requirements or success criteria confirmed during evaluation, drawn primarily from `evaluation-validation-planner` and `technical-discovery-planner`, including what was tested and the outcome.
4. **Open Commitments & Risks** — anything promised or validated with an unresolved dependency, an unmet success criterion, an unresolved cross-input conflict (§4 step 5), or a `risk_assumption_dependency`-tagged item.
5. **Key Stakeholders & Contacts** — buying-committee members and their roles, sourced from `account-opportunity-brief` and `gong-discovery-analysis`, with role/title and any noted sentiment or influence level.
6. **Source Documents Referenced** — a list of which sibling-skill outputs were provided as input to this run, and which were missing.

Every claim in sections 2-5 uses this row shape:

| Claim | Evidence Classification | Originating Skill(s) | Notes |
| --- | --- | --- | --- |

### 6.2 Equivalent JSON form (for programmatic consumption)

```json
{
  "account": "string",
  "opportunity_id": "string | null",
  "handoff_date": "YYYY-MM-DD",
  "deal_summary": {
    "stage": "string",
    "close_date": "string | null",
    "amount": "string | null",
    "narrative": "string"
  },
  "what_was_promised": [
    { "claim": "string", "classification": "string", "originating_skills": ["string"], "notes": "string" }
  ],
  "what_was_validated": [
    { "claim": "string", "classification": "string", "originating_skills": ["string"], "notes": "string" }
  ],
  "open_commitments_and_risks": [
    { "claim": "string", "classification": "string", "originating_skills": ["string"], "notes": "string" }
  ],
  "key_stakeholders": [
    { "name": "string", "role": "string", "influence_notes": "string", "originating_skills": ["string"] }
  ],
  "source_documents_referenced": {
    "provided": ["string"],
    "missing": ["string"]
  }
}
```

## 7. Quality Checklist

Before returning output, verify:

- [ ] No commitment, validation result, or stakeholder fact is listed without an evidence classification and an originating-skill citation.
- [ ] Conflicting claims across pasted inputs are surfaced explicitly (side by side, with both sources named) — never silently merged or silently resolved without a note.
- [ ] When the same fact appears with different classifications, the strongest classification per the §4 precedence order was kept, and the conflict is flagged, not hidden.
- [ ] Every sibling skill's output that was NOT pasted in is listed under "Source Documents Referenced → missing," not omitted from the packet entirely.
- [ ] Any deal-stage/close-date fact sourced from the optional `search_opportunities` call is tagged `salesforce_operating_context`, not asserted as if it came from a pasted input.
- [ ] The handoff JSON (§10) validates against the shared evidence schema shape and has `handoff_target: workiva-mcp-adapter` set.

## 8. Read-Only Disclaimer

This skill is **strictly read-only**. It never writes, updates, or deletes any record in Salesforce, Gong, Google Drive, or any other connected system, and it does not create tasks, log CS handoff notices, or update opportunity fields. Its only optional external call is Salesforce `search_opportunities` in read capacity (§3). Its only output is a structured handoff document and payload for downstream human review or another tool to consume.

## 9. Fallback Strings

Use these exact strings when data is unavailable — do not paraphrase them:

- `"Unknown — requires validation."` — use when no pasted input and no optional Salesforce lookup covers a requested field (e.g. no close date available anywhere).
- `"Requires Workiva-source validation."` — use when a claim depends on a Workiva-internal fact (product capability, roadmap, pricing) that no pasted upstream skill output independently confirmed against a Workiva-internal source.

## 10. MCP / Demo-Adapter Handoff Payload

End every run with a handoff JSON block matching the shared schema at [`../shared/evidence-schema.md`](../shared/evidence-schema.md). Set `handoff_target` to `workiva-mcp-adapter`, since the consumer of a completed deal-transition packet is the internal system that logs/attaches it to the account record for the CS team, not the demo-framework adapter.

```json
{
  "skill": "presales-handoff",
  "handoff_target": ["workiva-mcp-adapter"],
  "account": "string",
  "opportunity_id": "string | null",
  "handoff_date": "YYYY-MM-DD",
  "summary": "string",
  "evidence": [
    {
      "claim": "string",
      "classification": "confirmed_customer_statement | salesforce_operating_context | verified_workiva_internal_fact | inference_working_hypothesis | open_question_validation_required | risk_assumption_dependency",
      "source": "string (originating sibling skill + original source citation)"
    }
  ],
  "open_questions": ["string"],
  "read_only": true
}
```

## 11. Fully Synthetic Example

The following is a fabricated, illustrative walkthrough only. "Acme Test Corp," all quotes, names, and pasted skill outputs below are fictional and used solely to demonstrate the workflow end to end.

**User request:** "Build the handoff packet for Acme Test Corp — this just closed won, prep it for CS." (User pastes fabricated excerpts from four sibling skills below; no `rfp-security-analysis` output was provided.)

**Pasted excerpt from `account-opportunity-brief`:**
> Opportunity: "Acme Test Corp — FY27 Reporting Platform Renewal." Stage: Closed Won. Close date: 2026-09-10. Amount: $184,000 ARR. Buying committee: Jordan Lee (VP Finance, economic buyer), Sam Okafor (Controller, day-to-day admin), Priya Chandran (IT Security, evaluated SSO/SOC 2). Classification: `salesforce_operating_context` for stage/close date/amount.

**Pasted excerpt from `gong-discovery-analysis`:**
> Pain point: "Our close takes 9 business days and that's the single biggest thing slowing down our audit committee reporting." — Jordan Lee, VP Finance, call 2026-08-05. Classification: `confirmed_customer_statement`. AE verbally committed on the 2026-08-19 call to "prioritize the custom XBRL tagging template Acme needs by their Q1 board cycle" — classified there as `inference_working_hypothesis` (paraphrased by the analyst from AE's tone, not a verbatim AE commitment).

**Pasted excerpt from `technical-discovery-planner`:**
> Discovery agenda confirmed requirement: single sign-on via Okta, required by Priya Chandran (IT Security) as a go-live blocker. Also logged the same AE custom-XBRL-template commitment from the 2026-08-19 call, but classified as `confirmed_customer_statement` because the planner's notes cite a direct AE quote: "I'll make sure the custom XBRL template ships before your Q1 board cycle."

**Pasted excerpt from `evaluation-validation-planner`:**
> Eval result: Okta SSO integration validated successfully in the Acme sandbox on 2026-08-28 — `verified_workiva_internal_fact` (confirmed against Workiva internal GRC/Documents MCP integration test log). Eval result: custom XBRL tagging template was NOT tested during the eval window; POC scope excluded it. Classification: `open_question_validation_required`.

**Step 2 (inventory):** Provided — account-opportunity-brief, gong-discovery-analysis, technical-discovery-planner, evaluation-validation-planner. Missing — rfp-security-analysis.

**Step 3:** Stage and close date already present in the pasted brief; no Salesforce lookup needed.

**Step 5 (reconcile conflict):** The AE's custom-XBRL-template commitment appears in both `gong-discovery-analysis` (tagged `inference_working_hypothesis`) and `technical-discovery-planner` (tagged `confirmed_customer_statement`, citing a direct quote). Per precedence order, `confirmed_customer_statement` is stronger — kept as the classification — but the conflict is flagged below since one source treated it as inferred and the other as a direct quote.

### Handoff Packet

**1. Deal Summary**
Acme Test Corp — FY27 Reporting Platform Renewal. Stage: Closed Won. Close date: 2026-09-10. Amount: $184,000 ARR. Sales cycle ran roughly six weeks, driven by manual-close-process pain reported by the VP Finance and an SSO requirement from IT Security.

**2. What Was Promised**

| Claim | Evidence Classification | Originating Skill(s) | Notes |
| --- | --- | --- | --- |
| AE committed to ship the custom XBRL tagging template before Acme's Q1 board cycle. | confirmed_customer_statement | gong-discovery-analysis, technical-discovery-planner | **Conflicting Source Classifications**: gong-discovery-analysis tagged this `inference_working_hypothesis` (paraphrase); technical-discovery-planner tagged it `confirmed_customer_statement` (direct quote cited). Stronger classification kept per precedence rule; flagged for CS to confirm actual AE commitment language with the account team. |

**3. What Was Validated**

| Claim | Evidence Classification | Originating Skill(s) | Notes |
| --- | --- | --- | --- |
| Okta SSO integration validated successfully in Acme sandbox, 2026-08-28. | verified_workiva_internal_fact | evaluation-validation-planner | Confirmed against Workiva internal GRC/Documents MCP integration test log. Go-live blocker for Priya Chandran is satisfied. |

**4. Open Commitments & Risks**

| Claim | Evidence Classification | Originating Skill(s) | Notes |
| --- | --- | --- | --- |
| Custom XBRL tagging template was NOT tested during the eval window; POC scope excluded it. | open_question_validation_required | evaluation-validation-planner | This is an open commitment: promised (see §2) but unvalidated. CS must confirm delivery plan and timeline before Acme's Q1 board cycle. |
| Whether Acme's Q1 board cycle date is firm, and whether it conflicts with product's actual XBRL template delivery timeline. | open_question_validation_required | (none — gap identified during reconciliation) | Not addressed by any pasted input. |

**5. Key Stakeholders & Contacts**

| Name | Role | Notes | Originating Skill(s) |
| --- | --- | --- | --- |
| Jordan Lee | VP Finance, economic buyer | Primary sponsor; raised the original close-process pain point. | account-opportunity-brief, gong-discovery-analysis |
| Sam Okafor | Controller, day-to-day admin | Will be primary hands-on user post go-live. | account-opportunity-brief |
| Priya Chandran | IT Security | Owned the SSO requirement; go-live blocker now resolved per eval. | account-opportunity-brief, technical-discovery-planner |

**6. Source Documents Referenced**
- Provided: account-opportunity-brief, gong-discovery-analysis, technical-discovery-planner, evaluation-validation-planner
- Missing: rfp-security-analysis — `"Unknown — requires validation."` for any RFP-sourced commitments; CS should ask the SC/VC whether an RFP response exists.

### Handoff JSON

```json
{
  "skill": "presales-handoff",
  "handoff_target": ["workiva-mcp-adapter"],
  "account": "Acme Test Corp",
  "opportunity_id": "FICTIONAL-OPP-0001",
  "handoff_date": "2026-09-16",
  "summary": "Acme Test Corp closed won on 2026-09-10 ($184,000 ARR). Key open item for CS: the AE-promised custom XBRL tagging template was never validated during the eval and its classification was disputed between two upstream skills; Okta SSO is validated and satisfies the IT Security go-live blocker.",
  "evidence": [
    {
      "claim": "Opportunity stage: Closed Won, close date 2026-09-10, amount $184,000 ARR.",
      "classification": "salesforce_operating_context",
      "source": "account-opportunity-brief (pasted input)"
    },
    {
      "claim": "AE committed to ship the custom XBRL tagging template before Acme's Q1 board cycle.",
      "classification": "confirmed_customer_statement",
      "source": "technical-discovery-planner (direct quote cited); conflicting classification of inference_working_hypothesis also reported by gong-discovery-analysis — see notes"
    },
    {
      "claim": "Okta SSO integration validated successfully in Acme sandbox, 2026-08-28.",
      "classification": "verified_workiva_internal_fact",
      "source": "evaluation-validation-planner, citing Workiva internal GRC/Documents MCP integration test log"
    },
    {
      "claim": "Custom XBRL tagging template was NOT tested during the eval window; POC scope excluded it.",
      "classification": "open_question_validation_required",
      "source": "evaluation-validation-planner (pasted input)"
    },
    {
      "claim": "Unknown — requires validation. Whether an RFP response/commitment set exists for this account.",
      "classification": "open_question_validation_required",
      "source": "No rfp-security-analysis output was provided for this run."
    }
  ],
  "open_questions": [
    "Confirm the exact AE commitment language for the custom XBRL tagging template and reconcile the classification conflict between gong-discovery-analysis and technical-discovery-planner.",
    "Confirm delivery timeline for the custom XBRL tagging template against Acme's stated Q1 board cycle.",
    "Confirm whether an rfp-security-analysis output exists for this account and, if so, incorporate it into a revised packet."
  ],
  "read_only": true
}
```
