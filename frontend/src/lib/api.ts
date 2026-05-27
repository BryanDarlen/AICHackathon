import type { ExtractionResponse, HealthResponse, ReconciliationRun } from "../types";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://127.0.0.1:8000";

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_URL}${path}`, {
    ...options,
    headers: {
      ...(options?.body instanceof FormData ? {} : { "Content-Type": "application/json" }),
      ...(options?.headers || {})
    }
  });

  if (!response.ok) {
    let message = `Request failed with ${response.status}`;
    try {
      const body = await response.json();
      message = body.detail || message;
    } catch {
      // Keep default message.
    }
    throw new Error(message);
  }

  return response.json() as Promise<T>;
}

export const api = {
  health: () => request<HealthResponse>("/api/health"),
  extractDemo: () =>
    request<ExtractionResponse>("/api/extract", {
      method: "POST",
      body: JSON.stringify({ use_demo: true, document_ids: [] })
    }),
  upload: (files: FileList) => {
    const form = new FormData();
    Array.from(files).forEach((file) => form.append("files", file));
    return request<{ documents: ExtractionResponse["documents"] }>("/api/upload", {
      method: "POST",
      body: form
    });
  },
  extract: (documentIds: string[]) =>
    request<ExtractionResponse>("/api/extract", {
      method: "POST",
      body: JSON.stringify({ use_demo: false, document_ids: documentIds })
    }),
  reconcile: (documentIds: string[]) =>
    request<ReconciliationRun>("/api/reconcile", {
      method: "POST",
      body: JSON.stringify({ document_ids: documentIds })
    }),
  report: (runId: string) => request<ReconciliationRun>(`/api/report/${runId}`)
};
