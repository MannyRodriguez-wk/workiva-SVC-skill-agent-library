---
name: gong-discovery-analysis
description: "Analyzes Gong call recordings and transcripts tied to a Salesforce account or opportunity to produce a structured discovery-call intelligence report — key themes, stated pain points, competitive mentions, buying-committee signals, objections raised, and open questions still needing validation. Use when a Solution/Value Consultant asks things like 'analyze Gong calls for Acme Corp', 'what pain points came up on the discovery call', 'summarize Gong for this deal', 'what objections has the prospect raised', 'who's involved in the buying committee based on our calls', or 'pull discovery intel before I build the demo/value case'. Read-only — never writes back to Gong, Salesforce, or any other system."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Gong Discovery Call Analysis

Turn raw Gong call data into a structured, evidence-tagged discovery brief a Solution/Value Consultant (SC/VC) can use to prep a demo, build a value hypothesis, or brief an AE — without re-listening to every call.

This skill is one of nine sibling presales skills. It shares conventions with, and assumes familiarity with:

- [`../core-presales-intelligence/SKILL.md`](../core-presales-intelligence/SKILL.md) — the evidence classification taxonomy and general presales-intelligence conventions used across all skills in this library.
- [`../shared/evidence-schema.md`](../shared/evidence-schema.md) — the shared handoff JSON schema used to pass structured output to downstream MCP/demo-building adapters.

If those files are not yet present in your checkout, treat the classification and handoff format below as the authoritative interim spec — they are written to match those documents exactly once they land.

## 1. Purpose & Trigger Phrases

Invoke this skill when an SC/VC needs to extract and structure what actually happened on discovery/discussion calls for a specific account or deal, rather than manually reviewing Gong. Typical trigger phrases:

- "Analyze Gong calls for [account name]"
- "What pain points came up on the discovery call with [account]?"
- "Summarize Gong for this deal"
- "What objections has [account] raised so far?"
- "Who's on the buying committee for [account] based on our calls?"
- "Pull discovery intel on [account] before I build the demo"
- "What competitors have come up in calls with [account]?"

Do not invoke this skill for: scheduling calls, updating Gong data, editing Salesforce records, or any call analysis that requires listening to audio not indexed in Gong (flag those as `open_question_validation_required` instead).

## 2. Inputs

**Required** (at least one of):
- Account name (as it appears in Salesforce/Gong), or
- Salesforce Account ID

**Optional** (narrows or enriches the analysis):
- Specific Opportunity ID or name (scopes analysis to one deal rather than the full account history)
- Date range (e.g. "calls from the last 60 days")
- Specific Gong call ID(s), if the user already knows which call(s) matter
- Named stakeholders to focus on (e.g. "what did the CFO say about timeline")

If only a loosely-remembered account name is given, resolve it against Salesforce or Gong's own account matching before proceeding, and note the resolution step in the output. If the account cannot be resolved with confidence, stop and report `"Unknown — requires validation."` rather than guessing.

## 3. Source Retrieval: Gong MCP Tools

The Gong MCP is the source of truth for all call-derived claims in this skill's output. Three tools are available; use them for distinct purposes and prefer the narrowest tool that answers the question:

