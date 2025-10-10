import type { RiskAssessment as RiskAssessmentType } from '../../services/api';

interface RiskAssessmentProps {
  assessment: RiskAssessmentType | null;
}

export function RiskAssessment({ assessment }: RiskAssessmentProps) {
  if (!assessment) {
    return (
      <div className="risk-assessment-view">
        <h3>Risk Assessment</h3>
        <p className="empty-state">No risk assessment yet. Anonymize text to see risk analysis.</p>
      </div>
    );
  }

  const getRiskLevelClass = (level: string) => {
    switch (level) {
      case 'CRITICAL': return 'risk-critical';
      case 'HIGH': return 'risk-high';
      case 'MEDIUM': return 'risk-medium';
      case 'LOW': return 'risk-low';
      case 'NEGLIGIBLE': return 'risk-negligible';
      default: return '';
    }
  };

  return (
    <div className="risk-assessment-view">
      <h3>Risk Assessment</h3>

      <div className="risk-summary">
        <div className={`risk-level ${getRiskLevelClass(assessment.risk_level)}`}>
          <span className="label">Risk Level:</span>
          <span className="value">{assessment.risk_level}</span>
        </div>

        <div className="risk-score">
          <span className="label">Overall Score:</span>
          <span className="value">{assessment.overall_score}/100</span>
        </div>

        <div className={`gdpr-compliance ${assessment.gdpr_compliant ? 'compliant' : 'non-compliant'}`}>
          <span className="label">GDPR Compliant:</span>
          <span className="value">{assessment.gdpr_compliant ? '✓ Yes' : '✗ No'}</span>
        </div>

        <div className="confidence">
          <span className="label">Confidence:</span>
          <span className="value">{(assessment.confidence * 100).toFixed(1)}%</span>
        </div>
      </div>

      <div className="risk-reasoning">
        <h4>Reasoning</h4>
        <p>{assessment.reasoning}</p>
      </div>

      <div className="assessment-date">
        <small>Assessed: {new Date(assessment.assessment_date).toLocaleString()}</small>
      </div>
    </div>
  );
}
