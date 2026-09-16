---
name: evaluation-validation-planner
description: "Builds a structured evaluation / proof-of-concept (POC) validation plan for an opportunity moving into a technical evaluation stage — success criteria the prospect and Workiva agree define a 'pass,' a validation timeline with steps and owners, the stakeholders who must sign off, and risk factors that could derail the eval. Pulls Salesforce opportunity context (search_opportunities, retrieve_semantic_model) and can incorporate prior technical-discovery-planner or gong-discovery-analysis output when pasted in. Use when asked to 'build an eval plan for [opportunity]', 'what are the success criteria for this POC', 'plan the validation phase for [account]', 'draft a POC exit plan', or 'help me scope this technical evaluation'."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Evaluation / POC Validation Planner

This skill drafts a validation plan for an opportunity that is entering (or
already in) a technical evaluation or proof-of-concept stage. It turns
scattered discovery context into a single structured plan: what "pass" means,
who owns each step, what timeline the eval runs on, who must sign off before
the deal can move forward, and what could go wrong.

It is one of nine sibling skills in the Workiva presales skill family. It
follows the shared conventions defined in
[`../core-presales-intelligence/SKILL.md`](../core-presales-intelligence/SKILL.md)
and the evidence/handoff schema in
[`../shared/evidence-schema.md`](../shared/evidence-schema.md). Read both
before modifying this skill; this document restates the non-negotiable rules
in its own words but does not repeat them in full.

## 1. Purpose & trigger phrases

Use this skill when an opportunity is moving into (or already sitting in) a
technical evaluation, pilot, sandbox, or proof-of-concept stage, and someone
needs a plan for how that evaluation will be run, judged, and closed out.

Representative trigger phrases:

- "Build an eval plan for [opportunity]."
- "What are the success criteria for this POC?"
- "Plan the validation phase for [account]."
- "Draft a POC exit plan for [opportunity]."
- "Help me scope this technical evaluation."
- "Who needs to sign off before this eval closes?"
- "What could derail the [account] proof of concept?"

## 2. Required / optional inputs

**Required:**

- Opportunity name or Salesforce ID (e.g. `Acme Test Corp — Platform Eval`,
  `0061-acme-platform-eval`).
- Target evaluation end date (when the eval/POC is expected to conclude and a
  go/no-go decision is expected).

**Optional (improves plan quality but not required to run):**

- Pasted output from a prior `technical-discovery-planner` or
  `gong-discovery-analysis` skill run (requirements, pain points, stated
  timelines, named stakeholders already surfaced in discovery).
- Known competitor(s) also in the evaluation, if disclosed by the prospect or
  visible in Salesforce (e.g. a competing platform named in an opportunity
  field or a Gong call).

If required inputs are missing, ask for them before proceeding rather than
guessing an opportunity or date.

## 3. Source retrieval guidance (read-only)

**This skill is READ-ONLY**, per the shared constraint in
[`../core-presales-intelligence/SKILL.md §3`](../core-presales-intelligence/SKILL.md).
It never creates, updates, or deletes any Salesforce record, Google Drive
file, Gong entity, or Workiva internal document. It only calls query/search/
read-style tools, and treats every output as a draft for a human SC/VC to
review, edit, and manually act on — never an autonomous action taken on the
prospect's or Workiva's behalf. The sole write-shaped exception across the
whole skill family is `add_gtmasst_log`, used only to append this skill's own
audit-log entry, never to alter opportunity/account/contact data — and even
that is optional, not required to produce a plan.

Approved Salesforce tools for this skill (all read-only usage):

- `search_opportunities` — retrieve the opportunity's stage, amount, close
  date, owner, and any custom fields describing the eval (e.g. a POC
  start/end date field, competitor field).
- `retrieve_semantic_model` — resolve custom object/field names correctly
  before querying, so eval-specific fields aren't guessed at.
- `view_report` — pull an existing Salesforce report on the opportunity or
  account if one already tracks eval milestones or stakeholder engagement.
- `execute_soql_query` — for structured follow-up queries once field names are
  confirmed via the semantic model (e.g. related Contacts/Tasks tied to the
  opportunity).
- `search_contacts` — identify named stakeholders on the account who may need
  to be added to the sign-off list.
