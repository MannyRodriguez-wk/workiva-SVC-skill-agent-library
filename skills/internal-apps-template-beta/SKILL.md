---
name: internal-apps-template-beta
description: >
  Step-by-step guide for deploying Workiva internal web apps using Google Apps Script,
  clasp, and AI-assisted development (Cursor). Use this skill whenever someone wants to
  build, deploy, or customize a small internal tool, dashboard, form, or automation that
  runs on Apps Script and embeds in Confluence — especially non-developers using Cursor
  to vibe-code their way through it. Trigger on: "deploy an internal app", "build a
  dashboard on Confluence", "host my HTML prototype", "set up clasp", "push my Apps
  Script project", "how do I deploy a Google Apps Script", "internal apps template",
  "workiva-apps-template", "clasp push", "embed app in Confluence", "set up SPREADSHEET_ID",
  "Apps Script web app", "I built a tool with Claude/ChatGPT and need to host it", or
  any request to take an AI-generated HTML prototype and turn it into a secure internal
  tool. Proactively invoke this skill before writing any code or giving deployment steps.
---

# Internal Apps Template — Deploy Guide

A secure pattern for hosting small internal tools on Google Apps Script, backed by
Google Sheets, and embedded in Confluence — with Workiva Okta auth built in.
No servers, no GitHub required.

## When to use this skill
- User wants to deploy or customize the `workiva-apps-template` zip
- User has an HTML prototype (from Claude, ChatGPT, Cursor) and needs a safe place to host it internally
- User is working through `clasp` setup, auth errors, or deployment steps
- User wants to embed a tool in a Confluence wiki page

---

## Stack overview

