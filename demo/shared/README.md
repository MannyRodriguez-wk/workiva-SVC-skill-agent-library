# demo/shared/

This folder holds conventions shared by the `/demo` anchor/router skill and
its four domain sub-skills (`demo/grc/`, `demo/reporting/`, `demo/analytics/`,
`demo/sustainability/`) — it is not itself a skill (it has no `SKILL.md` and
is never invoked directly). `session-safety.md` is the full pre-flight safety
gate (memory, tenant/workspace confirmation, entitlement probing, live
correction protocol) that `demo/SKILL.md` runs and enforces once per session;
`output-standards.md` is the on-screen output/brand contract (palette rules,
number formatting, structure, and the no-placeholder-data rule) every domain
skill must follow when rendering anything to the prospect. Domain skills link
back to both files (`../shared/session-safety.md`,
`../shared/output-standards.md`) instead of restating them in full.
