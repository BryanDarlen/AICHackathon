# ReconPilot Pitch Deck Outline

Use [pitch_deck_final.md](pitch_deck_final.md) as the complete deck script.

1. **Title**  
   ReconPilot: Global Treasury Reconciliation Agent.

2. **Why Now**  
   Payment fraud, manual treasury workflows, and cross-border payment complexity make reconciliation urgent.

3. **Problem**  
   Invoices, payment proofs, FX differences, bank statements, and manual logs do not line up cleanly.

4. **Solution**  
   ReconPilot extracts, validates, matches, explains, and exports an audit report.

5. **Demo Workflow**  
   Load/upload documents, review extraction, run matching, inspect exceptions, export report.

6. **Agent Architecture**  
   ExtractAgent -> ValidateAgent -> MatchAgent -> ExplainAgent, with bounded LLM use.

7. **Technical Implementation**  
   Next.js, FastAPI, SQLite, OpenAI-compatible/Chutes-ready adapter, deterministic matching engine.

8. **Trust and Responsible AI**  
   Synthetic data, evidence, confidence, deterministic rules, human approval, audit trail.

9. **Impact and Scalability**  
   Faster reconciliation, stronger exception review, future bank/ERP/OCR/live-FX integrations.

10. **Closing**  
    ReconPilot turns messy cross-border treasury documents into explainable reconciliation decisions.
