from __future__ import annotations

import re
import uuid
from datetime import datetime
from difflib import SequenceMatcher
from typing import Iterable

from .models import EvidenceItem, FinancialRecord, MatchStatus, ReconciliationResult, ReconciliationRun, RecordType


FX_TO_MYR = {
    "MYR": 1.0,
    "RM": 1.0,
    "USD": 4.25,
    "SGD": 3.15,
    "EUR": 4.95,
    "GBP": 5.8,
}


def _new_id(prefix: str) -> str:
    return f"{prefix}_{uuid.uuid4().hex[:10]}"


def normalize_amount_myr(amount: float, currency: str) -> float:
    return round(amount * FX_TO_MYR.get(currency.upper(), 1.0), 2)


def _normalize_reference(value: str | None) -> str:
    if not value:
        return ""
    normalized = value.upper()
    normalized = normalized.replace("O", "0").replace("I", "1").replace("L", "1")
    return re.sub(r"[^A-Z0-9]", "", normalized)


def _similarity(a: str | None, b: str | None) -> float:
    left = _normalize_reference(a)
    right = _normalize_reference(b)
    if not left or not right:
        return 0.0
    if left in right or right in left:
        return 1.0
    return SequenceMatcher(None, left, right).ratio()


def _days_between(a: str, b: str) -> int | None:
    try:
        first = datetime.fromisoformat(a).date()
        second = datetime.fromisoformat(b).date()
        return abs((first - second).days)
    except ValueError:
        return None


def _date_score(invoice_date: str, transaction_date: str) -> float:
    days = _days_between(invoice_date, transaction_date)
    if days is None:
        return 0.35
    if days <= 2:
        return 1.0
    if days <= 7:
        return 0.75
    if days <= 14:
        return 0.45
    return 0.1


def _counterparty_score(invoice: FinancialRecord, transaction: FinancialRecord) -> float:
    if not invoice.payer or not transaction.payer:
        return 0.35
    return SequenceMatcher(None, invoice.payer.lower(), transaction.payer.lower()).ratio()


def _candidate_score(invoice: FinancialRecord, transaction: FinancialRecord) -> tuple[float, float]:
    invoice_myr = normalize_amount_myr(invoice.amount, invoice.currency)
    tx_myr = normalize_amount_myr(transaction.amount, transaction.currency)
    delta = abs(invoice_myr - tx_myr)
    tolerance = max(5.0, invoice_myr * 0.05)
    amount_score = max(0.0, 1.0 - min(delta / tolerance, 1.0))
    ref_score = max(
        _similarity(invoice.invoice_number, transaction.reference),
        _similarity(invoice.reference, transaction.reference),
        _similarity(invoice.invoice_number, transaction.description),
    )
    date_score = _date_score(invoice.date, transaction.date)
    counterparty_score = _counterparty_score(invoice, transaction)
    score = 0.48 * ref_score + 0.32 * amount_score + 0.12 * date_score + 0.08 * counterparty_score
    return round(score, 3), round(delta, 2)


def _proof_matches(invoice: FinancialRecord, proofs: Iterable[FinancialRecord]) -> list[FinancialRecord]:
    matches: list[FinancialRecord] = []
    invoice_myr = normalize_amount_myr(invoice.amount, invoice.currency)
    invoice_refs = [
        _normalize_reference(invoice.invoice_number),
        _normalize_reference(invoice.reference),
    ]
    for proof in proofs:
        proof_myr = normalize_amount_myr(proof.amount, proof.currency)
        proof_refs = [
            _normalize_reference(proof.reference),
            _normalize_reference(proof.invoice_number),
        ]
        exact_ref = any(
            left and right and (left in right or right in left)
            for left in invoice_refs
            for right in proof_refs
        )
        ref_score = max(
            _similarity(invoice.invoice_number, proof.reference),
            _similarity(invoice.reference, proof.reference),
            _similarity(invoice.invoice_number, proof.invoice_number),
        )
        amount_delta = abs(invoice_myr - proof_myr)
        if exact_ref or (ref_score >= 0.92 and amount_delta <= max(5.0, invoice_myr * 0.05)):
            matches.append(proof)
    return matches


def _evidence(invoice: FinancialRecord, transactions: list[FinancialRecord], delta: float | None) -> list[EvidenceItem]:
    items = [
        EvidenceItem(label="Invoice", value=invoice.invoice_number or invoice.reference or invoice.id, source=invoice.document_id),
        EvidenceItem(label="Invoice amount", value=f"{invoice.currency} {invoice.amount:.2f}", source=invoice.document_id),
        EvidenceItem(
            label="Expected MYR",
            value=f"MYR {normalize_amount_myr(invoice.amount, invoice.currency):.2f}",
            source="FX demo table",
        ),
    ]
    for tx in transactions:
        items.append(
            EvidenceItem(
                label="Bank transaction",
                value=f"{tx.date} | {tx.reference or 'no ref'} | {tx.currency} {tx.amount:.2f}",
                source=tx.document_id,
            )
        )
    if delta is not None:
        items.append(EvidenceItem(label="MYR delta", value=f"MYR {delta:.2f}", source="matching engine"))
    return items


