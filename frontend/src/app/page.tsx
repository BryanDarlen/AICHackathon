"use client";

import { useEffect, useMemo, useState, type ReactNode } from "react";
import { api } from "../lib/api";
import type {
  DocumentRecord,
  ExtractionResponse,
  FinancialRecord,
  MatchStatus,
  ReconciliationResult,
  ReconciliationRun
} from "../types";

const statusLabel: Record<MatchStatus, string> = {
  matched: "Matched",
  review: "Needs Review",
  missing_proof: "Missing Proof",
  duplicate: "Duplicate",
  unmatched: "Unmatched"
};

const workflowSteps = [
  {
    name: "ExtractAgent",
    detail: "Reads invoices, proofs, and bank rows into one finance record format."
  },
  {
    name: "ValidateAgent",
    detail: "Checks dates, currencies, references, and fields that need review."
  },
  {
    name: "MatchAgent",
    detail: "Compares amount, FX, date, reference, and counterparty evidence."
  },
  {
    name: "ExplainAgent",
    detail: "Turns each decision into confidence, evidence, and a next action."
  }
];

const trustControls = [
  { marker: "Data", label: "Synthetic demo data only" },
  { marker: "Rules", label: "Deterministic FX and matching" },
  { marker: "Gate", label: "Human approval for exceptions" },
  { marker: "LLM", label: "OpenAI-compatible / Chutes-ready" }
];

