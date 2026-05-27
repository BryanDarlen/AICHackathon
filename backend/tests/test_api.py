import unittest
import sys
from pathlib import Path

BACKEND_ROOT = Path(__file__).resolve().parents[1]
if str(BACKEND_ROOT) not in sys.path:
    sys.path.insert(0, str(BACKEND_ROOT))

from fastapi.testclient import TestClient

from app.main import app


class ApiFlowTests(unittest.TestCase):
    def test_demo_extract_then_swagger_placeholder_reconcile(self):
        client = TestClient(app)

        extraction = client.post(
            "/api/extract", json={"use_demo": True, "document_ids": []}
        )
        self.assertEqual(extraction.status_code, 200)
        self.assertEqual(len(extraction.json()["records"]), 15)

        # Swagger UI shows ["string"] by default. Treat it as no filter.
        reconcile = client.post("/api/reconcile", json={"document_ids": ["string"]})
        self.assertEqual(reconcile.status_code, 200)
        summary = reconcile.json()["summary"]
        self.assertEqual(summary["matched"], 2)
        self.assertEqual(summary["review"], 1)
        self.assertEqual(summary["missing_proof"], 1)
        self.assertEqual(summary["duplicate"], 1)
        self.assertEqual(summary["requires_human_review"], 3)
        self.assertEqual(summary["cleared_value_myr"], 361.25)
        self.assertEqual(summary["exception_value_myr"], 2335.0)
        self.assertEqual(len(reconcile.json()["agent_trace"]), 4)
        self.assertEqual(len(reconcile.json()["controls"]), 4)

        empty_body_reconcile = client.post("/api/reconcile")
        self.assertEqual(empty_body_reconcile.status_code, 200)

    def test_root_endpoint_guides_manual_users(self):
        client = TestClient(app)
        response = client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["docs"], "/docs")


if __name__ == "__main__":
    unittest.main()
