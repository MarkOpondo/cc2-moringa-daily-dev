import { roleLabel, roleColorClass } from "../../utils/format";

export default function RoleBadge({ role }) {
  if (role === "user") return null; // default role, no badge needed — reduces noise
  return (
    <span className={`text-[10px] font-mono uppercase tracking-wide ${roleColorClass(role)}`}>
      {roleLabel(role)}
    </span>
  );
}
