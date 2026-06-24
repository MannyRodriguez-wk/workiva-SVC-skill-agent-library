---
name: monday-impact-reporter
description: >
  Generates a QBR-ready impact narrative for Demo Engineering / Presales SC by
  pulling delivered work from all four Monday.com boards and translating it into
  business value. Use when user says "prep my QBR", "impact report", "what did
  we deliver this quarter", "leadership report", "how many demos/events did we
  support", or any request to summarize team output and impact for leadership.
metadata:
  author: Demo Engineering / Presales SC
  version: 2.0.0
  demo_ops_board: "7514031773"
  events_board: "9393422722"
  slack_dm_board: "18402787769"
  consensus_board: "8475747685"
---

# monday-impact-reporter

Pull completed work from all four boards. Translate it into a leadership narrative.
Not a spreadsheet — a story with evidence, organized by type and impact.

---

## Step 1: Confirm Reporting Window

If not specified, ask: "What time period? (e.g., Q1 2026, last 90 days, YTD)"
Default to current quarter if unspecified.

---

## Step 2: Pull Completed Work — Board by Board

### Board A: Demo Ops Request Form (7514031773)
Filter: status__1 = "Done" (label index 1)
Also include group: completed_tasks_mkm1nzd (Completed Tasks)
Collect per item: name, short_text__1 (stakeholder), numbers__1 (actual hours),
  color_mm22mcnw (OKR alignment), board_relation_mm19b49s (aligned OKR)

### Board B: Event Requests (9393422722)
Filter: group = "Past Events" (group_mksdy82d) OR color_mksdddc1 = "Assigned"
Collect per item: name, color_mks089rz (event type), formula_mksd1mqk (Total SC Hours — pre-calculated!),
  numeric_mks07w5k (# SCs), timerange_mks0wmgk (dates), dropdown_mks0g1gq (support type),
  multi_selectaxineucx (territory), dropdown_mksdtzef (SCs assigned)

### Board C: Slack DM Requests (18402787769)
WARNING: No top-level status column. Use date filter only (date_mm15rjan within window).
Collect per item: name, color_mm15cyf0 (request type), text_mm1518n0 (sender)
NOTE: These numbers will be incomplete until a Status column is added to this board.

### Board D: Consensus Management (8475747685)
Filter: status_mkn5qr85 = "Done" OR group = "Finished Requests" (group_mkp6kehs)
Collect per item: name, single_select__1 (request type), multi_select_mkn44fda (vertical),
  long_text_mkn4259e (impact statement), duration_mkv6wb1f (time tracked)

---

## Step 3: Value Translation

### Demo Ops (Demo Builds)
Each completed demo build:
- Estimated calls supported: 4–10 (use 7 as midpoint)
- SE prep hours saved per call: 3 hrs
- Total uplift = items × 7 calls × 3 hrs

### Events
USE THE FORMULA VALUE DIRECTLY — formula_mksd1mqk already = SCs × daily hrs × event days.
Sum formula_mksd1mqk across all past events. This is your real SC hour commitment number.

### Consensus Videos
Each completed video:
- New Content: ~10 calls supported, 2 hrs saved/call
- Updates to Existing: ~8 calls supported, 1.5 hrs saved/call
- Video Translation: ~6 calls supported, 1 hr saved/call (per language)

### Slack DM (Ad Hoc)
Count only — no hour calculation (no time tracking on this board).

---

## Step 4: Generate the Narrative

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
DEMO ENGINEERING — IMPACT REPORT
[Time Period]  |  Generated [Today's Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

BY THE NUMBERS
• [N] Demo Builds completed
• [N] Events staffed  |  [N] total SC hours committed (calculated)
• [N] Consensus videos delivered  |  [N] new, [N] updates, [N] translations
• [N] Ad hoc Slack requests handled
• ~[N] total sales calls supported (estimated)
• ~[N] hours of SE prep time saved (demo uplift)

TOP VERTICALS (from Consensus + Demo Ops)
1. [Vertical] — [N] assets, [N] calls supported
2. [Vertical] — [N] assets, [N] calls supported
3. [Vertical] — [N] assets, [N] calls supported

EVENTS SUMMARY
[N] events across [territories]. Total SC commitment: [N] hours.
Breakdown: [N] Trade Shows, [N] Conferences, [N] Webinars
Top event: [Name] — [N] SCs, [N] days, [territory]

STRATEGIC ALIGNMENT (Demo Ops OKR tags)
• Scale Demo Delivery & Improve Efficiency: [N] items
• Increase Visibility Between Demo Activity & Tech Qualification: [N] items
• Integrate AI Into Demo Operations Workflows: [N] items
• Achieve 100% Certification & Align to Enterprise Standards: [N] items

IMPACT HIGHLIGHTS (from Consensus impact field)
[Pull 3–5 strongest statements from long_text_mkn4259e. Paraphrase into 1-sentence bullets.]
• [Impact highlight 1]
• [Impact highlight 2]
• [Impact highlight 3]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 5: Data Quality Flag

Always append:
```
DATA QUALITY NOTES
• Slack DM board has no Status column — [N] requests included by date only (may include in-progress items)
• [N] Consensus items have no Impact statement — narrative highlights may be incomplete
• [N] Demo Ops items have no Actual Time logged — hour totals estimated
• [N] Consensus items have no Vertical set — excluded from vertical breakdown
```

---

## Step 6: Offer Follow-Ups

After displaying:
- "Want me to create this as a Monday.com Doc in your workspace?"
- "I can format this as slide-ready bullet points."
- "Want me to run a board audit first to improve these numbers?"