- `search_tasks` — surface any logged activities (calls, emails, meetings)
  that hint at eval milestones already in motion.

Do not call any Salesforce write tool (create/update/delete on Opportunity,
Account, Contact, or any custom object). Do not use `add_gtmasst_log` for
anything other than this skill's own audit entry.

## 4. Step-by-step workflow

1. **Confirm inputs.** Verify the opportunity name/ID and target eval end
   date. If a prior discovery-planner or gong-discovery-analysis output was
   pasted in, parse it for already-stated requirements, pain points, and named
   stakeholders.
2. **Resolve fields via `retrieve_semantic_model`.** Before querying,
   confirm the correct field/object names for stage, close date, and any
   custom eval-tracking fields on this org's Salesforce schema.
3. **Pull opportunity context via `search_opportunities`.** Get current
   stage, amount, close date, owner, and any populated eval/POC fields.
4. **Pull stakeholder context via `search_contacts` / `search_tasks`.**
   Identify named contacts on the account and recent activity that suggests
   who has been engaged so far (economic buyer, technical champion,
   security/IT reviewer, etc.).
5. **Check for an existing tracking report via `view_report`,** if the SC/VC
   indicates one exists, rather than reconstructing history from scratch.
6. **Draft success criteria.** For each criterion, state what "pass" looks
   like in observable, measurable terms — not vague aspirations. Assign an
   owner (prospect-side or Workiva-side) and classify the evidence behind it.
7. **Draft the validation timeline.** Sequence steps from kickoff to the
   go/no-go decision, working backward from the target eval end date. Each
   step gets a date and an owner.
8. **Draft sign-off stakeholders.** List every person/role whose approval is
   needed before the eval can be declared passed, distinguishing prospect-side
   from Workiva-side sign-off.
9. **Draft risk factors.** For each risk that could derail the eval (missing
   stakeholder, unclear success criteria, competitor in parallel eval, data
   access blockers, timeline compression), assign likelihood, a mitigation,
   and an evidence classification. Any risk without a clear mitigation must be
   flagged `open_question_validation_required`.
10. **Assemble the output** using the schema in §6, tag every claim per §5,
    and end with the handoff JSON block per §7.

## 5. Source classification & citation rules

