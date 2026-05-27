from __future__ import annotations

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class DocumentType(str, Enum):
    invoice = "invoice"
    payment_proof = "payment_proof"
    bank_statement = "bank_statement"
    unknown = "unknown"


class RecordType(str, Enum):
    invoice = "invoice"
    payment = "payment"
    bank_transaction = "bank_transaction"


class MatchStatus(str, Enum):
    matched = "matched"
    review = "review"
    missing_proof = "missing_proof"
    duplicate = "duplicate"
    unmatched = "unmatched"


class DocumentRecord(BaseModel):
    id: str
    filename: str
    document_type: DocumentType
    extracted_text: str = ""
    parse_status: str = "parsed"
    created_at: str


class FinancialRecord(BaseModel):
    id: str
    document_id: str
    record_type: RecordType
    amount: float
    currency: str
    date: str
    payer: str | None = None
    payee: str | None = None
    invoice_number: str | None = None
    reference: str | None = None
    description: str | None = None
    raw_text: str | None = None
    confidence: float = 0.75
    normalized_amount_myr: float | None = None
    validation_notes: list[str] = Field(default_factory=list)


class EvidenceItem(BaseModel):
    label: str
    value: str
    source: str | None = None


class ReconciliationResult(BaseModel):
    id: str
    status: MatchStatus
    confidence: float
    invoice: FinancialRecord | None = None
    payment_proofs: list[FinancialRecord] = Field(default_factory=list)
    bank_transactions: list[FinancialRecord] = Field(default_factory=list)
    delta_myr: float | None = None
    evidence: list[EvidenceItem] = Field(default_factory=list)
    explanation: str
    recommended_action: str


class ReconciliationRun(BaseModel):
    id: str
    created_at: str
    summary: dict[str, Any]
    agent_trace: list[str] = Field(default_factory=list)
    controls: list[str] = Field(default_factory=list)
    results: list[ReconciliationResult]


class UploadResponse(BaseModel):
    documents: list[DocumentRecord]


class ExtractRequest(BaseModel):
    document_ids: list[str] = Field(default_factory=list)
    use_demo: bool = False


class ExtractionResponse(BaseModel):
    documents: list[DocumentRecord]
    records: list[FinancialRecord]
    source: str


class ReconcileRequest(BaseModel):
    document_ids: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    status: str
    demo_mode: bool
    documents: int
    records: int
