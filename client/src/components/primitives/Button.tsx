interface ButtonProps {
  onClick?: () => void;
  disabled?: boolean;
  loading?: boolean;
  type?: 'button' | 'submit' | 'reset';
  children: preact.ComponentChildren;
  className?: string;
}

export function Button({
  onClick,
  disabled,
  loading,
  type = 'button',
  children,
  className = ''
}: ButtonProps) {
  return (
    <button
      type={type}
      onClick={onClick}
      disabled={disabled || loading}
      className={`button ${className} ${loading ? 'loading' : ''}`}
      aria-busy={loading}
    >
      {loading ? (
        <>
          <span className="spinner"></span>
          {children}
        </>
      ) : children}
    </button>
  );
}
