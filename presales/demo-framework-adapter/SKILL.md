---
name: demo-framework-adapter
description: "Adapter skill that translates the standard presales handoff JSON payload (per ../shared/evidence-schema.md), produced by upstream skills like account-opportunity-brief, gong-discovery-analysis, technical-discovery-planner, and evaluation-validation-planner, into a fully populated Workiva 'SC Demo Planning Document' — the internal CoM-Mantra-structured template Solution Consultants fill out to plan a live product demo narrative (Limbic Opening, Solution Demo Flow/tell-show-tell topics, Trap-Setting, Value Close, Customer Proof Points). This produces the demo NARRATIVE/SCRIPT plan, not a live MCP/connector execution — for that, see the /demo section of this repository. Primarily invoked automatically by other presales skills passing it a handoff payload, but can also be triggered directly by a user, e.g. 'build a demo planning doc from this discovery output', 'fill out the SC demo plan for [account]', 'turn this eval plan into a demo script', or 'draft the CoM mantra plan for [opportunity]'."
metadata:
  disable-model-invocation: true
  author: Manny Rodriguez-Lapido
  version: '2.0'
  license: MIT
---

# Demo Framework Adapter — SC Demo Planning Document Generator

An **adapter skill**, not a standalone user-facing analysis skill. It does not
gather new evidence and does not call any live connector itself. It consumes
the standard handoff JSON payload(s) already produced by upstream presales
skills and transforms them into a fully populated **SC Demo Planning
Document** — Workiva's internal template for planning a live demo's
narrative arc, built around the CoM (Concept of Message) Mantra: Limbic
Opening, a visual Solution Demo Flow of tell-show-tell topics, Trap-Setting
around Workiva Differentiators, and a Value Close.

**This is a narrative/script planning artifact, not a technical execution
plan.** It does not configure a demo org, provision synthetic data, or drive
any MCP/connector session. If you are looking for live demo *execution*
tooling (running an actual product walkthrough against connected systems),
see the `/demo` section elsewhere in this repository — that is a separate,
unrelated capability from this skill.

Because it is an adapter, `metadata.disable-model-invocation: true` is set —
it is not intended to be picked automatically by general model routing the
way an analysis skill would be. It is invoked explicitly, either by another
skill handing it a payload, or by a user directly asking for a demo plan.

This skill shares conventions with every other skill in `skills/presales/`.
See:

- [../core-presales-intelligence/SKILL.md](../core-presales-intelligence/SKILL.md)
  for the shared presales operating model, tone, and cross-skill handoff
  conventions.
- [../shared/evidence-schema.md](../shared/evidence-schema.md) for the full
  evidence classification taxonomy and the canonical handoff JSON schema
  referenced throughout this document.

## 1. Purpose & Trigger Phrases

**Purpose:** Generate a filled-out SC Demo Planning Document — the CoM
Mantra structure below — from upstream presales-skill outputs, so an SC
walks into demo prep with every template field already populated and traced
to a specific piece of evidence, rather than staring at a blank form. This
skill specifically maps:

- `account-opportunity-brief` → account/opportunity identity and Priority
  Value Driver(s).
- `gong-discovery-analysis` (and any discovery narrative embedded in
  `technical-discovery-planner`) → Before Scenarios & Negative Consequences.
- `technical-discovery-planner` → Required Capabilities and the topics that
  populate the Solution Demo Flow.
- `evaluation-validation-planner` → Metrics (the measurable "pass"
  criteria the demo should visibly move toward).

It never invents a pain point, capability, metric, or differentiator that
isn't traceable to one of these inputs (or to something the user explicitly
supplies in the current conversation).

**Primary invocation mode:** automatic, as the terminal step of another
skill's workflow. Upstream skills that are expected to hand off to this
skill include (non-exhaustive):

- `account-opportunity-brief`
- `gong-discovery-analysis`
- `technical-discovery-planner`
- `evaluation-validation-planner`

**Secondary invocation mode — direct user trigger phrases** (non-exhaustive;
match on intent, not exact wording):

- "Build a demo planning doc from this discovery output."
- "Fill out the SC Demo Plan for [account]."
- "What should my Limbic Opening be for [account]?"
- "Turn this eval plan into a demo script."
- "Draft the CoM Mantra plan for [opportunity]."
- "Given this handoff payload, what's my Solution Demo Flow?"

