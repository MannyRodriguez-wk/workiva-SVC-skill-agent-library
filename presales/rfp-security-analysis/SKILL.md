---
name: rfp-security-analysis
description: "Analyzes each security/compliance question in a customer or prospect RFP or security questionnaire against Workiva's documented internal security posture (via the internal Workiva GRC/Documents MCP, read-only), drafts a proposed answer for each question, and explicitly flags any question where Workiva's documented posture doesn't clearly cover the ask. Use when the user says: 'analyze this RFP's security section', 'answer these security questionnaire items', 'check our posture against [question]', 'draft responses to this security questionnaire', or 'does Workiva's documented posture cover this RFP question'."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# RFP Security/Compliance Question Analysis

Given a customer/prospect RFP or standalone security questionnaire, this skill walks each security/compliance question, checks it against Workiva's documented internal security posture, drafts a proposed answer, and explicitly flags any question the documented posture does not clearly cover. It never invents or assumes a compliance posture Workiva does not have documented evidence for.

This skill is part of the Workiva presales skill family. It shares conventions with:

- `../core-presales-intelligence/SKILL.md` — shared presales conventions, evidence taxonomy, read-only constraint, and orchestration patterns.
- `../shared/evidence-schema.md` — the evidence classification taxonomy and handoff JSON schema referenced throughout this file.

## 1. Purpose & Trigger Phrases

**Purpose:** Given a set of RFP or security-questionnaire questions, produce a draft answer for each one that is explicitly grounded in Workiva's documented internal security/compliance posture — and flag, rather than guess at, any question the documentation doesn't clearly cover.

**Trigger phrases** (non-exhaustive — use judgment for close paraphrases):
- "analyze this RFP's security section"
- "answer these security questionnaire items"
- "check our posture against [question]"
- "draft responses to this security questionnaire"
- "does Workiva's documented posture cover this RFP question"
- "review the compliance questions in this RFP"

## 2. Required / Optional Inputs

**Required:**
- The RFP or security-questionnaire text, or a list of discrete security/compliance questions to answer.

**Optional:**
- Target product line(s) the RFP concerns (e.g., Wdesk, ESG Reporting, Controls Management, Financial Reporting).
- Known customer-stated compliance framework(s) of interest (e.g., SOC 2 Type II, ISO 27001, FedRAMP, HIPAA, GDPR, NIST 800-53).
- Account/opportunity name and Salesforce IDs, for handoff payload context.
- Any prior `account-opportunity-brief` or `gong-discovery-analysis` output that mentions security concerns the customer has already raised.

## 3. Source Retrieval Guidance (Tool-Agnostic)

This skill's factual claims about Workiva's own security posture must come from **the Workiva internal GRC/Documents MCP** — a read-only, internal-only demo/reference environment described in `../core-presales-intelligence/SKILL.md` §4. This is a **special-access internal system, not part of general enterprise Claude access** — it is not guaranteed to be available or authorized in every environment this skill runs in. Treat its availability as a precondition to check, not an assumption.

1. For each security/compliance question, query the internal GRC/Documents MCP's read-only query/search/read tools for the relevant control, policy, or audit documentation (e.g., access-control policy, encryption-at-rest/in-transit documentation, current SOC 2 report scope, ISO 27001 certificate scope, incident-response policy, subprocessor list, data residency documentation).
2. Only treat a claim about Workiva's posture as `verified_workiva_internal_fact` if a specific internal document, control ID, or policy was actually retrieved and cited. Never default to this classification from general knowledge or prior training data about "typical" Workiva certifications.
3. **If the internal GRC/Documents MCP is not available or not authorized in the current session, the skill must say so explicitly** — do not proceed as if the documentation were checked. In that case, fall back to flagging **every question** in the batch as `open_question_validation_required` with the fallback string `"Requires Workiva-source validation."`, rather than guessing at an answer from general knowledge.
4. Optional read-only Salesforce lookups (`search_opportunities`, `search_accounts`) may be used only to populate handoff-payload context (account/opportunity IDs) — never to answer a security question.
5. Never call any write/create/update/delete tool against the GRC/Documents MCP, Salesforce, or any other connector. See §8.

## 4. Step-by-Step Workflow

1. **Ingest the RFP/questionnaire.** Parse the input into a discrete, numbered list of individual security/compliance questions. Preserve the customer's original question numbering where provided.
2. **Check internal GRC/Documents MCP availability.** Confirm the tool is reachable and authorized in this session. If not, immediately produce the fallback output described in §3.3 and §9 for every question, and stop further per-question research.
3. **For each question:**
   a. Identify the specific control, policy, certification, or capability the question is actually asking about.
   b. Query the internal GRC/Documents MCP for the most specific matching documentation.
   c. If a clear, specific match is found, draft a proposed answer grounded in that document, citing the control/policy by name/ID.
   d. If no clear match is found, or the match only partially covers the question, do not extrapolate — use the appropriate fallback string and mark the question as needing security-team review.
