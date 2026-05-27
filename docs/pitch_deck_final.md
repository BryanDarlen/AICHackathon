# ReconPilot Final Pitch Deck

Use this as the exact content source for PowerPoint or Canva. Keep visible slide text short. Put details in speaker notes, not on the slides.

## Design Direction

- Theme: dark retro-tech pitch deck matching the current PDF: black or deep purple background, neon magenta/cyan accents, sparse text, and large visuals.
- Fonts: Inter or similar clean sans for body text, IBM Plex Mono or pixel-style display font for the `RECON PILOT` title and numeric/chart labels.
- Colors: deep purple/navy background, magenta primary accent, cyan connector accent, white text, red/pink close accent.
- Rule: one main idea per slide.
- Avoid long bullet lists. Use large numbers, short claims, screenshots, simple 3D assets, and generous empty space.

## Screenshot Capture Plan

Create `docs/screenshots/` and save these files. Slides use `02`, `03`, and `04`; `01` and `05` are useful demo backup screenshots.

1. `01_home_ready.png`  
   Open `http://localhost:3002`. Capture the top of the app before clicking anything. Include the logo, backend status, buttons, and four metric cards.

2. `02_extraction_review.png`  
   Click **Load Demo Casebook**. Capture **Extraction Review** and **Uploaded Documents** together.

3. `03_reconciliation_dashboard.png`  
   Click **Run Matching**. Capture the **Reconciliation Dashboard** panel, including the metric cards labeled **Matched**, **Review**, **Missing Proof**, **Duplicate**, **Human Review**, **Cleared MYR**, **Exception MYR**, and **Automation**, plus the clickable result cards below them.

4. `04_exception_detail.png`  
   Click the first non-matched result. Capture **Exception Detail**, including confidence, explanation, recommended action, and evidence.

5. `05_audit_report.png`  
   Scroll to **Audit Report Preview**. Capture audit summary, agent trace, controls, and decision rows.

Recommended Windows capture method:

1. Press `Windows + Shift + S`.
2. Select only the app area, not the full desktop.
3. Save the image using the exact filename above.

## Slide 1: Title

**Visible Text**

RECON
PILOT

Global Treasury Reconciliation Agent

**Visual**

Match the current PDF title slide style.

Placement:
- Use a black-to-purple retro grid background.
- Put a white rounded-square `Reconpilot.` logo card on the left.
- Put the large pixel-style `RECON PILOT` title centered-right.
- Put "Global Treasury Reconciliation Agent" directly below the title.
- Use small decorative finance/tech assets around the edges, such as a bank icon and green network/blocks.
- Do not use an app screenshot on this slide.

**Example PPT Layout**

```text
+--------------------------------------------------------------+
|                                                              |
|                                                              |
| [Reconpilot. card]       RECON                               |
|                          PILOT                               |
|                          Global Treasury Reconciliation Agent |
|                                                              |
| [bank icon]                         [green tech/network asset] |
|                                                              |
+--------------------------------------------------------------+
```

**Speaker Notes**

Hi, I am presenting ReconPilot, a Global Treasury Reconciliation Agent. It helps finance teams turn messy invoices, payment proofs, and bank statements into explainable reconciliation decisions.

## Slide 2: Why Now

**Visible Text**

76%

of organizations faced attempted or actual payment fraud in 2026.

~80%

of treasury teams still use manual or fragmented workflows.

**Small Bottom Line**

Faster payments are increasing reconciliation pressure.

**Source Footer**

AFP Payments Fraud Survey 2026; TD Bank Treasury Automation Gap 2025; Federal Reserve Financial Services 2026; J.P. Morgan Payments Outlook 2026.

**Visual**

Create the current PDF's high-contrast statistic slide.

Canvas layout:
- Use a black background with a purple dotted-wave pattern on the left.
- Place `76%` large in the upper-left.
- Place the people/fraud icon cluster below the `76%` statement.
- Place money-stack icons on the upper-right.
- Place `~80%` large on the right side, with the manual-workflow statement beside or below it.
- Put the source footer at the bottom-left in very small text.

Left statistic block:
```text
76%
payment fraud exposure
```

Right statistic block:
```text
~80%
manual treasury workflows
```

