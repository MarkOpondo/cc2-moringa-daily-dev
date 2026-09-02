const VARIANTS = {
  // Solid orange CTA — "Chat with us", "Write" — the reference's primary action color.
  primary: "bg-brand-500 hover:bg-brand-600 text-white font-semibold disabled:opacity-50",
  // Neutral pill — quiet secondary actions on white surfaces.
  ghost: "bg-surface hover:bg-line/60 text-navy",
  // Outlined pill — matches the reference's inactive filter chips
  // ("Data Courses", "Cyber Security"): white fill, navy border/text,
  // orange border/text on hover to hint interactivity.
  outline: "bg-white border border-line hover:border-brand-500 hover:text-brand-600 text-navy",
  danger: "bg-red-50 hover:bg-red-100 text-red-600 border border-red-200",
};

const SIZES = {
  sm: "px-3 py-1.5 text-xs",
  md: "px-4 py-2 text-sm",
  lg: "py-2.5 text-sm w-full",
};

export default function Button({ variant = "primary", size = "md", className = "", ...props }) {
  return (
    <button
      className={`rounded-full transition duration-150 ${VARIANTS[variant]} ${SIZES[size]} ${className}`}
      {...props}
    />
  );
}

