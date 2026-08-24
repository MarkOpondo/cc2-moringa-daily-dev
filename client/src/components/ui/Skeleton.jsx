export function SkeletonLine({ className = "" }) {
  return <div className={`animate-pulse bg-slate-800/80 rounded ${className}`} />;
}

export function ContentCardSkeleton() {
  return (
    <div className="flex gap-4 p-4 rounded-xl border border-slate-800 bg-slate-900/40">
      <div className="w-1 shrink-0 rounded-full bg-slate-800 animate-pulse" />
      <div className="flex-1 space-y-3">
        <SkeletonLine className="h-3 w-20" />
        <SkeletonLine className="h-4 w-3/4" />
        <SkeletonLine className="h-3 w-full" />
        <SkeletonLine className="h-3 w-1/2" />
      </div>
    </div>
  );
}
