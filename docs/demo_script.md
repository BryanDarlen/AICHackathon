# ReconPilot Demo Script

Use this for the live walkthrough. Use [pitch_deck_final.md](pitch_deck_final.md) for the full 10-slide pitch.

## 0:00 - 0:20 Opening

Treasury reconciliation is still painfully manual. Finance teams compare invoices, payment proofs, and bank statements across currencies, often dealing with missing proofs, duplicate payments, FX differences, and reference typos. ReconPilot is an AI-assisted reconciliation agent built for this workflow.

## 0:20 - 0:45 Why Now

Payment fraud is still widespread and treasury teams are under pressure to move faster. Cross-border and real-time payments add complexity, but finance teams still need evidence and auditability. ReconPilot automates the first pass without removing human review.

## 0:45 - 1:15 Load Demo Casebook

Open the app and click **Load Demo Casebook**. Explain that all data is synthetic and privacy-safe.

## 1:15 - 1:45 Extraction Review

Show extracted invoices, payment proofs, and bank transactions. Point out currencies, references, invoice IDs, and dates.

## 1:45 - 2:25 Reconciliation Dashboard

Click **Run Matching**. Show the expected decision mix:

- Exact matches.
- FX tolerance review.
- Missing proof.
- Duplicate payment.
- Typo-tolerant match.

## 2:25 - 2:50 Exception Detail

Open the most interesting exception. Highlight confidence, evidence, explanation, and recommended action.

## 2:50 - 3:10 Audit Report

Scroll to the audit report preview. Show the agent trace, trust controls, decision rows, and exportable report.

## 3:10 - 3:30 Closing

Explain the technical architecture: LLM for extraction/explanation, Python for validation/math/matching, audit trail for trust. Close with scalability: live FX, OCR, accounting integrations, and privacy-aware inference.