If a user invokes this skill directly without an existing handoff payload,
ask them to either paste/attach the JSON payload from an upstream skill, or
run the relevant upstream skill first (e.g. `technical-discovery-planner`)
so this skill has traceable evidence to work from. Do not proceed on an
unsourced verbal description of "what the customer cares about" — that must
first be captured and classified upstream.

## 2. Required / Optional Inputs

**Required:**

- One or more handoff JSON payloads (per
  [../shared/evidence-schema.md](../shared/evidence-schema.md)) produced by
  upstream presales skills — most commonly `account-opportunity-brief`,
  `gong-discovery-analysis`, `technical-discovery-planner`, and/or
  `evaluation-validation-planner`. Each payload's `evidence[]` and
  `open_questions[]` entries are the raw material for this skill's output.

**Optional:**

- The name of the seller(s) working the opportunity alongside the SC (fills
  the "Seller(s)" template field). If not supplied, use the fallback string.
- A list of Workiva Differentiators the user wants considered for
  Trap-Setting (see Section 3 — this skill never invents its own list).
- Named Customer Proof Points (case studies, reference customers, published
  results) the user wants included. If not supplied, the Customer Proof
  Points section uses the fallback string rather than a fabricated proof
  point.
- A stated time budget or audience constraint for the demo — used to help
  prioritize which Solution Demo Flow topics make the final sequence, not to
  change which pain points/capabilities are covered.

If multiple upstream payloads are supplied for the same opportunity, merge
their `evidence[]` entries into a single deduplicated set before building
the plan, preserving each item's original evidence classification and
source skill.

## 3. Tool-Agnostic Source Retrieval Guidance

This skill does **not** call any live connector (Salesforce, Gong, or
otherwise) and does **not** provision or execute a demo environment. All of
its input is the already-gathered, already-classified evidence contained in
the upstream handoff payload(s). Its only job is transformation into the SC
Demo Planning Document template, not retrieval.

**Workiva Differentiators are a live, curated internal list this skill does
not have hardcoded** and must never invent. To populate the Trap-Setting
section, this skill must either:

