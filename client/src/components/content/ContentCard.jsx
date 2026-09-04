import { Link } from "react-router-dom";
import { FileText, Headphones, Video } from "lucide-react";

import { timeAgo } from "../../utils/format";

const TYPE_ICON = { video: Video, audio: Headphones, article: FileText, image: FileText };
const TYPE_LABEL = { video: "Video", audio: "Audio", article: "Article", image: "Image" };
const TYPE_TAG_COLOR = {
  video: "bg-blue-500/15 text-blue-400",
  audio: "bg-violet-500/15 text-violet-400",
  article: "bg-navy-raised text-slate-300",
  image: "bg-emerald-500/15 text-emerald-400",
};

export default function ContentCard({ item }) {
  const type = (item.type || item.contentType || "article").toLowerCase();
  const TypeIcon = TYPE_ICON[type] || FileText;
  const category = item.categories?.[0] || item.category;
  const author = item.author || {};
  const thumbnail = item.thumbnailUrl || item.thumbnail;
  const durationLabel = item.duration || item.readTime;
  const status = (item.status || "").toLowerCase();

  return (
    <Link
      to={`/content/${item.id}`}
      className="group block rounded-xl overflow-hidden border border-navy-border bg-navy hover:border-navy-borderLight hover:shadow-lg transition"
    >
      <div className="relative aspect-video bg-navy-raised overflow-hidden">
        {thumbnail ? (
          <img
            src={thumbnail}
            alt=""
            loading="lazy"
            className="w-full h-full object-cover group-hover:scale-[1.02] transition duration-300"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center text-slate-500">
            <TypeIcon className="w-10 h-10" strokeWidth={1.25} />
          </div>
        )}
        {durationLabel && (
          <span className="absolute bottom-2.5 right-2.5 bg-black/80 text-white text-[11px] font-mono px-2 py-1 rounded-md">
            {durationLabel}
          </span>
        )}
        {status && !["published", "approved"].includes(status) && (
          <span className="absolute top-2.5 left-2.5 text-[10px] font-mono uppercase text-amber-300 bg-black/80 rounded px-1.5 py-0.5">
            {status}
          </span>
        )}
      </div>

      <div className="p-4">
        <div className="flex items-center gap-2 mb-2.5">
          <span className={`flex items-center gap-1 text-[11px] font-medium px-2 py-0.5 rounded ${TYPE_TAG_COLOR[type] || TYPE_TAG_COLOR.article}`}>
            <TypeIcon className="w-3 h-3" strokeWidth={2} />
            {TYPE_LABEL[type] || "Article"}
          </span>
          {category?.name && (
            <span className="text-[11px] font-medium px-2 py-0.5 rounded bg-navy-raised text-slate-400">
              {category.name}
            </span>
          )}
        </div>

        <h3 className="font-display font-bold text-cream group-hover:text-brand-400 leading-snug text-lg transition">
          {item.title}
        </h3>

        <div className="flex items-center gap-2 mt-3 text-xs text-slate-400">
          {author.username && <span>{author.username}</span>}
          {author.username && <span>·</span>}
          {item.createdAt && <span>{timeAgo(item.createdAt)}</span>}
        </div>
      </div>
    </Link>
  );
}
