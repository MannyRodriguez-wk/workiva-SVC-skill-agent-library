# Asset Index — SVC Skill Library

The unified catalog of skills (and agents, when added) in this library.

Maintainers update this file when PRs merge — contributors do not need to edit it.

---

## Skills

| Asset | Function | Triggers (examples) |
|-------|----------|---------------------|
| [`internal-apps-template-beta`](./skills/internal-apps-template-beta/SKILL.md) | Deploy Workiva internal web apps on Google Apps Script + clasp; embed in Confluence | "deploy an internal app", "clasp push", "workiva-apps-template" |
| [`stop-slop`](./skills/stop-slop/SKILL.md) | Remove predictable AI writing patterns from prose | "remove AI patterns", "edit this draft", "stop slop" |
| [`tufte-charts`](./skills/tufte-charts/SKILL.md) | Tufte data-visualization methodology for charts and tables | "Tufte-style", "maximize data-ink", "executive-grade chart" |
| [`grillme`](./skills/grillme/grillme.md) | Relentless interview to sharpen a plan or design | `/grilling`, "grill my plan", "pressure-test this design" |

---

## Agents

| Asset | Function | Composes |
|-------|----------|----------|
| *(none yet)* | Drop YAML in [`agents/`](./agents/) — see [CONTRIBUTING.md](./CONTRIBUTING.md) | — |

---

## Usage and safety

See **[SC_USAGE_GUIDE.md](./SC_USAGE_GUIDE.md)** for install steps, Claude permissions, Workiva/Google access model, and security risks.

Skills must not embed credentials, must respect data boundaries, cite sources, never fabricate Workiva policy, and require human review for customer-facing or legal/financial output. See [CONTRIBUTING.md](./CONTRIBUTING.md).