Statistic styling:
- Numbers: very large, white, bold.
- Supporting statements: white, compact, and close to each number.
- Accent assets: green money stacks and white people icons.
- Keep the source footer tiny but legible.

Do not show the small bottom line on the slide if space is tight; keep it in speaker notes.

**Example PPT Layout**

```text
+--------------------------------------------------------------+
| 76%                                      [money stacks]      |
| of organizations faced attempted or actual payment fraud      |
|                                                              |
| [people icons]                                  ~80%          |
|                                of treasury teams still use    |
|                                manual or fragmented workflows |
|                                                              |
|        Faster payments are increasing reconciliation         |
|        pressure.                                             |
|                                                              |
| AFP Payments Fraud Survey 2026; TD Bank Treasury...          |
+--------------------------------------------------------------+
```

**Speaker Notes**

The timing matters. Fraud risk is high, treasury workflows are still fragmented, and cross-border or real-time payments create more reconciliation mismatches. Finance teams need faster matching without losing evidence or audit control.

## Slide 3: Problem

**Visible Text**

Reconciliation breaks when documents do not agree

Problem: Currency mismatch, FX fee, late settlement, reference typo, manual evidence check

**Visual**

Create a "broken reconciliation chain" diagram.

Canvas layout:
- Use a black background.
- Put the headline centered at the top. Color the words `breaks`, `not`, and `agree` in purple/magenta.
- Place 3 white same-size boxes in one horizontal row across the lower middle.
- Each box should be about 25% slide width and 28% slide height.
- Use black text inside the boxes for maximum contrast.
- Use cyan connector arrows above and below the boxes, matching the current PDF.

Box 1 text:
```text
INVOICE
INV-1042
USD 1,250.00
Due: 14 Jan
```

Box 2 text:
```text
PAYMENT PROOF
INV-1042
MYR 5,875.00
FX fee applied
```

Box 3 text:
```text
BANK STATEMENT
REF: INY-1042
MYR 5,861.25
Settled: 16 Jan
```

Connectors:
- Put a thick cyan arrow from Invoice to Payment Proof.
- Put a thick cyan arrow from Payment Proof to Bank Statement.
- On the lower connector, add a small red label: **REFERENCE TYPO!!!**.

Problem line:
- Put the full problem line in very small white text along the bottom-left:
```text
Problem: Currency mismatch, FX fee, late settlement, reference typo, manual evidence check
```

Purpose:
- The judge should instantly see that the documents refer to the same business event but do not match perfectly.

**Example PPT Layout**

```text
+--------------------------------------------------------------+
| Reconciliation breaks when documents do not agree             |
|                                                              |
|                 +------------+ +------------+ +------------+ |
|                 | INVOICE    | | PAYMENT    | | BANK       | |
|                 | INV-1042   | | PROOF      | | STATEMENT  | |
|                 | USD 1,250  | | MYR 5,875  | | MYR 5,861  | |
|                 +------------+ +------------+ +------------+ |
|                         cyan arrows + red typo callout        |
|                                                              |
| Problem: Currency mismatch, FX fee, late settlement, typo...  |
+--------------------------------------------------------------+
```

**Speaker Notes**

In real operations, a USD invoice may become an MYR bank deposit. A proof may be missing or duplicated. References may be mistyped. A simple keyword match is not enough, and a black-box AI answer is too risky.

## Slide 4: Product

**Visible Text**

ReconPilot is...

an AI-assisted treasury workspace that extracts financial documents, matches cross-border payments, flags exceptions, and exports audit-ready evidence.

**Visual**

Use `docs/screenshots/02_extraction_review.png`.

Canvas layout:
- Left text area: 38% slide width.
- Right screenshot area: 56% slide width.
- Gap between text and screenshot: 6% slide width.
- To match the current PDF, place the screenshot stack on the left and the `ReconPilot is...` product text on the right.
- Use a deep purple background with a large blue/purple semicircle behind the screenshots.
- Add small diagonal magenta line accents in the bottom-right.

Screenshot placement:
- Insert `02_extraction_review.png`.
- Crop to show only:
  - **Extraction Review** panel
  - **Uploaded Documents** panel
  - at least 3 rows in the Extraction Review table
- Do not include browser tabs, address bar, Windows taskbar, or desktop.
- Align the screenshot vertically centered with the slide text.

