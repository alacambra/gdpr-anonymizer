import type { ValidationIssue } from '../../services/api';

interface ReplacementsViewProps {
  mappings: Record<string, string> | null;
  validationIssues: ValidationIssue[];
  validationPassed: boolean;
}

export function ReplacementsView({
  mappings,
  validationIssues,
  validationPassed
}: ReplacementsViewProps) {
  const mappingEntries = mappings ? Object.entries(mappings) : [];

  if (!mappings) {
    return (
      <div className="replacements-view">
        <h3>Replacements</h3>
        <p className="empty-state">No replacements yet. Anonymize text to see mappings.</p>
      </div>
    );
  }

  return (
    <div className="replacements-view">
      <section className="mappings">
        <h3>Replacements Performed</h3>
        {mappingEntries.length === 0 ? (
          <p className="empty-state">No replacements were made.</p>
        ) : (
          <table>
            <thead>
              <tr>
                <th>Original</th>
                <th>Replacement</th>
              </tr>
            </thead>
            <tbody>
              {mappingEntries.map(([original, replacement]) => (
                <tr key={original}>
                  <td className="original">{original}</td>
                  <td className="replacement">{replacement}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      {!validationPassed && validationIssues.length > 0 && (
        <section className="validation-issues">
          <h3 className="warning">⚠️ Validation Issues Found</h3>
          <p>The following identifiers were detected but not anonymized:</p>
          <ul>
            {validationIssues.map((issue, idx) => (
              <li key={idx} className="issue-item">
                <strong>{issue.identifier_type}:</strong> {issue.value}
                <br />
                <span className="context">Context: {issue.context}</span>
                <br />
                <span className="hint">Location: {issue.location_hint}</span>
              </li>
            ))}
          </ul>
        </section>
      )}
    </div>
  );
}
