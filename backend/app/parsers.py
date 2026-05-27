from __future__ import annotations

import csv
from pathlib import Path

from .models import DocumentType


SUPPORTED_EXTENSIONS = {".txt", ".csv", ".xlsx", ".xls", ".pdf", ".png", ".jpg", ".jpeg"}


def detect_document_type(filename: str, text: str) -> DocumentType:
    haystack = f"{filename}\n{text}".lower()
    if "bank statement" in haystack or filename.lower().endswith(".csv") or "counterparty" in haystack:
        return DocumentType.bank_statement
    if "payment proof" in haystack or "amount paid" in haystack:
        return DocumentType.payment_proof
    if "invoice" in haystack:
        return DocumentType.invoice
    return DocumentType.unknown


def parse_file(path: Path) -> tuple[str, str]:
    suffix = path.suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        return "", f"unsupported file type: {suffix}"

    if suffix == ".txt":
        return path.read_text(encoding="utf-8", errors="ignore"), "parsed"

    if suffix == ".csv":
        return _read_csv(path), "parsed"

    if suffix in {".xlsx", ".xls"}:
        return _read_excel(path), "parsed"

    if suffix == ".pdf":
        return _read_pdf(path), "parsed"

    if suffix in {".png", ".jpg", ".jpeg"}:
        return "", "image uploaded; OCR adapter not enabled in MVP"

    return "", "unknown parse status"


def _read_csv(path: Path) -> str:
    with path.open("r", encoding="utf-8", errors="ignore", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = list(reader)
        if not rows:
            return path.read_text(encoding="utf-8", errors="ignore")
        header = ",".join(reader.fieldnames or [])
        body = ["|".join(f"{key}={row.get(key, '')}" for key in reader.fieldnames or []) for row in rows]
        return "\n".join([header, *body])


def _read_excel(path: Path) -> str:
    try:
        import pandas as pd

        df = pd.read_excel(path)
        return df.to_csv(index=False)
    except Exception as exc:  # pragma: no cover - depends on optional workbook engines
        return f"Excel parsing failed: {exc}"


def _read_pdf(path: Path) -> str:
    try:
        import pdfplumber

        pages: list[str] = []
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                pages.append(page.extract_text() or "")
        text = "\n".join(pages).strip()
        if text:
            return text
    except Exception:
        pass

    try:
        import fitz

        doc = fitz.open(path)
        return "\n".join(page.get_text() for page in doc)
    except Exception as exc:  # pragma: no cover - depends on optional PDF engines
        return f"PDF parsing failed: {exc}"
