# Output & Brand Standards — Shared Contract

This is the shared output/brand contract for anything rendered on-screen
during a live `/demo` session — tables, charts, summaries, generated
documents. `demo/SKILL.md` and all four domain sub-skills
(`demo/grc/`, `demo/reporting/`, `demo/analytics/`, `demo/sustainability/`)
must follow these rules whenever they produce content the prospect will
actually see. Domain skills link here (`../shared/output-standards.md`)
instead of restating the full rule set.

## (a) Color palette — one palette per artifact, chosen by domain

Pick exactly **one** palette for a given artifact, based on its domain. Do
not mix palettes within a single artifact.

| Domain | Palette |
|---|---|
| Financial Reporting | Purple Mountain |
| Audit & Risk / GRC | Presentation Yellow |
| Sustainability | Link Blue |
| Mixed / cross-domain / platform-level | Zesty Neue / Brand green |

**There is no red in any of these palettes.** Favorable vs. unfavorable, or
pass vs. fail, must never be communicated by color alone (and never by a
green/red pairing at all, since red isn't part of the approved palette
system). Always pair the palette's neutral-vs-accent color choice with an
explicit non-color marker:

- A directional glyph: `▲` (favorable/increase) or `▼` (unfavorable/decrease),
  or
- An explicit suffix: `(F)` for favorable, `(U)` for unfavorable.

Example: `Revenue variance: +$1.2M (F) ▲` rather than a bare green number.

## (b) Numbers

- **Never blanket-round.** Match the precision of the source data exactly —
  if the source returns `1,284,392.17`, do not display `1.3M` unless the
  domain skill's own convention explicitly calls for a rollup view (and if
  so, state that a rollup is being shown).
- **Always state the currency** (or unit) explicitly next to the figure or
  in an unambiguous column header — never leave a bare number that could be
  misread as a different currency or unit.
- **Right-align** numeric columns in any table.
- **Never show raw GUIDs, vertex IDs, or other internal identifiers** to the
  prospect. If an identifier must be referenced for traceability, use a
  human-readable label instead (e.g. the entity/document/control name), and
  keep the raw ID only in SC-facing notes, never on the shared screen.

## (c) Structure

Every substantive output during a demo should follow this shape, in order:

1. **BLUF** (bottom line up front) — one sentence stating the answer/result
   before any supporting detail.
2. **Scope line** — immediately after the BLUF, state: organization,
   workspace, source (which tool/system the data came from), any filters
   applied, and the period covered. This is not optional boilerplate — it is
   what lets the SC and prospect both know exactly what they're looking at.
3. **The data** — table, chart, or figure.
4. **Caveats placed next to the affected figure** — never buried in a
   footnote or a separate section at the bottom. If a number has a caveat
   (partial period, excludes a subsidiary, entitlement-limited scope, etc.),
   put it directly next to that number, not somewhere the reader has to hunt
   for it.
5. **2-3 suggested next steps** — concrete, short, tied to what was just
   shown.

## (d) Never fabricate to fill a gap

If a query returns no data, say so plainly ("No results returned for this
query/workspace/period") and stop there. Do not render an empty chart frame
styled to look like it's waiting on data, and do not fill the gap with
illustrative or placeholder numbers under any circumstance — this is the
single most damaging failure mode observed in Wave 1 testing (see
`../shared/session-safety.md`) and it must never recur.

## (e) Generated artifacts require a manual-import disclaimer

Any artifact generated during a demo session — a Word document, an Excel
export, an HTML page, a slide — **must state explicitly that it needs to be
manually imported back into Workiva.** It is not automatically part of the
platform, it did not write anything back to any Workiva system, and the
prospect should not be left with the impression that generating the artifact
was itself a platform action. State this plainly next to the artifact, not
in fine print.