| Layer | What it is |
|---|---|
| **Runtime** | Google Apps Script (GAS) — no servers to provision |
| **Auth** | Workiva Okta — organization-only access, no tokens to build |
| **Data** | Google Sheet — `Items` tab (rows) + `Config` tab (key/value) |
| **Deploy tool** | `clasp` (Google's official CLI, installed via npm) |
| **AI editor** | Cursor + Composer 2.5 — non-developers describe changes in chat |
| **Embed** | Confluence HTML macro (`Confluence.html`) wrapping the `/exec` URL |

---

## First-time deploy (step by step)

Walk the user through each step. For each, provide the **Ask Cursor** prompt they can copy-paste, plus the raw terminal command if they want to run it themselves.

### Prerequisites

Confirm the user has:
- Workiva Google account (already have it)
- [Cursor](https://cursor.com) installed
- Node.js (LTS) from nodejs.org — needed for `clasp`
- Google Chrome — required for `clasp login`
- A blank Google Sheet created in Drive

### Step 1 — Download and open in Cursor
Download `workiva-apps-template.zip` from Google Drive, unzip, open the `workiva-apps` folder in Cursor via **File → Open Folder**. Do not open a single file — the whole folder must be open so `.clasp.json` binding is preserved.

### Step 2 — Install clasp (once per machine)
```
Ask Cursor: Install clasp globally on my machine, confirm it works, and fix any npm permission errors if they appear.
```
```bash
npm install -g @google/clasp
```
When Cursor asks to run npm install commands, allow it — clasp is Google's official deploy tool.

### Step 3 — Log in to Google
```
Ask Cursor: Run clasp login for this workiva-apps folder. Tell me when Chrome is ready for me to sign in with my Workiva Google account.
```
```bash
clasp login
```

### Step 4 — Create the Apps Script project
```
Ask Cursor: Create a new Apps Script web app project for me from this workiva-apps folder (copy .clasp.json.example to .clasp.json first). Use a title like "My Internal App" and confirm .clasp.json was created.
```
```bash
cp .clasp.json.example .clasp.json
clasp create --type webapp --title "My Internal App" --rootDir .
```
Keep `.clasp.json` in the folder — do not delete it.

### Step 5 — Connect a Google Sheet
Create a blank Google Sheet. Copy the Sheet ID from the URL:
```
https://docs.google.com/spreadsheets/d/<SPREADSHEET_ID>/edit
```
```
Ask Cursor: I created a Google Sheet. The URL is [PASTE URL] — set SPREADSHEET_ID in Apps Script script properties for me.
```
In the Apps Script editor (open via `clasp open`), go to **Project Settings → Script properties** and set:
- `SPREADSHEET_ID` — your sheet ID
- `APP_ADMINS` — optional, comma-separated emails who can write

### Step 6 — Initialize sheet tabs (one time)
```
Ask Cursor: Walk me through running ensureSheetStructure once in Apps Script to create the Items and Config tabs and a sample row.
```

### Step 7 — Push code to Google
```
Ask Cursor: Run clasp push --force for this workiva-apps project and tell me if anything failed.
```
```bash
clasp push --force
```

### Step 8 — Publish (first deploy)
Use the Apps Script web UI for first deploy. Ask Cursor:
```
Ask Cursor: Open my Apps Script project with clasp open. Then walk me through Deploy → New deployment: Web app, Execute as Me, Only people in Workiva. I will click Deploy in the browser and paste you my Web app URL.
```
Production URL format:
```
https://script.google.com/a/macros/workiva.com/s/<DEPLOYMENT_ID>/exec
```

### Step 9 — Test the app
```
Ask Cursor: Open my production exec URL from this project's deployments and tell me what to click in the app to confirm Items are saving to my spreadsheet.
```

### Step 10 — Embed in Confluence (optional)
Recommended: duplicate the ENG template wiki page into your space, then replace only the HTML macro contents.
1. Open the Workiva Internal Apps Template on the ENG wiki
2. Use Confluence **Copy** or **Duplicate** into your team's space
3. Edit the page → open the HTML macro → replace all macro HTML with your `Confluence.html` (after `GAS_APP_URL` points at your `/exec` URL)
4. Publish and test

```
Ask Cursor: Set GAS_APP_URL in Confluence.html to my production exec URL from this project's deployments. Then walk me through duplicating the ENG template page into my Confluence space and overwriting the HTML macro with my Confluence.html file.
```

---

## Pushing updates later

After Cursor helps you change the app, use this to ship — no manual terminal commands:
```
Ask Cursor: Push my workiva-apps changes and redeploy to my existing production deployment. Use a timestamped description. Do not create a new deployment unless I ask.
```
Cursor finds the existing deployment ID automatically. Your `/exec` URL stays the same — no need to re-paste `Confluence.html` unless the wrapper file itself changed.

---

## Customizing with Cursor (vibe coding)

Describe what you want in plain language. Examples:
```
# Rename the app
Change the app title to "Team Budget Tracker" everywhere users see it, including Docs.

# Add a column
Add a "Priority" column to the Items sheet and show it in the Item tracker table and Data grid.

# Ship changes
Update Docs.html change log for today, then push and redeploy to my existing production deployment.
```
Always ask Cursor to update `Docs.html` when user-facing behavior changes, and add a dated Change Log entry.

---

## File reference

| File | Uploaded on deploy | Purpose |
|---|---|---|
| `Code.js`, `SheetData.js` | Yes | Server logic and spreadsheet access |
| `Index.html`, `Docs.html` | Yes | Main app and documentation |
| `Confluence.html` | No | Overwrite the HTML macro on a wiki page |
| `README.md` | No | Technical reference |

**Data model** — two sheet tabs after first-time setup:
- `Items` — one row per tracked item (`id`, `name`, `status`, `owner`, `updated_at`)
- `Config` — key/value settings such as `app_title`

---

## Example apps (sidebar)

Three examples ship with the template:
- **Item tracker** — CRUD table backed by the sheet (add, edit, delete rows)
- **Chart gallery** — Chart.js layouts with sample data only
- **Data grid** — AG Grid with sort, filter, pagination; loads Items sheet rows

Deep-link examples: `?example=charts` or `?example=grid` on your web app URL.

---

## Design system

Two palettes:
- `Index.html` — dense product palette (`--bg-default: #EDEDED`, 14px body)
- `Docs.html` — editorial cover palette (`--cover-cream: #FFF7EA`, 16px body)

Sidebar is a narrow icon rail that **expands on hover**. Full token names and component classes are in `DESIGN-SYSTEM.md` inside the zip.

**Confluence embed contract**: The iframe posts `{ type: 'resize', bounded: true, source: 'workivaAppFrame' }` so the macro sizes to the visible viewport. Navigation between app and docs uses `{ type: 'navigate', target: 'docs' | '' }`.

---

## Permissions

- Anyone who can open the deployed web app can **read** items
- **Writes** require edit access to the linked Sheet, or set `APP_ADMINS` in Script Properties

---

## Troubleshooting

| Problem | Fix |
|---|---|
| `clasp` not found | Ask Cursor to install clasp and retry push/deploy |
| Login / auth errors | Ask Cursor to run `clasp login` again; complete sign-in in Chrome |
| `SPREADSHEET_ID` error | Ask Cursor to set script properties from your Sheet URL |
| Blank Confluence iframe | Ask Cursor to verify `GAS_APP_URL` and deployment access |
| Changes not visible | Ask Cursor to redeploy to your existing production deployment (`/exec`, not only push) |

**Browser issues with the embedded app** (blank box or "refused to connect"):
1. Disable privacy extensions (Privacy Badger, uBlock, Ghostery) for this page
2. Allow third-party cookies in Chrome (`chrome://settings/cookies`)
3. If you have multiple Google accounts, sign out at accounts.google.com and sign back in with your Workiva account first

For further help, post in **#cop-ai-internal-apps** on Slack (Internal Apps Community of Practice).

---

## Scope note

This skill is for **internal dashboards and automation** on Apps Script and Confluence. To prototype apps on the Workiva platform itself, use `wk-ai-prototyping` on GitHub instead.
