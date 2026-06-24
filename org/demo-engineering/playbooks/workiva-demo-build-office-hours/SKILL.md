---
name: workiva-demo-build-office-hours
version: 1.0.0
description: |
  Workiva Demo Build Office Hours — YC-style forcing questions for designing
  polished, in-platform Workiva demo packages. Produces a structured Demo Build
  Design Doc covering: use case focus, audience profile, source dataset design,
  platform asset plan (Presentations, Reporting Documents, Source Spreadsheets),
  narrative arc, wow moments, and setup instructions. Use when someone says
  "help me build a demo", "demo build office hours", "I want to create a Workiva
  demo package", "design a demo for [persona/industry/use case]", "what should
  my demo include", or any request to plan a new Workiva in-platform demo.
  Proactively invoke this skill when the user is scoping or brainstorming a new
  demo — before any assets are built. Use before /plan-ceo-review,
  /plan-eng-review, or /plan-design-review for demo build planning.
---

# Workiva Demo Build Office Hours

A structured forcing-question session to design a complete, polished Workiva
in-platform demo package before you touch a single file. Inspired by YC Office
Hours — short, sharp questions that expose what you're really building and why.

## Session Goal

Produce a **Demo Build Design Doc** that captures:
- Who this demo is for and what it must prove
- The source dataset(s) and how they power every asset
- A precise asset plan (Presentation, Reporting Document, Source Spreadsheet)
- The narrative arc and the 1–2 "wow" moments
- Setup instructions (what to prep, what to click, what to show)

No asset gets built until this doc exists. The doc is the demo's source of truth.

---

## Phase 0: Orientation Check

Before asking anything, assess what the user has already provided.

If they've given you a use case, persona, industry, or partial spec — extract
what you already know. Populate those fields silently. Only ask about gaps.

If the request is blank ("help me build a demo") — proceed to Phase 1 in full.

---

## Phase 1: Six Forcing Questions

Ask ONE question at a time. Wait for the answer before proceeding. Do not
batch questions. Do not give the user a form to fill out.

---

### Q1 — Use Case Specificity (The "Who's Desperate?" Question)

**What you're surfacing:** Is this demo solving a real, felt pain? Or is it
a generic "here's Workiva" walkthrough? Generic demos don't win deals.

Ask:
> "Who is the main persona sitting across the table when you'd show this — and
> what specific problem are they trying to solve right now that keeps them up
> at night?"

Press for specificity if vague. "A CFO at an enterprise company" is not enough.
"A VP Controller at a manufacturing company who has 14 entities consolidating
into one report in Excel and it breaks every close" is a persona.

Probe: What's the status quo? What are they doing today without Workiva?
What's the cost of that status quo (time, risk, embarrassment)?

Don't move on until you have: **persona + industry + specific pain**.

---

### Q2 — The Proof Point (The "What Must They Believe?" Question)

**What you're surfacing:** What is the single belief this demo must install in
the buyer's mind? Every asset, every click, every dataset choice should serve
that belief.

Ask:
> "If this demo works perfectly, what's the one sentence the buyer says to
> their colleague after the meeting? What belief did you install?"

Examples of strong proof points:
- "Workiva made our consolidation 10x faster and our auditors actually love it"
- "I can trust the number on the slide because I can trace it to the source"
- "My team can collaborate on the same document without version chaos"

Weak proof points: "It's a platform for connected reporting" — that's a
category claim, not a belief.

Don't move on until you have: **one crisp belief statement**.

---

### Q3 — The Dataset (The "What Powers Everything?" Question)

**What you're surfacing:** The dataset is the spine of the demo. If it's fake,
generic, or doesn't match the persona's world, the demo loses credibility
the moment a buyer asks "what's in there?"

Ask:
> "What source data should power this demo? Walk me through the scenario —
> what company, what fiscal structure, what kinds of numbers, and why does
> this dataset make the demo feel real to your buyer?"

Press on:
- Does the dataset reflect the persona's actual reporting structure?
- Should it have intentional messiness (e.g., a formula error that Workiva
  surfaces)? Or is it pristine to show polish?
- How many entities / sheets / data dimensions?
- What's the story the data tells? (Revenue growth + cost pressure?
  Multi-entity consolidation? Audit trail complexity?)

Output: **Dataset narrative + structure sketch**.

---

### Q4 — The Asset Plan (The "What Do They See?" Question)

**What you're surfacing:** A Workiva demo package has three asset types.
Each serves a different moment in the demo. Knowing which you need — and why —
prevents over-building.

Ask:
> "Walk me through your demo flow. At which moments do you need to be IN
> Workiva showing something? What does the buyer see on screen at each
> moment — a spreadsheet, a document, a presentation, or something linked
> across all three?"

Map answers to:

| Asset Type | Workiva Component | Best Demo Moment |
|---|---|---|
| Source Spreadsheet | Wdata / Workiva Sheets | "Here's the live source of truth" |
| Reporting Document | Workiva Docs | "Here's the linked, auditable output" |
| Presentation | Workiva Slides | "Here's the board-ready deliverable" |

Not every demo needs all three. Ask what the minimum set is that tells the
full story.

Output: **Asset list with purpose for each**.

---

### Q5 — The Wow Moment (The "What Makes Them Lean Forward?" Question)

**What you're surfacing:** Every great demo has 1–2 moments where the buyer
visibly reacts. These moments are engineered, not accidental. If you can't
name them before you build, you won't build them in.

Ask:
> "What's the one moment in this demo where you want the buyer to audibly
> say 'wait, how did it do that?' — what do you click, what changes, and
> why is it surprising?"

Press for a second wow moment if they have one.

