# Presales Handoff Payload — Evidence Schema

This document defines the JSON shape every skill under `skills/presales/`
must emit as the final block of its output, per
`../core-presales-intelligence/SKILL.md` §5. It is the contract consumed by
the two downstream adapter skills: `workiva-mcp-adapter` and
`demo-framework-adapter`.

Sibling skills should link to this file (`../shared/evidence-schema.md`)
rather than copying it inline.

## JSON Schema

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://workiva-scvm-skill-library/presales/shared/evidence-schema.json",
  "title": "Presales Skill Handoff Payload",
  "type": "object",
  "required": ["skill", "summary", "evidence", "open_questions", "handoff_target"],
  "properties": {
    "skill": {
      "type": "string",
      "description": "Kebab-case name of the emitting sibling skill, e.g. 'gong-call-brief', 'rfp-gap-analysis'."
    },
    "account_id": {
      "type": ["string", "null"],
      "description": "Salesforce Account ID this output pertains to, or a synthetic placeholder in examples. Null if not applicable."
    },
    "opportunity_id": {
      "type": ["string", "null"],
      "description": "Salesforce Opportunity ID this output pertains to, or a synthetic placeholder in examples. Null if not applicable."
    },
    "summary": {
      "type": "string",
      "description": "One-paragraph, human-readable summary of the skill's output."
    },
    "evidence": {
      "type": "array",
      "description": "Every factual claim made by the skill, each individually classified.",
      "items": {
        "type": "object",
        "required": ["claim", "classification", "source"],
        "properties": {
          "claim": {
            "type": "string",
            "description": "The claim text, or one of the two fixed fallback strings ('Unknown — requires validation.' / 'Requires Workiva-source validation.') when unverifiable."
          },
          "classification": {
            "type": "string",
            "enum": [
              "confirmed_customer_statement",
              "salesforce_operating_context",
              "verified_workiva_internal_fact",
              "inference_working_hypothesis",
              "open_question_validation_required",
              "risk_assumption_dependency"
            ],
            "description": "Exactly one of the six evidence classifications defined in core-presales-intelligence/SKILL.md §1."
          },
          "source": {
            "type": "string",
            "description": "Traceable provenance: transcript date + speaker, Salesforce object + tool name, document title + location, etc. Never blank, even for fallback claims (state what was checked and came up empty)."
          }
        },
        "additionalProperties": false
      }
    },
    "open_questions": {
      "type": "array",
      "description": "Plain-text questions requiring human or customer validation before being treated as fact.",
      "items": { "type": "string" }
    },
    "handoff_target": {
      "type": "array",
      "description": "Which downstream adapter skill(s) should consume this payload.",
      "items": {
        "type": "string",
        "enum": ["workiva-mcp-adapter", "demo-framework-adapter"]
      },
      "minItems": 1
    }
  },
  "additionalProperties": true
}
```

`additionalProperties: true` at the top level lets individual sibling skills
add their own extra fields (e.g. an RFP skill might add a `questions_answered`
count) without breaking the shared contract — but the six required fields
above must always be present and well-formed.

## Worked example

```json
{
  "skill": "rfp-gap-analysis",
  "account_id": "acme-test-corp-001",
  "opportunity_id": "0061-acme-esg-renewal",
  "summary": "Acme Test Corp's RFP asks about CSRD taxonomy tagging and SOC 2 Type II coverage. Workiva's ESG Reporting solution covers the first; SOC 2 scope needs confirmation from security team.",
  "evidence": [
    {
      "claim": "Acme Test Corp's RFP question 14 asks whether the platform supports CSRD taxonomy tagging.",
      "classification": "confirmed_customer_statement",
      "source": "RFP document 'Acme_Test_Corp_RFP_2026.pdf', question 14 (Google Drive)"
    },
    {
      "claim": "Opportunity 0061-acme-esg-renewal is in stage 'Negotiation/Review', close date 2026-10-30.",
      "classification": "salesforce_operating_context",
      "source": "search_opportunities (Salesforce)"
    },
    {
      "claim": "Workiva's ESG Reporting solution supports CSRD taxonomy tagging as of the FY26 release.",
      "classification": "verified_workiva_internal_fact",
      "source": "Workiva internal GRC/Documents MCP, FY26 release notes"
    },
    {
      "claim": "Requires Workiva-source validation.",
      "classification": "open_question_validation_required",
      "source": "No internal GRC/Documents record found covering current SOC 2 Type II report scope; checked internal docs MCP on 2026-09-16, no match."
    }
  ],
  "open_questions": [
    "Does the current SOC 2 Type II report cover the specific modules Acme Test Corp asked about in question 22?"
  ],
  "handoff_target": ["workiva-mcp-adapter", "demo-framework-adapter"]
}
```

## Validation rules (plain-language, for skills that can't run a JSON Schema validator)

1. `skill`, `summary`, `evidence`, `open_questions`, and `handoff_target` must
   always be present.
2. Every item in `evidence` must have all three of `claim`, `classification`,
   `source` — never omit `source`, even for fallback claims.
3. `classification` must be exactly one of the six enum values in
   `../core-presales-intelligence/SKILL.md` §1 — no free text, no new values.
4. `handoff_target` must contain at least one of the two known adapter names.
5. Use synthetic account/person names and IDs in all example payloads, per
   `../core-presales-intelligence/SKILL.md` §6.
