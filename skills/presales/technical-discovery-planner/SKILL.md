---
name: technical-discovery-planner
description: "Generates a tailored technical-discovery call agenda and question set for a Workiva Solution/Value Consultant, organized by Current State, Requirements, Technical Fit, and Risks/Blockers. Consumes existing account-opportunity-brief and/or gong-discovery-analysis outputs (or raw pasted context) to produce qualification questions on current tooling/process, integration/security requirements, stakeholder technical concerns, and success-criteria signals, each tagged with an evidence classification and citation. Use when the user says: 'build a technical discovery agenda for [account]', 'what should I ask on the technical call', 'prep discovery questions for [opportunity]', 'help me plan the tech deep-dive with [account]', or 'what are the open technical questions for [opportunity]'."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Technical Discovery Planner

Builds a structured, evidence-tagged technical-discovery agenda for an upcoming Workiva Solution/Value Consultant (SC/VC) call. The output is a question set organized by discovery topic — not a generic discovery template — grounded in whatever account/opportunity evidence already exists, with explicit flags on where evidence is missing and the question exists purely to close that gap.

This skill is part of the Workiva presales skill family. It shares conventions with:

- `../core-presales-intelligence/SKILL.md` — shared presales conventions, tone, and orchestration patterns.
- `../shared/evidence-schema.md` — the evidence classification taxonomy and handoff JSON schema referenced throughout this file.

## 1. Purpose & Trigger Phrases

**Purpose:** Given everything known about an account/opportunity, produce a technical-discovery call agenda that qualifies:
- Current tooling/process (what the prospect uses today, and its pain points)
- Integration/security requirements (SSO, API, data residency, IT security review posture)
- Stakeholder technical concerns (who on the technical/IT side needs to be satisfied, and about what)
- Success-criteria signals (what "technically won" looks like to this prospect)

**Trigger phrases** (non-exhaustive — use judgment for close paraphrases):
- "build a technical discovery agenda for [account]"
- "what should I ask on the technical call"
- "prep discovery questions for [opportunity]"
- "help me plan the tech deep-dive with [account]"
- "what are the open technical questions for [opportunity]"
- "generate a discovery call agenda"

## 2. Required / Optional Inputs

**Required (at least one of):**
- Account or opportunity name, AND/OR
- A pasted `account-opportunity-brief` output, AND/OR
- A pasted `gong-discovery-analysis` output

At minimum the skill needs *something* to ground questions in — a bare account name with zero other context should trigger the gap-filling behavior in Section 3 and produce a heavily-flagged, hypothesis-driven agenda rather than a fabricated one.

**Optional:**
- Known product line(s) of interest (e.g., Wdesk, ESG, Controls Management, Financial Reporting)
- Known competitor(s) currently in evaluation
- Prior `gong-discovery-analysis` output (call transcript themes, stated pains, stakeholder quotes)
- Named stakeholders and their roles (especially technical/IT-side contacts)
- Known deal stage / timeline constraints

## 3. Source Retrieval Guidance (Tool-Agnostic)

This skill is a **synthesis** skill, not a data-fetching skill. It should primarily work from context already assembled by upstream skills:

1. Prefer a pasted `account-opportunity-brief` output as the primary source of account/opportunity facts.
2. Prefer a pasted `gong-discovery-analysis` output as the primary source of prospect-stated pains, quotes, and stakeholder concerns.
3. If neither is provided, or if either leaves clear gaps relevant to the four discovery topics, this skill **may optionally** call read-only Salesforce MCP tools to fill gaps:
   - `search_opportunities` — to confirm opportunity name, stage, product line(s), close date.
   - `retrieve_semantic_model` — to understand what fields/objects are available before querying further.
   - Do not call any write/create/update Salesforce tool. This skill never mutates CRM data.
4. If no upstream brief exists and no MCP tool is available or authorized in the current session, proceed with whatever raw input the user pasted and mark every unverified claim per the fallback strings in Section 9. Do not fabricate account facts to fill gaps — fabricate only the synthetic worked example in Section 11.

## 4. Step-by-Step Workflow

1. **Ingest inputs.** Read the account/opportunity name, any pasted brief/analysis, and optional inputs (product line, competitor, stakeholders).
2. **Extract known facts, pains, and gaps.** Build three working lists:
   - Confirmed facts (with source tag)
   - Stated pains/quotes (with source tag)
   - Explicit gaps — topics required for the four sections where no evidence exists yet