4. **Classify every drafted answer** using the shared evidence taxonomy (§5) — defaulting to `verified_workiva_internal_fact` only when step 3(c) actually occurred.
5. **Assemble the output table** (§6), one row per question.
6. **Run the quality checklist** (§7) before finalizing.
7. **Emit the human-readable table plus the MCP/demo-adapter handoff payload** (§10).

## 5. Source Classification & Citation Rules

Apply the shared evidence taxonomy from `../shared/evidence-schema.md` to every drafted answer:

| Classification | Applies when the answer's basis is... |
|---|---|
| `confirmed_customer_statement` | A direct quote/paraphrase of the customer's own question or stated requirement (used to clarify what's being asked, not to answer it). |
| `salesforce_operating_context` | Deal-context facts (product line, opportunity stage) relevant to scoping which Workiva product the question applies to. |
| `verified_workiva_internal_fact` | A specific control, policy, or certification document was actually retrieved from the internal GRC/Documents MCP and cited by name/ID. This is the only classification that should ever ground a "yes, Workiva does X" answer. |
| `inference_working_hypothesis` | A reasonable but unconfirmed extrapolation from adjacent documented controls (e.g., inferring encryption-in-transit coverage from a general security-architecture doc that doesn't name the specific protocol asked about). Must be labeled as a hypothesis, never presented as a confirmed answer. |
| `open_question_validation_required` | No internal documentation was found (or the GRC/Documents MCP was unavailable) covering this specific question. |
| `risk_assumption_dependency` | The draft answer depends on an assumption (e.g., "assuming this applies to the SaaS-hosted deployment model, not on-prem") that, if wrong, would change the answer. |

Every drafted answer must cite the specific control/policy/document it is based on, or state plainly that none was found. Never leave the source/citation field blank.

## 6. Output Schema

| RFP Question | Draft Answer | Source Control/Policy | Evidence Classification | Needs Security-Team Review (yes/no) |
|---|---|---|---|---|
| (verbatim or paraphrased question, preserving original numbering) | (drafted answer, or fallback string) | (specific control/policy/doc name+ID, or "None found — GRC/Documents MCP returned no match" / "GRC/Documents MCP unavailable this session") | (one of the six taxonomy values) | (yes/no — see §7 for the rule) |

## 7. Quality Checklist

Before finalizing the table:

- [ ] Never invents a compliance certification or control Workiva doesn't hold or hasn't documented — every "yes" answer traces to a retrieved document.
- [ ] Flags every answer sourced from `inference_working_hypothesis` or `risk_assumption_dependency` as needing security-team review, not just `open_question_validation_required` ones.
- [ ] No answer is submitted (i.e., presented as final) without a "Needs Security-Team Review = yes" flag where the classification is anything other than `verified_workiva_internal_fact`.
- [ ] Every row's Source Control/Policy field is non-blank — including rows where nothing was found.
- [ ] If the internal GRC/Documents MCP was unavailable for the session, this is stated once, clearly, at the top of the output — not silently implied by every row being flagged.
- [ ] Question numbering/order matches the original RFP so the SC/VC (and eventual security-team reviewer) can cross-reference easily.

## 8. Read-Only / No-Write Disclaimer

This skill is **read-only and non-authoritative**. It never submits an RFP response, uploads a document, or writes to any system — including the internal GRC/Documents MCP, Salesforce, or any RFP-management tool. Every drafted answer in this skill's output is a **draft for a human to review and manually submit**, and any answer not classified as `verified_workiva_internal_fact` should be treated as provisional until Workiva's security team explicitly signs off. This skill does not have authority to represent Workiva's compliance posture to a customer on its own.

## 9. Fallback Strings

Use these exact strings whenever a value cannot be confirmed:

- `"Unknown — requires validation."` — for any question whose subject matter isn't security/compliance-specific and simply has no available answer basis.
- `"Requires Workiva-source validation."` — the primary fallback for this skill: use for any question about Workiva's own security/compliance posture, certification, or control that could not be confirmed against a retrieved internal GRC/Documents MCP document, or for every question in the batch if the GRC/Documents MCP was unavailable this session.

## 10. MCP/Demo-Adapter Handoff Payload

Emit this JSON block at the end of every run. Structure follows `../shared/evidence-schema.md`; `handoff_target` is fixed to `workiva-mcp-adapter` for this skill since its output routes back to the internal GRC/Documents environment for security-team follow-up, not to the demo-framework-adapter.

```json
{
  "skill": "rfp-security-analysis",
  "account_id": "string | null",
  "opportunity_id": "string | null",
  "summary": "One-paragraph human-readable summary of the RFP security analysis run.",
  "evidence": [
    {
      "claim": "string — a specific claim from a drafted answer, or a fallback string",
      "classification": "confirmed_customer_statement | salesforce_operating_context | verified_workiva_internal_fact | inference_working_hypothesis | open_question_validation_required | risk_assumption_dependency",
      "source": "string — specific control/policy/document name+ID, or explicit statement of what was checked and came up empty"
    }
  ],
  "open_questions": [
    "list of RFP question strings needing security-team validation before submission"
  ],
  "handoff_target": ["workiva-mcp-adapter"],
  "questions_answered": 0,
  "questions_flagged_for_security_review": 0,
  "grc_mcp_available_this_session": true
}
```

## 11. Worked Example — Northwind Test Holdings (Fully Synthetic)

> All names, questions, policy titles, and control IDs below are fabricated for illustration only. None refer to real Workiva documentation.

**Input assumed:** Northwind Test Holdings' RFP, Section 4 ("Security & Compliance"), five questions.

| RFP Question | Draft Answer | Source Control/Policy | Evidence Classification | Needs Security-Team Review |
|---|---|---|---|---|
| Q4.1: "Does the vendor maintain a current SOC 2 Type II report covering the proposed hosted environment?" | Workiva maintains a current SOC 2 Type II report covering the multi-tenant SaaS platform, renewed annually, per internal policy `SEC-POL-014 (SOC 2 Type II Attestation Program)` retrieved from the internal GRC/Documents MCP. | `SEC-POL-014 — SOC 2 Type II Attestation Program` (internal GRC/Documents MCP) | verified_workiva_internal_fact | no |
| Q4.2: "Is customer data encrypted at rest using AES-256 or equivalent?" | Workiva's data-at-rest encryption standard specifies AES-256 for all customer content storage, per `SEC-CTRL-022 (Data-at-Rest Encryption Standard)` retrieved from the internal GRC/Documents MCP. | `SEC-CTRL-022 — Data-at-Rest Encryption Standard` (internal GRC/Documents MCP) | verified_workiva_internal_fact | no |
| Q4.3: "Does the vendor hold ISO 27001 certification specifically for the ESG Reporting module's data pipeline?" | The internal GRC/Documents MCP returned Workiva's general-platform ISO 27001 certificate scope document, but it does not name the ESG Reporting module's data pipeline specifically — coverage for this exact sub-component is not confirmed. | `SEC-CERT-008 — ISO 27001 Certificate Scope (platform-level)` (internal GRC/Documents MCP) — partial match only | inference_working_hypothesis | yes |
| Q4.4: "What is the vendor's documented breach notification SLA to customers?" | Requires Workiva-source validation. | None found — GRC/Documents MCP returned no matching policy for customer-facing breach notification SLA timing. | open_question_validation_required | yes |
| Q4.5: "Does the vendor support customer-managed encryption keys (BYOK) for this product line?" | Requires Workiva-source validation. | GRC/Documents MCP unavailable this session (connection not authorized) — flagged per fallback rule in §3.3; no per-question research was possible for this or any other question in this batch beyond what had already been retrieved before the outage. | open_question_validation_required | yes |

**Handoff payload:**

```json
{
  "skill": "rfp-security-analysis",
  "account_id": "northwind-test-holdings-001",
  "opportunity_id": "0071-northwind-esg-rfp",
  "summary": "Northwind Test Holdings' RFP Section 4 asks five security/compliance questions. Workiva's documented SOC 2 Type II and AES-256 encryption-at-rest posture directly cover Q4.1 and Q4.2. ISO 27001 scope for the ESG Reporting data pipeline specifically (Q4.3), the breach-notification SLA (Q4.4), and BYOK support (Q4.5) are not confirmed by retrieved documentation and require security-team validation before submission.",
  "evidence": [
    {
      "claim": "Workiva maintains a current SOC 2 Type II report covering the multi-tenant SaaS platform.",
      "classification": "verified_workiva_internal_fact",
      "source": "SEC-POL-014 — SOC 2 Type II Attestation Program (internal GRC/Documents MCP)"
    },
    {
      "claim": "Workiva's data-at-rest encryption standard specifies AES-256 for all customer content storage.",
      "classification": "verified_workiva_internal_fact",
      "source": "SEC-CTRL-022 — Data-at-Rest Encryption Standard (internal GRC/Documents MCP)"
    },
    {
      "claim": "Workiva's ISO 27001 certificate scope is documented at the platform level; specific coverage of the ESG Reporting module's data pipeline is not separately confirmed.",
      "classification": "inference_working_hypothesis",
      "source": "SEC-CERT-008 — ISO 27001 Certificate Scope (platform-level), internal GRC/Documents MCP — partial match only"
    },
    {
      "claim": "Requires Workiva-source validation.",
      "classification": "open_question_validation_required",
      "source": "No matching policy found in internal GRC/Documents MCP for customer-facing breach notification SLA."
    },
    {
      "claim": "Requires Workiva-source validation.",
      "classification": "open_question_validation_required",
      "source": "Internal GRC/Documents MCP was unavailable/unauthorized this session; BYOK support could not be checked."
    }
  ],
  "open_questions": [
    "Does Workiva's ISO 27001 certification scope specifically cover the ESG Reporting module's data pipeline, or only the general platform?",
    "What is Workiva's documented breach notification SLA to customers?",
    "Does Workiva support customer-managed encryption keys (BYOK) for the ESG Reporting product line?"
  ],
  "handoff_target": ["workiva-mcp-adapter"],
  "questions_answered": 5,
  "questions_flagged_for_security_review": 3,
  "grc_mcp_available_this_session": false
}
```