Every success criterion and every risk factor must carry exactly one
classification from the six-value taxonomy defined in
[`../core-presales-intelligence/SKILL.md §1`](../core-presales-intelligence/SKILL.md#1-evidence-classification-taxonomy):
`confirmed_customer_statement`, `salesforce_operating_context`,
`verified_workiva_internal_fact`, `inference_working_hypothesis`,
`open_question_validation_required`, `risk_assumption_dependency`. Use the
literal values verbatim.

Where evidence is missing entirely, use one of the two fixed fallback strings
from §2 of the shared skill, verbatim: `"Unknown — requires validation."` or
`"Requires Workiva-source validation."`.

Examples applied to this skill's own output shapes:

- **Success criterion, `salesforce_operating_context`:** "The opportunity
  `Acme Test Corp — Platform Eval` has a custom field `POC_End_Date__c` set to
  2026-11-06 (source: `search_opportunities`)." — a system-of-record fact, not
  a customer quote.
- **Success criterion, `confirmed_customer_statement`:** "Priya Chandran
  (Acme Test Corp, VP Controllership) said on the 2026-09-10 call: 'We need to
  see a full close cycle run through the platform before we sign off.'" —
  directly attributable to the prospect.
- **Risk factor, `risk_assumption_dependency`:** "This validation plan assumes
  Acme Test Corp's IT security team can provision sandbox access within 5
  business days; if provisioning takes longer, the timeline in §6 slips
  accordingly."
- **Risk factor, `open_question_validation_required`:** "Unclear whether a
  competing platform is also in a parallel eval at Acme Test Corp — needs
  validation with the account owner before finalizing the sign-off list."

## 6. Output schema

Produce all four tables. Use `"Unknown — requires validation."` or
`"Requires Workiva-source validation."` in any cell that cannot be filled from
available evidence — never leave a cell blank or invent a value.

**Success Criteria**

| Criterion | Owner | Evidence Classification | How Measured |
|---|---|---|---|
| ... | ... | ... | ... |

**Validation Timeline**

| Step | Date | Owner |
|---|---|---|
| ... | ... | ... |

**Sign-off Stakeholders**

| Name/Role | Side (Prospect/Workiva) | Sign-off Required For |
|---|---|---|
| ... | ... | ... |

**Risk Factors**

| Risk | Likelihood | Mitigation | Evidence Classification |
|---|---|---|---|
| ... | ... | ... | ... |

## 7. Quality checklist

Before returning output, confirm:

- Every success criterion is measurable ("pass" is observable), not a vague
  aspiration like "customer is happy."
- Every success criterion, timeline step, and risk factor has an owner or is
  explicitly flagged as missing one via `open_question_validation_required`.
- Every risk factor has either a concrete mitigation or is tagged
  `open_question_validation_required` — no risk is left with neither.
- Every claim across all four tables carries exactly one of the six evidence
  classifications, or one of the two verbatim fallback strings where evidence
  is absent.
- The validation timeline is internally consistent with the stated target
  eval end date (steps do not extend past it without an explicit note).
- Only synthetic account/person names appear in this document's own examples;
  a real run against a live opportunity uses real Salesforce data but never
  fabricates facts not returned by a tool call.

## 8. Read-only disclaimer

This skill never writes to Salesforce, Gong, Google Drive, or any Workiva
internal system. It only calls query/search/read/get-style tools (§3). Every
plan it produces is a **draft for the SC/VC to review, adjust, and manually
enter into Salesforce or share with the account team** — it does not
autonomously update opportunity fields, create tasks, or notify stakeholders.
The only tool with write semantics this skill may ever call is
`add_gtmasst_log`, and only to append its own audit/activity log entry — never
to alter opportunity, account, or contact data.

## 9. Fallback strings

Use these two strings verbatim wherever a claim cannot be classified or
verified:

- `"Unknown — requires validation."`
- `"Requires Workiva-source validation."`

## 10. MCP / demo-adapter handoff payload

End every run with a single JSON block conforming to
[`../shared/evidence-schema.md`](../shared/evidence-schema.md). Because an
eval plan primarily defines what the demo/POC environment must show, the
`handoff_target` for this skill is `demo-framework-adapter`.

```json
{
  "skill": "evaluation-validation-planner",
  "account_id": "acme-test-corp-001",
  "opportunity_id": "0061-acme-platform-eval",
  "summary": "Validation plan for the Acme Test Corp Platform Eval: five success criteria centered on close-process automation and audit trail visibility, a six-week timeline ending 2026-11-06, four sign-off stakeholders, and three risk factors including one open sandbox-access question.",
  "evidence": [
    {
      "claim": "The opportunity has a custom field POC_End_Date__c set to 2026-11-06.",
      "classification": "salesforce_operating_context",
      "source": "search_opportunities, Opportunity 0061-acme-platform-eval"
    },
    {
      "claim": "Priya Chandran (Acme Test Corp, VP Controllership) said on the 2026-09-10 call: 'We need to see a full close cycle run through the platform before we sign off.'",
      "classification": "confirmed_customer_statement",
      "source": "Gong call 2026-09-10, Priya Chandran"
    }
  ],
  "open_questions": [
    "Unclear whether a competing platform is also in a parallel eval at Acme Test Corp.",
    "Unclear whether IT security sandbox provisioning can complete within 5 business days."
  ],
  "handoff_target": ["demo-framework-adapter"]
}
```

## 11. Fully synthetic worked example

**Opportunity:** `Acme Test Corp — Platform Eval` (`0061-acme-platform-eval`)
**Target eval end date:** 2026-11-06
**Known competitor in eval:** Globex Test Industries' internal build (per
account owner, unconfirmed with prospect)

**Success Criteria**

