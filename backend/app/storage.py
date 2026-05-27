from __future__ import annotations

import json
import os
import sqlite3
from pathlib import Path
from typing import Iterable

from .models import DocumentRecord, FinancialRecord, ReconciliationRun


def _model_dump(model):
    if hasattr(model, "model_dump"):
        return model.model_dump(mode="json")
    return model.dict()


def database_path() -> Path:
    raw = os.getenv("DATABASE_URL", "sqlite:///backend/.runtime/reconpilot.sqlite")
    if raw.startswith("sqlite:///"):
        return Path(raw[len("sqlite:///") :])
    return Path(raw)


class Repository:
    def __init__(self, path: Path | None = None):
        self.path = path or database_path()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self.init()

    def connect(self):
        return sqlite3.connect(self.path)

    def init(self) -> None:
        with self.connect() as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS documents (id TEXT PRIMARY KEY, payload TEXT NOT NULL)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS financial_records (id TEXT PRIMARY KEY, document_id TEXT NOT NULL, payload TEXT NOT NULL)"
            )
            conn.execute(
                "CREATE TABLE IF NOT EXISTS runs (id TEXT PRIMARY KEY, payload TEXT NOT NULL)"
            )

    def clear_demo(self) -> None:
        with self.connect() as conn:
            conn.execute("DELETE FROM documents")
            conn.execute("DELETE FROM financial_records")
            conn.execute("DELETE FROM runs")

    def save_documents(self, documents: Iterable[DocumentRecord]) -> None:
        with self.connect() as conn:
            for doc in documents:
                conn.execute(
                    "INSERT OR REPLACE INTO documents (id, payload) VALUES (?, ?)",
                    (doc.id, json.dumps(_model_dump(doc))),
                )

    def list_documents(self, ids: list[str] | None = None) -> list[DocumentRecord]:
        with self.connect() as conn:
            if ids:
                placeholders = ",".join("?" for _ in ids)
                rows = conn.execute(
                    f"SELECT payload FROM documents WHERE id IN ({placeholders})", ids
                ).fetchall()
            else:
                rows = conn.execute("SELECT payload FROM documents").fetchall()
        return [DocumentRecord(**json.loads(row[0])) for row in rows]

    def save_records(self, records: Iterable[FinancialRecord]) -> None:
        with self.connect() as conn:
            for record in records:
                conn.execute(
                    "INSERT OR REPLACE INTO financial_records (id, document_id, payload) VALUES (?, ?, ?)",
                    (
                        record.id,
                        record.document_id,
                        json.dumps(_model_dump(record)),
                    ),
                )

    def list_records(self, document_ids: list[str] | None = None) -> list[FinancialRecord]:
        with self.connect() as conn:
            if document_ids:
                placeholders = ",".join("?" for _ in document_ids)
                rows = conn.execute(
                    f"SELECT payload FROM financial_records WHERE document_id IN ({placeholders})",
                    document_ids,
                ).fetchall()
            else:
                rows = conn.execute("SELECT payload FROM financial_records").fetchall()
        return [FinancialRecord(**json.loads(row[0])) for row in rows]

    def save_run(self, run: ReconciliationRun) -> None:
        with self.connect() as conn:
            conn.execute(
                "INSERT OR REPLACE INTO runs (id, payload) VALUES (?, ?)",
                (run.id, json.dumps(_model_dump(run))),
            )

    def get_run(self, run_id: str) -> ReconciliationRun | None:
        with self.connect() as conn:
            row = conn.execute("SELECT payload FROM runs WHERE id = ?", (run_id,)).fetchone()
        if not row:
            return None
        return ReconciliationRun(**json.loads(row[0]))

    def counts(self) -> tuple[int, int]:
        with self.connect() as conn:
            documents = conn.execute("SELECT COUNT(*) FROM documents").fetchone()[0]
            records = conn.execute("SELECT COUNT(*) FROM financial_records").fetchone()[0]
        return documents, records
