export interface AnonymizeRequest {
  text: string;
  document_id?: string;
}

export interface ValidationIssue {
  identifier_type: string;
  value: string;
  context: string;
  location_hint: string;
}

export interface ValidationResult {
  passed: boolean;
  issues: ValidationIssue[];
  reasoning: string;
  confidence: number;
}

export interface RiskAssessment {
  overall_score: number;
  risk_level: 'CRITICAL' | 'HIGH' | 'MEDIUM' | 'LOW' | 'NEGLIGIBLE';
  gdpr_compliant: boolean;
  confidence: number;
  reasoning: string;
  assessment_date: string;
}

export interface AnonymizeResponse {
  document_id?: string;
  anonymized_text: string;
  mappings: Record<string, string>;
  validation: ValidationResult;
  risk_assessment: RiskAssessment;
  iterations: number;
  success: boolean;
  llm_provider: string;
  llm_model: string;
}

export async function anonymizeText(
  text: string,
  documentId?: string
): Promise<AnonymizeResponse> {
  const response = await fetch('/api/v1/anonymize', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      text,
      document_id: documentId
    })
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({}));
    throw new Error(
      error.detail || `API error: ${response.status}`
    );
  }

  return response.json();
}
