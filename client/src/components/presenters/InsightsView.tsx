
interface InsightsViewProps {
  llmProvider: string | null;
  llmModel: string | null;
  iterations: number | null;
  success: boolean | null;
  validationConfidence: number | null;
  riskConfidence: number | null;
}

export function InsightsView({
  llmProvider,
  llmModel,
  iterations,
  success,
  validationConfidence,
  riskConfidence
}: InsightsViewProps) {
  if (llmProvider === null) {
    return (
      <div className="insights-view">
        <h3>Insights</h3>
        <p className="empty-state">No insights yet. Anonymize text to see workflow information.</p>
      </div>
    );
  }

  return (
    <div className="insights-view">
      <section className="workflow-info">
        <h3>Workflow Information</h3>
        <dl>
          <dt>Status</dt>
          <dd className={success ? 'success' : 'failure'}>
            {success ? '✓ Success' : '✗ Failed'}
          </dd>

          <dt>Iterations</dt>
          <dd>{iterations}</dd>

          <dt>LLM Provider</dt>
          <dd>{llmProvider}</dd>

          <dt>LLM Model</dt>
          <dd>{llmModel}</dd>
        </dl>
      </section>

      <section className="confidence-scores">
        <h3>Confidence Scores</h3>
        <dl>
          <dt>Validation Confidence</dt>
          <dd>
            <meter
              value={validationConfidence ?? 0}
              min={0}
              max={1}
              optimum={1}
            >
              {((validationConfidence ?? 0) * 100).toFixed(0)}%
            </meter>
            <span>{((validationConfidence ?? 0) * 100).toFixed(1)}%</span>
          </dd>

          <dt>Risk Assessment Confidence</dt>
          <dd>
            <meter
              value={riskConfidence ?? 0}
              min={0}
              max={1}
              optimum={1}
            >
              {((riskConfidence ?? 0) * 100).toFixed(0)}%
            </meter>
            <span>{((riskConfidence ?? 0) * 100).toFixed(1)}%</span>
          </dd>
        </dl>
      </section>
    </div>
  );
}