Screenshot styling:
- Radius: 8px.
- Border: 1.5px teal.
- Shadow: 0 14px 30px with 25% black opacity.

Text styling:
- `ReconPilot is...` should be large and bold.
- The product sentence should be split into short lines:
```text
an AI-assisted treasury workspace
that extracts financial documents,
matches cross-border payments,
flags exceptions,
and exports audit-ready evidence.
```

**Example PPT Layout**

```text
+--------------------------------------------------------------+
| PRODUCT                                                      |
|                                                              |
| +-----------------------------+     ReconPilot is...          |
| | 02_extraction_review.png    |                              |
| | crop: Extraction Review     |     an AI-assisted treasury   |
| | + Uploaded Documents        |     workspace                 |
| +-----------------------------+     that extracts documents,  |
|       [uploaded docs crop]          matches payments,         |
|                                    flags exceptions,          |
|                                    exports audit evidence.    |
+--------------------------------------------------------------+
```

**Speaker Notes**

ReconPilot is not replacing the reviewer. It automates the first pass: extraction, validation, matching, exception flagging, and audit report generation.

## Slide 5: The Way It Works

**Visible Text**

The way it works

Load Files

Extract

Matching

Review

Export

From messy treasury files to an explainable audit report

**Visual**

Create a five-step workflow row.

Canvas layout:
- Use the same deep purple background as the current PDF.
- Put `The way it works` centered at the top in magenta.
- Place the five workflow words in two rows, connected by thick purple arrows:
  `Load Files -> Extract -> Matching`
  `Review -> Export`
- Add the bottom line in red/pink near the lower-left.
- Add a large muted gear icon on the right.

Workflow text:
```text
Load Files
```

```text
Extract
```

```text
Matching
```

```text
Review
```

```text
Export
```

Connector styling:
- Use thick purple arrows, matching the PDF.

Text styling:
- Step labels: large, white, bold.
- Title: magenta, bold.
- Bottom line: red/pink, medium weight.

Do not use screenshots on this slide.

**Example PPT Layout**

```text
+--------------------------------------------------------------+
| The way it works                                             |
|                                                              |
| Load Files -> Extract -> Matching                [gear icon] |
|                                                              |
| Review -> Export                                             |
|                                                              |
| From messy treasury files to an explainable audit report     |
+--------------------------------------------------------------+
```

**Speaker Notes**

The workflow mirrors how a finance reviewer works. Start with files, review extracted records, run matching, inspect exceptions, then export the audit report.

## Slide 6: System Architecture + Agent Framework

**Visible Text**

Next.js calls FastAPI.

FastAPI extracts and validates records.

Python reconciles with MYR-normalized scoring.

SQLite stores documents, records, and runs.

Evidence and human review stay visible.

**Visual**

Create a simple architecture and agent framework diagram. Include the label:
```text
Agent Framework Diagram
```

This slide should explain how the system is built and how the agent workflow moves from document input to auditable output.

Use five nodes connected by thick purple arrows:
```text
Next.js Dashboard
FastAPI API
Extraction + Validation
Reconciliation Engine
SQLite + Audit JSON
```

Canvas layout:
- Use the current PDF's deep purple background.
- Put `System Architecture` centered at the top in magenta.
- Arrange the technical nodes across the slide with thick purple arrows.
- Keep the app/backend nodes small on the left, the reconciliation engine node on the upper-right, extraction/validation on the lower-left, and SQLite + Audit JSON on the lower-right.
- Add a city/finance asset in the bottom-right corner.
- Do not use a screenshot on this slide.

Layer 1:
```text
Next.js Dashboard
frontend/src/lib/api.ts
```

Layer 2:
```text
FastAPI API
/api/upload /api/extract /api/reconcile /api/report/{run_id}
```

Layer 3:
```text
Extraction + Validation
parsers + optional OpenAI-compatible LLM adapter
```

Layer 4:
```text
Reconciliation Engine
MYR normalization + match scoring + status decisions
```

Layer 5:
```text
SQLite + Audit JSON
documents + financial_records + runs
```

Add one small callout next to Layer 3:
```text
LLM only assists extraction when configured.
```

Add one small callout next to Layer 4:
```text
Financial decisions stay rule-based.
```

