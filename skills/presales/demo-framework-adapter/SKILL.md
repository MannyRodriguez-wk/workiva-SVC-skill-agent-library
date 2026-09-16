---
name: demo-framework-adapter
description: "Adapter skill that translates the standard presales handoff JSON payload (per ../shared/evidence-schema.md), produced by upstream skills like account-opportunity-brief, technical-discovery-planner, and evaluation-validation-planner, into a concrete demo-environment setup recommendation — which Workiva product modules/features to configure, what synthetic data to load, and what workflow to walk through, each mapped to a specific stated pain point or success criterion from the input payload. Primarily invoked automatically by other presales skills passing it a handoff payload, but can also be triggered directly by a user, e.g. 'build a demo plan from this discovery output', 'what should I show in the demo for [account]', 'turn this eval plan into a demo script', or 'map these pain points to demo moments'."
metadata:
  disable-model-invocation: true
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Demo Environment Framework Adapter

An **adapter skill**, not a standalone user-facing analysis skill. It does not
gather new evidence and does not call any live connector itself. It consumes
the standard handoff JSON payload already produced by an upstream presales
skill and transforms it into a concrete, evidence-traced demo-environment
setup plan: which product modules/features to configure, what synthetic data
scenario to load, and what workflow/narrative beat to walk through for each
prospect-stated pain point or success criterion.

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

**Purpose:** Take evidence already gathered elsewhere (discovery notes, call
transcripts, eval criteria, Salesforce context) and turn it into a demo plan
a Solution/Value Consultant (SVC) can hand to whoever configures and runs the
demo environment — without re-discovering or inventing anything new.

**Primary invocation mode:** automatic, as the terminal step of another
skill's workflow. Upstream skills that are expected to hand off to this
skill include (non-exhaustive):

- `account-opportunity-brief`
- `technical-discovery-planner`
- `evaluation-validation-planner`
- `gong-discovery-analysis`

**Secondary invocation mode — direct user trigger phrases** (non-exhaustive;
match on intent, not exact wording):

- "Build a demo plan from this discovery output."
- "What should I show in the demo for [account]?"
- "Turn this eval plan into a demo script."
- "Map these pain points to demo moments."
- "Given this handoff payload, what should the demo environment look like?"
- "Take the discovery notes for [account] and tell me what to configure in
  the demo org."

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
  `technical-discovery-planner`, and/or `evaluation-validation-planner`.
  Each payload's `claims`, `open_questions`, `risks`, and any explicit
  pain-point / success-criterion fields are the raw material for this
  skill's output.

**Optional:**