3. **Fill gaps (optional).** If gaps are material and a read-only Salesforce lookup is available/authorized, call `search_opportunities` and/or `retrieve_semantic_model` to close them. Otherwise leave the gap explicit.
4. **Draft questions per section.** For each of the four sections (Current State, Requirements, Technical Fit, Risks/Blockers), draft 3–6 questions. Every question must trace to either:
   - A specific fact/pain from the brief or Gong analysis (cite it), or
   - An explicit gap this call needs to close (flag `open_question_validation_required: true`)
5. **Classify each question's justification** using the shared evidence taxonomy (Section 5).
6. **Deduplicate across sections.** A question addressing integration architecture belongs in Technical Fit, not Requirements and Technical Fit both — check for overlap and merge/move as needed.
7. **Run the quality checklist** (Section 7) before finalizing.
8. **Emit the agenda** in the output schema (Section 6) plus the MCP/demo-adapter handoff payload (Section 10).

## 5. Source Classification & Citation Rules

Apply the shared evidence taxonomy from `../shared/evidence-schema.md` to the **justification** of every generated question (i.e., why we're asking it / what evidence prompted it) — not to the question text itself:

| Classification | Applies when the justification is... |
|---|---|
| `confirmed_customer_statement` | A direct quote or paraphrase from the prospect (e.g., from a Gong call, email, or brief that cites the customer directly) |
| `salesforce_operating_context` | Drawn from CRM fields — stage, product line, opportunity amount, close date, account industry, etc. |
| `verified_workiva_internal_fact` | A Workiva-side fact independently verifiable (e.g., product capability, integration availability, security cert status) |
| `inference_working_hypothesis` | A reasonable inference from available signals, not directly stated by anyone |
| `open_question_validation_required` | No evidence exists yet — the question exists specifically to close this gap on the call |
| `risk_assumption_dependency` | Justification depends on an assumption that, if wrong, changes deal risk materially |

Every question in the output must carry exactly one classification tag. Questions whose justification is `open_question_validation_required` must also carry the boolean flag `open_question_validation_required: true` in the output schema (Section 6) — the tag and the flag are related but the flag is what downstream tooling filters on.

## 6. Output Schema

Emit the agenda as both human-readable markdown and the structured object below (the structured object is also embedded in the handoff payload in Section 10).

```json
{
  "account": "string",
  "opportunity": "string | null",
  "generated_from": ["account-opportunity-brief", "gong-discovery-analysis", "salesforce-lookup", "user-provided-context"],
  "sections": [
    {
      "section": "Current State",
      "questions": [
        {
          "question": "string",
          "justification": "string — what evidence or gap prompted this question",
          "evidence_classification": "confirmed_customer_statement | salesforce_operating_context | verified_workiva_internal_fact | inference_working_hypothesis | open_question_validation_required | risk_assumption_dependency",
          "open_question_validation_required": false
        }
      ]
    },
    { "section": "Requirements", "questions": [ "..." ] },
    { "section": "Technical Fit", "questions": [ "..." ] },
    { "section": "Risks/Blockers", "questions": [ "..." ] }
  ]
}
```

Sections are fixed: **Current State, Requirements, Technical Fit, Risks/Blockers** — always in this order, each with 3–6 questions.

## 7. Quality Checklist

Before finalizing the agenda, confirm:

- [ ] No duplicate or near-duplicate questions across sections.
- [ ] Every question ties back to a stated pain point, a confirmed fact, or an explicit gap — none are generic filler unconnected to this account.
- [ ] Every question has exactly one evidence classification tag, and `open_question_validation_required` questions are flagged `true`.
- [ ] Questions requiring product/engineering input to answer on Workiva's side (not just the prospect's) are explicitly called out in a short "needs internal follow-up" note.
- [ ] Each section has 3–6 questions — no section is empty, none exceeds 6.
- [ ] Nothing presented as a confirmed fact is actually an assumption — check every `verified_workiva_internal_fact` and `salesforce_operating_context` tag against its actual source.

## 8. Read-Only Disclaimer

