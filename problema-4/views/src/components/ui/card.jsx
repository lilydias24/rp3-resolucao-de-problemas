export function Card({ children, className = "" }) {
  return (
    <div className={`min-h-screen flex items-center justify-center bg-blue-600 ${className}`}>
      {children}
    </div>
  );
}

export function CardHeader({ children, className = "" }) {
  return <div className={`mb-4 ${className}`}>{children}</div>;
}

export function CardTitle({ children, className = "" }) {
  return <h2 className={`text-lg font-bold bg-blue-400 ${className}`}>{children}</h2>;
}

export function CardContent({ children, className = "" }) {
  return <div className={className}>{children}</div>;
}

export function CardDescription({ children, className = "" }) {
  return <p className={`text-gray-500 text-sm text-center ${className}`}>{children}</p>;
}