Add one compact agent workflow strip above or below the layer diagram:
```text
Documents -> Extraction + Validation -> Match Scoring -> Human Review -> Audit Report
```

Add one small guardrails strip under the layer diagram:
```text
Guardrails: evidence, confidence, human review, demo fallback
```

Highlight:
- Make arrows purple to match the PDF.
- Use white labels and smaller light text for file/API details.
- Keep the agent framework label small so it satisfies the guidebook without crowding the slide.

Style:
- Slide background: `#0F172A`.
- Normal boxes: `#1E293B`.
- Highlight box: `#0F766E`.
- Box border: `#334155`.
- Arrow color: `#60A5FA`.
- Main text: white.
- Notes: slate or teal.
- Border radius: 8px.
- Use Inter Medium for block labels.

How to build this slide:
1. Create the five architecture nodes.
2. Connect them with thick purple arrows.
3. Add the small `Agent Framework Diagram` label.
4. Add the two small callouts beside Extraction + Validation and Reconciliation Engine.
5. Add the compact agent workflow strip.
6. Add the guardrails strip.
7. Keep all text short and high contrast.

**Example PPT Layout**

```text
+--------------------------------------------------------------+
| System Architecture                                          |
|                                                              |
| Next.js Dashboard -> FastAPI API -> Reconciliation Engine     |
|        |                                      |               |
|        v                                      v               |
| Extraction + Validation  ->              SQLite + Audit JSON  |
|                                                              |
| Agent Framework: Documents -> Extract/Validate -> Match      |
| -> Review -> Report                                          |
+--------------------------------------------------------------+
```

**Speaker Notes**

The implementation shown here is based on the actual codebase. The frontend calls FastAPI through `frontend/src/lib/api.ts`. The backend exposes upload, extract, reconcile, and report routes in `backend/app/main.py`. Extraction and validation live in `backend/app/agents.py`. The financial matching logic lives in `backend/app/reconcile.py`, where amounts are normalized to MYR and candidate matches are scored. SQLite stores documents, financial records, and reconciliation runs through `backend/app/storage.py`. The agent framework is documents to extraction and validation, match scoring, human review, and audit report. Guardrails come from visible evidence, confidence scores, human review for exceptions, and demo fallback behavior.

## Slide 7: Target and Business Potential

**Visible Text**

Beachhead:

SME finance teams handling cross-border payments

Revenue path:

SaaS subscription

Per-document usage

Bank / ERP integrations

**Visual**

Use `docs/screenshots/03_reconciliation_dashboard.png` and one crop from `docs/screenshots/04_exception_detail.png`.

Canvas layout:
- Use the current PDF's deep purple background.
- Center the slide title at the top in magenta.
- Left text area: 34% slide width.
- Right screenshot area: 58% slide width.
- Gap: 6% slide width.
- Underline `Beachhead:` and `Revenue path:` in cyan.

Main screenshot:
- Insert `03_reconciliation_dashboard.png`.
- Crop to show:
  - the panel title **Reconciliation Dashboard**
  - the metric cards labeled **Matched**, **Review**, **Missing Proof**, **Duplicate**, **Human Review**, **Cleared MYR**, **Exception MYR**, and **Automation**
  - at least three clickable result cards showing a status label, invoice/reference, and confidence percentage
  - one active result card if it is visible
- Place it on the right side.
- Radius: 8px.
- Border: 1px slate.

Overlay crop:
- Insert `04_exception_detail.png`.
- Crop to show only:
  - the panel title **Exception Detail**
  - the status pill and confidence percentage
  - the **Recommended action** callout
  - the **Evidence** list
- Place it overlapping the bottom-right corner of the main screenshot.
- Overlay size: 38% of slide width.
- Border: 1.5px teal.
- Radius: 8px.

Label:
- Above the main screenshot, add:
```text
Exception queue with evidence
```
- Use Inter SemiBold.
- Color: white.

**Example PPT Layout**

```text
+--------------------------------------------------------------+
| TARGET AND BUSINESS POTENTIAL                                |
|                                                              |
| Beachhead:                    Exception queue with evidence  |
| SME finance teams             +----------------------------+ |
| handling cross-border         | 03_reconciliation_dashboard | |
| payments                      | crop: Reconciliation       | |
|                               | Dashboard + metric cards   | |
| Revenue path:                 |                            | |
| SaaS subscription             |                    +------+ | |
| Per-document usage            |                    |04_   | | |
| Bank / ERP integrations       |                    |except| | |
|                               |                    |detail| | |
|                               +--------------------+------+ |
+--------------------------------------------------------------+
```

