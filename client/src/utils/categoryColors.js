
const PALETTE = {
  Frontend: { text: "text-sky-400", bg: "bg-sky-400", border: "border-sky-400", soft: "bg-sky-400/10" },
  Backend: { text: "text-emerald-400", bg: "bg-emerald-400", border: "border-emerald-400", soft: "bg-emerald-400/10" },
  DevOps: { text: "text-amber-400", bg: "bg-amber-400", border: "border-amber-400", soft: "bg-amber-400/10" },
  Fullstack: { text: "text-violet-400", bg: "bg-violet-400", border: "border-violet-400", soft: "bg-violet-400/10" },
  Career: { text: "text-rose-400", bg: "bg-rose-400", border: "border-rose-400", soft: "bg-rose-400/10" },
  "Data Science": { text: "text-cyan-400", bg: "bg-cyan-400", border: "border-cyan-400", soft: "bg-cyan-400/10" },
};

const FALLBACK = { text: "text-slate-400", bg: "bg-slate-400", border: "border-slate-400", soft: "bg-slate-400/10" };

export function categoryColor(name) {
  return PALETTE[name] || FALLBACK;
}