| Tool | What it returns | When to use it |
| --- | --- | --- |
| **Ask Account** | Account-level synthesis across all Gong-indexed calls for a given account — cross-call themes, recurring stakeholders, overall sentiment trends. | Start here when the request is account-wide ("summarize Gong for this account") or when no specific opportunity/call was given. |
| **Ask Deal** | Deal/opportunity-scoped synthesis — themes, pain points, and signals specific to one Salesforce opportunity, filtered to calls tagged against that deal. | Use when the user names a specific opportunity, or after Ask Account when you need to narrow to one active deal. |
| **Generate Brief** | A structured pre-built call/deal brief (Gong's own summarization), useful as a cross-check or starting skeleton, and often includes verbatim quote snippets with speaker attribution. | Use to sanity-check themes pulled via Ask Account/Ask Deal, and as the primary source for verbatim quotes since it preserves speaker attribution more reliably than free-form Q&A. |

Do not fabricate call content. If a tool call returns no data, empty results, or an error, record that explicitly in the output (see Fallback Strings, §9) rather than inferring what a call "probably" contained.

## 4. Step-by-Step Workflow

1. **Resolve the account/opportunity.** Confirm the account name or ID; if an opportunity was named, confirm it belongs to that account.
2. **Retrieve account-level context.** Call Gong `Ask Account` for the resolved account to get the broad landscape of themes, stakeholders, and sentiment.
3. **Narrow to deal-level detail, if applicable.** If an opportunity was specified (or one active deal clearly dominates), call Gong `Ask Deal` for that opportunity to get deal-specific pain points, objections, and timeline signals.
4. **Pull a structured brief.** Call Gong `Generate Brief` to cross-check the themes surfaced above and to source verbatim quotes with speaker attribution where available.
5. **Extract and bucket findings** into the five output categories: key themes, pain points, competitive mentions, buying-committee signals, objections. Every extracted item gets a source note (which tool/call it came from) and a classification tag (§5).
6. **Identify gaps.** Explicitly list what none of the three Gong tools covered — unaddressed stakeholders, unanswered budget/timeline questions, topics the user asked about that never came up on any indexed call. These become the "open questions" section.
7. **Cross-reference Salesforce operating context if available** (e.g. opportunity stage, close date, named competitor field) to tag items as `salesforce_operating_context` rather than inferring them from Gong alone.
8. **Assemble the output** using the schema in §6, run the quality checklist in §7, and emit the handoff JSON in §10.
9. **Never write anything back.** This skill only reads Gong/Salesforce data and returns a report (§8).

## 5. Source Classification & Citation Rules

Every extracted claim in the output **must** carry exactly one evidence classification, using the taxonomy defined in [`../core-presales-intelligence/SKILL.md`](../core-presales-intelligence/SKILL.md):

- `confirmed_customer_statement` — something a prospect/customer stakeholder said directly on a Gong-indexed call, ideally with a verbatim or near-verbatim quote and speaker attribution.
- `salesforce_operating_context` — factual metadata pulled from Salesforce (stage, amount, close date, named competitor field, etc.), not from the call itself.
- `verified_workiva_internal_fact` — a Workiva-side fact (product capability, roadmap status, pricing) that has been independently confirmed against a Workiva-internal source, not merely asserted.
- `inference_working_hypothesis` — a conclusion the analyst (skill) drew by connecting multiple signals, not something anyone stated outright. Must be labeled as a hypothesis, not fact.
- `open_question_validation_required` — something Gong/Salesforce does not clearly answer and must be confirmed with the account team or the prospect directly.
- `risk_assumption_dependency` — a stated or implied condition that, if false, would undermine the deal or the value case (e.g. "assumes budget is already approved for FY27").

A claim with no classification tag is not valid output — regenerate it or move it to open questions.

**Example tagged claims:**

1. *"The VP of Finance said their current close process takes 9 business days and that's 'the single biggest thing slowing down our audit committee reporting.'"* → `confirmed_customer_statement` (Gong call, 2026-08-14, Ask Deal — speaker: VP Finance)
2. *"Given two separate calls mentioned a Q1 board deadline, this deal likely needs to close before end of Q4 to hit that timeline."* → `inference_working_hypothesis` (derived from Ask Account + Ask Deal synthesis, not directly stated by any single speaker)

## 6. Output Schema

Return the analysis as a markdown report with the following structure. Every row must carry an evidence classification from §5.

### 6.1 Summary Table

| Category | Item | Evidence Classification | Source (tool / call date / speaker) |
| --- | --- | --- | --- |
| Key Theme | ... | ... | ... |
| Pain Point | ... | ... | ... |
| Competitive Mention | ... | ... | ... |
| Buying-Committee Signal | ... | ... | ... |
| Objection | ... | ... | ... |
| Open Question | ... | ... | ... |

### 6.2 Equivalent JSON form (for programmatic consumption)

```json
{
  "account": "string",
  "opportunity_id": "string | null",
  "analysis_date": "YYYY-MM-DD",
  "themes": [
    { "text": "string", "classification": "confirmed_customer_statement", "source": "string" }
  ],
  "pain_points": [
    { "text": "string", "classification": "confirmed_customer_statement", "source": "string" }
  ],
  "competitive_mentions": [
    { "text": "string", "classification": "confirmed_customer_statement", "source": "string" }
  ],
  "buying_committee_signals": [
    { "text": "string", "classification": "inference_working_hypothesis", "source": "string" }
  ],
  "objections": [
    { "text": "string", "classification": "confirmed_customer_statement", "source": "string" }
  ],
  "open_questions": [
    { "text": "string", "classification": "open_question_validation_required", "source": "string" }
  ]
}
```

## 7. Quality Checklist

Before returning output, verify:

- [ ] Every extracted claim carries exactly one evidence classification from the shared taxonomy.
- [ ] No quote is fabricated or paraphrased into a false verbatim — anything not word-for-word from a Gong source is marked as paraphrase or reclassified as `inference_working_hypothesis`.
- [ ] Every claim cites its source tool (Ask Account / Ask Deal / Generate Brief) and, where available, call date and speaker.
- [ ] Gaps are explicit — anything the user asked about that Gong didn't cover is listed under Open Questions with `open_question_validation_required`, not silently omitted.
- [ ] No Salesforce or Workiva-internal fact is asserted without being tagged `salesforce_operating_context` or `verified_workiva_internal_fact` respectively; unverified Workiva claims use the fallback string in §9.
- [ ] The handoff JSON (§10) validates against the shared evidence schema shape and has a `handoff_target` set.

## 8. Read-Only Disclaimer

This skill is **strictly read-only**. It never writes, updates, or deletes any record in Gong, Salesforce, or any other connected system. It does not create tasks, log notes, update opportunity fields, or post comments anywhere. Its only output is a structured report and handoff payload for downstream human review or another tool to consume.

## 9. Fallback Strings

Use these exact strings when data is unavailable — do not paraphrase them:

- `"Unknown — requires validation."` — use when Gong (or Salesforce) simply has no data covering a requested item (e.g. no calls mention budget authority).
- `"Requires Workiva-source validation."` — use when a claim depends on a Workiva-internal fact (product capability, roadmap, pricing) that hasn't been independently confirmed against a Workiva-internal source.

## 10. MCP / Demo-Adapter Handoff Payload

End every run with a handoff JSON block matching the shared schema at [`../shared/evidence-schema.md`](../shared/evidence-schema.md). Set `handoff_target` to `workiva-mcp-adapter` when the downstream consumer is a live Salesforce/Gong-connected workflow, `demo-framework-adapter` when the output feeds a demo-building skill, or both when the analysis should feed both.

```json
{
  "skill": "gong-discovery-analysis",
  "handoff_target": ["workiva-mcp-adapter", "demo-framework-adapter"],
  "account": "string",
  "opportunity_id": "string | null",
  "analysis_date": "YYYY-MM-DD",
  "evidence_items": [
    {
      "category": "theme | pain_point | competitive_mention | buying_committee_signal | objection | open_question",
      "text": "string",
      "classification": "confirmed_customer_statement | salesforce_operating_context | verified_workiva_internal_fact | inference_working_hypothesis | open_question_validation_required | risk_assumption_dependency",
      "source": "string"
    }
  ],
  "gaps_identified": ["string"],
  "read_only": true
}
```

## 11. Fully Synthetic Example

The following is a fabricated, illustrative walkthrough only. "Acme Test Corp," all quotes, and all names below are fictional and used solely to demonstrate the workflow end to end.

**User request:** "Analyze Gong calls for Acme Test Corp — what came up on the discovery call?"

**Step 1-2 (resolve + Ask Account):** Gong `Ask Account` for "Acme Test Corp" returns synthesis across 3 indexed calls (2026-07-22, 2026-08-05, 2026-08-19), all tagged to one open opportunity, "Acme Test Corp — FY27 Reporting Platform Renewal."

**Step 3 (Ask Deal):** Gong `Ask Deal` for that opportunity surfaces recurring mentions of manual close-process pain and a named competitor, "Fictional Reporting Co."

**Step 4 (Generate Brief):** Gong `Generate Brief` for the 2026-08-05 call returns a verbatim snippet from "Jordan Lee, VP Finance (Acme Test Corp)."

**Step 5-7 (extract, bucket, cross-reference):**

### Summary Table

| Category | Item | Evidence Classification | Source |
| --- | --- | --- | --- |
| Key Theme | Acme's close process is largely manual, spread across spreadsheets and email approvals | confirmed_customer_statement | Ask Deal, 2026-08-05 |
| Pain Point | "Our close takes 9 business days and that's the single biggest thing slowing down our audit committee reporting." | confirmed_customer_statement | Generate Brief, 2026-08-05, speaker: Jordan Lee (VP Finance) |
| Competitive Mention | Prospect mentioned an active POC with "Fictional Reporting Co." | confirmed_customer_statement | Ask Deal, 2026-08-19 |
| Buying-Committee Signal | Both VP Finance and a Controller have appeared on calls; no CFO or IT stakeholder has appeared on any indexed call yet | inference_working_hypothesis | Ask Account synthesis (3 calls) |
| Objection | Prospect raised concern about migration effort from their current spreadsheet-based process | confirmed_customer_statement | Ask Deal, 2026-08-19 |
| Open Question | Whether budget has been formally approved for FY27 | open_question_validation_required | Not covered on any indexed call |
| Open Question | Whether IT/security stakeholders have been looped in | open_question_validation_required | Not covered on any indexed call |
| Salesforce Context | Opportunity stage: "Solution Validation," Close Date: 2026-11-30 | salesforce_operating_context | Salesforce opportunity record |

**Step 8-9 (assemble output, run checklist, no writes performed).**

### Handoff JSON

```json
{
  "skill": "gong-discovery-analysis",
  "handoff_target": ["workiva-mcp-adapter", "demo-framework-adapter"],
  "account": "Acme Test Corp",
  "opportunity_id": "FICTIONAL-OPP-0001",
  "analysis_date": "2026-09-16",
  "evidence_items": [
    {
      "category": "theme",
      "text": "Acme's close process is largely manual, spread across spreadsheets and email approvals.",
      "classification": "confirmed_customer_statement",
      "source": "Gong Ask Deal, call 2026-08-05"
    },
    {
      "category": "pain_point",
      "text": "\"Our close takes 9 business days and that's the single biggest thing slowing down our audit committee reporting.\"",
      "classification": "confirmed_customer_statement",
      "source": "Gong Generate Brief, call 2026-08-05, speaker: Jordan Lee (VP Finance)"
    },
    {
      "category": "competitive_mention",
      "text": "Active POC with \"Fictional Reporting Co.\" mentioned by prospect.",
      "classification": "confirmed_customer_statement",
      "source": "Gong Ask Deal, call 2026-08-19"
    },
    {
      "category": "buying_committee_signal",
      "text": "No CFO or IT stakeholder has appeared on any indexed call yet; VP Finance and Controller are the only confirmed participants.",
      "classification": "inference_working_hypothesis",
      "source": "Gong Ask Account synthesis across 3 calls"
    },
    {
      "category": "objection",
      "text": "Concern raised about migration effort from current spreadsheet-based process.",
      "classification": "confirmed_customer_statement",
      "source": "Gong Ask Deal, call 2026-08-19"
    },
    {
      "category": "open_question",
      "text": "Unknown — requires validation. Whether FY27 budget has been formally approved.",
      "classification": "open_question_validation_required",
      "source": "Not covered on any indexed Gong call"
    },
    {
      "category": "open_question",
      "text": "Unknown — requires validation. Whether IT/security stakeholders have been looped in.",
      "classification": "open_question_validation_required",
      "source": "Not covered on any indexed Gong call"
    }
  ],
  "gaps_identified": [
    "No IT/security stakeholder present on any indexed call.",
    "No explicit budget confirmation on any indexed call."
  ],
  "read_only": true
}
```
