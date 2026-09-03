import { Link } from "react-router-dom";
import { Video, Headphones, FileText } from "lucide-react";
import { timeAgo } from "../../utils/format";

const TYPE_ICON = { video: Video, audio: Headphones, article: FileText };
const TYPE_LABEL = { video: "Video", audio: "Audio", article: "Article" };
const TYPE_TAG_COLOR = {
  video: "bg-blue-500/15 text-blue-400",
  audio: "bg-violet-500/15 text-violet-400",
  article: "bg-surface text-navy/70",
};

export default function ContentCard({ item }) {
  const TypeIcon = TYPE_ICON[item.type] || FileText;
  const durationLabel = item.duration || item.readTime;

  return (
    <Link
      to={`/content/${item.id}`}
      className="group block rounded-xl overflow-hidden border border-line bg-white hover:border-brand-500/50 hover:shadow-lg transition"
    >
      <div className="relative aspect-video bg-surface overflow-hidden">
        <img
          src={item.thumbnail}
          alt=""
          loading="lazy"
          className="w-full h-full object-cover group-hover:scale-[1.02] transition duration-300"
        />
        {durationLabel && (
          <span className="absolute bottom-2.5 right-2.5 flex items-center gap-1 bg-black/80 text-white text-[11px] font-mono px-2 py-1 rounded-md">
            {durationLabel}
          </span>
        )}
        {item.status && item.status !== "approved" && (
          <span className="absolute top-2.5 left-2.5 text-[10px] font-mono uppercase text-amber-300 bg-black/80 rounded px-1.5 py-0.5">
            {item.status}
          </span>
        )}
      </div>

      <div className="p-4">
        <div className="flex items-center gap-2 mb-2.5">
          <span className={`flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded ${TYPE_TAG_COLOR[item.type]}`}>
            <TypeIcon className="w-3 h-3" strokeWidth={2} />
            {TYPE_LABEL[item.type]}
          </span>
          <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-surface text-muted">
            {item.category?.name}
          </span>
        </div>

        <h3 className="font-display font-bold text-navy group-hover:text-brand-400 leading-snug text-lg transition">
          {item.title}
        </h3>

        <div className="flex items-center gap-2 mt-3 text-xs text-muted">
          <span>{item.author?.username}</span>
          <span>·</span>
          <span>{timeAgo(item.createdAt)}</span>
        </div>
      </div>
    </Link>
  );
}

