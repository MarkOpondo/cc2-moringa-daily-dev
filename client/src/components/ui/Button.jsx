const VARIANTS = {
  primary: "bg-brand-500 hover:bg-brand-600 text-cream font-semibold disabled:opacity-50",
  ghost: "bg-navy-raised hover:bg-navy-borderLight text-slate-300",
  outline: "bg-transparent border border-navy-border hover:border-navy-borderLight text-slate-300",
  danger: "bg-red-500/10 hover:bg-red-500/20 text-red-400 border border-red-500/20",
};

const SIZES = {
  sm: "px-3 py-1.5 text-xs",
  md: "px-4 py-2 text-sm",
  lg: "py-2.5 text-sm w-full",
};

export default function Button({ variant = "primary", size = "md", className = "", ...props }) {
  return (
    <button
      className={`rounded-lg transition duration-150 ${VARIANTS[variant]} ${SIZES[size]} ${className}`}
      {...props}
    />
  );
}
