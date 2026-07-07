---
name: tufte-charts
description: "Design charts and tables using Edward Tufte's data-visualization methodology from The Visual Display of Quantitative Information. Use when the user asks for Tufte-style charts, high data-ink visuals, small multiples, minimal/clean charts, executive-grade graphics, or says to apply Tufte principles, maximize data-ink, remove chartjunk, or design for comparison and analytical clarity. Tool-agnostic — applies to matplotlib, plotly, D3, ggplot, Excel, or any rendering tool."
metadata:
  author: Manny Rodriguez-Lapido
  version: '1.0'
  license: MIT
---

# Tufte Charts — Data-Visualization Methodology

Apply Edward Tufte's principles (The Visual Display of Quantitative Information) to design analytical charts and tables. This skill is a **design methodology, not a tooling library** — the rules apply regardless of whether you render in matplotlib, plotly, D3, ggplot2, Vega, or a spreadsheet. The output should reveal complexity and support comparison without clutter, and be suitable for executive review rather than presentation filler.

## When to Use This Skill

Load this skill whenever you produce a chart, a small set of charts, or a dense comparison table and the user wants analytical clarity. Triggers include: "Tufte-style", "maximize data-ink", "remove chartjunk", "small multiples", "minimal/clean charts", "executive-grade", "make it analytical", or any request where the graphic must support decision-making.

## The Core Discipline (apply to every graphic)

1. **Maximize the data-ink ratio.** Every drop of ink should encode data. Erase everything that doesn't: heavy gridlines, borders, tick marks, background fills, redundant labels, 3D effects, drop shadows, gradients.
2. **Erase non-data-ink, then erase redundant data-ink.** Two passes. First remove decoration; then remove repeated encodings (e.g., a value shown both as a bar length and a label and an axis tick — keep the most direct one).
3. **No chartjunk.** No moiré patterns, no decorative textures, no ducks (graphics that exist to look impressive), no gratuitous color. If an element doesn't change the reader's understanding, delete it.
4. **Maximize data density.** Show many numbers in a small, coherent space. Prefer one dense, information-rich graphic over several sparse ones.
5. **Reveal complexity at several levels** — broad overview down to fine structure — in a single coherent view.
6. **Tell the truth.** Proportional encoding (the lie factor ≈ 1). Don't truncate a bar-chart baseline; don't over-smooth or over-aggregate away the real values.

See `references/tufte-principles.md` for the full ruleset, the data-ink checklist, and Tufte's specific techniques (range-frame, dot-dash plot, small multiples, multifunctioning elements).

## Workflow

1. **Identify the comparison.** Ask: what does the reader need to compare, rank, or detect? The chart type follows from the comparison, not the other way around. Use `references/chart-selection.md` to pick the form.
2. **Choose the most direct encoding.** Position along a common scale beats length beats angle/area beats color intensity. Default to this hierarchy.
3. **Draft minimally.** Start with data marks only — no frame, no grid, no legend. Add back only what a reader provably needs.
4. **Label directly.** Put labels on or beside the data (end-of-line labels, point labels) instead of forcing a round-trip to a legend. Remove the legend if direct labeling works.
5. **Restrain color.** Default to a single ink color plus grey for context. Add one accent color only to mark the analytically important series/outlier. Never use color decoratively.
6. **Annotate strategically, not decoratively.** A few words placed at the outlier or key point — explaining *why* it matters — outperform a caption block. Use sparingly.
7. **Inspect and prune.** Look at the rendered output. For every element ask "what would be lost if I deleted this?" If nothing, delete it. Check for: text overflow/wrapping, label collisions, low text-vs-background contrast, truncated baselines.

## Non-negotiable defaults

- **Horizontal layouts** for ranked categorical data (horizontal bars) — labels read naturally left-to-right and long category names fit.
- **Small multiples** when comparing the same measure across many accounts, segments, time periods, or categories: a grid of identical small charts, shared scales, sorted meaningfully. This is Tufte's highest-leverage technique for comparison.
- **Direct value labels** on bars/points when exact values matter; **omit them** when the shape/pattern is the point and labels would add clutter.
- **Thin lines, light context.** Reference/median lines in pale grey, data lines thin and dark.
- **Sort by insight,** not alphabetically — rank bars by value, order small multiples by the dimension being compared.
- **No legend if direct labeling is possible. No gridlines unless reading exact values off an axis is essential — and then make them faint.**

## Tables (Tufte treats tables as first-class)

- Use tables for **exact values and dense comparison** — they often beat a chart when there are few rows or precision matters.
- Right-align numbers, align decimals, use consistent significant figures.
- Minimal rules: a line under the header and one at the bottom is usually enough — no vertical rules, no full grid.
- Order rows by insight value (rank by the key metric). Put the most important column near the labels.
- For composite scores, show the **raw components alongside the score** so the reader can audit it.

## What "done" looks like

A reader can extract the main comparison in seconds and the fine detail on closer inspection; nothing on the page is decorative; the important point is visually obvious without a caption explaining the chart; and the graphic would survive Tufte's test — *"Above all else show the data."*

Read `references/tufte-principles.md` and `references/chart-selection.md` for the detailed rules and per-chart-type guidance before producing the visuals.
