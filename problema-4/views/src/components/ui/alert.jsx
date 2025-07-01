export function Alert({ children, variant = "default" }) {
  const base = "p-3 rounded-md mb-2";
  const variants = {
    default: "bg-gray-100 text-gray-800",
    destructive: "bg-red-100 text-red-800",
    success: "bg-green-100 text-green-800",
  };
  return <div className={`${base} ${variants[variant]}`}>{children}</div>;
}

export function AlertDescription({ children }) {
  return <div>{children}</div>;
}
