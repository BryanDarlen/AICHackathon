from __future__ import annotations

import csv
import io
import re
import uuid

from .llm_client import LLMUnavailable, chat_json
from .models import DocumentRecord, DocumentType, FinancialRecord, RecordType


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def _label(text: str, *labels: str) -> str | None:
    for label in labels:
        pattern = rf"^{re.escape(label)}\s*:\s*(.+)$"
        match = re.search(pattern, text, re.IGNORECASE | re.MULTILINE)
        if match:
            return match.group(1).strip()
    return None


def _amount(text: str) -> float:
    raw = _label(text, "Amount", "Amount Paid", "Total", "Payment Amount") or "0"
    match = re.search(r"-?\d+(?:,\d{3})*(?:\.\d+)?", raw)
    if not match:
        return 0.0
    return float(match.group(0).replace(",", ""))


def _currency(text: str) -> str:
    raw = _label(text, "Currency") or ""
    match = re.search(r"\b(MYR|RM|USD|SGD|EUR|GBP)\b", raw, re.IGNORECASE)
    if match:
        value = match.group(1).upper()
        return "MYR" if value == "RM" else value
    match = re.search(r"\b(MYR|RM|USD|SGD|EUR|GBP)\b", text, re.IGNORECASE)
    if match:
        value = match.group(1).upper()
        return "MYR" if value == "RM" else value
    return "MYR"


class ExtractAgent:
    def extract(self, documents: list[DocumentRecord]) -> tuple[list[FinancialRecord], str]:
        records: list[FinancialRecord] = []
        source = "deterministic_parser"
        for document in documents:
            records.extend(self._extract_document(document))
        return records, source

    def _extract_document(self, document: DocumentRecord) -> list[FinancialRecord]:
        if document.document_type == DocumentType.bank_statement:
            return self._extract_bank_statement(document)

        llm_records = self._try_llm_extract(document)
        if llm_records:
            return llm_records

        return [self._extract_text_financial_record(document)]

    def _try_llm_extract(self, document: DocumentRecord) -> list[FinancialRecord]:
        system = (
            "Extract financial records as JSON. Return {'records':[...]} only. "
            "Each record needs record_type, amount, currency, date, payer, payee, "
            "invoice_number, reference, description, confidence."
        )
        user = f"Filename: {document.filename}\nDocument type: {document.document_type}\n\n{document.extracted_text}"
        try:
            payload = chat_json(system, user)
        except LLMUnavailable:
            return []

        records: list[FinancialRecord] = []
        for item in payload.get("records", []):
            try:
                records.append(
                    FinancialRecord(
                        id=_new_id("rec"),
                        document_id=document.id,
                        record_type=RecordType(item.get("record_type", document.document_type.value)),
                        amount=float(item.get("amount", 0)),
                        currency=str(item.get("currency", "MYR")).upper(),
                        date=str(item.get("date", "")),
                        payer=item.get("payer"),
                        payee=item.get("payee"),
                        invoice_number=item.get("invoice_number"),
                        reference=item.get("reference"),
                        description=item.get("description"),
                        raw_text=document.extracted_text,
                        confidence=float(item.get("confidence", 0.75)),
                    )
                )
            except Exception:
                continue
        return records

    def _extract_text_financial_record(self, document: DocumentRecord) -> FinancialRecord:
        text = document.extracted_text
        if document.document_type == DocumentType.payment_proof:
            record_type = RecordType.payment
            date = _label(text, "Payment Date", "Date") or ""
            payer = _label(text, "Payer", "Buyer")
            payee = _label(text, "Payee", "Seller")
            invoice_number = _label(text, "Invoice Number")
            reference = _label(text, "Bank Reference", "Reference") or invoice_number
        else:
            record_type = RecordType.invoice
            date = _label(text, "Invoice Date", "Date") or ""
            payer = _label(text, "Buyer", "Payer")
            payee = _label(text, "Seller", "Payee")
            invoice_number = _label(text, "Invoice Number")
            reference = _label(text, "Reference", "Bank Reference") or invoice_number

        return FinancialRecord(
            id=_new_id("rec"),
            document_id=document.id,
            record_type=record_type,
            amount=_amount(text),
            currency=_currency(text),
            date=date,
            payer=payer,
            payee=payee,
            invoice_number=invoice_number,
            reference=reference,
            description=_label(text, "Description"),
            raw_text=text,
            confidence=0.82,
        )

    def _extract_bank_statement(self, document: DocumentRecord) -> list[FinancialRecord]:
        records: list[FinancialRecord] = []
        lines = [line for line in document.extracted_text.splitlines() if line.strip()]
        if not lines:
            return records

        if "|" in document.extracted_text:
            parsed_rows = []
            for line in lines[1:]:
                row = {}
                for part in line.split("|"):
                    if "=" in part:
                        key, value = part.split("=", 1)
                        row[key.strip()] = value.strip()
                parsed_rows.append(row)
        else:
            parsed_rows = list(csv.DictReader(io.StringIO(document.extracted_text)))

        for row in parsed_rows:
            try:
                records.append(
                    FinancialRecord(
                        id=_new_id("bank"),
                        document_id=document.id,
                        record_type=RecordType.bank_transaction,
                        amount=float(str(row.get("amount", "0")).replace(",", "")),
                        currency=str(row.get("currency", "MYR")).upper(),
                        date=str(row.get("date", "")),
                        payer=str(row.get("counterparty", "") or ""),
                        payee=None,
                        invoice_number=None,
                        reference=str(row.get("reference", "") or ""),
                        description=str(row.get("description", "") or ""),
                        raw_text="; ".join(f"{key}={value}" for key, value in row.items()),
                        confidence=0.9,
                    )
                )
            except ValueError:
                continue
        return records


class ValidateAgent:
    def validate(self, records: list[FinancialRecord]) -> list[FinancialRecord]:
        for record in records:
            notes: list[str] = []
            if record.amount <= 0:
                notes.append("Amount is missing or invalid.")
            if not record.currency:
                notes.append("Currency is missing.")
            if not record.date:
                notes.append("Date is missing.")
            if record.record_type != RecordType.bank_transaction and not (
                record.invoice_number or record.reference
            ):
                notes.append("Invoice number or reference is missing.")
            record.validation_notes = notes
        return records