**Speaker Notes**

The first target is SMEs that receive or send cross-border payments but do not have enterprise treasury software. The business model can start as SaaS, then add usage-based document processing and integrations with banks, accounting platforms, or ERP systems.

## Slide 8: Target Revenue Path

**Visible Text**

Target revenue path, 2026-2035

Amounts in US$ M

Main point => Primary revenue: SME SaaS + document usage
Connection => Refers to the first revenue layer: SME subscriptions and per-document processing
Connection => Supports the target path by validating product value and pricing before later channels scale

Main point => Primary revenue: accounting integrations
Connection => Refers to an added revenue layer: paid integrations with accounting workflows
Connection => Supports the target path by increasing document volume after core product validation

Main point => Primary revenue: bank / ERP partnerships
Connection => Refers to an added revenue layer: bank / ERP workflow partnerships
Connection => Supports the target path by expanding distribution through partner channels

Target revenue:
US$194M by 2035

**Important Note**

This is an assumption-based target model, not actual revenue. Use it to explain commercial ambition, not to claim validated sales.

**Visual**

Create a dark revenue projection chart similar to the reference image.

Chart endpoint:
```text
2035 target revenue: US$194M
```

The current PDF shows a visual projection curve ending near the 2035 target. Do not invent annual values unless the team confirms the year-by-year revenue model.

Revenue phase labels:
```text
2026-2028
Main point => Primary revenue: SME SaaS + document usage
Connection => Refers to the first revenue layer: SME subscriptions and per-document processing
Connection => Supports the target path by validating product value and pricing before later channels scale
```

```text
2029-2030
Main point => Primary revenue: accounting integrations
Connection => Refers to an added revenue layer: paid integrations with accounting workflows
Connection => Supports the target path by increasing document volume after core product validation
```

```text
2031-2035
Main point => Primary revenue: bank / ERP partnerships
Connection => Refers to an added revenue layer: bank / ERP workflow partnerships
Connection => Supports the target path by expanding distribution through partner channels
```

Canvas layout:
- Use the current PDF's black chart background.
- Put the title centered at the top in bright magenta.
- Put **Amounts in US$ M** directly under the title.
- Put the y-axis on the left with labels up to `200`.
- Put the x-axis along the bottom with years `2026` to `2035`.
- Draw a smooth rising magenta line ending near `US$194M` in 2035.
- Add a soft glow behind the line if using PowerPoint shape effects.
- Put small circular markers on 2026, 2027, 2029, 2031, and 2035.
- Place the three revenue phase labels near the line.
- Put the final target label on the right side:
```text
Target revenue:
US$194M
by 2035
```
- Put the assumption note at the bottom-left in small amber text:
```text
Assumption-based target model; not actual revenue.
```

How to build this slide in PowerPoint:
1. Insert a line chart that visually matches the current PDF and ends at `US$194M` in 2035.
2. Format the chart background as black or `#0F172A`.
3. Remove gridlines except for very faint horizontal guides if needed.
4. Format the revenue line as bright magenta or teal, 4px width.
5. Add a glow effect to the revenue line.
6. Add text boxes for the three revenue phase labels.
7. Add the large right-side target label: `US$194M by 2035`.
8. Add the small bottom-left assumption note.

Style:
- Slide background: black or `#0F172A`.
- Chart line: magenta `#E879F9` or teal `#14B8A6`.
- Axis labels: light slate.
- Main title: Inter Bold, magenta or white.
- Amount subtitle: Inter Italic, light slate.
- Phase labels: Inter SemiBold, white.
- Phase details: small light slate.
- Final target: large Inter Bold, white.
- Assumption note: amber.

**Example PPT Layout**

