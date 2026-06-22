---
name: monday-board-auditor
description: >
  Audits all four Demo Engineering Monday.com boards for data quality issues:
  missing fields, stale items, unlinked deliverables, and items that can't be
  counted in QBR impact reports. Use when user says "audit our boards", "what's
  stale", "board health check", "clean up Monday", "what items are missing a field",
  or before running an impact report. Covers Demo Ops, Events, Slack DM, and
  Consensus Management boards.
metadata:
  author: Demo Engineering / Presales SC
  version: 2.0.0
  demo_ops_board: "7514031773"
  events_board: "9393422722"
  slack_dm_board: "18402787769"
  consensus_board: "8475747685"
---

# monday-board-auditor

Scan all four boards. Surface what's broken before leadership asks.

---

## Step 1: Pull Items from All Four Boards

For each board, call get_board_items_page with includeColumns: true, limit: 500.

Board A: Demo Ops (7514031773) — focus on active groups (External Requests, Internal Projects)
Board B: Events (9393422722) — focus on Unassigned and Assigned Events groups
Board C: Slack DM (18402787769) — all items
Board D: Consensus (8475747685) — Active Requests and Future Requests groups

---

## Step 2: Run Checks Per Board

### Demo Ops (7514031773)
- CRITICAL: status__1 empty → can't be counted as done
- CRITICAL: short_text2__1 (Request Title) empty → unnamed items are invisible in reports
- MEDIUM: numbers__1 (Actual Time) = 0 after Done → effort totals will be wrong
- MEDIUM: status__1 = "Working on it" AND last updated > 14 days → stale in-progress
- LOW: board_relation_mm19b49s empty AND color_mm22mcnw empty → not linked to any OKR

### Event Requests (9393422722)
- CRITICAL: numeric_mks07w5k (# SCs) = 0 → Total SC Hours formula will return 0
- CRITICAL: numeric_mksdyb5h (daily hours) = 0 → same issue
- CRITICAL: timerange_mks0wmgk empty → can't calculate event length or sort by date
- MEDIUM: dropdown_mksdtzef (SC Assigned) empty AND color_mksdddc1 = "Assigned" → assigned but no SC named
- MEDIUM: color_mksdddc1 = "Finding Resources" AND event start < 14 days away → urgent staffing gap
- LOW: multi_selectaxineucx (Territory) empty → can't report by region

### Slack DM Requests (18402787769)
- STRUCTURAL GAP: No top-level Status column exists on this board.
  Flag prominently: "Slack DM board is missing a Status column. Without it, completed
  requests can't be filtered and won't appear in impact reports. Recommend adding one."
  Offer to create it: create_column on board 18402787769, type: status,
  title: "Status", suggested labels: Done, In Progress, Not Started
- MEDIUM: text_mm1518n0 (Sender) empty → can't attribute request to anyone
- MEDIUM: color_mm15cyf0 (Type) empty → can't categorize for reporting
- MEDIUM: Items older than 30 days with no update → likely forgotten/stale

### Consensus Management (8475747685)
- CRITICAL: multi_select_mkn44fda (Solution/Vertical) empty → excluded from vertical breakdown
- CRITICAL: long_text_mkn4259e (Impact) empty → no narrative available for QBR
- MEDIUM: status_mkn5qr85 = "Working on it" AND last updated > 21 days → stale
- MEDIUM: duration_mkv6wb1f (Time Tracking) not started on active items → no actual time data
- LOW: date_mkn5h3n9 (Due Date) empty on Active Requests → no deadline visibility

---

## Step 3: Generate the Audit Report

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
BOARD HEALTH REPORT — ALL 4 BOARDS
Audited: [Today's Date]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

OVERVIEW
Demo Ops:        [N] active items  |  [N] critical gaps
Event Requests:  [N] active items  |  [N] critical gaps
Slack DM:        [N] active items  |  STRUCTURAL GAP (no Status column)
Consensus:       [N] active items  |  [N] critical gaps
QBR Readiness Score: [X/10]

STRUCTURAL ISSUE (fix first)
Slack DM Requests board is missing a Status column.
This means none of its [N] items can be marked Done or filtered for impact reporting.
→ Want me to add a Status column to this board now?

CRITICAL — Fix Before Next QBR
Demo Ops:
  • [N] items with no Status set
  • [N] items with no Request Title
Events:
  • [N] events missing SC count or daily hours (Total Hours formula = 0)
  • [N] upcoming events still in "Finding Resources" → staffing risk
Consensus:
  • [N] items with no Vertical
  • [N] items with no Impact statement

MEDIUM — Fix for Better Reporting
  • [N] Demo Ops items stale in progress (>14 days no update): [names]
  • [N] Consensus items stale in progress (>21 days): [names]
  • [N] Events assigned but SC name missing
  • [N] Slack DM items with no sender or type

NICE TO HAVE
  • [N] Demo Ops items not linked to any OKR
  • [N] Events missing territory
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

---

## Step 4: Offer Fixes

1. "Want me to add a Status column to the Slack DM board now?" (highest value action)
2. "Want me to walk through the critical Consensus items and prompt for missing Impact statements?"
3. "I can add a comment to each stale item asking for a status update."

For adding Status to Slack DM:
  create_column, board 18402787769, title: "Status", type: status
  Suggested labels: Done, In Progress, Not Started, Waiting on Requestor

---

## Pre-QBR Shortcut

If user says "prep for QBR" and hasn't audited recently:
Proactively offer: "Before I generate the impact report, want a 30-second board health
check? It'll make the numbers more accurate."
If yes → run audit, surface critical gaps, then hand off to monday-impact-reporter.
