# Asset Index — SVC Skill Library

The unified catalog of every skill in this library.

**Validation legend:** ✅ passes stock `agentskills validate` · ⚠️ functional but uses frontmatter the stock validator may reject — see [README → Validation](./README.md#validation).

---

## Skills

| Asset | Function | Target audience | Triggers (examples) | Validates |
|-------|----------|-----------------|---------------------|-----------|
| [`internal-apps-template-beta`](./skills/internal-apps-template-beta/SKILL.md) | Deploy Workiva internal web apps on Google Apps Script + clasp; embed in Confluence; Okta org-only auth | SCs, Demo Engineering, anyone building small internal tools | "deploy an internal app", "clasp push", "embed in Confluence", "workiva-apps-template" | ✅ |
| [`stop-slop`](./skills/stop-slop/SKILL.md) | Remove predictable AI writing patterns from prose | SCs, VM, anyone drafting customer or leadership copy | "remove AI patterns", "edit this draft", "stop slop" | ✅ |
| [`tufte-charts`](./skills/tufte-charts/SKILL.md) | Tufte data-visualization methodology for charts and dense tables | SCs, VM, analytics storytelling | "Tufte-style", "maximize data-ink", "small multiples", "executive-grade chart" | ✅ |
| [`grillme`](./skills/grillme/grillme.md) | Relentless interview to sharpen a plan or design (`/grilling`) | SCs planning demos, builds, or narratives | `/grilling`, "grill my plan", "pressure-test this design" | ✅ |

---

## Usage and safety

See **[SC_USAGE_GUIDE.md](./SC_USAGE_GUIDE.md)** for install steps, Claude permissions, Workiva/Google access model, and security risks.

Skills must not embed credentials, must respect data boundaries, cite sources, never fabricate Workiva policy, and require human review for customer-facing or legal/financial output. See [CONTRIBUTING.md](./CONTRIBUTING.md).