This skill is **read-only and non-authoritative**. It does not create, update, or delete any record in Salesforce, Gong, or any other system. Any Salesforce lookups it performs (Section 3) are read-only queries used solely to fill informational gaps. All outputs are planning aids for the SC/VC to prepare a call — they are not a substitute for validating requirements directly with the prospect, and nothing in this output should be treated as a committed technical or contractual position without Workiva-source validation.

## 9. Fallback Strings

Use these exact strings whenever a value cannot be confirmed:

- `"Unknown — requires validation."` — for any fact that is simply unavailable.
- `"Requires Workiva-source validation."` — for any claim about Workiva product/security/integration capability that isn't independently verified in this session.

## 10. MCP/Demo-Adapter Handoff Payload

Emit this JSON block at the end of every run so downstream tooling (notably the demo-framework-adapter, which uses discovery topics to decide what to show in a follow-on demo) can consume it directly. Structure follows `../shared/evidence-schema.md`.

```json
{
  "handoff_target": "demo-framework-adapter",
  "source_skill": "technical-discovery-planner",
  "account": "string",
  "opportunity": "string | null",
  "generated_at": "ISO-8601 timestamp",
  "evidence_taxonomy_version": "see ../shared/evidence-schema.md",
  "discovery_agenda": {
    "sections": [
      { "section": "Current State", "questions": [ "...as in Section 6 schema..." ] },
      { "section": "Requirements", "questions": [ "..." ] },
      { "section": "Technical Fit", "questions": [ "..." ] },
      { "section": "Risks/Blockers", "questions": [ "..." ] }
    ]
  },
  "open_questions_requiring_validation": [
    "list of question strings where open_question_validation_required == true"
  ],
  "internal_follow_up_needed": [
    "list of question strings flagged as needing product/engineering input"
  ],
  "disclaimer": "Read-only planning aid. Not a substitute for direct validation. Requires Workiva-source validation where noted."
}
```

## 11. Worked Example — Acme Test Corp (Fully Synthetic)

> All names, quotes, and figures below are fabricated for illustration only.

**Inputs assumed:**
- Account: Acme Test Corp (fictional mid-market insurance company)
- Opportunity: "Acme Test Corp — Financial Close & ESG Reporting, FY26"
- Pasted `account-opportunity-brief` excerpt: stage = Technical Validation, product line of interest = Financial Reporting + ESG, competitor = Workday Adaptive (mentioned once, unconfirmed strength)
- Pasted `gong-discovery-analysis` excerpt: CFO quoted saying *"our close process still lives in about 40 linked spreadsheets and every quarter someone finds a broken formula"*; IT contact (name unconfirmed) raised a question about SSO in a follow-up email thread, unconfirmed if resolved

**Generated Agenda:**