def reconcile_records(records: list[FinancialRecord]) -> ReconciliationRun:
    normalized_records = []
    for record in records:
        record.normalized_amount_myr = normalize_amount_myr(record.amount, record.currency)
        normalized_records.append(record)

    invoices = [record for record in normalized_records if record.record_type == RecordType.invoice]
    proofs = [record for record in normalized_records if record.record_type == RecordType.payment]
    transactions = [record for record in normalized_records if record.record_type == RecordType.bank_transaction]

    results: list[ReconciliationResult] = []
    used_transaction_ids: set[str] = set()

    for invoice in invoices:
        scored = []
        for transaction in transactions:
            score, delta = _candidate_score(invoice, transaction)
            if score >= 0.58:
                scored.append((score, delta, transaction))
        scored.sort(key=lambda item: item[0], reverse=True)

        strong = [(score, delta, tx) for score, delta, tx in scored if score >= 0.82]
        selected = strong if len(strong) > 1 else scored[:1]
        selected_transactions = [item[2] for item in selected]
        for transaction in selected_transactions:
            used_transaction_ids.add(transaction.id)

        proof_matches = _proof_matches(invoice, proofs)
        best_score = scored[0][0] if scored else 0.0
        best_delta = scored[0][1] if scored else None
        invoice_myr = normalize_amount_myr(invoice.amount, invoice.currency)
        exact_delta = best_delta is not None and best_delta <= 2.0

        if len(strong) > 1:
            status = MatchStatus.duplicate
            confidence = min(0.98, best_score)
            explanation = "Multiple high-confidence bank transactions match the same invoice, indicating a likely duplicate payment."
            action = "Review duplicate transactions and confirm whether one should be refunded or reversed."
        elif not selected_transactions:
            status = MatchStatus.unmatched
            confidence = 0.35
            explanation = "No bank transaction reached the minimum match threshold for this invoice."
            action = "Request payment proof or check whether the payment has not arrived yet."
        elif not proof_matches:
            status = MatchStatus.missing_proof
            confidence = min(0.9, best_score)
            explanation = "A bank transaction appears to match the invoice, but no payment proof was provided."
            action = "Ask the customer or finance team to attach the missing payment proof."
        elif exact_delta and best_score >= 0.82:
            status = MatchStatus.matched
            confidence = min(0.97, best_score)
            explanation = "Invoice, payment proof, and bank transaction align by reference, date proximity, and MYR-normalized amount."
            action = "Approve reconciliation after human review."
        else:
            status = MatchStatus.review
            confidence = min(0.88, best_score)
            explanation = "The records are likely related, but the MYR amount differs enough to require review for FX fees, bank charges, or manual correction."
            action = "Review FX rate, bank fees, and payment proof before approving."

        results.append(
            ReconciliationResult(
                id=_new_id("result"),
                status=status,
                confidence=round(confidence, 2),
                invoice=invoice,
                payment_proofs=proof_matches,
                bank_transactions=selected_transactions,
                delta_myr=best_delta,
                evidence=_evidence(invoice, selected_transactions, best_delta),
                explanation=explanation,
                recommended_action=action,
            )
        )

    for transaction in transactions:
        if transaction.id in used_transaction_ids:
            continue
        if not any(_similarity(result.invoice.reference if result.invoice else "", transaction.reference) > 0.7 for result in results):
            results.append(
                ReconciliationResult(
                    id=_new_id("result"),
                    status=MatchStatus.unmatched,
                    confidence=0.4,
                    invoice=None,
                    payment_proofs=[],
                    bank_transactions=[transaction],
                    delta_myr=None,
                    evidence=[
                        EvidenceItem(
                            label="Unmatched bank transaction",
                            value=f"{transaction.date} | {transaction.reference or 'no ref'} | {transaction.currency} {transaction.amount:.2f}",
                            source=transaction.document_id,
                        )
                    ],
                    explanation="This bank transaction was not confidently linked to any invoice in the uploaded records.",
                    recommended_action="Check whether an invoice is missing or the reference was entered incorrectly.",
                )
            )

    total_value_myr = round(
        sum(normalize_amount_myr(invoice.amount, invoice.currency) for invoice in invoices), 2
    )
    cleared_value_myr = round(
        sum(
            normalize_amount_myr(result.invoice.amount, result.invoice.currency)
            for result in results
            if result.invoice and result.status == MatchStatus.matched
        ),
        2,
    )
    exception_value_myr = round(total_value_myr - cleared_value_myr, 2)

    summary = {
        "total_results": len(results),
        "matched": sum(1 for item in results if item.status == MatchStatus.matched),
        "review": sum(1 for item in results if item.status == MatchStatus.review),
        "missing_proof": sum(1 for item in results if item.status == MatchStatus.missing_proof),
        "duplicate": sum(1 for item in results if item.status == MatchStatus.duplicate),
        "unmatched": sum(1 for item in results if item.status == MatchStatus.unmatched),
        "requires_human_review": sum(1 for item in results if item.status != MatchStatus.matched),
        "total_value_myr": total_value_myr,
        "cleared_value_myr": cleared_value_myr,
        "exception_value_myr": exception_value_myr,
        "automation_rate": _automation_rate(results),
    }

    return ReconciliationRun(
        id=_new_id("run"),
        created_at=datetime.utcnow().isoformat(timespec="seconds") + "Z",
        summary=summary,
        agent_trace=[
            "ExtractAgent parsed invoices, payment proofs, and bank statement rows into structured records.",
            "ValidateAgent checked required fields, dates, currencies, amounts, and references.",
            "MatchAgent normalized currencies to MYR and scored reference, amount, date, and counterparty evidence.",
            "ExplainAgent generated human-readable decisions with confidence, evidence, and recommended action.",
        ],
        controls=[
            "LLM is bounded to extraction and explanation; matching and financial math are deterministic.",
            "Synthetic demo data avoids real bank or personal information.",
            "Human approval is required for review, missing proof, duplicate, and unmatched cases.",
            "OpenAI-compatible inference adapter keeps Chutes/OpenAI-style providers swappable.",
        ],
        results=results,
    )


def _automation_rate(results: list[ReconciliationResult]) -> float:
    if not results:
        return 0.0
    auto = sum(1 for result in results if result.status == MatchStatus.matched)
    return round((auto / len(results)) * 100, 1)
