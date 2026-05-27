from __future__ import annotations

import os
import shutil
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from .agents import ExtractAgent, ValidateAgent
from .llm_client import demo_mode_enabled
from .models import (
    AgentStatusResponse,
    ExtractRequest,
    ExtractionResponse,
    HealthResponse,
    ReconcileRequest,
    ReconciliationRun,
    UploadResponse,
    DocumentRecord,
)
from .parsers import SUPPORTED_EXTENSIONS, detect_document_type, parse_file
from .reconcile import reconcile_records
from .sample_data import UPLOADS_DIR, load_demo_documents
from .storage import Repository


app = FastAPI(title="ReconPilot API", version="0.1.0")
DEV_FRONTEND_ORIGINS = [
    f"http://localhost:{port}" for port in range(3000, 3006)
] + [
    f"http://127.0.0.1:{port}" for port in range(3000, 3006)
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=DEV_FRONTEND_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

repo = Repository()
extract_agent = ExtractAgent()
validate_agent = ValidateAgent()


def _new_doc_id() -> str:
    return f"doc_{uuid.uuid4().hex[:10]}"


def _clean_document_ids(document_ids: list[str]) -> list[str]:
    """Ignore Swagger's default placeholder so manual API testing is forgiving."""
    return [item for item in document_ids if item and item.lower() != "string"]


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "ReconPilot API",
        "status": "ok",
        "docs": "/docs",
        "health": "/api/health",
    }


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    documents, records = repo.counts()
    return HealthResponse(
        status="ok",
        demo_mode=demo_mode_enabled(),
        documents=documents,
        records=records,
    )


@app.get("/api/agent/status", response_model=AgentStatusResponse)
def agent_status() -> AgentStatusResponse:
    documents, records = repo.counts()
    demo_mode = demo_mode_enabled()
    mode = "demo fallback" if demo_mode else "live LLM adapter"
    return AgentStatusResponse(
        status="connected",
        mode=mode,
        pipeline=["ExtractAgent", "ValidateAgent", "MatchAgent", "ExplainAgent"],
        documents=documents,
        records=records,
        message=(
            "Dashboard is connected to the bounded agent pipeline. "
            "LLM extraction is disabled in demo mode."
            if demo_mode
            else "Dashboard is connected to the bounded agent pipeline with live LLM extraction available."
        ),
    )


@app.post("/api/upload", response_model=UploadResponse)
async def upload(files: list[UploadFile] = File(...)) -> UploadResponse:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    documents: list[DocumentRecord] = []

    for file in files:
        suffix = Path(file.filename or "").suffix.lower()
        if suffix not in SUPPORTED_EXTENSIONS:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {suffix}")

        safe_name = Path(file.filename or "upload").name
        target = UPLOADS_DIR / f"{uuid.uuid4().hex}_{safe_name}"
        with target.open("wb") as handle:
            shutil.copyfileobj(file.file, handle)

        text, status = parse_file(target)
        documents.append(
            DocumentRecord(
                id=_new_doc_id(),
                filename=safe_name,
                document_type=detect_document_type(safe_name, text),
                extracted_text=text,
                parse_status=status,
                created_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
            )
        )

    repo.save_documents(documents)
    return UploadResponse(documents=documents)


@app.post("/api/extract", response_model=ExtractionResponse)
def extract(request: ExtractRequest | None = None) -> ExtractionResponse:
    request = request or ExtractRequest()
    document_ids = _clean_document_ids(request.document_ids)
    if request.use_demo:
        repo.clear_demo()
        documents = load_demo_documents()
        repo.save_documents(documents)
    else:
        documents = repo.list_documents(document_ids or None)

    if not documents:
        raise HTTPException(status_code=404, detail="No documents found. Upload files or use demo data.")

    records, source = extract_agent.extract(documents)
    records = validate_agent.validate(records)
    repo.save_records(records)
    return ExtractionResponse(documents=documents, records=records, source=source)


@app.post("/api/reconcile", response_model=ReconciliationRun)
def reconcile(request: ReconcileRequest | None = None) -> ReconciliationRun:
    request = request or ReconcileRequest()
    document_ids = _clean_document_ids(request.document_ids)
    records = repo.list_records(document_ids or None)
    if not records:
        raise HTTPException(status_code=404, detail="No extracted records found. Run extraction first.")
    run = reconcile_records(records)
    repo.save_run(run)
    return run


@app.get("/api/report/{run_id}", response_model=ReconciliationRun)
def report(run_id: str) -> ReconciliationRun:
    run = repo.get_run(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Report not found")
    return run