1. Ask the user to supply the differentiator(s) relevant to this deal (e.g.
   "which Workiva differentiator(s) do you want to use to expand Required
   Capabilities/Metrics for this opportunity?"), or
2. If none are supplied, leave the field populated with the fallback string
   `"Requires Workiva-source validation."` and flag it as a missing element
   in Presentation Planning — never substitute a plausible-sounding but
   unconfirmed differentiator.

The same discipline applies to Customer Proof Points: only include a proof
point the user supplies or that already appears, cited, in an upstream
payload's `evidence[]`. Never fabricate a case study, statistic, or
reference customer.

## 4. Step-by-Step Workflow

1. **Ingest and validate the payload(s).** Confirm each input JSON payload
   conforms to [../shared/evidence-schema.md](../shared/evidence-schema.md).
   If a payload is malformed or missing required fields, surface that
   explicitly rather than guessing its content.
2. **Deduplicate and merge.** If multiple upstream payloads cover the same
   opportunity/account, merge overlapping evidence, keeping the strongest
   (most directly sourced) evidence classification and citing all
   contributing source skills.
3. **Populate header fields.** Pull `Customer/Opportunity Name` from
   `account-opportunity-brief` (account/opportunity identity fields). Pull
   `Priority Value Driver(s)` from the same source's stated value drivers or
   product-fit notes; if none are stated, use the fallback string and flag
   it in Presentation Planning as a missing element. `Your Name` and
   `Seller(s)` come from the current user/conversation context, not from any
   upstream payload — ask if not supplied.
4. **Draft Presentation Planning.** Summarize, in the SC's own framing, how
   discovery evidence (across all merged payloads) will shape the demo, and
   explicitly enumerate any template field below that has no supporting
   evidence — do not silently leave a gap unflagged.
5. **Populate Before Scenarios & Negative Consequences.** Pull from
   `gong-discovery-analysis` pain points/objections (and any discovery
   narrative embedded in a `technical-discovery-planner` payload). Each
   scenario must cite the specific `evidence[]` entry it traces to.
6. **Populate After Scenarios & Positive Business Outcomes.** Pull from the
   same discovery evidence where the customer or SC has articulated a
   desired future state; where only the "before" is stated, mark the
   "after" as `inference_working_hypothesis` and flag it for validation.
7. **Populate Required Capabilities.** Pull from `technical-discovery-planner`
   requirement/technical-fit findings. Each capability must trace to a
   specific evidence entry.
8. **Populate Metrics.** Pull from `evaluation-validation-planner` success
   criteria (the "what does pass look like" table). Each metric must trace
   to a specific success-criterion entry, carrying that entry's evidence
   classification.
9. **Draft the Limbic Opening.** Choose exactly one Limbic Opening type
   (Illustrative Analogy, Industry Insight, Discovery Findings, Case Study,
   Other) grounded in the merged evidence, and describe what will be on
   screen. If grounded only in discovery findings, classify as whatever the
   underlying discovery evidence is classified as (typically
   `confirmed_customer_statement`).
10. **Build the Solution Demo Flow.** For each Required Capability (or
    cluster of related capabilities) identified in step 7, draft one topic
    row: Product/Solution Feature, customer-language Topic Name, the
    closing operational benefit connecting the capability to a Positive
    Business Outcome from step 6, and an Executive Impact (PSI) classified
    against exactly one of the four lenses in Section 4a. Sequence topics
    into a coherent tell-show-tell roadmap.
11. **Draft Trap-Setting.** Per Section 3, only populate with
    user-supplied or already-cited Workiva Differentiators; otherwise use
    the fallback string.
12. **Draft the Value Close.** Summarize how the demo closes back to the
    seller, referencing which Mantra elements were used.
13. **Populate Customer Proof Points.** Per Section 3, only from
    user-supplied or already-cited proof points.
14. **Classify every populated field's source claim** using the shared
    evidence taxonomy (Section 5). Any field with no available basis must
    use a fallback string per Section 9, never be silently omitted.
15. **Assemble the SC Demo Planning Document** per the schema in Section 6.
16. **Run the quality checklist** (Section 7) before returning the plan.
17. **Emit the output payload** (Section 10) for logging/consistency, noting
    `handoff_target: none` since this is a terminal adapter skill.

### 4a. Executive Impact (PSI) Lens Classification

Every Solution Demo Flow topic's "Executive Impact" must be classified
against **exactly one** of these four lenses — never a fifth, invented
lens:

| Lens | Use when the topic's executive-level payoff is... |
|---|---|
| Drive Growth | Enabling revenue expansion, new market/product entry, faster deal/reporting cycles that unlock growth |
| Drive Efficiency | Reducing manual effort, cycle time, headcount burden, or process cost |
| Improve Customer Experience | Improving the experience of the customer's own downstream customers, employees, or internal stakeholders consuming the output |
| Mitigate Risk | Reducing audit/compliance/security/error exposure |

If a topic plausibly spans two lenses, pick the lens most directly supported
by the underlying evidence (e.g. a stated customer pain about audit findings
→ Mitigate Risk, even if efficiency also improves as a side effect) and note
the secondary lens as a parenthetical, not a second classification.

## 5. Source Classification & Citation Rules

Use the shared evidence taxonomy defined in
[../shared/evidence-schema.md](../shared/evidence-schema.md). Every Before
Scenario, After Scenario, Required Capability, Metric, and Solution Demo
Flow topic in the output must inherit the evidence classification of the
specific input claim it addresses — this skill never assigns a new,
independent classification, it propagates the one already present on the
input evidence entry. The classifications are:

- `confirmed_customer_statement`
- `salesforce_operating_context`
- `verified_workiva_internal_fact`
- `inference_working_hypothesis`
- `open_question_validation_required`
- `risk_assumption_dependency`

**No template field content may be invented without a traced claim from the
input payload(s).** Where discovery genuinely didn't surface something a
template field needs (e.g. no stated Priority Value Driver, no Workiva
Differentiator supplied, no Customer Proof Point supplied), this skill must
use the fallback string for that field **and** explicitly flag it as a
missing element in the Presentation Planning section — never blend a guess
in alongside evidence-traced content.

**Examples:**

1. *Input claim: "Customer's Controller stated their quarterly close takes 3
   weeks due to manual multi-entity consolidation." [confirmed_customer_statement]*
   → Before Scenario: "3-week close driven by manual multi-entity
   consolidation" — classification carried forward as
   `confirmed_customer_statement`. Feeds a Solution Demo Flow topic on
   automated consolidation, Executive Impact = Drive Efficiency.
2. *Input claim: "Eval scorecard requires a demonstrable, exportable audit
   trail for every consolidation adjustment." [confirmed_customer_statement]*
   → Metric: "Exportable audit trail present for every consolidation
   adjustment demoed" — Executive Impact of the corresponding topic =
   Mitigate Risk.
3. *Input claim: "Team believes current ESG disclosure prep is manual, but
   this was not directly stated by the customer." [inference_working_hypothesis]*
   → Required Capability listed as tentative, tagged
   `inference_working_hypothesis`, and the corresponding Solution Demo Flow
   topic is flagged as lower-confidence framing rather than presented with
   the same certainty as confirmed items.
4. *No Workiva Differentiator supplied by the user, none present in any
   upstream payload* → Trap-Setting's "Relevant Differentiator to Highlight"
   field = `"Requires Workiva-source validation."`, flagged in Presentation
   Planning as a missing element.

## 6. Output Schema

Produce the SC Demo Planning Document using the verbatim Workiva template
structure below, fully populated. Every Before/After Scenario, Required
Capability, Metric, and Solution Demo Flow topic must end with an evidence
classification citation. Any field with no available basis must use a
fallback string from Section 9 rather than being omitted or guessed.

```
# SC Demo Planning Document

Your Name: <name, or fallback string if not supplied>
Seller(s): <name(s), or fallback string if not supplied>
Customer/Opportunity Name: <from account-opportunity-brief>
Priority Value Driver(s): <from account-opportunity-brief, or fallback + flag>
Demo Goal/Objectives: <synthesized from merged evidence>

## Presentation Planning
<How discovery evidence frames the demo. Explicitly list any missing
elements (ideally present before the demo) and what will be done without
them, per field-by-field flags raised elsewhere in this document.>

## Elements of the CoM Mantra
Indicate the specifics of the opportunity — where will each item be used:
- Limbic opening: <where/how, or "Will not use">
- Visual roadmap (tell-show-tell topics): <where/how, or "Will not use">
- Value close: <where/how, or "Will not use">
- Other: <where/how, or "Will not use">

## Before Scenarios & Negative Consequences
| Scenario | Source Claim | Evidence Classification |
|---|---|---|
(repeat per scenario, sourced from gong-discovery-analysis / discovery narrative)

## After Scenarios & Positive Business Outcomes
| Scenario | Source Claim | Evidence Classification |
|---|---|---|
(repeat per scenario)

## Required Capabilities
| Capability | Source Claim | Evidence Classification |
|---|---|---|
(repeat per capability, sourced from technical-discovery-planner)

## Metrics
| Metric | Source Claim | Evidence Classification |
|---|---|---|
(repeat per metric, sourced from evaluation-validation-planner)

## Limbic Opening
- Summary of Concept (which Mantra elements leveraged): <text>
- Type: <Illustrative Analogy | Industry Insight | Discovery Findings | Case Study | Other>
- Description of what's on screen: <text>
- Evidence Classification: <classification>

## Solution Demo Flow
| Product/Solution Feature (HWDI & Better) | Topic Name (customer language) | Closing Operational Benefit (Required Capability → Positive Business Outcome) | Executive Impact (PSI lens) | Evidence Classification |
|---|---|---|---|---|
(repeat per topic, in tell-show-tell roadmap sequence; Executive Impact must be exactly one of: Drive Growth, Drive Efficiency, Improve Customer Experience, Mitigate Risk)

## Trap-Setting
| Relevant Differentiator to Highlight | Question to Expand Required Capabilities/Metrics |
|---|---|
(repeat, or single row with fallback string if no differentiator supplied)

## Value Close
Summary of closing concept (which Mantra elements leveraged): <text>
Evidence Classification: <classification>

## Customer Proof Points
| Proof Point | How I'll Talk About It (Slide/Audible/Other) | Evidence Classification |
|---|---|---|
(repeat, or single row with fallback string if none supplied)
```

## 7. Quality Checklist

Before returning the plan, confirm:

- [ ] Every Before/After Scenario, Required Capability, Metric, and Solution
      Demo Flow topic traces to a specific input claim from an upstream
      skill's `evidence[]` — none are invented.
- [ ] Every Solution Demo Flow topic's Executive Impact is classified as
      exactly one of the four lenses (Drive Growth, Drive Efficiency, Improve
      Customer Experience, Mitigate Risk) — never a fifth, invented lens.
- [ ] No Workiva Differentiator or Customer Proof Point appears unless
      supplied by the user or already cited in an upstream payload; otherwise
      the fallback string is used and the gap is flagged in Presentation
      Planning.
- [ ] Every template field with no available basis uses one of the two
      fallback strings verbatim — none are left blank or guessed.
- [ ] Missing elements (e.g. no stated Priority Value Driver) are explicitly
      called out in Presentation Planning, not silently absorbed elsewhere.
- [ ] Every row carries the same evidence classification as its source
      claim — none are upgraded or invented.
- [ ] The output payload (Section 10) is included and validates against
      `../shared/evidence-schema.md`.

## 8. Read-Only / No-Write Disclaimer

**This skill never provisions, configures, or modifies an actual demo
environment, Salesforce org, or any other live system, and it does not
execute a live demo.** It produces a document — the SC Demo Planning
Document — for a human SC to review, refine, and use to script/rehearse the
actual demo. It has no write access and makes no live connector calls of any
kind. If a user asks this skill to "set up the demo" or "run the demo,"
clarify that it can only produce the narrative planning document; live
demo execution against connected systems is handled by the separate `/demo`
capability in this repository, not by this skill.

## 9. Fallback Strings

Use these exact strings whenever information is unavailable or unconfirmed —
never fabricate a substitute:

- `"Unknown — requires validation."` — for missing factual fields (e.g. no
  stated Priority Value Driver, no seller name supplied).
- `"Requires Workiva-source validation."` — for claims that would need
  confirmation from an internal Workiva source (e.g. an unconfirmed
  differentiator, an unconfirmed product capability claim) not accessible to
  this skill.

## 10. Output / Handoff Payload

This skill is a **terminal adapter** — it does not hand off to a further
downstream presales skill. It still emits the shared JSON envelope for
consistency and logging purposes, with `handoff_target` set to `none`.

```json
{
  "schema_ref": "../shared/evidence-schema.md",
  "handoff_target": "none",
  "source_skill": "demo-framework-adapter",
  "upstream_source_skills": ["<e.g. technical-discovery-planner>"],
  "account": {
    "name": "<Account Name>",
    "salesforce_id": "<Account ID or Unknown — requires validation.>"
  },
  "opportunity": {
    "name": "<Opportunity Name>",
    "salesforce_id": "<Opportunity ID or Unknown — requires validation.>"
  },
  "sc_demo_planning_document": {
    "your_name": "<text or fallback>",
    "sellers": "<text or fallback>",
    "priority_value_drivers": "<text or fallback>",
    "demo_goal": "<text>",
    "presentation_planning": "<text, including flagged missing elements>",
    "com_mantra_elements": {
      "limbic_opening": "<text or 'Will not use'>",
      "visual_roadmap": "<text or 'Will not use'>",
      "value_close": "<text or 'Will not use'>",
      "other": "<text or 'Will not use'>"
    },
    "before_scenarios": [
      { "text": "<text>", "evidence_classification": "<classification>" }
    ],
    "after_scenarios": [
      { "text": "<text>", "evidence_classification": "<classification>" }
    ],
    "required_capabilities": [
      { "text": "<text>", "evidence_classification": "<classification>" }
    ],
    "metrics": [
      { "text": "<text>", "evidence_classification": "<classification>" }
    ],
    "limbic_opening_detail": {
      "type": "<Illustrative Analogy | Industry Insight | Discovery Findings | Case Study | Other>",
      "screen_description": "<text>",
      "evidence_classification": "<classification>"
    },
    "solution_demo_flow": [
      {
        "feature": "<text>",
        "topic_name": "<text>",
        "closing_operational_benefit": "<text>",
        "executive_impact_lens": "<Drive Growth | Drive Efficiency | Improve Customer Experience | Mitigate Risk>",
        "evidence_classification": "<classification>"
      }
    ],
    "trap_setting": [
      {
        "differentiator": "<text or fallback string>",
        "expansion_question": "<text or fallback string>"
      }
    ],
    "value_close": {
      "summary": "<text>",
      "evidence_classification": "<classification>"
    },
    "customer_proof_points": [
      {
        "proof_point": "<text or fallback string>",
        "delivery_mode": "<Slide | Audible | Other | fallback string>",
        "evidence_classification": "<classification>"
      }
    ]
  }
}
```

## 11. Worked Example (Fully Synthetic)

All names, IDs, figures, and differentiators below are fabricated for
illustration. No real account, contact, deal, or product data is
represented.

### Fabricated Inputs (handoff payloads from upstream skills)

```json
{
  "skill": "account-opportunity-brief",
  "account_id": "acme-test-corp-001",
  "opportunity_id": "0061-acme-enterprise-expansion",
  "summary": "Acme Test Corp is expanding its Workiva footprint; the Controller's office has flagged close-cycle speed and audit defensibility as the top value drivers for the FY26 expansion opportunity.",
  "evidence": [
    {
      "claim": "Opportunity 'Acme Test Corp — Enterprise Expansion FY26' is in stage 'Technical Evaluation', close date 2026-11-15.",
      "classification": "salesforce_operating_context",
      "source": "search_opportunities"
    },
    {
      "claim": "Priority value driver stated by the Controller's office is faster, more defensible quarterly close.",
      "classification": "confirmed_customer_statement",
      "source": "Gong call 2026-08-20, Priya Nandakumar (Controller)"
    }
  ],
  "open_questions": [
    "Whether the CFO will attend the demo is unconfirmed."
  ],
  "handoff_target": ["demo-framework-adapter"]
}
```

```json
{
  "skill": "gong-discovery-analysis",
  "account_id": "acme-test-corp-001",
  "opportunity_id": "0061-acme-enterprise-expansion",
  "summary": "Discovery calls surface a 3-week manual multi-entity consolidation as the primary pain, with an inferred (unconfirmed) manual ESG disclosure process as a secondary theme.",
  "evidence": [
    {
      "claim": "Priya Nandakumar (Controller) said on the 2026-08-20 call: 'Our quarterly close takes 3 weeks because we're manually consolidating across 6 subsidiaries in spreadsheets.'",
      "classification": "confirmed_customer_statement",
      "source": "Gong call 2026-08-20, Priya Nandakumar"
    },
    {
      "claim": "Team believes current ESG disclosure prep is manual, but this was not directly stated by the customer.",
      "classification": "inference_working_hypothesis",
      "source": "Discovery notes, 2026-08-22"
    }
  ],
  "open_questions": [
    "Whether ESG disclosure prep is actually manual, or already partially tooled, is unconfirmed."
  ],
  "handoff_target": ["demo-framework-adapter"]
}
```

```json
{
  "skill": "technical-discovery-planner",
  "account_id": "acme-test-corp-001",
  "opportunity_id": "0061-acme-enterprise-expansion",
  "summary": "Required capabilities center on automated multi-entity consolidation and a fully exportable, adjustment-level audit trail.",
  "evidence": [
    {
      "claim": "Prospect requires automated multi-entity consolidation across at least 6 subsidiaries with mismatched fiscal periods.",
      "classification": "confirmed_customer_statement",
      "source": "Gong call 2026-08-20, Priya Nandakumar"
    },
    {
      "claim": "Prospect's eval scorecard requires a demonstrable, exportable audit trail for every consolidation adjustment.",
      "classification": "confirmed_customer_statement",
      "source": "Eval criteria doc, 'Acme_Test_Corp_Eval_Scorecard.pdf'"
    }
  ],
  "open_questions": [
    "Whether the security/compliance reviewer will attend the demo is unconfirmed."
  ],
  "handoff_target": ["demo-framework-adapter"]
}
```

```json
{
  "skill": "evaluation-validation-planner",
  "account_id": "acme-test-corp-001",
  "opportunity_id": "0061-acme-enterprise-expansion",
  "summary": "Success criteria for the eval center on a measurable close-cycle reduction and a verifiable audit trail export.",
  "evidence": [
    {
      "claim": "Success criterion: demonstrated consolidation workflow must show a path from 3 weeks to under 3 days for the same multi-entity close scenario.",
      "classification": "confirmed_customer_statement",
      "source": "Eval criteria doc, 'Acme_Test_Corp_Eval_Scorecard.pdf'"
    },
    {
      "claim": "Success criterion: every consolidation adjustment made during the demo must produce a visible, exportable audit trail entry.",
      "classification": "confirmed_customer_statement",
      "source": "Eval criteria doc, 'Acme_Test_Corp_Eval_Scorecard.pdf'"
    }
  ],
  "open_questions": [],
  "handoff_target": ["demo-framework-adapter"]
}
```

### Output

```
# SC Demo Planning Document

Your Name: Unknown — requires validation.
Seller(s): Unknown — requires validation.
Customer/Opportunity Name: Acme Test Corp — Enterprise Expansion FY26
Priority Value Driver(s): Faster, more defensible quarterly close
Demo Goal/Objectives: Show a credible path from a 3-week manual multi-entity close to a fast, audit-defensible close, validated against the prospect's own eval scorecard.

## Presentation Planning
Discovery (Gong 2026-08-20) establishes the Controller's own words as the frame for the demo: the 3-week manual consolidation pain opens the story, and the eval scorecard's audit-trail and cycle-time requirements close it. Missing elements: (1) Your Name and Seller(s) were not supplied — flagged, using fallback strings until provided; (2) whether the CFO or security/compliance reviewer will attend is unconfirmed — the demo will proceed assuming a Controller-office-led audience and can be adjusted if either stakeholder confirms attendance; (3) no Workiva Differentiator was supplied for Trap-Setting — flagged below with fallback string.

## Elements of the CoM Mantra
- Limbic opening: Discovery Findings — opens directly on Priya Nandakumar's own words about the 3-week close.
- Visual roadmap (tell-show-tell topics): Two topics — automated consolidation, then audit-trail export — sequenced pain-first.
- Value close: Ties both topics back to the stated eval scorecard pass criteria.
- Other: Will not use.

## Before Scenarios & Negative Consequences
| Scenario | Source Claim | Evidence Classification |
|---|---|---|
| 3-week manual multi-entity close across 6 subsidiaries, done in spreadsheets | Priya Nandakumar (Controller), Gong call 2026-08-20: "Our quarterly close takes 3 weeks because we're manually consolidating across 6 subsidiaries in spreadsheets." | confirmed_customer_statement |
| ESG disclosure prep believed manual (unconfirmed) | Team inference, discovery notes 2026-08-22 | inference_working_hypothesis |

## After Scenarios & Positive Business Outcomes
| Scenario | Source Claim | Evidence Classification |
|---|---|---|
| Multi-entity close collapses from 3 weeks to under 3 days | Eval scorecard success criterion, 'Acme_Test_Corp_Eval_Scorecard.pdf' | confirmed_customer_statement |
| Every adjustment auditable and exportable without manual reconstruction | Eval scorecard success criterion, 'Acme_Test_Corp_Eval_Scorecard.pdf' | confirmed_customer_statement |

## Required Capabilities
| Capability | Source Claim | Evidence Classification |
|---|---|---|
| Automated multi-entity consolidation across 6+ subsidiaries with mismatched fiscal periods | Gong call 2026-08-20, Priya Nandakumar | confirmed_customer_statement |
| Exportable, adjustment-level audit trail | Eval criteria doc, 'Acme_Test_Corp_Eval_Scorecard.pdf' | confirmed_customer_statement |

## Metrics
| Metric | Source Claim | Evidence Classification |
|---|---|---|
| Consolidation demo shows path from 3 weeks to under 3 days | Eval criteria doc, 'Acme_Test_Corp_Eval_Scorecard.pdf' | confirmed_customer_statement |
| Every consolidation adjustment produces a visible, exportable audit trail entry | Eval criteria doc, 'Acme_Test_Corp_Eval_Scorecard.pdf' | confirmed_customer_statement |

## Limbic Opening
- Summary of Concept (which Mantra elements leveraged): Opens on the Controller's own quote about the 3-week close, framing the whole demo as closing that specific gap (Limbic Opening + sets up the Visual Roadmap).
- Type: Discovery Findings
- Description of what's on screen: A slide showing the current 3-week close timeline broken out by subsidiary, annotated with the Controller's quote.
- Evidence Classification: confirmed_customer_statement

## Solution Demo Flow
| Product/Solution Feature (HWDI & Better) | Topic Name (customer language) | Closing Operational Benefit (Required Capability → Positive Business Outcome) | Executive Impact (PSI lens) | Evidence Classification |
|---|---|---|---|---|
| Automated multi-entity consolidation workflow | "From 3 Weeks to 3 Days" | Automated consolidation across 6 subsidiaries replaces manual spreadsheet work, directly closing the stated close-cycle metric | Drive Efficiency | confirmed_customer_statement |
| Adjustment-level audit trail and export | "Every Adjustment, Fully Defensible" | Exportable audit trail on every adjustment satisfies the eval scorecard's audit-defensibility requirement | Mitigate Risk | confirmed_customer_statement |

## Trap-Setting
| Relevant Differentiator to Highlight | Question to Expand Required Capabilities/Metrics |
|---|---|
| Requires Workiva-source validation. | Requires Workiva-source validation. |

## Value Close
Summary of closing concept (which Mantra elements leveraged): Close by restating the Controller's own "3 weeks" quote against the demoed "under 3 days" outcome and the visible audit trail, then hand back to the seller to discuss eval scorecard sign-off and next steps (Value Close, tying back to the Limbic Opening).
Evidence Classification: confirmed_customer_statement

## Customer Proof Points
| Proof Point | How I'll Talk About It (Slide/Audible/Other) | Evidence Classification |
|---|---|---|
| Unknown — requires validation. | Unknown — requires validation. | open_question_validation_required |
```

```json
{
  "schema_ref": "../shared/evidence-schema.md",
  "handoff_target": "none",
  "source_skill": "demo-framework-adapter",
  "upstream_source_skills": ["account-opportunity-brief", "gong-discovery-analysis", "technical-discovery-planner", "evaluation-validation-planner"],
  "account": {
    "name": "Acme Test Corp",
    "salesforce_id": "acme-test-corp-001"
  },
  "opportunity": {
    "name": "Acme Test Corp — Enterprise Expansion FY26",
    "salesforce_id": "0061-acme-enterprise-expansion"
  },
  "sc_demo_planning_document": {
    "your_name": "Unknown — requires validation.",
    "sellers": "Unknown — requires validation.",
    "priority_value_drivers": "Faster, more defensible quarterly close",
    "demo_goal": "Show a credible path from a 3-week manual multi-entity close to a fast, audit-defensible close, validated against the prospect's own eval scorecard.",
    "presentation_planning": "Discovery establishes the Controller's own words as the frame for the demo; missing elements (Your Name/Seller(s), CFO/security reviewer attendance, Workiva Differentiator) are flagged.",
    "com_mantra_elements": {
      "limbic_opening": "Opens on the Controller's own words about the 3-week close.",
      "visual_roadmap": "Two topics: automated consolidation, then audit-trail export.",
      "value_close": "Ties both topics back to the eval scorecard pass criteria.",
      "other": "Will not use"
    },
    "before_scenarios": [
      { "text": "3-week manual multi-entity close across 6 subsidiaries, done in spreadsheets.", "evidence_classification": "confirmed_customer_statement" },
      { "text": "ESG disclosure prep believed manual (unconfirmed).", "evidence_classification": "inference_working_hypothesis" }
    ],
    "after_scenarios": [
      { "text": "Multi-entity close collapses from 3 weeks to under 3 days.", "evidence_classification": "confirmed_customer_statement" },
      { "text": "Every adjustment auditable and exportable without manual reconstruction.", "evidence_classification": "confirmed_customer_statement" }
    ],
    "required_capabilities": [
      { "text": "Automated multi-entity consolidation across 6+ subsidiaries with mismatched fiscal periods.", "evidence_classification": "confirmed_customer_statement" },
      { "text": "Exportable, adjustment-level audit trail.", "evidence_classification": "confirmed_customer_statement" }
    ],
    "metrics": [
      { "text": "Consolidation demo shows path from 3 weeks to under 3 days.", "evidence_classification": "confirmed_customer_statement" },
      { "text": "Every consolidation adjustment produces a visible, exportable audit trail entry.", "evidence_classification": "confirmed_customer_statement" }
    ],
    "limbic_opening_detail": {
      "type": "Discovery Findings",
      "screen_description": "Slide showing the current 3-week close timeline broken out by subsidiary, annotated with the Controller's quote.",
      "evidence_classification": "confirmed_customer_statement"
    },
    "solution_demo_flow": [
      {
        "feature": "Automated multi-entity consolidation workflow",
        "topic_name": "From 3 Weeks to 3 Days",
        "closing_operational_benefit": "Automated consolidation across 6 subsidiaries replaces manual spreadsheet work, directly closing the stated close-cycle metric.",
        "executive_impact_lens": "Drive Efficiency",
        "evidence_classification": "confirmed_customer_statement"
      },
      {
        "feature": "Adjustment-level audit trail and export",
        "topic_name": "Every Adjustment, Fully Defensible",
        "closing_operational_benefit": "Exportable audit trail on every adjustment satisfies the eval scorecard's audit-defensibility requirement.",
        "executive_impact_lens": "Mitigate Risk",
        "evidence_classification": "confirmed_customer_statement"
      }
    ],
    "trap_setting": [
      {
        "differentiator": "Requires Workiva-source validation.",
        "expansion_question": "Requires Workiva-source validation."
      }
    ],
    "value_close": {
      "summary": "Restate the Controller's own '3 weeks' quote against the demoed 'under 3 days' outcome and the visible audit trail, then hand back to the seller for eval scorecard sign-off discussion.",
      "evidence_classification": "confirmed_customer_statement"
    },
    "customer_proof_points": [
      {
        "proof_point": "Unknown — requires validation.",
        "delivery_mode": "Unknown — requires validation.",
        "evidence_classification": "open_question_validation_required"
      }
    ]
  }
}
```
