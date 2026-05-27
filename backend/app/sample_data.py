from __future__ import annotations

import shutil
import uuid
from datetime import datetime
from pathlib import Path

from .models import DocumentRecord
from .parsers import detect_document_type, parse_file


ROOT = Path(__file__).resolve().parents[2]
SAMPLES_DIR = ROOT / "data" / "samples"
UPLOADS_DIR = ROOT / "backend" / ".runtime" / "uploads"


def _new_id() -> str:
    return f"doc_{uuid.uuid4().hex[:10]}"


def load_demo_documents() -> list[DocumentRecord]:
    UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
    documents: list[DocumentRecord] = []
    for sample in sorted(SAMPLES_DIR.iterdir()):
        if not sample.is_file():
            continue
        target = UPLOADS_DIR / f"demo_{sample.name}"
        shutil.copyfile(sample, target)
        text, status = parse_file(target)
        documents.append(
            DocumentRecord(
                id=_new_id(),
                filename=sample.name,
                document_type=detect_document_type(sample.name, text),
                extracted_text=text,
                parse_status=status,
                created_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
            )
        )
    return documents