| Criterion | Owner | Evidence Classification | How Measured |
|---|---|---|---|
| Platform completes one full monthly close cycle using Acme's actual close checklist, end to end. | Sam Okafor (Acme Test Corp, Controller) | `confirmed_customer_statement` | Close cycle run in sandbox produces a final consolidated report matching Acme's manual close output within 2 business days. |
| Audit trail shows every edit to a consolidated figure with user, timestamp, and reason. | Priya Chandran (Acme Test Corp, VP Controllership) | `confirmed_customer_statement` | Reviewer pulls audit log for 3 sample edits during the eval and confirms all three fields are populated. |
| Sandbox environment is provisioned and accessible to Acme's close team within 5 business days of eval kickoff. | Workiva SC (Jordan Rivera) | `salesforce_operating_context` | Provisioning ticket closed and login confirmed by Acme IT within the 5-day window (source: `search_tasks`). |
| Integration with Acme's ERP (system unconfirmed) does not require manual CSV export/import. | Workiva SC | `open_question_validation_required` | Requires confirmation of which ERP Acme runs before an integration method can be tested. |
| Workiva's platform supports the specific CSRD taxonomy tags Acme says it needs. | Workiva SC | `verified_workiva_internal_fact` | Confirm against internal GRC/Documents MCP product documentation before the eval kickoff call. |

**Validation Timeline**

| Step | Date | Owner |
|---|---|---|
| Eval kickoff call — confirm scope, success criteria, and sandbox requirements | 2026-09-22 | Jordan Rivera (Workiva SC) |
| Sandbox provisioned and access confirmed | 2026-09-29 | Workiva IT / Acme IT |
| First close-cycle dry run in sandbox | 2026-10-10 | Sam Okafor (Acme Test Corp) |
| Audit trail review session | 2026-10-17 | Priya Chandran (Acme Test Corp) |
| ERP integration method confirmed and tested | "Unknown — requires validation." | "Unknown — requires validation." |
| Final go/no-go review | 2026-11-06 | Priya Chandran + Jordan Rivera |

**Sign-off Stakeholders**

| Name/Role | Side (Prospect/Workiva) | Sign-off Required For |
|---|---|---|
| Priya Chandran, VP Controllership | Prospect | Overall eval pass/fail decision |
| Sam Okafor, Controller | Prospect | Close-cycle accuracy criterion |
| Acme IT Security (name TBD) | Prospect | "Unknown — requires validation." |
| Jordan Rivera, Workiva SC | Workiva | Technical readiness confirmation before go/no-go |

**Risk Factors**

| Risk | Likelihood | Mitigation | Evidence Classification |
|---|---|---|---|
| Sandbox provisioning slips past 5 business days, compressing the remaining timeline. | Medium | Escalate provisioning ticket at day 3 if not yet closed; flag to account owner. | `risk_assumption_dependency` |
| Acme is running a parallel eval against a Globex Test Industries internal build. | Unknown | Confirm directly with Priya Chandran whether a competing eval is in progress. | `open_question_validation_required` |
| ERP integration approach is untested because Acme's specific ERP has not been confirmed. | Medium | Ask Sam Okafor to confirm ERP system before the first dry run on 2026-10-10. | `open_question_validation_required` |

```json
{
  "skill": "evaluation-validation-planner",
  "account_id": "acme-test-corp-001",
  "opportunity_id": "0061-acme-platform-eval",
  "summary": "Validation plan for the Acme Test Corp Platform Eval: five success criteria anchored on a full close-cycle dry run and audit-trail review, a timeline running 2026-09-22 through the 2026-11-06 go/no-go, four sign-off stakeholders, and three risk factors including an unconfirmed parallel competitor eval and an unconfirmed ERP integration path.",
  "evidence": [
    {
      "claim": "Sam Okafor (Acme Test Corp, Controller) requires the platform to complete one full monthly close cycle using Acme's actual close checklist.",
      "classification": "confirmed_customer_statement",
      "source": "Gong call 2026-09-10, Sam Okafor"
    },
    {
      "claim": "Priya Chandran (Acme Test Corp, VP Controllership) requires the audit trail to show every edit with user, timestamp, and reason.",
      "classification": "confirmed_customer_statement",
      "source": "Gong call 2026-09-10, Priya Chandran"
    },
    {
      "claim": "The opportunity 0061-acme-platform-eval has a target eval end date of 2026-11-06.",
      "classification": "salesforce_operating_context",
      "source": "search_opportunities, Opportunity 0061-acme-platform-eval"
    }
  ],
  "open_questions": [
    "Which ERP system does Acme Test Corp run, and does it require a manual CSV export/import to integrate?",
    "Is Acme Test Corp running a parallel eval against a Globex Test Industries internal build?",
    "Who on Acme IT Security must sign off, and on what specific criterion?"
  ],
  "handoff_target": ["demo-framework-adapter"]
}
```