- A list of Workiva product modules known to be available/configured in the
  target demo environment (e.g. "the demo org has modules X, Y, Z
  provisioned"). If not supplied, this skill uses placeholder module names
  (see Section 3) rather than guessing which real modules exist.
- A stated time budget for the demo (e.g. "we only have 30 minutes") — used
  to prioritize which demo moments make the cut.
- A stated audience (e.g. "this is for the economic buyer, keep it
  business-outcome framed" vs. "this is for the technical evaluator team") —
  used to adjust narrative framing, not to change which pain points are
  covered.

If multiple upstream payloads are supplied (e.g. both a discovery payload
and an eval-criteria payload for the same opportunity), merge their claims,
pain points, and success criteria into a single deduplicated set before
building the demo plan, preserving each item's original evidence
classification and source skill.

## 3. Tool-Agnostic Source Retrieval Guidance

This skill does **not** call any live connector (Salesforce, Gong, or
otherwise) and does **not** provision or query a demo environment. All of
its input is the already-gathered, already-classified evidence contained in
the upstream handoff payload(s). Its only job is transformation, not
retrieval.

If richer product/module reference material (a canonical list of Workiva
demo-org modules, a demo-data catalog, a scripted-workflow library, etc.)
exists elsewhere in this repository or in the user's environment, it should
be consulted and referenced by path when available. Absent that reference
material, **never invent a specific Workiva product module name.** Use
placeholders in the form `[Product Module A]`, `[Product Module B]`, etc.,
and explicitly instruct the user/reader to substitute the real Workiva
module names that apply to their demo environment before the plan is
executed.

The same placeholder discipline applies to synthetic data scenarios: name
the *shape* of the data needed (e.g. "a mid-size manufacturing entity with
three consolidating subsidiaries and one open audit finding") without
asserting that specific pre-built demo data exists unless the input payload
or supplied reference material confirms it.

## 4. Step-by-Step Workflow

1. **Ingest and validate the payload(s).** Confirm each input JSON payload
   conforms to [../shared/evidence-schema.md](../shared/evidence-schema.md).
   If a payload is malformed or missing required fields, surface that
   explicitly rather than guessing its content.
2. **Extract pain points and success criteria.** Pull every claim, risk, and
   open question from the input payload(s) that represents a stated
   customer pain point, desired outcome, or success/eval criterion. Discard
   nothing silently — anything not turned into a demo moment must be listed
   as a gap (see Section 7).
3. **Deduplicate and merge.** If multiple upstream payloads cover the same
   opportunity/account, merge overlapping pain points and criteria, keeping
   the strongest (most directly sourced) evidence classification and citing
   all contributing source skills.
4. **Map each pain point/criterion to a demo moment.** For each item,
   identify: which placeholder product module/feature would address it,
   what synthetic data scenario is needed to make the demonstration
   concrete, and what narrative beat (the story the SVC tells while showing
   it) connects the feature back to the customer's own words.
5. **Sequence the demo moments.** Order moments into a coherent narrative
   arc (typically: biggest/most urgent pain point first, success-criteria
   validation moments woven in, close on a moment that ties to the
   opportunity's overall value story). If a time budget was supplied,
   prioritize accordingly and note what was cut.
6. **Classify every demo moment's source claim.** Tag each row of the output
   table with the evidence classification of the underlying pain
   point/criterion per Section 5.
7. **Identify coverage gaps.** Flag any pain point or success criterion from
   the input payload that has no corresponding demo moment (e.g. because no
   plausible module mapping exists) as an explicit gap, not a silent
   omission.
8. **Assemble the Demo Plan** per the schema in Section 6.
9. **Run the quality checklist** (Section 7) before returning the plan.
10. **Emit the output payload** (Section 10) for logging/consistency, noting
    `handoff_target: none` since this is a terminal adapter skill.

## 5. Source Classification & Citation Rules

Use the shared evidence taxonomy defined in
[../shared/evidence-schema.md](../shared/evidence-schema.md). Every demo
moment in the output must inherit the evidence classification of the
specific pain point / success criterion it addresses — this skill never
assigns a new, independent classification, it propagates the one already
present on the input claim. The classifications are:

- `confirmed_customer_statement`
- `salesforce_operating_context`
- `verified_workiva_internal_fact`
- `inference_working_hypothesis`
- `open_question_validation_required`
- `risk_assumption_dependency`

**No demo moment may be invented without a traced pain point or success
criterion from the input payload.** If the SVC or user wants to add a
generic "feature tour" moment not tied to any input claim, this skill must
label it explicitly as *not evidence-traced* rather than presenting it
alongside evidence-backed moments — and should recommend against including
it, per the quality checklist.

**Examples:**

1. *Input claim: "Customer stated their close process takes 3 weeks due to
   manual consolidation" [confirmed_customer_statement]* → Demo moment:
   show `[Product Module A]`'s automated consolidation workflow against a
   synthetic multi-entity close scenario, narrated as "here's how this
   3-week manual step collapses" — classification carried forward as
   `confirmed_customer_statement`.
2. *Input claim: "Likely champion is the Controller based on meeting
   attendance" [inference_working_hypothesis]* → Not a demo moment itself,
   but used to frame audience/narrative tone; if turned into a moment (e.g.
   "show the Controller's dashboard view"), it is tagged
   `inference_working_hypothesis` and flagged as lower-confidence framing.
3. *Input item: "Security/IT reviewer not yet identified"
   [open_question_validation_required]* → No demo moment; noted as an open
   question that may affect whether a security/compliance-focused demo
   moment is needed at all.

## 6. Output Schema

Produce a Demo Plan table, plus a short narrative header. Every row must end
with an evidence classification.

```
# Demo Plan: <Account Name> — <Opportunity Name>

Source payload(s): <source_skill(s) and, if available, date/identifier>

| Demo Moment | Product Module/Feature | Pain Point / Success Criterion Addressed | Synthetic Data Needed | Evidence Classification |
|---|---|---|---|---|
| <short label> | [Product Module A] | <verbatim or lightly paraphrased pain point/criterion> | <data scenario description> | <classification> |
(repeat per demo moment, in narrative sequence order)

## Coverage Gaps
- <pain point / success criterion with no demo moment> — "Requires Workiva-source validation." or reason
  (repeat, or state "No gaps identified.")

## Non-Evidence-Traced Additions (if any)
- <any generic feature-tour moment explicitly requested but not traced to input evidence>
  (omit this section entirely if none exist — do not include an empty header)
```

Any field with no available basis must use the fallback strings in
Section 9 rather than being omitted or guessed.

## 7. Quality Checklist

Before returning the plan, confirm:

- [ ] Every demo moment ties to a real, traceable input claim (pain point or
      success criterion) — not a generic feature tour.
- [ ] Every input pain point / success criterion is either mapped to a demo
      moment or explicitly listed under Coverage Gaps.
- [ ] No specific Workiva product module name is invented; unresolved
      modules use `[Product Module A]`-style placeholders with an explicit
      instruction to substitute real names.
- [ ] Every row carries the same evidence classification as its source
      claim — none are upgraded or invented.
- [ ] Any non-evidence-traced addition requested by the user is clearly
      segregated and flagged, not blended into the main table.
- [ ] The output payload (Section 10) is included and validates against
      `../shared/evidence-schema.md`.

## 8. Read-Only / No-Write Disclaimer

**This skill never provisions, configures, or modifies an actual demo
environment, Salesforce org, or any other live system.** It produces a plan
— a document — for a human (or a separate provisioning process) to execute.
It has no write access and makes no live connector calls of any kind. If a
user asks this skill to "set up the demo" or "load this data," clarify that
it can only produce the plan describing what should be set up; the actual
provisioning is a manual or separately tooled step.

## 9. Fallback Strings

Use these exact strings whenever information is unavailable or unconfirmed —
never fabricate a substitute:

- `"Unknown — requires validation."` — for missing factual fields (e.g. no
  clear synthetic data scenario derivable from the input payload).
- `"Requires Workiva-source validation."` — for claims that would need
  confirmation from an internal Workiva source (e.g. whether a named module
  actually supports the workflow implied by a pain point) not accessible to
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
  "demo_plan": [
    {
      "demo_moment": "<label>",
      "product_module": "[Product Module A]",
      "pain_point_or_criterion": "<text>",
      "synthetic_data_needed": "<text>",
      "evidence_classification": "<classification>"
    }
  ],
  "coverage_gaps": [
    {
      "item": "<pain point / success criterion text>",
      "reason": "<text>",
      "evidence_classification": "<classification>"
    }
  ],
  "non_evidence_traced_additions": [
    {
      "item": "<text>",
      "flag": "requested without traced evidence"
    }
  ]
}
```

## 11. Worked Example (Fully Synthetic)

All names, IDs, figures, and module names below are fabricated for
illustration. No real account, contact, deal, or product data is
represented.

### Fabricated Input (handoff payload from `technical-discovery-planner`)

```json
{
  "schema_ref": "../shared/evidence-schema.md",
  "handoff_target": ["demo-framework-adapter"],
  "source_skill": "technical-discovery-planner",
  "account": {
    "name": "Acme Test Corp",
    "salesforce_id": "001TEST0000ACME"
  },
  "opportunity": {
    "name": "Acme Test Corp — Enterprise Expansion FY26",
    "salesforce_id": "006TEST0000ACME"
  },
  "claims": [
    {
      "field": "pain_point.close_process",
      "value": "Customer's Controller stated their quarterly close takes 3 weeks due to manual multi-entity consolidation.",
      "evidence_classification": "confirmed_customer_statement",
      "source_tool": "call_transcript"
    },
    {
      "field": "success_criterion.audit_trail",
      "value": "Eval scorecard requires a demonstrable, exportable audit trail for every consolidation adjustment.",
      "evidence_classification": "confirmed_customer_statement",
      "source_tool": "eval_criteria_doc"
    },
    {
      "field": "pain_point.esg_reporting",
      "value": "Team believes current ESG disclosure prep is manual, but this was not directly stated by the customer.",
      "evidence_classification": "inference_working_hypothesis",
      "source_tool": "discovery_notes"
    }
  ],
  "open_questions": [
    {
      "question": "Whether the security/compliance reviewer will attend the demo is unconfirmed.",
      "evidence_classification": "open_question_validation_required"
    }
  ],
  "risks": []
}
```

### Output

```
# Demo Plan: Acme Test Corp — Acme Test Corp — Enterprise Expansion FY26

Source payload(s): technical-discovery-planner

| Demo Moment | Product Module/Feature | Pain Point / Success Criterion Addressed | Synthetic Data Needed | Evidence Classification |
|---|---|---|---|---|
| "From 3 weeks to 3 clicks" consolidation walkthrough | [Product Module A] (automated multi-entity consolidation) | Controller stated quarterly close takes 3 weeks due to manual multi-entity consolidation | A synthetic parent entity with 3 consolidating subsidiaries, mismatched fiscal periods, and 2 elimination entries pre-loaded | confirmed_customer_statement |
| Live audit-trail export on a consolidation adjustment | [Product Module B] (audit trail / change history) | Eval scorecard requires exportable audit trail for every consolidation adjustment | Same synthetic consolidation scenario, with one adjustment made live during the demo to show the resulting trail entry | confirmed_customer_statement |
| ESG disclosure prep tour (framed tentatively) | [Product Module C] (ESG disclosure workbook) | Team's inference that ESG disclosure prep is manual (not directly confirmed by customer) | A synthetic ESG disclosure workbook with 2 pending data requests | inference_working_hypothesis |

## Coverage Gaps
- Whether a security/compliance-focused demo moment is needed depends on whether that reviewer attends — "Unknown — requires validation."

## Non-Evidence-Traced Additions
(none requested)
```

```json
{
  "schema_ref": "../shared/evidence-schema.md",
  "handoff_target": "none",
  "source_skill": "demo-framework-adapter",
  "upstream_source_skills": ["technical-discovery-planner"],
  "account": {
    "name": "Acme Test Corp",
    "salesforce_id": "001TEST0000ACME"
  },
  "opportunity": {
    "name": "Acme Test Corp — Enterprise Expansion FY26",
    "salesforce_id": "006TEST0000ACME"
  },
  "demo_plan": [
    {
      "demo_moment": "\"From 3 weeks to 3 clicks\" consolidation walkthrough",
      "product_module": "[Product Module A]",
      "pain_point_or_criterion": "Controller stated quarterly close takes 3 weeks due to manual multi-entity consolidation.",
      "synthetic_data_needed": "Synthetic parent entity with 3 consolidating subsidiaries, mismatched fiscal periods, 2 elimination entries pre-loaded.",
      "evidence_classification": "confirmed_customer_statement"
    },
    {
      "demo_moment": "Live audit-trail export on a consolidation adjustment",
      "product_module": "[Product Module B]",
      "pain_point_or_criterion": "Eval scorecard requires exportable audit trail for every consolidation adjustment.",
      "synthetic_data_needed": "Same consolidation scenario, one adjustment made live to show resulting trail entry.",
      "evidence_classification": "confirmed_customer_statement"
    },
    {
      "demo_moment": "ESG disclosure prep tour (framed tentatively)",
      "product_module": "[Product Module C]",
      "pain_point_or_criterion": "Team's inference that ESG disclosure prep is manual (not directly confirmed by customer).",
      "synthetic_data_needed": "Synthetic ESG disclosure workbook with 2 pending data requests.",
      "evidence_classification": "inference_working_hypothesis"
    }
  ],
  "coverage_gaps": [
    {
      "item": "Security/compliance reviewer attendance and needs",
      "reason": "Unknown — requires validation.",
      "evidence_classification": "open_question_validation_required"
    }
  ],
  "non_evidence_traced_additions": []
}
```
