interface OriginalTextProps {
  text: string;
}

export function OriginalText({ text }: OriginalTextProps) {
  return (
    <div className="original-text-view">
      <h3>Original Text</h3>
      {text ? (
        <pre className="text-content">{text}</pre>
      ) : (
        <p className="empty-state">No text entered yet. Enter text above to get started.</p>
      )}
    </div>
  );
}
