export function SkeletonLine({ className = "" }) {
  return <div className={`animate-pulse bg-line/70 rounded ${className}`} />;
}

export function ContentCardSkeleton() {
  return (
    <div className="rounded-xl overflow-hidden border border-line bg-white">
      <div className="aspect-video bg-line/70 animate-pulse" />
      <div className="p-4 space-y-3">
        <div className="flex gap-2">
          <SkeletonLine className="h-5 w-16 rounded-full" />
          <SkeletonLine className="h-5 w-20 rounded-full" />
        </div>
        <SkeletonLine className="h-4 w-full" />
        <SkeletonLine className="h-4 w-2/3" />
        <SkeletonLine className="h-3 w-1/3" />
      </div>
    </div>
  );
}

