# skills/presales/shared/

This folder holds shared conventions and schemas referenced by every skill
under `skills/presales/` — it is not itself a skill (it has no `SKILL.md` and
is never invoked directly). The nine presales sibling skills (Gong/Salesforce/
RFP-analysis skills for presales engineers) and the
`../core-presales-intelligence/SKILL.md` reference document link back into
this folder — currently `evidence-schema.md`, the JSON Schema for the
handoff payload every presales skill must emit — so the rules live in one
place instead of being copy-pasted across nine `SKILL.md` files.
