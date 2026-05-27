# ReconPilot

ReconPilot is a Global Treasury Reconciliation Agent built for **AI Marathon 2026**. It processes invoices, payment proofs, and bank statements, then matches transactions across currencies with confidence scores, evidence, and audit-ready explanations.

## Why It Matters

SMEs often receive local-currency bank deposits for foreign-currency invoices. Manual reconciliation requires reading documents, converting currencies, checking references, detecting duplicates, and logging exceptions. ReconPilot automates the first pass while keeping a human reviewer in control.

## Features

- Upload invoices, payment proofs, and bank statements.
- Extract structured financial records.
- Normalize currencies to MYR.
- Match invoices to payment proofs and bank transactions.
- Detect missing proof, duplicates, FX tolerance issues, and reference typos.
- Explain every result with confidence, evidence, recommended action, and an audit trail.
- Run a complete demo offline with synthetic data.

## Architecture

```text
Next.js dashboard -> FastAPI backend -> Bounded agent pipeline -> SQLite/local storage
                                          -> OpenAI-compatible LLM adapter
                                          -> deterministic reconciliation engine
```

The LLM is intentionally bounded. It extracts and explains, while Python performs validation, currency math, scoring, and final status decisions. This matches the workshop guidance: tools over cleverness, visible agent loops, privacy-conscious inference, and human review for sensitive actions.

The dashboard communicates with the backend agent layer through the API. On load, it calls `/api/health` and `/api/agent/status` so the UI can show whether the backend is reachable, whether it is using demo fallback or live LLM mode, and which agent steps are available.

## Quick Start

### 1. Install Backend Dependencies

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r backend/requirements.txt
```

### 2. Install Frontend Dependencies

```powershell
npm install
```

### 3. Start the Backend

```powershell
npm run backend
```

The backend runs on `http://127.0.0.1:8000`. Keep this terminal open while using the app.

If port `8000` is already occupied by a stale ReconPilot backend process, use:

```powershell
npm run backend:clean
```

### 4. Start the Frontend

Open a second terminal and run:

```powershell
npm run frontend
```

Open `http://localhost:3002`.

The root `dev` command also runs the safe frontend helper. It stops a stale Node process on port `3002`, clears the generated `.next` cache, and starts Next.js in the visible terminal. Keep that terminal open while using the app. Press `Ctrl+C` in that same terminal to stop the frontend cleanly.

If you prefer to call the helper directly, use:

```powershell
.\scripts\run_frontend.ps1 -StopExisting -CleanCache
```

To stop the frontend without starting it again:

```powershell
.\scripts\stop_frontend.ps1
```

If the project folder path contains exclamation marks, `run_frontend.ps1` also maps a temporary drive automatically to avoid Next.js/Webpack path validation issues.

## Environment Variables

Copy `.env.example` to `.env` for the backend and update values if using live inference.

```env
LLM_BASE_URL=https://llm.chutes.ai/v1
LLM_API_KEY=replace_with_key
LLM_MODEL=replace_with_model
DATABASE_URL=sqlite:///backend/.runtime/reconpilot.sqlite
DEMO_MODE=true
NEXT_PUBLIC_API_URL=http://127.0.0.1:8000
```

With `DEMO_MODE=true`, ReconPilot can run without a live API key using synthetic sample data and deterministic extraction.

To test a configured Chutes/OpenAI-compatible API key without starting the full app:

```powershell
python scripts\test_chutes.py
```

The test reads `.env`, temporarily forces live inference for the test process, and prints whether the provider responded with valid JSON.

## Sample Data

The `data/samples/` folder contains synthetic invoices, payment proofs, and bank statements. No real financial data is used.

Demo scenarios:

- Perfect USD invoice to MYR bank payment.
- FX fee/tolerance mismatch.
- Missing payment proof.
- Duplicate payment.
- OCR/reference typo that is still matchable.

## API

| Method | Endpoint | Purpose |
| --- | --- | --- |
| GET | `/api/health` | Backend health check |
| GET | `/api/agent/status` | Dashboard-to-agent connectivity, mode, and pipeline status |
| POST | `/api/upload` | Upload user files |
| POST | `/api/extract` | Extract structured records |
| POST | `/api/reconcile` | Run reconciliation |
| GET | `/api/report/{run_id}` | Fetch final report |

The frontend uses `NEXT_PUBLIC_API_URL` to reach the backend. If it is not set, the dashboard defaults to `http://127.0.0.1:8000`.

The agent status endpoint returns the current operating mode:

- `demo fallback` when `DEMO_MODE=true`
- `live LLM adapter` when live inference is enabled

It also returns the visible pipeline used by the dashboard: `ExtractAgent`, `ValidateAgent`, `MatchAgent`, and `ExplainAgent`.

When using Swagger at `/docs`, run `POST /api/extract` first with:

```json
{ "use_demo": true, "document_ids": [] }
```

Then run `POST /api/reconcile`. If Swagger shows `["string"]` as the default document ID, ReconPilot now safely treats that placeholder as "use all extracted records."

## Testing

```powershell
python -m unittest discover backend/tests
```

The same tests also pass from inside the backend folder:

```powershell
cd backend
python -m unittest discover tests
```

## Privacy and Responsible AI

- Demo data is synthetic.
- API keys are kept in environment variables.
- The LLM is not allowed to make final financial decisions alone.
- Every match includes confidence, evidence, and a recommended human action.
- Deterministic validation and matching reduce hallucination risk.
- The UI shows the agent trace and trust controls so judges can inspect how decisions were produced.

## Known Limitations

- OCR for scanned images is adapter-ready but not enabled by default.
- FX rates are fixed demo rates, not live market rates.
- SQLite/local storage is used for the hackathon MVP.
- The current UI is optimized for demo clarity rather than enterprise role-based access.

## Future Enhancements

- Live FX API integration.
- Chutes-specific privacy/inference configuration.
- Multi-model routing.
- OCR for low-quality scans.
- Accounting platform integrations.
- Sign in with Chutes for user-owned inference credits.
