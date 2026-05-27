# ReconPilot Project Walkthrough

## 1. Competition Strategy

ReconPilot targets the **Global Treasury Agent** problem statement from AI Marathon 2026. The product helps SMEs reconcile cross-border payments by processing invoices, payment proofs, and bank statements, then matching transactions across currencies with explanations and confidence scores.

The judging strategy is simple:

- Maximize **Impact and Problem Relevance** by solving the exact reconciliation workflow end-to-end.
- Maximize **Innovation and Creativity** by showing a bounded multi-step agent instead of a generic chatbot.
- Maximize **Technical Implementation** by combining LLM extraction with deterministic validation, FX conversion, matching, and audit reports.

## 2. MVP Scope

ReconPilot must demonstrate:

1. Document intake for invoices, payment proofs, and bank statements.
2. Structured extraction into financial records.
3. Currency normalization into MYR.
4. Matching across invoice, proof, and bank transaction records.
5. Exception detection for mismatch, duplicate payment, missing proof, and typo-tolerant references.
6. Explainable output with confidence, evidence, and recommended action.
7. Visible agent trace, trust controls, and exportable audit-style report.

The MVP intentionally avoids overbuilding. Live LLM extraction is supported through an OpenAI-compatible API, but the demo works offline using synthetic sample data and deterministic parsers.

## 3. Architecture

```text
Frontend (Next.js)
  Upload Workspace
  Extraction Review
  Reconciliation Dashboard
  Exception Detail
  Audit Report

Backend (FastAPI)
  /api/upload
  /api/extract
  /api/reconcile
  /api/report/{run_id}
  /api/health

Agent Pipeline
  ExtractAgent -> ValidateAgent -> MatchAgent -> ExplainAgent

Storage
  SQLite database
  Local uploads
  Synthetic sample documents

Inference
  OpenAI-compatible API adapter
  Demo-mode fallback
```

## 4. Agent Pipeline

### ExtractAgent

Reads uploaded or sample files, extracts raw text/tables, and converts them into structured financial records.

### ValidateAgent

Checks required fields, normalizes dates and currencies, and marks records that need review.

### MatchAgent

Uses deterministic rules to compare records:

- Amount after FX conversion.
- Date proximity.
- Invoice/reference similarity.
- Counterparty similarity.
- Presence or absence of payment proof.
- Duplicate transaction detection.

### ExplainAgent

Produces judge-friendly explanations with evidence, confidence, and recommended next action.

## 5. Demo Cases

| Case | Scenario | Expected Output |
| --- | --- | --- |
| 1 | USD invoice matched to exact MYR bank payment | Matched |
| 2 | USD invoice with FX fee difference | Review |
| 3 | SGD invoice has bank payment but no payment proof | Missing Proof |
| 4 | MYR invoice paid twice | Duplicate |
| 5 | USD invoice with OCR/reference typo | Matched with explanation |

All data is synthetic and safe for demonstration.

## 6. Environment Variables

```env
LLM_BASE_URL=https://llm.chutes.ai/v1
LLM_API_KEY=replace_with_key
LLM_MODEL=replace_with_model
DATABASE_URL=sqlite:///backend/.runtime/reconpilot.sqlite
DEMO_MODE=true
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

## 7. Local Run

Backend:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
python -m uvicorn app.main:app --app-dir backend --host 127.0.0.1 --port 8000 --reload
```

Frontend:

```powershell
cd frontend
npm install
npm run dev
```

If Windows/Next.js fails because the project path contains `!`, run:

```powershell
.\scripts\run_frontend.ps1
```

Open:

```text
http://localhost:3000
```

## 8. Pitch Story

Opening hook:

> SMEs do not lose time because invoices are missing. They lose time because a USD invoice, an RM bank deposit, and a messy payment proof do not look like the same transaction. ReconPilot turns that chaos into an explainable reconciliation decision.

Technical positioning:

- LLMs extract and explain.
- Python validates, calculates, and matches.
- Every decision includes evidence.
- Human approval stays in the loop.
- Demo data is synthetic and privacy-safe.

## 9. Final Submission Checklist

- Working app.
- Public/shared repository.
- README with setup instructions.
- `.env.example`.
- Synthetic sample data.
- Agent framework diagram.
- 3-4 minute demo video.
- Pitch deck under 10 content slides.
- Backup screenshots or recorded demo.
- No API keys committed.
