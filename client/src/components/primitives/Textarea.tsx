interface TextareaProps {
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  className?: string;
  rows?: number;
  disabled?: boolean;
}

export function Textarea({
  value,
  onChange,
  placeholder = '',
  className = '',
  rows = 10,
  disabled = false
}: TextareaProps) {
  return (
    <textarea
      value={value}
      onInput={(e) => onChange((e.target as HTMLTextAreaElement).value)}
      placeholder={placeholder}
      className={`textarea ${className}`}
      rows={rows}
      disabled={disabled}
    />
  );
}
