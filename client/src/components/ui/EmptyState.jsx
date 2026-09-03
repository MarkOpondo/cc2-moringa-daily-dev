export default function EmptyState({ icon: Icon, title, description, action }) {
  return (
    <div className="text-center py-16 px-6 border border-dashed border-line rounded-xl bg-surface/50">
      {Icon && <Icon className="w-8 h-8 mx-auto text-navy/40 mb-3" strokeWidth={1.5} />}
      <h3 className="text-sm font-semibold text-navy">{title}</h3>
      {description && <p className="text-xs text-muted mt-1 max-w-sm mx-auto">{description}</p>}
      {action && <div className="mt-4">{action}</div>}
    </div>
  );
}