export default function Home() {
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [health, setHealth] = useState<string>("checking");
  const [documents, setDocuments] = useState<DocumentRecord[]>([]);
  const [records, setRecords] = useState<FinancialRecord[]>([]);
  const [source, setSource] = useState<string>("");
  const [run, setRun] = useState<ReconciliationRun | null>(null);
  const [selectedId, setSelectedId] = useState<string | null>(null);

  useEffect(() => {
    api
      .health()
      .then((value) => setHealth(value.demo_mode ? "demo mode" : "live inference ready"))
      .catch(() => setHealth("backend offline"));
  }, []);

  const selected = useMemo(
    () => run?.results.find((result) => result.id === selectedId) || run?.results[0] || null,
    [run, selectedId]
  );

  async function withBusy(action: () => Promise<void>) {
    setBusy(true);
    setError(null);
    try {
      await action();
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unexpected error");
    } finally {
      setBusy(false);
    }
  }

  function applyExtraction(response: ExtractionResponse) {
    setDocuments(response.documents);
    setRecords(response.records);
    setSource(response.source);
    setRun(null);
    setSelectedId(null);
  }

  async function loadDemo() {
    await withBusy(async () => {
      const extraction = await api.extractDemo();
      applyExtraction(extraction);
    });
  }

  async function upload(files: FileList | null) {
    if (!files || files.length === 0) return;
    await withBusy(async () => {
      const uploaded = await api.upload(files);
      const extraction = await api.extract(uploaded.documents.map((document) => document.id));
      applyExtraction(extraction);
    });
  }

  async function reconcile() {
    await withBusy(async () => {
      const documentIds = documents.map((document) => document.id);
      const nextRun = await api.reconcile(documentIds);
      setRun(nextRun);
      const firstException = nextRun.results.find((result) => result.status !== "matched");
      setSelectedId(firstException?.id || nextRun.results[0]?.id || null);
    });
  }

  function exportReport() {
    if (!run) return;
    const blob = new Blob([JSON.stringify(run, null, 2)], { type: "application/json" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `reconpilot-report-${run.id}.json`;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <main className="shell">
      <section className="hero">
        <div>
          <p className="eyebrow">AI Marathon 2026 - Global Treasury Agent</p>
          <div className="brandPlate" aria-hidden="true">
            <img src="/reconpilot.png" alt="" />
          </div>
          <h1 className="srOnly">ReconPilot</h1>
          <p className="subtitle">
            A treasury workspace for extracting finance documents, matching cross-border payments,
            and reviewing exceptions with clear evidence.
          </p>
        </div>
        <div className="heroPanel">
          <span className="statusDot" />
          <div>
            <p className="panelLabel">Backend</p>
            <strong>{health}</strong>
          </div>
        </div>
      </section>

      <section className="toolbar" aria-label="Primary actions">
        <button className="primaryButton" onClick={loadDemo} disabled={busy}>
          Load Demo Casebook
        </button>
        <label className="secondaryButton">
          Upload Treasury Files
          <input
            type="file"
            multiple
            accept=".txt,.csv,.xlsx,.xls,.pdf,.png,.jpg,.jpeg"
            onChange={(event) => upload(event.target.files)}
          />
        </label>
        <button className="secondaryButton" onClick={reconcile} disabled={busy || records.length === 0}>
          Run Matching
        </button>
        <button className="ghostButton" onClick={exportReport} disabled={!run}>
          Export Audit JSON
        </button>
      </section>

      {error && <div className="error">{error}</div>}

      <section className="metrics">
        <Metric label="Documents" value={documents.length.toString()} />
        <Metric label="Records" value={records.length.toString()} />
        <Metric label="Extraction" value={source || "not started"} />
        <Metric label="Run status" value={run ? "complete" : busy ? "working" : "ready"} />
      </section>

      <section className="grid two">
        <Panel title="Agent Workflow" action="controlled agent" className="panelWorkflow">
          <div className="workflow">
            {workflowSteps.map((step, index) => (
              <div className="workflowStep" key={step.name}>
                <span>{index + 1}</span>
                <div>
                  <strong>{step.name}</strong>
                  <p>{step.detail}</p>
                </div>
              </div>
            ))}
          </div>
        </Panel>

        <Panel title="Trust Controls" action="review gates" className="panelCompact">
          <div className="controlList">
            {trustControls.map((control) => (
              <div className="controlItem" key={control.label}>
                <span aria-hidden="true">{control.marker}</span>
                <strong>{control.label}</strong>
              </div>
            ))}
          </div>
        </Panel>
      </section>

      <section className="grid two">
        <Panel title="Extraction Review" action={`${records.length} records ready`} className="panelTable">
          <div className="tableWrap">
            <table>
              <thead>
                <tr>
                  <th>Type</th>
                  <th>Reference</th>
                  <th>Date</th>
                  <th>Amount</th>
                  <th>Party</th>
                </tr>
              </thead>
              <tbody>
                {records.map((record) => (
                  <tr key={record.id}>
                    <td><Badge>{record.record_type.replace("_", " ")}</Badge></td>
                    <td className="dataCell">{record.invoice_number || record.reference || "-"}</td>
                    <td className="dataCell">{record.date || "-"}</td>
                    <td className="amountCell">{record.currency} {record.amount.toFixed(2)}</td>
                    <td>{record.payer || record.payee || "-"}</td>
                  </tr>
                ))}
                {records.length === 0 && (
                  <tr>
                    <td colSpan={5} className="empty">Start with the demo casebook, or upload treasury files.</td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </Panel>

        <Panel title="Uploaded Documents" action={`${documents.length} files staged`} className="panelCompact">
          <div className="docList">
            {documents.map((document) => (
              <div className="docItem" key={document.id}>
                <strong>{document.filename}</strong>
                <span>{document.document_type.replace("_", " ")} - {document.parse_status}</span>
              </div>
            ))}
            {documents.length === 0 && <p className="empty">No files staged yet.</p>}
          </div>
        </Panel>
      </section>

      <section className="grid resultGrid">
        <Panel title="Reconciliation Dashboard" action={run ? `${run.results.length} decisions` : "not run"} className="panelDashboard">
          {run && (
            <div className="summaryStrip">
              <Metric label="Matched" value={String(run.summary.matched ?? 0)} />
              <Metric label="Review" value={String(run.summary.review ?? 0)} />
              <Metric label="Missing Proof" value={String(run.summary.missing_proof ?? 0)} />
              <Metric label="Duplicate" value={String(run.summary.duplicate ?? 0)} />
              <Metric label="Human Review" value={String(run.summary.requires_human_review ?? 0)} />
              <Metric label="Cleared MYR" value={String(run.summary.cleared_value_myr ?? 0)} />
              <Metric label="Exception MYR" value={String(run.summary.exception_value_myr ?? 0)} />
              <Metric label="Automation" value={`${run.summary.automation_rate ?? 0}%`} />
            </div>
          )}
          <div className="resultList">
            {run?.results.map((result) => (
              <button
                key={result.id}
                className={`resultItem ${selectedId === result.id ? "active" : ""}`}
                onClick={() => setSelectedId(result.id)}
              >
                <span className={`status ${result.status}`}>{statusLabel[result.status]}</span>
                <strong className="dataText">{result.invoice?.invoice_number || result.bank_transactions[0]?.reference || "Unmatched transaction"}</strong>
                <small className="dataText">{Math.round(result.confidence * 100)}% confidence</small>
              </button>
            ))}
            {!run && <p className="empty">Run matching after extraction to review decisions.</p>}
          </div>
        </Panel>

        <Panel title="Exception Detail" action={selected ? statusLabel[selected.status] : "select result"} className="panelDetail">
          {selected ? <ResultDetail result={selected} /> : <p className="empty">Select a result to inspect evidence.</p>}
        </Panel>
      </section>

      <section className="grid reportGrid">
        <Panel title="Audit Report Preview" action={run ? `run ${run.id}` : "waiting"} className="panelReport">
          {run ? <AuditReport run={run} /> : <p className="empty">Run matching to generate an audit-ready report.</p>}
        </Panel>
      </section>
    </main>
  );
}

function Metric({ label, value }: { label: string; value: string }) {
  return (
    <div className="metric">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function Panel({
  title,
  action,
  children,
  className = ""
}: {
  title: string;
  action: string;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={`panel ${className}`}>
      <div className="panelHeader">
        <h2>{title}</h2>
        <span>{action}</span>
      </div>
      {children}
    </section>
  );
}

function Badge({ children }: { children: ReactNode }) {
  return <span className="badge">{children}</span>;
}

function ResultDetail({ result }: { result: ReconciliationResult }) {
  return (
    <div className="detail">
      <div className="detailTop">
        <span className={`status ${result.status}`}>{statusLabel[result.status]}</span>
        <strong className="dataText">{Math.round(result.confidence * 100)}% confidence</strong>
      </div>
      <p>{result.explanation}</p>
      <div className="callout">
        <span>Recommended action</span>
        <strong>{result.recommended_action}</strong>
      </div>
      <h3>Evidence</h3>
      <div className="evidenceList">
        {result.evidence.map((item, index) => (
          <div className="evidence" key={`${item.label}-${index}`}>
            <span>{item.label}</span>
            <strong className="dataText">{item.value}</strong>
            {item.source && <small>{item.source}</small>}
          </div>
        ))}
      </div>
    </div>
  );
}

function AuditReport({ run }: { run: ReconciliationRun }) {
  return (
    <div className="audit">
      <div className="auditSummary">
        <Metric label="Total Value" value={`MYR ${run.summary.total_value_myr ?? 0}`} />
        <Metric label="Auto Cleared" value={`MYR ${run.summary.cleared_value_myr ?? 0}`} />
        <Metric label="Needs Review" value={`MYR ${run.summary.exception_value_myr ?? 0}`} />
        <Metric label="Decisions" value={String(run.summary.total_results ?? 0)} />
      </div>
      <div className="auditColumns">
        <div>
          <h3>Agent Trace</h3>
          <ol>
            {run.agent_trace.map((step) => (
              <li key={step}>{step}</li>
            ))}
          </ol>
        </div>
        <div>
          <h3>Controls</h3>
          <ul>
            {run.controls.map((control) => (
              <li key={control}>{control}</li>
            ))}
          </ul>
        </div>
      </div>
      <div className="decisionTable">
        {run.results.map((result) => (
          <div className="decisionRow" key={result.id}>
            <span className={`status ${result.status}`}>{statusLabel[result.status]}</span>
            <strong className="dataText">{result.invoice?.invoice_number || result.bank_transactions[0]?.reference || "Unmatched"}</strong>
            <span>{result.recommended_action}</span>
          </div>
        ))}
      </div>
    </div>
  );
}
