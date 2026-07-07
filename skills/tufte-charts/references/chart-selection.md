# Chart Selection — Match the Form to the Comparison

Pick the chart from the question the reader is asking. The comparison drives the form. Encoding precision hierarchy (use the most precise that fits): **position on a common scale > position on non-aligned scales > length > angle/slope > area > volume > color hue/saturation.**

## By analytical question

| Reader's question | Preferred form | Tufte notes |
|---|---|---|
| "Rank these categories" | **Horizontal bar**, sorted by value | Direct value labels at bar ends; no gridlines; baseline at zero. |
| "Compare the same metric across many groups" | **Small multiples** | Shared scales, sorted panels. Beats a crowded multi-series chart. |
| "How are two variables related?" | **Scatter / dot plot** | Range-frame axes; label notable points directly; reference lines at medians in pale grey. |
| "What's the distribution / spread?" | **Strip / dot plot**, or histogram | Strip plot shows every value; jitter only to avoid overlap. Marginal rug if useful. |
| "How does it change over time?" | **Thin line**, single or small-multiple | End-of-line direct labels instead of legend; non-zero baseline OK if labeled. |
| "How does a flow narrow?" (funnel/stage) | **Horizontal bars by stage** | Count labels at bar ends; annotate the key conversion in words. |
| "What are the exact values?" | **Table** | Right-aligned numbers, minimal rules, sorted by key metric. |
| "What composes this total?" | **Stacked horizontal bar** (few segments) or **small multiples** | Avoid pie charts — angle/area encoding is imprecise. Limit stack to ~4 segments. |
| "Where on a map?" | **Choropleth / dot map**, restrained palette | Sequential single-hue ramp; label extremes. |
| "Trend inside a table row" | **Sparkline** | Word-sized, axis-less, in the table cell. |

## Defaults and anti-patterns

**Defaults**
- Horizontal over vertical for ranked categories (labels read naturally, long names fit).
- One accent color to mark the analytically important element; everything else dark-ink + grey.
- Direct labels over legends. Sort by value, not alphabetically.
- Reference lines (median, target, prior period) thin and pale, behind the data.
- Annotate the outlier with a few words explaining *why* it matters.

**Avoid**
- **Pie / donut charts** — angle and area are read poorly; a sorted bar or a table is almost always better.
- **Dual-axis charts** — they invite spurious correlation and scale manipulation. Use small multiples instead.
- **3D anything** — adds a fake dimension and distorts encoding.
- **Stacked bars with many segments** — beyond ~4, the middle segments can't be compared; switch to small multiples or a table.
- **Heavy gridlines, frames, background fills, legends-when-direct-labels-work.**
- **Over-smoothing** a line or **over-binning** a histogram so the real structure disappears.

## Composite-score charts (common analytical need)

When ranking entities by a composite score:
1. Lead with a **sorted horizontal bar** of the score, direct value labels, color = tier/segment.
2. Follow with a **decomposition**: stacked horizontal bar showing each weighted component's contribution — lets the reader audit *why* each score landed where it did.
3. Always pair with (or back with) a **table showing the raw components** beside the score, so the encoding is verifiable. Never present a composite score without exposing its parts.

## Quality gate before delivering
- Main comparison readable in seconds; fine detail readable on inspection.
- No element survives the "what's lost if I delete this?" test as decoration.
- No text overflow, label collisions, or low contrast (check dark-text-on-dark-fill).
- Baselines honest; scales shared across small multiples; values not over-aggregated.
