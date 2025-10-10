
interface AnonymizedTextProps {
  text: string | null;
}

export function AnonymizedText({ text }: AnonymizedTextProps) {
  return (
    <div className="anonymized-text-view">
      <h3>Anonymized Text</h3>
      {text ? (
        <pre className="text-content">{text}</pre>
      ) : (
        <p className="empty-state">No anonymized text yet. Click "Anonymize" to process your text.</p>
      )}
    </div>
  );
}