```json
{
  "account": "Acme Test Corp",
  "opportunity": "Acme Test Corp — Financial Close & ESG Reporting, FY26",
  "generated_from": ["account-opportunity-brief", "gong-discovery-analysis"],
  "sections": [
    {
      "section": "Current State",
      "questions": [
        {
          "question": "Walk us through the current close process end-to-end — which of the ~40 linked spreadsheets are the highest-risk (most manual, most error-prone)?",
          "justification": "CFO stated close process 'lives in about 40 linked spreadsheets' with recurring broken-formula incidents.",
          "evidence_classification": "confirmed_customer_statement",
          "open_question_validation_required": false
        },
        {
          "question": "Who owns the spreadsheet consolidation today, and how much time per close cycle does that role spend on manual reconciliation?",
          "justification": "Inferred follow-up to quantify the pain already confirmed by the CFO quote.",
          "evidence_classification": "inference_working_hypothesis",
          "open_question_validation_required": false
        },
        {
          "question": "Is there an incumbent reporting/EPM tool in place today beyond spreadsheets, and if so, what triggered this evaluation?",
          "justification": "No incumbent tool is confirmed in the brief or Gong analysis — needed to size the actual competitive displacement.",
          "evidence_classification": "open_question_validation_required",
          "open_question_validation_required": true
        },
        {
          "question": "How is ESG data currently collected and by whom, given ESG Reporting is a named product line of interest?",
          "justification": "Opportunity brief lists ESG as a product line of interest but gives no detail on current ESG data process.",
          "evidence_classification": "salesforce_operating_context",
          "open_question_validation_required": false
        }
      ]
    },
    {
      "section": "Requirements",
      "questions": [
        {
          "question": "What SSO/identity provider does Acme Test Corp standardize on, and is there a hard security requirement for SSO at go-live?",
          "justification": "IT contact raised an SSO question in a follow-up email thread; resolution status unconfirmed.",
          "evidence_classification": "open_question_validation_required",
          "open_question_validation_required": true
        },
        {
          "question": "Are there data residency or industry-specific compliance requirements (e.g., state insurance regulatory data handling) we need to design around?",
          "justification": "Inferred from account industry (insurance) — no explicit requirement confirmed yet.",
          "evidence_classification": "inference_working_hypothesis",
          "open_question_validation_required": false
        },
        {
          "question": "What source systems need to feed the close/reporting workflow via API or file integration (GL, sub-ledgers, ESG data sources)?",
          "justification": "Required to scope Technical Fit but not yet described in the brief or Gong analysis.",
          "evidence_classification": "open_question_validation_required",
          "open_question_validation_required": true
        },
        {
          "question": "Does Acme Test Corp's IT security review process require a SOC 2 report or a formal security questionnaire before technical validation can close?",
          "justification": "Common Workiva IT-security-review dependency for mid-market financial services accounts; Workiva SOC 2 posture is independently verifiable.",
          "evidence_classification": "verified_workiva_internal_fact",
          "open_question_validation_required": false
        }
      ]
    },
    {
      "section": "Technical Fit",
      "questions": [
        {
          "question": "How would the proposed Financial Reporting workflow map onto the existing close calendar — where are the hard deadlines that can't slip during migration?",
          "justification": "Deal stage is Technical Validation per Salesforce — implies a migration/cutover plan needs to be technically credible now.",
          "evidence_classification": "salesforce_operating_context",
          "open_question_validation_required": false
        },
        {
          "question": "If Workday Adaptive is genuinely in evaluation, what specific technical capability is it being compared on (planning depth, reporting, ESG)?",
          "justification": "Competitor mentioned once in the brief but strength/relevance to this deal is unconfirmed.",
          "evidence_classification": "risk_assumption_dependency",
          "open_question_validation_required": true
        },
        {
          "question": "What level of formula/logic complexity exists in the current spreadsheet models that would need to be reproduced or re-architected in Workiva?",
          "justification": "Directly follows from the CFO's 'broken formula' quote — needed to size technical migration effort.",
          "evidence_classification": "confirmed_customer_statement",
          "open_question_validation_required": false
        },
        {
          "question": "Who are the technical stakeholders (beyond the CFO) who need to sign off on the integration architecture, and what are their specific concerns?",
          "justification": "An IT contact exists in the email thread but is not confirmed as a formal stakeholder in the brief.",
          "evidence_classification": "open_question_validation_required",
          "open_question_validation_required": true
        }
      ]
    },
    {
      "section": "Risks/Blockers",
      "questions": [
        {
          "question": "Is there a hard external reporting deadline (e.g., regulatory ESG disclosure date) driving the FY26 timeline, and what happens if implementation slips past it?",
          "justification": "ESG Reporting is a named product line; regulatory deadlines are a common hidden driver not yet confirmed.",
          "evidence_classification": "inference_working_hypothesis",
          "open_question_validation_required": false
        },
        {
          "question": "Has budget been formally allocated for this initiative, or is it still pending internal approval?",
          "justification": "No budget confirmation present in the opportunity brief — material to deal risk if unconfirmed.",
          "evidence_classification": "risk_assumption_dependency",
          "open_question_validation_required": true
        },
        {
          "question": "Are there any prior failed technology implementations at Acme Test Corp that could create internal skepticism we need to address directly?",
          "justification": "Not addressed in brief or Gong analysis; common hidden blocker worth surfacing directly.",
          "evidence_classification": "open_question_validation_required",
          "open_question_validation_required": true
        },
        {
          "question": "Does IT security review (SOC 2 / questionnaire) have a known turnaround time at Acme Test Corp that could affect the close timeline?",
          "justification": "Follows directly from the Requirements-section SOC 2 question — flagged here as a timeline risk, not just a requirement.",
          "evidence_classification": "verified_workiva_internal_fact",
          "open_question_validation_required": false
        }
      ]
    }
  ]
}
```

**Internal follow-up needed:** the Workday Adaptive competitive-technical-fit question and the SSO/identity-provider requirement both likely need input from Workiva product/solutions engineering to answer with confidence beyond "Requires Workiva-source validation."