```text
+--------------------------------------------------------------+
|             Target revenue path, 2026-2035                   |
|                   Amounts in US$ M                           |
|                                                              |
| 200|                                             o US$194M    |
|    |                                      o-----/ by 2035     |
| 150|                                o----/                   |
| 100|                          o----/                         |
|  50|                    o----/                               |
|  0 | o-----o-----o----/                                      |
|     2026  2027  2028  2029  2030  2031  2032  2033  2034  2035 |
|                                                              |
| Main: SME SaaS + docs  Main: accounting integrations Main: Bank/ERP |
| Refers: subscriptions  Refers: paid workflows        Refers: workflow |
| Supports: validation   Supports: volume growth       Supports: channels |
|                                                              |
| Assumption-based target model; not actual revenue.           |
+--------------------------------------------------------------+
```

**Speaker Notes**

This slide is a target revenue model, not actual revenue. The current presentation sets the target at US$194M by 2035. The revenue logic follows the business path already stated in Slide 7: SaaS subscription, per-document usage, accounting integrations, and bank or ERP integrations. The primary revenue does not need to be described as replacing itself over time. A safer explanation is that revenue layers expand over time: the first point refers to SME subscriptions and per-document processing; it supports the main idea by validating product value and pricing before additional channels scale. The second refers to paid integrations with accounting workflows; it supports the main idea by increasing document volume after core product validation. The third refers to bank or ERP workflow partnerships; it supports the main idea by expanding distribution through partner channels. If judges ask, say the numbers are illustrative targets that would need validation through pricing tests, customer discovery, and partner conversations.

## Slide 9: Team Composition

**Visible Text**

Team composition

[Member 1]
[confirmed role / contribution]

[Member 2]
[confirmed role / contribution]

[Member 3]
[confirmed role / contribution]

[Member 4]
[confirmed role / contribution]

**Visual**

Create a clean four-column team layout.

Canvas layout:
- Use one equal-width column per confirmed team member.
- If the team has fewer than four members, remove unused columns.
- Each column should show the member name and their confirmed role or contribution.
- Do not invent responsibilities. Use only confirmed team details.

Suggested role wording examples:
```text
Product + Pitch
Frontend + Demo
Backend + Agent Workflow
Research + Validation
```

Use the examples only if they match the real team contributions.

Style:
- Slide background: `#0F172A`.
- Member names: Inter Bold, white.
- Role/contribution lines: Inter Medium, light slate.
- Optional thin teal divider under the title.
- Keep the layout simple and readable.

**Example PPT Layout**

```text
+--------------------------------------------------------------+
| TEAM COMPOSITION                                             |
|                                                              |
| [Member 1]       [Member 2]       [Member 3]       [Member 4] |
| [role/contrib]   [role/contrib]   [role/contrib]   [role/contrib] |
|                                                              |
| Use confirmed names and contributions only.                  |
+--------------------------------------------------------------+
```

**Speaker Notes**

This slide should introduce the registered team members and each person's confirmed contribution. Replace placeholders with real names and roles before submission.

## Slide 10: Closing

**Visible Text**

ReconPilot turns treasury mess into explainable decisions.

Faster reconciliation.

Clearer exceptions.

Human-controlled AI.

**Final Line**

Reconcile faster without giving up control.

**Visual**

Use `frontend/public/reconpilot.png`.

Canvas layout:
- Center the logo horizontally.
- Logo width: 38% of slide width.
- Place the visible text above the logo.
- Place **Reconcile faster without giving up control.** below the logo.

Text styling:
- Main closing line: large Inter Bold.
- Three short lines:
  - Faster reconciliation.
  - Clearer exceptions.
  - Human-controlled AI.
  should be smaller and spaced evenly.
- Final line should be teal.

Do not use screenshots on this slide.

**Example PPT Layout**

```text
+--------------------------------------------------------------+
| ReconPilot turns treasury mess into explainable decisions.   |
|                                                              |
| Faster reconciliation.                                       |
| Clearer exceptions.                                          |
| Human-controlled AI.                                         |
|                                                              |
|                    [reconpilot.png logo]                     |
|                    width: 38% of slide                       |
|                                                              |
|             Reconcile faster without giving up control.      |
+--------------------------------------------------------------+
```

**Speaker Notes**

ReconPilot is practical, demo-ready, and aligned with real treasury needs. It does not overpromise full autonomy. It gives reviewers a faster, clearer, and safer way to reconcile cross-border payments.

## 3-Minute Pitch Script

