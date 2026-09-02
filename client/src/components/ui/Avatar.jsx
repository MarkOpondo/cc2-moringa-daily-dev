import { initials, roleColorClass } from "../../utils/format";

export default function Avatar({ username, role, size = "md" }) {
  const sizes = { sm: "w-7 h-7 text-[10px]", md: "w-9 h-9 text-xs", lg: "w-14 h-14 text-base" };
  return (
    <div
      className={`${sizes[size]} shrink-0 rounded-full bg-surface border border-line flex items-center justify-center font-mono font-medium ${roleColorClass(role)}`}
      aria-hidden="true"
    >
      {initials(username)}
    </div>
  );
}