Common Workiva wow moments to probe:
- Changing a source number and watching it cascade into the slide + doc live
- Showing the audit trail / change log on a number
- Rolling forward a report and having all links update
- Side-by-side collaboration view
- Sign-off / certification workflow
- Connected report with a drill-down

Output: **Wow moment 1 (required) + Wow moment 2 (optional)**.

---

### Q6 — Setup & Constraints (The "What Can Actually Ship?" Question)

**What you're surfacing:** Demo packages that can't be set up in under 30
minutes by a new SE don't get used. Setup complexity kills reuse.

Ask:
> "Who needs to be able to run this demo after you build it — just you, or
> other SEs on the team? And what constraints exist: time to set up,
> Workiva org access, anything that could block someone from using it?"

Press on:
- Does the org need specific modules enabled?
- Is this a sandbox / demo org or a customer-facing environment?
- What's the maximum acceptable setup time?
- Should the demo be fully pre-built (just open and present) or partially
  live (SE assembles it during the call)?

Output: **Setup constraint profile**.

---

## Phase 2: Premise Challenge

After the six questions, run a brief premise challenge before writing the doc.

State back your understanding of the demo in one paragraph. Then challenge
three things:

1. **Is the persona desperate enough?** If the persona could "live with"
   the status quo, this demo won't create urgency. Push: is there a sharper
   persona or a higher-stakes moment?

2. **Is the proof point differentiated?** Can a competitor claim the same
   belief? If yes, what's the Workiva-specific angle that makes this
   undeniable?

3. **Is the dataset realistic enough to survive a hard question?**
   If a buyer asks "where did these numbers come from?" — does the dataset
   have a credible answer? Probe for a tighter industry/scenario fit.

Ask the user to confirm, adjust, or push back before proceeding to the doc.

---

## Phase 3: Write the Demo Build Design Doc

Once Phase 2 is confirmed, produce the full **Demo Build Design Doc** in this
structure. Write it as a clean markdown document.

```
# Demo Build Design Doc
**Use Case:** [one-line label]
**Version:** 1.0  |  **Date:** [today]  |  **Owner:** [user's name if known]

---

## 1. Persona & Pain
- **Primary Persona:** [title, industry, company profile]
- **Status Quo Pain:** [what they do today and why it hurts]
- **Cost of Status Quo:** [time / risk / embarrassment — be specific]

## 2. Proof Point
> "[The single belief this demo must install — one sentence]"

## 3. Dataset Design
- **Scenario:** [company name, industry, fiscal structure]
- **Structure:** [entities, sheets, dimensions]
- **Data Narrative:** [the story the data tells]
- **Intentional Messiness (if any):** [formula error? missing data? audit issue?]
- **Source Files Needed:** [list: CSV / XLSX / manual entry]

## 4. Asset Plan
| Asset | Workiva Component | Purpose in Demo | Build Priority |
|---|---|---|---|
| [name] | [component] | [what it proves] | [1/2/3] |

## 5. Demo Narrative Arc
**Opening hook:** [how the demo starts — what problem is set up]
**Act 1:** [first platform moment — what is shown]
**Act 2:** [second platform moment — what deepens the story]
**Wow Moment 1:** [exact action + why it lands]
**Wow Moment 2 (if applicable):** [exact action + why it lands]
**Close:** [how the demo ends — what belief is confirmed]

## 6. Setup Instructions
**Org / Environment:** [sandbox, demo org, etc.]
**Estimated Setup Time:** [X minutes for a new SE]
**Pre-requisites:**
- [ ] [module enabled / access granted / etc.]
**Build Steps:**
1. [step]
2. [step]
**Reset Instructions:** [how to reset the demo to starting state]

## 7. Open Questions / Risks
- [anything unresolved from the session]

## 8. Recommended Next Steps
- [ ] Build dataset: [specific file + structure]
- [ ] Build [Asset 1]: [Workiva component + key content]
- [ ] Build [Asset 2]: [Workiva component + key content]
- [ ] Test wow moment 1: [verify the cascade / link / workflow]
- [ ] Dry-run with [teammate] before first use
```

---

## Phase 4: Next-Skill Recommendations

After delivering the doc, recommend the natural next step based on what's
most needed:

- **Asset complexity is high** → suggest `/plan-ceo-review` (SELECTIVE
  EXPANSION mode) to stress-test whether the scope is right before building
- **UI/UX of the demo flow needs refinement** → suggest `/plan-design-review`
  to pressure-test the visual narrative and layout decisions
- **Dataset or Workiva platform setup is technically complex** → suggest
  `/plan-eng-review` to lock in the build architecture before starting
- **Ready to build immediately** → recommend starting with the dataset
  (it's the dependency everything else needs), then the Source Spreadsheet,
  then Reporting Document, then Presentation

Always close with:
> "The design doc is your demo's source of truth. Every asset you build
> should serve the proof point. If a piece of the demo doesn't serve
> Q2's belief statement, cut it."

---

## Rules

- **Questions are ONE AT A TIME.** Never stack multiple questions in a single
  turn.
- **Press for specificity.** Generic answers produce generic demos. Push back
  once before accepting vague input.
- **Never start building.** This skill produces a design doc, not assets.
  Not even a draft spreadsheet. The doc must be approved before anything ships.
- **The dataset is always the first build artifact.** State this clearly —
  it's the dependency everything else links to.
- **Demo arc > feature list.** A demo that tells a story beats a feature
  walkthrough every time. If the user is building a checklist of features,
  redirect to narrative.
- **Setup complexity is a first-class concern.** A demo that only one person
  can run is a single point of failure. Push for reusability.
