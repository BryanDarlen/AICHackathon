export type DocumentType = "invoice" | "payment_proof" | "bank_statement" | "unknown";
export type RecordType = "invoice" | "payment" | "bank_transaction";
export type MatchStatus = "matched" | "review" | "missing_proof" | "duplicate" | "unmatched";

export interface DocumentRecord {
  id: string;
  filename: string;
  document_type: DocumentType;
  extracted_text: string;
  parse_status: string;
  created_at: string;
}

export interface FinancialRecord {
  id: string;
  document_id: string;
  record_type: RecordType;
  amount: number;
  currency: string;
  date: string;
  payer?: string | null;
  payee?: string | null;
  invoice_number?: string | null;
  reference?: string | null;
  description?: string | null;
  raw_text?: string | null;
  confidence: number;
  normalized_amount_myr?: number | null;
  validation_notes: string[];
}

export interface EvidenceItem {
  label: string;
  value: string;
  source?: string | null;
}

export interface ReconciliationResult {
  id: string;
  status: MatchStatus;
  confidence: number;
  invoice?: FinancialRecord | null;
  payment_proofs: FinancialRecord[];
  bank_transactions: FinancialRecord[];
  delta_myr?: number | null;
  evidence: EvidenceItem[];
  explanation: string;
  recommended_action: string;
}

export interface ReconciliationRun {
  id: string;
  created_at: string;
  summary: Record<string, number | string>;
  agent_trace: string[];
  controls: string[];
  results: ReconciliationResult[];
}

export interface ExtractionResponse {
  documents: DocumentRecord[];
  records: FinancialRecord[];
  source: string;
}

export interface HealthResponse {
  status: string;
  demo_mode: boolean;
  documents: number;
  records: number;
}

export interface AgentStatusResponse {
  status: string;
  mode: string;
  pipeline: string[];
  documents: number;
  records: number;
  message: string;
}
