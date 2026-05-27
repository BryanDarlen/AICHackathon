import unittest
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from app.models import FinancialRecord, RecordType, MatchStatus
from app.reconcile import reconcile_records


def record(record_type, amount, currency, date, reference, payer=None, invoice_number=None):
    return FinancialRecord(
        id=f"{record_type}_{reference}_{amount}",
        document_id=f"doc_{reference}",
        record_type=record_type,
        amount=amount,
        currency=currency,
        date=date,
        payer=payer,
        payee="Vendor",
        invoice_number=invoice_number,
        reference=reference,
        description=reference,
        confidence=0.9,
    )


class ReconciliationTests(unittest.TestCase):
    def test_exact_match(self):
        run = reconcile_records(
            [
                record(RecordType.invoice, 10, "USD", "2026-05-12", "INV-1001", "Buyer", "INV-1001"),
                record(RecordType.payment, 10, "USD", "2026-05-13", "INV-1001", "Buyer"),
                record(RecordType.bank_transaction, 42.50, "MYR", "2026-05-13", "INV-1001", "Buyer"),
            ]
        )
        self.assertEqual(run.results[0].status, MatchStatus.matched)

    def test_missing_proof(self):
        run = reconcile_records(
            [
                record(RecordType.invoice, 300, "SGD", "2026-05-15", "INV-1003", "APU Robotics Lab", "INV-1003"),
                record(RecordType.bank_transaction, 945, "MYR", "2026-05-16", "INV-1003", "APU Robotics Lab"),
            ]
        )
        self.assertEqual(run.results[0].status, MatchStatus.missing_proof)

    def test_duplicate_payment(self):
        run = reconcile_records(
            [
                record(RecordType.invoice, 880, "MYR", "2026-05-16", "INV-1004", "Merdeka Books", "INV-1004"),
                record(RecordType.payment, 880, "MYR", "2026-05-17", "INV-1004", "Merdeka Books"),
                record(RecordType.bank_transaction, 880, "MYR", "2026-05-17", "INV-1004", "Merdeka Books"),
                record(RecordType.bank_transaction, 880, "MYR", "2026-05-17", "INV-1004", "Merdeka Books"),
            ]
        )
        self.assertEqual(run.results[0].status, MatchStatus.duplicate)

    def test_reference_typo_still_matches(self):
        run = reconcile_records(
            [
                record(RecordType.invoice, 75, "USD", "2026-05-18", "INV-1005", "GreenMart Asia", "INV-1005"),
                record(RecordType.payment, 75, "USD", "2026-05-19", "INV-I005", "GreenMart Asia"),
                record(RecordType.bank_transaction, 318.75, "MYR", "2026-05-19", "INV-I005", "GreenMart Asia"),
            ]
        )
        self.assertEqual(run.results[0].status, MatchStatus.matched)


if __name__ == "__main__":
    unittest.main()
