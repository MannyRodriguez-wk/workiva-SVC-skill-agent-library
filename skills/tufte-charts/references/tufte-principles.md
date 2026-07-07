# Tufte Principles — Detailed Reference

Distilled from Edward Tufte, *The Visual Display of Quantitative Information* (2nd ed.). Use these as the rule-set behind every graphic. The chapter ideas are paraphrased for application, not quoted.

## 1. Graphical excellence (the goal)

> Graphical excellence is the well-designed presentation of interesting data — a matter of substance, of statistics, and of design. It gives the viewer the greatest number of ideas in the shortest time with the least ink in the smallest space.

Excellent graphics are **truthful, dense, and clear**. They are about the data first; design serves the data.

## 2. Graphical integrity — tell the truth

- **Lie Factor** = (size of effect shown in graphic) / (size of effect in data). Aim for ≈ 1.0. Anything beyond 1.05 or below 0.95 distorts.
- **Start bar-chart and area baselines at zero.** Length/area encodes magnitude; a truncated baseline lies. (Line charts tracking change over time may use a non-zero baseline if labeled clearly — bars may not.)
- **Use a consistent scale.** No broken axes that hide the real gap unless explicitly marked.
- **Show data variation, not design variation.** Don't let the design (binning, smoothing, projection) manufacture or hide patterns.
- **Number of information-carrying dimensions should not exceed the dimensions in the data.** No 3D bars for 1D data; no area encoding for a single value.
- **Don't over-aggregate or over-smooth.** Preserve the real values; let outliers show.

## 3. Data-ink and its maximization

- **Data-ink** = the non-erasable core of a graphic, the ink that represents data.
- **Data-ink ratio** = data-ink / total ink. **Maximize it.**
- **Two erasing principles:**
  1. *Erase non-data-ink* — within reason (frames, backgrounds, heavy grids, tick marks, redundant axes, decorative elements).
  2. *Erase redundant data-ink* — when the same number is encoded multiple ways, keep the most effective one.
- **Revise and edit.** Good information graphics are redrawn and pruned, like prose.

### Data-ink checklist (run on every draft)
- [ ] Removed chart border / frame?
- [ ] Removed or greatly lightened gridlines? (Keep only if reading exact values off an axis.)
- [ ] Removed tick marks that don't aid reading?
- [ ] Removed background fill / panel color?
- [ ] Removed legend in favor of direct labels where possible?
- [ ] Removed redundant labels / duplicate encodings?
- [ ] Removed 3D, shadows, gradients, bevels?
- [ ] Every remaining mark encodes data or essential context?

## 4. Chartjunk — what to delete

- **Moiré / vibrating patterns** (hatching, dense fills) — use flat tone or none.
- **The grid as prison** — heavy gridlines that dominate the data. Lighten to pale grey or remove.
- **The duck** — a graphic dressed up as decoration; form overwhelming function.
- **Gratuitous color, clip art, 3D, drop shadows.** None of it carries data.

## 5. Tufte's specific techniques (use where they fit)

- **Range-frame / range-bar axes:** trim axis lines to span only the actual data range, so the frame itself reports the min/max.
- **Dot-dash-plot (marginal rugs):** project data ticks onto the axes to show marginal distributions for free.
- **Small multiples:** repeat a small chart across a varying dimension (time, account, category) with **shared scales and axes**. The eye compares panels effortlessly. The single most powerful comparison device — use it whenever you'd otherwise overplot many series.
- **Multifunctioning graphical elements:** let one element do several jobs (e.g., a data point that also labels itself; an axis that is also the range of the data). But avoid overloading to the point of confusion.
- **Sparklines (from later Tufte work):** word-sized, axis-less inline charts for dense tables/dashboards — useful for trend-at-a-glance in a table cell.
- **Layering and separation:** use subtle weight/value/color differences to layer foreground data over background context, instead of heavy borders.

## 6. Data density

- **Data density** = number of entries in the data matrix / area of the graphic. Most published graphics are far too sparse.
- **Maximize density, then add white space for clarity** (the "shrink principle": most graphics can be shrunk without loss). Dense-but-legible beats sparse-and-decorated.

## 7. Aesthetics and technique (practical defaults)

- **Proportion:** favor graphics wider than tall (≈ 1.4–1.6 : 1, near the golden ratio) unless the data dictates otherwise; horizontal layouts suit the eye and accommodate labels.
- **Typography:** clean, legible, consistent. Use type weight/size for hierarchy, not boxes or color.
- **Color:** the quietest palette that does the job. Grey for context, one dark ink for data, one accent for the point. Color encodes meaning or it is removed.
- **Words and data together:** integrate labels, scales, and brief explanatory annotation directly into the graphic rather than relegating everything to a separate caption.

## The one-line test
> "Above all else show the data." — strip until only the data and the minimum context needed to read it remain.