**0:00-0:20 Opening**
Treasury reconciliation is still painfully manual. Finance teams compare invoices, payment proofs, and bank statements across currencies, often dealing with missing proofs, duplicate payments, FX differences, and reference typos. ReconPilot is an AI-assisted reconciliation agent built for this workflow.

**0:20-0:45 Why Now**
This problem matters now because payment fraud is still widespread and treasury teams are under pressure to move faster. Cross-border and real-time payments add complexity, but finance teams still need evidence and auditability. ReconPilot helps automate the first pass without removing human review.

**0:45-1:20 Solution**
ReconPilot extracts structured records from messy documents, validates key fields, normalizes currency values, matches likely transactions, and flags exceptions. Each result includes a status, confidence score, evidence, explanation, and recommended next action.

**1:20-2:15 Demo**
In the demo, I load a synthetic casebook. The Extraction Review shows invoices, payment proofs, and bank transactions as structured records. Then I run matching. ReconPilot returns exact matches, FX tolerance issues, missing proof, duplicate payment, and typo-tolerant matches. I can open any exception and see why it was flagged.

**2:15-2:45 Technical Credibility**
The architecture is deliberately bounded. The LLM extracts and explains, while Python handles financial math, validation, scoring, and final reconciliation status. This reduces hallucination risk and makes the system more credible for treasury operations.

**2:45-3:00 Growth and Close**
ReconPilot starts as a focused reconciliation workspace, then grows through OCR, live FX, accounting integrations, and bank or ERP workflows. It is fast enough for a hackathon demo, practical enough for real finance teams, and designed to scale without giving up human control.

## Demo Cues

Use this order during the live demo:

1. Open `http://localhost:3002`.
2. Click **Load Demo Casebook**.
3. Point to Extraction Review and say: "These are structured records from synthetic treasury documents."
4. Click **Run Matching**.
5. Point to the summary counts: matched, review, missing proof, duplicate.
6. Open one exception and highlight confidence, evidence, and recommended action.
7. Scroll to Audit Report Preview.
8. Click **Export Audit JSON**.

## Expected Demo Result

```json
{
  "matched": 2,
  "review": 1,
  "missing_proof": 1,
  "duplicate": 1,
  "unmatched": 0,
  "automation_rate": 40
}
```

## Likely Judge Questions and Answers

**Q: Why not let the LLM do the whole reconciliation?**
A: Treasury needs reliability. The LLM is useful for extraction and explanation, but deterministic Python logic handles math, FX normalization, scoring, and final status decisions.

**Q: Is the data real?**
A: No. The demo uses synthetic data to avoid privacy risk. The pipeline is designed so real documents could be uploaded later with proper security and compliance controls.

**Q: How do you reduce hallucination?**
A: The LLM is bounded. Results are validated with Pydantic schemas, and final matching decisions are produced by deterministic rules. Every result includes evidence and confidence.

**Q: What makes this different from a normal OCR tool?**
A: OCR only reads documents. ReconPilot connects extracted records across invoices, proofs, and bank statements, then explains reconciliation status and exceptions.

**Q: How would this scale?**
A: Add bank feeds, ERP/accounting integrations, live FX rates, OCR for scanned documents, role-based approvals, and deployment with secure storage and audit logs.

**Q: What is the business value?**
A: It reduces manual reconciliation time, improves exception visibility, supports fraud review, and gives SMEs a practical treasury automation layer without requiring enterprise software.

## Screenshot Checklist

Capture these exact files for the deck and save them in `docs/screenshots/`:

1. `01_home_ready.png` - app top section before clicking anything.
2. `02_extraction_review.png` - after **Load Demo Casebook**, showing Extraction Review and Uploaded Documents.
3. `03_reconciliation_dashboard.png` - after **Run Matching**, showing the **Reconciliation Dashboard** panel, metric cards, and clickable result cards.
4. `04_exception_detail.png` - first non-matched result selected, showing **Exception Detail**, confidence, recommended action, and evidence.
5. `05_audit_report.png` - Audit Report Preview section.

## Submission Reminder

- Keep the deck at 10 slides.
- Replace team-composition placeholders with confirmed names and roles.
- Confirm the 2035 target amount and chart values before final export.
- Keep visible text short.
- Use screenshots only where specified.
- Include source footer only on Slide 2.
- Let the live demo carry the technical detail.
